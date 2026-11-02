"""KataGo Training API model catalog and download services."""

from __future__ import annotations

import hashlib
import gzip
import json
import os
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterator
from urllib.parse import unquote, urlparse

import requests


API_BASE_URL = "https://katagotraining.org/api"
NETWORKS_URL = f"{API_BASE_URL}/networks/"
NETWORKS_JSON_URL = f"{API_BASE_URL}/networks/?format=json"


class KataGoModelError(RuntimeError):
    """Base error raised by the KataGo model service."""


class KataGoModelFormatError(KataGoModelError):
    """Raised when the API response is missing required model fields."""


class KataGoModelChecksumError(KataGoModelError):
    """Raised when a downloaded model does not match its advertised hash."""


class KataGoModelNetworkError(KataGoModelError):
    """Raised when the model API cannot be reached."""


class KataGoModelHTTPError(KataGoModelError):
    """Raised when the model API returns an HTTP error."""


class KataGoModelCancelled(KataGoModelError):
    """Raised when a download is cancelled by the caller."""


@dataclass(frozen=True)
class KataGoModel:
    name: str
    created_at: str
    network_size: str
    model_file: str
    model_file_bytes: int
    model_file_sha256: str
    training_games_enabled: bool = False
    rating_games_enabled: bool = False
    notes: str = ""

    @classmethod
    def from_api_data(cls, data: dict[str, Any]) -> "KataGoModel":
        required = (
            "name",
            "created_at",
            "network_size",
            "model_file",
            "model_file_bytes",
            "model_file_sha256",
        )
        missing = [key for key in required if key not in data]
        if missing:
            raise KataGoModelFormatError(
                f"Model response is missing required fields: {', '.join(missing)}"
            )

        try:
            return cls(
                name=str(data["name"]),
                created_at=str(data["created_at"]),
                network_size=str(data["network_size"]),
                model_file=str(data["model_file"]),
                model_file_bytes=int(data["model_file_bytes"]),
                model_file_sha256=str(data["model_file_sha256"]).lower(),
                training_games_enabled=bool(data.get("training_games_enabled", False)),
                rating_games_enabled=bool(data.get("rating_games_enabled", False)),
                notes=str(data.get("notes", "")),
            )
        except (TypeError, ValueError) as exc:
            raise KataGoModelFormatError("Model response contains invalid field types") from exc


@dataclass(frozen=True)
class KataGoModelPage:
    count: int
    next_url: str | None
    previous_url: str | None
    results: tuple[KataGoModel, ...]
    url: str


@dataclass(frozen=True)
class DownloadProgress:
    model: KataGoModel
    downloaded_bytes: int
    total_bytes: int

    @property
    def fraction(self) -> float:
        if self.total_bytes <= 0:
            return 0.0
        return min(1.0, self.downloaded_bytes / self.total_bytes)


ProgressCallback = Callable[[DownloadProgress], None]


def migrate_mislabeled_text_model(
    path: str | os.PathLike[str],
    model_name: str,
) -> Path:
    """Repair an older download incorrectly saved with a .bin.gz suffix."""
    model_path = Path(path)
    if not model_path.is_file() or not model_path.name.lower().endswith(".bin.gz"):
        return model_path

    try:
        with gzip.open(model_path, "rb") as source:
            header = source.readline(256).decode("ascii").strip()
    except (OSError, UnicodeDecodeError):
        return model_path

    expected_headers = {model_name}
    if model_name.startswith("kata1-"):
        expected_headers.add(model_name[len("kata1-") :])
    if header not in expected_headers:
        return model_path

    repaired_path = model_path.with_name(
        f"{model_path.name[:-len('.bin.gz')]}.txt.gz"
    )
    if not repaired_path.exists():
        os.replace(model_path, repaired_path)
    return repaired_path


