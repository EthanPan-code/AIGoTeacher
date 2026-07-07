import json
import threading
import traceback

from opencc import OpenCC

from services.keyring_service import get_github_token, normalize_api_key

from .base import LLMProvider


GITHUB_MODELS = [
    "openai/gpt-4o-mini",
    "openai/gpt-4.1-mini",
    "openai/gpt-4.1-nano",
    "openai/gpt-4.1",
]

# 模型 ID → 顯示名稱對照表（UI 顯示用，API 呼叫仍使用 ID）
GITHUB_MODEL_DISPLAY_NAMES = {
    "openai/gpt-4o-mini": "GPT-4o mini",
    "openai/gpt-4.1-mini": "GPT-4.1 mini",
    "openai/gpt-4.1-nano": "GPT-4.1 nano",
    "openai/gpt-4.1": "GPT-4.1",
}

GITHUB_MODELS_ENDPOINT = "https://models.github.ai/inference/chat/completions"


class GithubProvider(LLMProvider):
    def __init__(
        self,
        ui_callback,
        status_callback=None,
        model_name=None,
        translator=None,
        language_getter=None,
        api_key=None,
        on_complete_callback=None,
        tone="friendly",
        custom_prompt=None,
    ):
        super().__init__(ui_callback, status_callback, translator, language_getter, on_complete_callback, tone, custom_prompt)
        self.model_name = model_name or GITHUB_MODELS[0]
        self.api_key = normalize_api_key(api_key) or get_github_token()
        self.cc = OpenCC("s2twp")

    def get_available_models(self):
        return GITHUB_MODELS

    @staticmethod
    def get_model_display_name(model_id):
        return GITHUB_MODEL_DISPLAY_NAMES.get(model_id, model_id)

    def validate_config(self):
        if not self.api_key:
            return (False, self.tr("error.github_token_missing_env"))
        return (True, None)

    def set_model(self, model_name):
        self.model_name = model_name
        if self.status_callback:
            self.status_callback(self.tr("status.llm_provider_switched", provider="GitHub Models", model=self.get_model_display_name(model_name)))

    def start_commentary(self, critical_data):
        if self.is_generating:
            return

        self.is_generating = True
        self.ui_callback(critical_data.get("thinking_text", self.tr("teacher.github_thinking")))
        threading.Thread(target=self._generate_task, args=(critical_data,), daemon=True).start()

    def _generate_task(self, data):
        try:
            import requests

            user_prompt = self.build_commentary_prompt(data)
            conversation = data.get("conversation")
            stream = True
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Accept": "text/event-stream" if stream else "application/json",
                "Content-Type": "application/json",
            }

            # Build messages list from conversation history + current prompt
            messages = []
            if conversation:
                for msg in conversation:
                    messages.append({"role": msg["role"], "content": msg["content"]})
            messages.append({"role": "user", "content": user_prompt})

            payload = {
                "model": self.model_name,
                "messages": messages,
                "max_tokens": 512,
                "temperature": 0.60,
                "top_p": 0.95,
                "stream": stream,
            }

            response = requests.post(GITHUB_MODELS_ENDPOINT, headers=headers, json=payload, stream=stream, timeout=30)

            if response.status_code != 200:
                raise Exception(f"GitHub Models API error (HTTP {response.status_code}): {response.text}")

            full_content = ""
            for line in response.iter_lines():
                if line:
                    line_str = line.decode("utf-8") if isinstance(line, bytes) else line
                    if line_str.startswith("data: "):
                        if line_str[6:].strip() == "[DONE]":
                            break
                        try:
                            chunk_json = json.loads(line_str[6:])
                            if "choices" in chunk_json and len(chunk_json["choices"]) > 0:
                                delta = chunk_json["choices"][0].get("delta", {})
                                if "content" in delta:
                                    part = delta["content"]
                                    full_content += part
                                    converted_text = self.cc.convert(full_content) if self.language_getter() == "zh_TW" else full_content
                                    self.ui_callback(converted_text)
                        except json.JSONDecodeError:
                            continue

        except Exception as e:
            print(f"GitHub Models API commentary failed: {e}")
            if getattr(self, "error_callback", None):
                try:
                    self.error_callback(e, traceback.format_exc())
                except Exception as callback_error:
                    print(f"GitHub error callback failed: {callback_error}")
            self.ui_callback(self._fallback_commentary(data, e))
            if self.status_callback:
                self.status_callback(self.tr("status.github_fallback"))
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

        return self.tr(
            "teacher.fallback",
            turn=turn,
            user_move=user_move,
            winrate_drop=winrate_drop,
            best_move=best_move,
            hint=self.tr("teacher.github_fallback"),
        )
