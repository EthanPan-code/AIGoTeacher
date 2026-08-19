import threading
import traceback
from typing import Dict, Optional

from opencc import OpenCC

from services.ollama_manager import (
    DEFAULT_OLLAMA_MODEL,
    OLLAMA_RECOMMENDED_MODELS,
    OllamaModelInfo,
)

from .base import LLMProvider


# Compatibility exports for older integrations. These are recommendations only;
# runtime availability comes from OllamaManager's /api/tags catalog.
OLLAMA_MODELS = OLLAMA_RECOMMENDED_MODELS
OLLAMA_MODEL_DISPLAY_NAMES = {}


class OllamaProvider(LLMProvider):
    def __init__(
        self,
        ui_callback,
        status_callback=None,
        model_name=DEFAULT_OLLAMA_MODEL,
        translator=None,
        language_getter=None,
        on_complete_callback=None,
        tone="friendly",
        custom_prompt=None,
    ):
        super().__init__(
            ui_callback=ui_callback,
            status_callback=status_callback,
            translator=translator,
            language_getter=language_getter,
            on_complete_callback=on_complete_callback,
            tone=tone,
            custom_prompt=custom_prompt,
        )
        self.model_name = model_name or DEFAULT_OLLAMA_MODEL
        self.cc = OpenCC("s2twp")

    def get_available_models(self):
        from services.ollama_manager import get_ollama_manager

        return [info.name for info in get_ollama_manager().get_model_catalog()]

    @staticmethod
    def get_model_display_name(model_id):
        return model_id

    def get_model_info(self, model_name: Optional[str] = None) -> Optional[OllamaModelInfo]:
        from services.ollama_manager import get_ollama_manager

        return get_ollama_manager().get_model(model_name or self.model_name)

    def is_cloud_model(self, model_name: str) -> bool:
        info = self.get_model_info(model_name)
        return bool(info and info.is_cloud)

    def validate_config(self):
        from services.ollama_manager import get_ollama_manager

        available, detail = get_ollama_manager().check_service()
        if available:
            return (True, None)
        return (False, self.tr("error.ollama_service_unavailable", error=detail))

    def set_model(self, model_name):
        self.model_name = model_name
        if self.status_callback:
            self.status_callback(self.tr("status.ollama_model_changed", model=self.get_model_display_name(model_name)))

    def get_local_models(self):
        from services.ollama_manager import get_ollama_manager

        return get_ollama_manager().get_local_models()

    def get_cloud_models(self):
        from services.ollama_manager import get_ollama_manager

        return get_ollama_manager().get_cloud_models()

    def get_model_status(self, all_models=None) -> Dict[str, str]:
        from services.ollama_manager import get_ollama_manager

        return get_ollama_manager().get_model_status(all_models)

    def is_model_available(self, model_name: str) -> bool:
        from services.ollama_manager import get_ollama_manager

        return get_ollama_manager().is_model_available(model_name)

    def get_model_size(self, model_name: str) -> Optional[str]:
        from services.ollama_manager import get_ollama_manager

        return get_ollama_manager().get_model_size(model_name)

    def start_model_download(self, model_name, progress_callback=None, complete_callback=None) -> bool:
        from services.ollama_manager import get_ollama_manager

        return get_ollama_manager().pull_model_async(model_name, progress_callback, complete_callback)

    def is_downloading(self) -> bool:
        from services.ollama_manager import get_ollama_manager

        return get_ollama_manager().is_downloading()

    def start_commentary(self, critical_data):
        if self.is_generating:
            return

        self.is_generating = True
        self.ui_callback(critical_data.get("thinking_text", self.tr("teacher.thinking")))
        threading.Thread(target=self._generate_task, args=(critical_data,), daemon=True).start()

    def _generate_task(self, data):
        try:
            import ollama

            prompt = self.build_commentary_prompt(data)
            messages = list(data.get("conversation") or [])
            messages.append({"role": "user", "content": prompt})
            response = ollama.chat(model=self.model_name, messages=messages, stream=True)

            full_content = ""
            for chunk in response:
                if "message" in chunk and "content" in chunk["message"]:
                    part = chunk["message"]["content"]
                    full_content += part
                    converted_text = self.cc.convert(full_content) if self.language_getter() == "zh_TW" else full_content
                    self.ui_callback(converted_text)

        except Exception as error:
            print(f"Ollama commentary failed: {error}")
            if getattr(self, "error_callback", None):
                try:
                    self.error_callback(error, traceback.format_exc())
                except Exception as callback_error:
                    print(f"Ollama error callback failed: {callback_error}")
            self.ui_callback(self._fallback_commentary(data, error))
            if self.status_callback:
                self.status_callback(self.tr("status.ollama_fallback"))
        finally:
            self.is_generating = False
            if self.on_complete_callback:
                try:
                    self.on_complete_callback()
                except Exception as error:
                    print(f"Completion callback failed: {error}")

    def _fallback_commentary(self, data, error):
        if data.get("fallback_text"):
            return data["fallback_text"]

        turn = data.get("turn", "?")
        user_move = data.get("user_move", "?")
        winrate_drop = data.get("winrate_drop", 0) * 100
        best_move = self.tr("teacher.best_unknown")
        # Fallback must never present the opponent's post-mistake response as
        # an alternative available to the player who made the mistake.
        best_moves = data.get("post_mistake_opponent_best_moves") or []
        if best_moves:
            best_move = best_moves[0].get("move", self.tr("teacher.best_unknown"))

        error_text = str(error)
        if "requires more system memory" in error_text:
            hint = self.tr("teacher.memory_hint")
        elif "model" in error_text.lower() and ("not found" in error_text.lower() or "pull" in error_text.lower()):
            hint = self.tr("teacher.model_not_found_hint", model=self.model_name)
        elif self.is_cloud_model(self.model_name):
            hint = self.tr("teacher.cloud_error_hint")
        else:
            hint = self.tr("teacher.generic_error_hint", error=error_text)

        return self.tr(
            "teacher.fallback",
            turn=turn,
            user_move=user_move,
            winrate_drop=winrate_drop,
            best_move=best_move,
            hint=hint,
        )