class KataGoModelManager:
    """Fetch and safely download models from katagotraining.org."""

    def __init__(
        self,
        download_dir: str | os.PathLike[str],
        *,
        session: requests.Session | None = None,
        api_timeout: tuple[float, float] = (10.0, 30.0),
        download_timeout: tuple[float, float] = (10.0, 60.0),
        chunk_size: int = 1024 * 1024,
    ) -> None:
        self.download_dir = Path(download_dir)
        self.session = session or requests.Session()
        self.api_timeout = api_timeout
        self.download_timeout = download_timeout
        self.chunk_size = chunk_size
        self._download_lock = threading.Lock()
        self._cancel_event = threading.Event()
        self._catalog_cache_path = self.download_dir / ".katago_model_catalog.json"
        self._catalog_cache_lock = threading.Lock()

    @property
    def is_downloading(self) -> bool:
        return self._download_lock.locked()

    def fetch_page(self, url: str = NETWORKS_URL) -> KataGoModelPage:
        try:
            response = self.session.get(url, timeout=self.api_timeout)
            response.raise_for_status()
        except requests.Timeout as exc:
            raise KataGoModelNetworkError("The model service timed out") from exc
        except requests.ConnectionError as exc:
            raise KataGoModelNetworkError("The model service is unavailable") from exc
        except requests.HTTPError as exc:
            raise KataGoModelHTTPError("The model service returned an HTTP error") from exc
        try:
            payload = response.json()
        except (TypeError, ValueError) as exc:
            raise KataGoModelFormatError("The model catalog did not return valid JSON") from exc

        if not isinstance(payload, dict) or not isinstance(payload.get("results"), list):
            raise KataGoModelFormatError("The model catalog has an invalid pagination response")

        try:
            count = int(payload.get("count", len(payload["results"])))
        except (TypeError, ValueError) as exc:
            raise KataGoModelFormatError("The model catalog count is invalid") from exc

        return KataGoModelPage(
            count=count,
            next_url=payload.get("next"),
            previous_url=payload.get("previous"),
            results=tuple(KataGoModel.from_api_data(item) for item in payload["results"]),
            url=url,
        )

    def fetch_all_models(self) -> tuple[KataGoModel, ...]:
        """Fetch every paginated model page for local search and filtering."""
        models: list[KataGoModel] = []
        next_url: str | None = NETWORKS_JSON_URL
        while next_url:
            page = self.fetch_page(next_url)
            models.extend(page.results)
            next_url = page.next_url
        return tuple(models)

    def load_cached_models(self) -> tuple[KataGoModel, ...]:
        """Load the last catalog without contacting the network.

        A damaged or old cache is treated as empty so opening the browser can
        still fall back to a normal network refresh.
        """
        try:
            with self._catalog_cache_path.open("r", encoding="utf-8") as source:
                payload = json.load(source)
            if not isinstance(payload, list):
                return ()
            return tuple(KataGoModel.from_api_data(item) for item in payload)
        except (OSError, TypeError, ValueError, KataGoModelError):
            return ()

    def fetch_models_incremental(
        self,
        cached_models: tuple[KataGoModel, ...] = (),
        *,
        on_batch: Callable[[tuple[KataGoModel, ...], int], None] | None = None,
    ) -> tuple[KataGoModel, ...]:
        """Refresh the catalog while reusing the local cache.

        Page 1 is always the only validation request when the cache is current
        or only a few models behind.  A large cache miss fetches the remaining
        pages with four workers.  ``on_batch`` receives the merged catalog
        after every page, allowing the UI and disk cache to update immediately.
        """
        first_page = self.fetch_page(NETWORKS_JSON_URL)
        count = max(0, first_page.count)
        models = self._merge_models(cached_models, first_page.results)
        self._save_cached_models(models)
        if on_batch:
            on_batch(models, count)

        missing = max(0, count - len(cached_models))
        page_size = len(first_page.results)
        if not first_page.next_url or page_size <= 0 or missing <= page_size:
            return models

        total_pages = (count + page_size - 1) // page_size
        page_urls = [
            f"{NETWORKS_JSON_URL}&page={page_number}"
            for page_number in range(2, total_pages + 1)
        ]
        with ThreadPoolExecutor(max_workers=4, thread_name_prefix="katago-models") as pool:
            futures = [pool.submit(self.fetch_page, url) for url in page_urls]
            for future in as_completed(futures):
                page = future.result()
                models = self._merge_models(models, page.results)
                self._save_cached_models(models)
                if on_batch:
                    on_batch(models, count)
        return models

    @staticmethod
    def _merge_models(
        existing: tuple[KataGoModel, ...] | list[KataGoModel],
        incoming: tuple[KataGoModel, ...],
    ) -> tuple[KataGoModel, ...]:
        by_name = {model.name: model for model in existing}
        for model in incoming:
            by_name[model.name] = model
        return tuple(
            sorted(
                by_name.values(),
                key=lambda model: (model.created_at, model.name),
                reverse=True,
            )
        )

    def _save_cached_models(self, models: tuple[KataGoModel, ...]) -> None:
        """Atomically persist catalog progress; a partial write never becomes cache."""
        payload = [
            {
                "name": model.name,
                "created_at": model.created_at,
                "network_size": model.network_size,
                "model_file": model.model_file,
                "model_file_bytes": model.model_file_bytes,
                "model_file_sha256": model.model_file_sha256,
                "training_games_enabled": model.training_games_enabled,
                "rating_games_enabled": model.rating_games_enabled,
                "notes": model.notes,
            }
            for model in models
        ]
        temporary_path = self._catalog_cache_path.with_suffix(".tmp")
        try:
            self._catalog_cache_path.parent.mkdir(parents=True, exist_ok=True)
            with self._catalog_cache_lock:
                with temporary_path.open("w", encoding="utf-8") as target:
                    json.dump(payload, target, ensure_ascii=False)
                os.replace(temporary_path, self._catalog_cache_path)
        except OSError:
            temporary_path.unlink(missing_ok=True)

    def cancel_download(self) -> None:
        self._cancel_event.set()

    def download_model(
        self,
        model: KataGoModel,
        *,
        progress_callback: ProgressCallback | None = None,
    ) -> Path:
        if not self._download_lock.acquire(blocking=False):
            raise KataGoModelError("Another model download is already in progress")

        self._cancel_event.clear()
        temporary_path = self._temporary_path(model)
        final_path = self._final_path(model)
        try:
            self.download_dir.mkdir(parents=True, exist_ok=True)
            try:
                response = self.session.get(
                    model.model_file,
                    stream=True,
                    timeout=self.download_timeout,
                )
                response.raise_for_status()
            except requests.Timeout as exc:
                raise KataGoModelNetworkError("The model download timed out") from exc
            except requests.ConnectionError as exc:
                raise KataGoModelNetworkError("The model download was interrupted") from exc
            except requests.HTTPError as exc:
                raise KataGoModelHTTPError("The model download returned an HTTP error") from exc
            total_bytes = model.model_file_bytes
            digest = hashlib.sha256()
            downloaded_bytes = 0
            with temporary_path.open("wb") as output:
                for chunk in self._iter_chunks(response):
                    if self._cancel_event.is_set():
                        raise KataGoModelCancelled("Model download cancelled")
                    if not chunk:
                        continue
                    output.write(chunk)
                    digest.update(chunk)
                    downloaded_bytes += len(chunk)
                    if progress_callback:
                        progress_callback(
                            DownloadProgress(model, downloaded_bytes, total_bytes)
                        )

            if downloaded_bytes != model.model_file_bytes:
                raise KataGoModelChecksumError(
                    f"Downloaded size mismatch: expected {model.model_file_bytes}, "
                    f"received {downloaded_bytes}"
                )
            actual_sha256 = digest.hexdigest().lower()
            if actual_sha256 != model.model_file_sha256.lower():
                raise KataGoModelChecksumError(
                    f"SHA-256 mismatch: expected {model.model_file_sha256}, "
                    f"received {actual_sha256}"
                )

            os.replace(temporary_path, final_path)
            return final_path
        except Exception:
            temporary_path.unlink(missing_ok=True)
            raise
        finally:
            self._cancel_event.clear()
            self._download_lock.release()

    def _iter_chunks(self, response: Any) -> Iterator[bytes]:
        yield from response.iter_content(chunk_size=self.chunk_size)

    def _final_path(self, model: KataGoModel) -> Path:
        return self.download_dir / f"{self._safe_name(model.name)}{self._model_suffix(model)}"

    def _temporary_path(self, model: KataGoModel) -> Path:
        return self.download_dir / f".{self._safe_name(model.name)}{self._model_suffix(model)}.part"

    @staticmethod
    def _model_suffix(model: KataGoModel) -> str:
        """Preserve KataGo's model format from the API download filename."""
        filename = Path(unquote(urlparse(model.model_file).path)).name.lower()
        if filename.endswith(".txt.gz"):
            return ".txt.gz"
        if filename.endswith(".bin.gz"):
            return ".bin.gz"
        raise KataGoModelFormatError(
            "Unsupported model format; expected a .txt.gz or .bin.gz download"
        )

    @staticmethod
    def _safe_name(name: str) -> str:
        safe_name = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("._")
        if not safe_name:
            raise KataGoModelFormatError("Model name cannot be used as a filename")
        return safe_name
