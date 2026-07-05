import json
import threading

from opencc import OpenCC

from services.keyring_service import get_nvidia_api_key, normalize_api_key

from .base import LLMProvider


NVIDIA_MODELS = [
    "meta/llama-3.1-70b-instruct",
    "openai/gpt-oss-120b",
    "moonshotai/kimi-k2.6",
    "z-ai/glm-5.2",
    "google/gemma-4-31b-it",
    "nvidia/llama-3.1-nemotron-nano-vl-8b-v1",
]


class NvidiaProvider(LLMProvider):
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
        self.model_name = model_name or NVIDIA_MODELS[0]
        self.api_key = normalize_api_key(api_key) or get_nvidia_api_key()
        self.cc = OpenCC("s2twp")

    def get_available_models(self):
        return NVIDIA_MODELS

    def validate_config(self):
        if not self.api_key:
            return (False, self.tr("error.nvidia_api_key_missing_env"))
        if not self.api_key.startswith("nvapi-"):
            return (False, self.tr("error.nvidia_api_key_invalid"))
        return (True, None)

    def set_model(self, model_name):
        self.model_name = model_name
        if self.status_callback:
            self.status_callback(self.tr("status.llm_provider_switched", provider="NVIDIA", model=model_name))

    def start_commentary(self, critical_data):
        if self.is_generating:
            return

        self.is_generating = True
        self.ui_callback(critical_data.get("thinking_text", self.tr("teacher.nvidia_thinking")))
        threading.Thread(target=self._generate_task, args=(critical_data,), daemon=True).start()

    def _generate_task(self, data):
        try:
            import requests

            user_prompt = self.build_commentary_prompt(data)
            stream = True
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Accept": "text/event-stream" if stream else "application/json",
                "Content-Type": "application/json",
            }

            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "user", "content": user_prompt},
                ],
                "max_tokens": 512,
                "temperature": 0.60,
                "top_p": 0.95,
                "stream": stream,
            }

            invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
            response = requests.post(invoke_url, headers=headers, json=payload, stream=stream, timeout=30)

            if response.status_code != 200:
                raise Exception(f"NVIDIA API error (HTTP {response.status_code}): {response.text}")

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
            print(f"NVIDIA API commentary failed: {e}")
            self.ui_callback(self._fallback_commentary(data, e))
            if self.status_callback:
                self.status_callback(self.tr("status.nvidia_fallback"))
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
            hint=self.tr("teacher.nvidia_fallback"),
        )
