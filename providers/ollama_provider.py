import threading
from typing import Callable, Dict, Optional

from opencc import OpenCC

from .base import LLMProvider


OLLAMA_MODELS = ["qwen2.5:1.5b", "llama3.2:1b", "gemma2:2b", "qwen2.5:3b", "qwen2.5:7b"]


class OllamaProvider(LLMProvider):
    def __init__(
        self,
        ui_callback,
        status_callback=None,
        model_name="qwen2.5:1.5b",
        translator=None,
        language_getter=None,
        on_complete_callback=None,
        tone="friendly",
        custom_prompt=None,
    ):
        super().__init__(ui_callback, status_callback, translator, language_getter, on_complete_callback, tone, custom_prompt)
        self.model_name = model_name
        self.cc = OpenCC("s2twp")

    def get_available_models(self):
        return OLLAMA_MODELS

    def validate_config(self):
        try:
            import ollama  # noqa: F401

            return (True, None)
        except Exception as e:
            return (False, f"Ollama validation failed: {str(e)}")

    def set_model(self, model_name):
        self.model_name = model_name
        if self.status_callback:
            self.status_callback(self.tr("status.ollama_model_changed", model=model_name))

    def get_local_models(self):
        from services.ollama_manager import get_ollama_manager

        return get_ollama_manager().get_local_models()

    def get_model_status(self) -> Dict[str, str]:
        from services.ollama_manager import get_ollama_manager

        return get_ollama_manager().get_model_status(OLLAMA_MODELS)

    def is_model_available(self, model_name: str) -> bool:
        from services.ollama_manager import get_ollama_manager

        return get_ollama_manager().is_model_available(model_name)

    def get_model_size(self, model_name: str) -> Optional[str]:
        from services.ollama_manager import get_ollama_manager

        return get_ollama_manager().get_model_size(model_name)

    def start_model_download(
        self,
        model_name: str,
        progress_callback: Optional[Callable[[str], None]] = None,
        complete_callback: Optional[Callable[[bool, str], None]] = None,
    ) -> bool:
        from services.ollama_manager import get_ollama_manager

        return get_ollama_manager().pull_model_async(model_name, progress_callback, complete_callback)

    def is_downloading(self) -> bool:
        from services.ollama_manager import get_ollama_manager

        return get_ollama_manager().downloading

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

            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt},
                ],
                stream=True,
            )

            full_content = ""
            for chunk in response:
                if "message" in chunk and "content" in chunk["message"]:
                    part = chunk["message"]["content"]
                    full_content += part
                    converted_text = self.cc.convert(full_content) if self.language_getter() == "zh_TW" else full_content
                    self.ui_callback(converted_text)

        except Exception as e:
            print(f"Ollama commentary failed: {e}")
            self.ui_callback(self._fallback_commentary(data, e))
            if self.status_callback:
                self.status_callback(self.tr("status.ollama_fallback"))
        finally:
            self.is_generating = False
            if self.on_complete_callback:
                try:
                    self.on_complete_callback()
                except Exception as e:
                    print(f"Completion callback failed: {e}")

    def _fallback_commentary(self, data, error):
        if data.get("fallback_text"):
            return data["fallback_text"]

        turn = data.get("turn", "?")
        user_move = data.get("user_move", "?")
        winrate_drop = data.get("winrate_drop", 0) * 100
        best_move = self.tr("teacher.best_unknown")
        best_moves = data.get("current_best_moves") or []
        if best_moves:
            best_move = best_moves[0].get("move", self.tr("teacher.best_unknown"))

        error_text = str(error)
        if "requires more system memory" in error_text:
            hint = self.tr("teacher.memory_hint")
        elif "model" in error_text.lower() and ("not found" in error_text.lower() or "pull" in error_text.lower()):
            hint = self.tr("teacher.model_not_found_hint", model=self.model_name)
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
