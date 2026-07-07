import threading
import traceback
from typing import Callable, Dict, Optional

from opencc import OpenCC

from .base import LLMProvider


OLLAMA_LOCAL_MODELS = ["qwen2.5:1.5b", "llama3.2:1b", "gemma2:2b", "qwen2.5:3b", "qwen2.5:7b"]
OLLAMA_CLOUD_MODELS = ["gemma4:31b-cloud", "minimax-m2.1:cloud"]
OLLAMA_PAID_MODELS = {"kimi-k2.6:cloud"}
OLLAMA_MODELS = [
    model
    for model in [*OLLAMA_LOCAL_MODELS, *OLLAMA_CLOUD_MODELS]
    if model not in OLLAMA_PAID_MODELS
]

# 模型 ID → 顯示名稱對照表（UI 顯示用，ollama CLI 與 API 呼叫仍使用 ID）
# 未列於此表的 ID 會 fallback 顯示原始 ID（支援使用者自行 ollama pull 的模型）
OLLAMA_MODEL_DISPLAY_NAMES = {
    "qwen2.5:1.5b": "Qwen2.5 1.5B",
    "llama3.2:1b": "Llama3.2 1B",
    "gemma2:2b": "Gemma2 2B",
    "qwen2.5:3b": "Qwen2.5 3B",
    "qwen2.5:7b": "Qwen2.5 7B",
    "gemma4:31b-cloud": "Gemma4 31B",
    "minimax-m2.1:cloud": "MiniMax M2.1",
}


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

    @staticmethod
    def get_model_display_name(model_id):
        return OLLAMA_MODEL_DISPLAY_NAMES.get(model_id, model_id)

    @staticmethod
    def is_cloud_model(model_name: str) -> bool:
        return "cloud" in (model_name or "").lower()

    @staticmethod
    def is_paid_model(model_name: str) -> bool:
        normalized = (model_name or "").lower()
        return normalized in OLLAMA_PAID_MODELS or ":paid" in normalized

    def validate_config(self):
        try:
            import ollama  # noqa: F401

            return (True, None)
        except Exception as e:
            return (False, f"Ollama validation failed: {str(e)}")

    def set_model(self, model_name):
        self.model_name = model_name
        if self.status_callback:
            self.status_callback(self.tr("status.ollama_model_changed", model=self.get_model_display_name(model_name)))

    def get_local_models(self):
        from services.ollama_manager import get_ollama_manager

        return get_ollama_manager().get_local_models()

    def get_model_status(self) -> Dict[str, str]:
        from services.ollama_manager import get_ollama_manager

        visible_models = [model for model in OLLAMA_MODELS if not self.is_paid_model(model)]
        status = get_ollama_manager().get_model_status(
            [model for model in visible_models if not self.is_cloud_model(model)]
        )
        for model in visible_models:
            if self.is_cloud_model(model):
                status[model] = "cloud"
        return status

    def is_model_available(self, model_name: str) -> bool:
        if self.is_cloud_model(model_name):
            return True

        from services.ollama_manager import get_ollama_manager

        return get_ollama_manager().is_model_available(model_name)

    def get_model_size(self, model_name: str) -> Optional[str]:
        if self.is_cloud_model(model_name):
            return None

        from services.ollama_manager import get_ollama_manager

        return get_ollama_manager().get_model_size(model_name)

    def start_model_download(
        self,
        model_name: str,
        progress_callback: Optional[Callable[[str], None]] = None,
        complete_callback: Optional[Callable[[bool, str], None]] = None,
    ) -> bool:
        if self.is_cloud_model(model_name):
            return False

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
            conversation = data.get("conversation")

            # Build messages list from conversation history + current prompt
            messages = []
            if conversation:
                for msg in conversation:
                    messages.append({"role": msg["role"], "content": msg["content"]})
            messages.append({"role": "user", "content": prompt})

            response = ollama.chat(
                model=self.model_name,
                messages=messages,
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
            if getattr(self, "error_callback", None):
                try:
                    self.error_callback(e, traceback.format_exc())
                except Exception as callback_error:
                    print(f"Ollama error callback failed: {callback_error}")
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
