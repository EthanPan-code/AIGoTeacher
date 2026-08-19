import json
import threading
import traceback

from opencc import OpenCC

from services.keyring_service import get_openrouter_api_key, normalize_api_key

from .base import LLMProvider


OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_MODELS_ENDPOINT = f"{OPENROUTER_BASE_URL}/models"
OPENROUTER_CHAT_ENDPOINT = f"{OPENROUTER_BASE_URL}/chat/completions"
OPENROUTER_REFERER = "https://github.com/EthanPan-code/AIGoTeacher"
OPENROUTER_TITLE = "AI Go Teacher"

# Used only when /models cannot be reached. Successful discovery always wins.
OPENROUTER_MODELS = [
    "openai/gpt-4o-mini",
    "google/gemini-2.0-flash-001",
    "anthropic/claude-3.5-sonnet",
]


def get_publisher_from_model_id(model_id):
    if not model_id or not isinstance(model_id, str):
        return "unknown"
    return model_id.split("/", 1)[0] if "/" in model_id else "unknown"


def group_models_by_publisher(model_ids):
    grouped = {}
    for model_id in model_ids or []:
        grouped.setdefault(get_publisher_from_model_id(model_id), []).append(model_id)
    return grouped


def discover_openrouter_models(api_key=None, timeout=8):
    """Return (True, model_ids) or (False, error_message)."""
    try:
        import requests

        headers = {"Accept": "application/json"}
        normalized = normalize_api_key(api_key) or get_openrouter_api_key()
        if normalized:
            headers["Authorization"] = f"Bearer {normalized}"
        response = requests.get(OPENROUTER_MODELS_ENDPOINT, headers=headers, timeout=timeout)
        if response.status_code != 200:
            return (False, f"HTTP {response.status_code}")

        data = response.json()
        items = data.get("data", []) if isinstance(data, dict) else []
        model_ids = []
        for item in items:
            if isinstance(item, dict) and item.get("id"):
                model_ids.append(item["id"])
            elif isinstance(item, str) and item:
                model_ids.append(item)
        if not model_ids:
            return (False, "empty model list")
        return (True, model_ids)
    except Exception as error:
        return (False, str(error))


class OpenRouterProvider(LLMProvider):
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
        super().__init__(
            ui_callback=ui_callback,
            status_callback=status_callback,
            translator=translator,
            language_getter=language_getter,
            on_complete_callback=on_complete_callback,
            tone=tone,
            custom_prompt=custom_prompt,
        )
        self.model_name = model_name or OPENROUTER_MODELS[0]
        self.api_key = normalize_api_key(api_key) or get_openrouter_api_key()
        self.cc = OpenCC("s2twp")

    def get_available_models(self):
        return OPENROUTER_MODELS

    @staticmethod
    def get_model_display_name(model_id):
        return model_id

    def discover_available_models(self):
        ok, result = discover_openrouter_models(self.api_key, timeout=8)
        if ok:
            return (result, False, None)
        return (OPENROUTER_MODELS, True, result)

    def validate_config(self):
        if not self.api_key:
            return (False, self.tr("error.openrouter_api_key_missing_env"))
        return (True, None)

    def set_model(self, model_name):
        self.model_name = model_name
        if self.status_callback:
            self.status_callback(self.tr(
                "status.llm_provider_switched",
                provider="OpenRouter",
                model=self.get_model_display_name(model_name),
            ))

    def start_commentary(self, critical_data):
        if self.is_generating:
            return
        self.is_generating = True
        self.ui_callback(critical_data.get("thinking_text", self.tr("teacher.openrouter_thinking")))
        threading.Thread(target=self._generate_task, args=(critical_data,), daemon=True).start()

    def _generate_task(self, data):
        try:
            import requests

            user_prompt = self.build_commentary_prompt(data)
            messages = list(data.get("conversation") or [])
            messages.append({"role": "user", "content": user_prompt})
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Accept": "text/event-stream",
                "Content-Type": "application/json",
                "HTTP-Referer": OPENROUTER_REFERER,
                "X-OpenRouter-Title": OPENROUTER_TITLE,
            }
            payload = {
                "model": self.model_name,
                "messages": messages,
                "max_tokens": 512,
                "temperature": 0.60,
                "top_p": 0.95,
                "stream": True,
            }
            response = requests.post(
                OPENROUTER_CHAT_ENDPOINT,
                headers=headers,
                json=payload,
                stream=True,
                timeout=30,
            )
            if response.status_code != 200:
                raise RuntimeError(f"OpenRouter API error (HTTP {response.status_code}): {response.text}")

            full_content = ""
            for line in response.iter_lines():
                if not line:
                    continue
                line_str = line.decode("utf-8") if isinstance(line, bytes) else line
                if not line_str.startswith("data: "):
                    continue
                raw_data = line_str[6:].strip()
                if raw_data == "[DONE]":
                    break
                try:
                    chunk = json.loads(raw_data)
                except json.JSONDecodeError:
                    continue
                if chunk.get("error"):
                    error = chunk["error"]
                    raise RuntimeError(error.get("message", "OpenRouter stream error"))
                choices = chunk.get("choices") or []
                if not choices:
                    continue
                choice = choices[0]
                if choice.get("finish_reason") == "error":
                    raise RuntimeError("OpenRouter stream finished with an error")
                delta = choice.get("delta") or {}
                part = delta.get("content")
                if part:
                    full_content += part
                    converted = self.cc.convert(full_content) if self.language_getter() == "zh_TW" else full_content
                    self.ui_callback(converted)
        except Exception as error:
            print(f"OpenRouter API commentary failed: {error}")
            if getattr(self, "error_callback", None):
                try:
                    self.error_callback(error, traceback.format_exc())
                except Exception as callback_error:
                    print(f"OpenRouter error callback failed: {callback_error}")
            self.ui_callback(self._fallback_commentary(data, error))
            if self.status_callback:
                self.status_callback(self.tr("status.openrouter_fallback"))
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
        best_moves = data.get("post_mistake_opponent_best_moves") or []
        best_move = best_moves[0].get("move", self.tr("teacher.best_unknown")) if best_moves else self.tr("teacher.best_unknown")
        return self.tr(
            "teacher.fallback",
            turn=data.get("turn", "?"),
            user_move=data.get("user_move", "?"),
            winrate_drop=data.get("winrate_drop", 0) * 100,
            best_move=best_move,
            hint=self.tr("teacher.openrouter_fallback"),
        )
