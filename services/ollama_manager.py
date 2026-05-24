import json
import subprocess
import threading
import time
from typing import Callable, Dict, Optional, Set


class OllamaManager:
    """Small wrapper around the Ollama CLI for local model management."""

    LIST_TIMEOUT_SECONDS = 10
    PULL_IDLE_WARNING_SECONDS = 30
    PULL_TIMEOUT_SECONDS = 3600

    def __init__(self):
        self.local_models: Set[str] = set()
        self.downloading = False
        self._lock = threading.Lock()

    def get_local_models(self) -> Set[str]:
        """Return local model names from `ollama list`."""
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=self.LIST_TIMEOUT_SECONDS,
                encoding="utf-8",
                errors="replace",
            )
        except FileNotFoundError:
            print("Ollama command was not found. Please install Ollama first.")
            return set()
        except subprocess.TimeoutExpired:
            print("Timed out while running `ollama list`.")
            return set()
        except Exception as exc:
            print(f"Failed to list Ollama models: {exc}")
            return set()

        if result.returncode != 0:
            print(f"`ollama list` failed: {result.stderr}")
            return set()

        models = set()
        for line in result.stdout.splitlines()[1:]:
            parts = line.split()
            if parts:
                models.add(parts[0])

        with self._lock:
            self.local_models = models
        return models

    def is_model_available(self, model_name: str) -> bool:
        with self._lock:
            return model_name in self.local_models

    def get_model_size(self, model_name: str) -> Optional[str]:
        """Best-effort model size lookup for downloaded and remote models."""
        local_size = self._get_local_model_size(model_name)
        if local_size:
            return local_size
        return self._get_remote_model_size(model_name)

    def _get_local_model_size(self, model_name: str) -> Optional[str]:
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=self.LIST_TIMEOUT_SECONDS,
                encoding="utf-8",
                errors="replace",
            )
        except Exception:
            return None

        if result.returncode != 0:
            return None

        for line in result.stdout.splitlines()[1:]:
            parts = line.split()
            if len(parts) >= 4 and parts[0] == model_name:
                return f"{parts[2]} {parts[3]}"
        return None

    def _get_remote_model_size(self, model_name: str) -> Optional[str]:
        try:
            result = subprocess.run(
                ["ollama", "show", model_name, "--json"],
                capture_output=True,
                text=True,
                timeout=self.LIST_TIMEOUT_SECONDS,
                encoding="utf-8",
                errors="replace",
            )
        except Exception:
            return None

        if result.returncode != 0:
            return None

        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError:
            return None

        size = data.get("size") or data.get("details", {}).get("size")
        if isinstance(size, int):
            return self._format_bytes(size)
        if isinstance(size, str):
            return size
        return None

    @staticmethod
    def _format_bytes(size: int) -> str:
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
        """Start `ollama pull` in a background thread."""
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
            process = None
            last_output_at = time.monotonic()
            warned_about_idle = False
            try:
                emit_progress(f"Starting download: {model_name}")
                process = subprocess.Popen(
                    ["ollama", "pull", model_name],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                )

                while True:
                    line = process.stdout.readline() if process.stdout else ""
                    if line:
                        last_output_at = time.monotonic()
                        emit_progress(line.strip())
                    elif process.poll() is not None:
                        break
                    else:
                        idle_seconds = time.monotonic() - last_output_at
                        if idle_seconds >= self.PULL_IDLE_WARNING_SECONDS and not warned_about_idle:
                            emit_progress(
                                "No download progress for 30 seconds. Please check your network or Ollama service."
                            )
                            warned_about_idle = True
                        time.sleep(0.2)

                    if time.monotonic() - last_output_at > self.PULL_TIMEOUT_SECONDS:
                        raise subprocess.TimeoutExpired(["ollama", "pull", model_name], self.PULL_TIMEOUT_SECONDS)

                returncode = process.wait(timeout=5)
                if returncode == 0:
                    self.get_local_models()
                    emit_complete(True, f"Downloaded {model_name}")
                else:
                    emit_complete(False, f"`ollama pull` exited with code {returncode}")
            except subprocess.TimeoutExpired:
                if process:
                    process.kill()
                emit_complete(False, "Download timed out.")
            except FileNotFoundError:
                emit_complete(False, "Ollama command was not found.")
            except Exception as exc:
                emit_complete(False, f"Download failed: {exc}")
            finally:
                with self._lock:
                    self.downloading = False

        threading.Thread(target=download_task, daemon=True).start()
        return True

    def get_model_status(self, all_models: list) -> Dict[str, str]:
        self.get_local_models()
        return {
            model: "available" if self.is_model_available(model) else "pending"
            for model in all_models
        }


_ollama_manager_instance: Optional[OllamaManager] = None


def get_ollama_manager() -> OllamaManager:
    global _ollama_manager_instance
    if _ollama_manager_instance is None:
        _ollama_manager_instance = OllamaManager()
    return _ollama_manager_instance
