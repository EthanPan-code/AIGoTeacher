import json
import os
import threading
import time
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Set


OLLAMA_BASE_URL = os.getenv("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
OLLAMA_RECOMMENDED_LOCAL_MODELS = [
    "qwen2.5:1.5b",
    "llama3.2:1b",
    "gemma2:2b",
    "qwen2.5:3b",
    "qwen2.5:7b",
]
OLLAMA_RECOMMENDED_CLOUD_MODELS = [
    "gemma4:31b-cloud",
    "minimax-m2.1:cloud",
]
OLLAMA_RECOMMENDED_MODELS = [
    *OLLAMA_RECOMMENDED_LOCAL_MODELS,
    *OLLAMA_RECOMMENDED_CLOUD_MODELS,
]
DEFAULT_OLLAMA_MODEL = "qwen2.5:3b"


@dataclass(frozen=True)
class OllamaModelInfo:
    name: str
    model: str = ""
    kind: str = "local"
    remote_model: Optional[str] = None
    remote_host: Optional[str] = None
    size_bytes: Optional[int] = None
    modified_at: Optional[str] = None
    details: Dict = field(default_factory=dict)
    capabilities: List[str] = field(default_factory=list)

    @classmethod
    def from_payload(cls, payload: dict):
        name = str(payload.get("name") or payload.get("model") or "").strip()
        remote_model = payload.get("remote_model")
        remote_host = payload.get("remote_host")
        kind = "cloud" if remote_model or remote_host else "local"
        size = payload.get("size")
        if not isinstance(size, int):
            size = None
        details = payload.get("details") if isinstance(payload.get("details"), dict) else {}
        capabilities = payload.get("capabilities")
        if not isinstance(capabilities, list):
            capabilities = []
        return cls(
            name=name,
            model=str(payload.get("model") or name),
            kind=kind,
            remote_model=str(remote_model) if remote_model else None,
            remote_host=str(remote_host) if remote_host else None,
            size_bytes=size,
            modified_at=payload.get("modified_at"),
            details=details,
            capabilities=[str(item) for item in capabilities],
        )

    @property
    def is_cloud(self) -> bool:
        return self.kind == "cloud"


class OllamaManager:
    """REST client and catalog cache for the local Ollama service."""

    REQUEST_TIMEOUT_SECONDS = 10
    CATALOG_TTL_SECONDS = 10
    PULL_TIMEOUT_SECONDS = 3600

    def __init__(self, base_url: str = OLLAMA_BASE_URL):
        self.base_url = (base_url or OLLAMA_BASE_URL).rstrip("/")
        self.local_models: Set[str] = set()
        self.cloud_models: Set[str] = set()
        self.catalog: Dict[str, OllamaModelInfo] = {}
        self.catalog_error: Optional[str] = None
        self.service_version: Optional[str] = None
        self.catalog_updated_at = 0.0
        self.downloading = False
        self._lock = threading.Lock()

    def check_service(self):
        """Return (available, version_or_error) without changing the catalog."""
        try:
            import requests

            response = requests.get(
                f"{self.base_url}/api/version",
                timeout=self.REQUEST_TIMEOUT_SECONDS,
            )
            if response.status_code != 200:
                return False, f"HTTP {response.status_code}"
            data = response.json()
            version = data.get("version") if isinstance(data, dict) else None
            return True, str(version or "unknown")
        except Exception as error:
            return False, str(error)

    def refresh_model_catalog(self, force: bool = False):
        """Return (models, error), retaining the last good catalog on failure."""
        with self._lock:
            if not force and self.catalog and time.monotonic() - self.catalog_updated_at < self.CATALOG_TTL_SECONDS:
                return list(self.catalog.values()), self.catalog_error

        try:
            import requests

            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=self.REQUEST_TIMEOUT_SECONDS,
            )
            if response.status_code != 200:
                raise RuntimeError(f"HTTP {response.status_code}")
            data = response.json()
            items = data.get("models", []) if isinstance(data, dict) else []
            models = {}
            for item in items:
                if not isinstance(item, dict):
                    continue
                info = OllamaModelInfo.from_payload(item)
                if info.name:
                    models[info.name] = info
            with self._lock:
                self.catalog = models
                self.local_models = {name for name, info in models.items() if not info.is_cloud}
                self.cloud_models = {name for name, info in models.items() if info.is_cloud}
                self.catalog_error = None
                self.catalog_updated_at = time.monotonic()
                return list(models.values()), None
        except Exception as error:
            message = str(error)
            with self._lock:
                self.catalog_error = message
                return list(self.catalog.values()), message

    def get_model_catalog(self, force: bool = False) -> List[OllamaModelInfo]:
        models, _error = self.refresh_model_catalog(force=force)
        return models

    def get_model(self, model_name: str, refresh: bool = False) -> Optional[OllamaModelInfo]:
        self.refresh_model_catalog(force=refresh)
        with self._lock:
            return self.catalog.get(model_name)

    def get_cached_model(self, model_name: str) -> Optional[OllamaModelInfo]:
        """Read a model without triggering network I/O."""
        with self._lock:
            return self.catalog.get(model_name)

    def get_local_models(self, force: bool = False) -> Set[str]:
        self.refresh_model_catalog(force=force)
        with self._lock:
            return set(self.local_models)

    def get_cloud_models(self, force: bool = False) -> Set[str]:
        self.refresh_model_catalog(force=force)
        with self._lock:
            return set(self.cloud_models)

    def is_model_available(self, model_name: str) -> bool:
        return self.get_model(model_name) is not None

    def get_model_size(self, model_name: str) -> Optional[str]:
        info = self.get_model(model_name)
        if not info or info.size_bytes is None:
            return None
        return self.format_bytes(info.size_bytes)

    @staticmethod
    def format_bytes(size: int) -> str:
        value = float(size)
        for unit in ("B", "KB", "MB", "GB", "TB"):
            if value < 1024 or unit == "TB":
                return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
            value /= 1024
        return f"{size} B"

    def pull_model_async(
        self,
        model_name: str,
        progress_callback: Optional[Callable[[str], None]] = None,
        complete_callback: Optional[Callable[[bool, str], None]] = None,
    ) -> bool:
        """Start a streaming REST pull for a local model."""
        model_name = (model_name or "").strip()
        if not model_name:
            if complete_callback:
                complete_callback(False, "Model name is required.")
            return False
        info = self.get_model(model_name)
        if info and info.is_cloud:
            if complete_callback:
                complete_callback(False, "Cloud models cannot be downloaded.")
            return False

        with self._lock:
            if self.downloading:
                if progress_callback:
                    progress_callback("Another Ollama model download is already running.")
                return False
            self.downloading = True

        def emit_progress(message: str):
            if progress_callback:
                progress_callback(message)

        def emit_complete(success: bool, message: str):
            if complete_callback:
                complete_callback(success, message)

        def download_task():
            try:
                import requests

                emit_progress(f"Starting download: {model_name}")
                response = requests.post(
                    f"{self.base_url}/api/pull",
                    json={"model": model_name, "stream": True},
                    stream=True,
                    timeout=self.PULL_TIMEOUT_SECONDS,
                )
                if response.status_code != 200:
                    raise RuntimeError(f"HTTP {response.status_code}: {response.text}")
                completed = total = None
                for line in response.iter_lines():
                    if not line:
                        continue
                    raw = line.decode("utf-8") if isinstance(line, bytes) else line
                    try:
                        item = json.loads(raw)
                    except json.JSONDecodeError:
                        emit_progress(raw)
                        continue
                    if item.get("error"):
                        raise RuntimeError(str(item["error"]))
                    status = item.get("status") or ""
                    completed = item.get("completed", completed)
                    total = item.get("total", total)
                    if completed is not None and total:
                        emit_progress(f"{status} ({completed}/{total})")
                    elif status:
                        emit_progress(status)
                self.refresh_model_catalog(force=True)
                emit_complete(True, f"Downloaded {model_name}")
            except Exception as error:
                emit_complete(False, f"Download failed: {error}")
            finally:
                with self._lock:
                    self.downloading = False

        threading.Thread(target=download_task, daemon=True).start()
        return True

    def is_downloading(self) -> bool:
        with self._lock:
            return self.downloading

    def get_model_status(self, all_models: Optional[list] = None) -> Dict[str, str]:
        models = self.get_model_catalog()
        status = {info.name: ("cloud" if info.is_cloud else "available") for info in models}
        for model in all_models or []:
            status.setdefault(model, "available" if model in self.catalog else "pending")
        return status


_ollama_manager_instance: Optional[OllamaManager] = None


def get_ollama_manager() -> OllamaManager:
    global _ollama_manager_instance
    if _ollama_manager_instance is None:
        _ollama_manager_instance = OllamaManager()
    return _ollama_manager_instance
