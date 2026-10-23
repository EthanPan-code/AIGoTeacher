"""KataGo Training API model catalog and download services."""

from __future__ import annotations

import hashlib
import os
import re
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterator

import requests


API_BASE_URL = "https://katagotraining.org/api"
NETWORKS_URL = f"{API_BASE_URL}/networks/"


class KataGoModelError(RuntimeError):
    """Base error raised by the KataGo model service."""


class KataGoModelFormatError(KataGoModelError):
    """Raised when the API response is missing required model fields."""


class KataGoModelChecksumError(KataGoModelError):
    """Raised when a downloaded model does not match its advertised hash."""


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

    @property
    def is_downloading(self) -> bool:
        return self._download_lock.locked()

    def fetch_page(self, url: str = NETWORKS_URL) -> KataGoModelPage:
        response = self.session.get(url, timeout=self.api_timeout)
        response.raise_for_status()
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
            response = self.session.get(
                model.model_file,
                stream=True,
                timeout=self.download_timeout,
            )
            response.raise_for_status()
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
        return self.download_dir / f"{self._safe_name(model.name)}.bin.gz"

    def _temporary_path(self, model: KataGoModel) -> Path:
        return self.download_dir / f".{self._safe_name(model.name)}.bin.gz.part"

    @staticmethod
    def _safe_name(name: str) -> str:
        safe_name = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("._")
        if not safe_name:
            raise KataGoModelFormatError("Model name cannot be used as a filename")
        return safe_name
