import json
import threading
import traceback

from opencc import OpenCC

from services.keyring_service import get_nvidia_api_key, normalize_api_key

from .base import LLMProvider


# NIM 端點基礎 URL
NIM_BASE_URL = "https://integrate.api.nvidia.com"

# 內建 fallback 模型清單（端點探索失敗時使用）
NVIDIA_MODELS = [
    "meta/llama-3.1-70b-instruct",
    "openai/gpt-oss-120b",
    "moonshotai/kimi-k2.7-code",
    "z-ai/glm-5.2",
    "google/gemma-4-31b-it",
    "nvidia/nemotron-3-nano-30b-a3b",
]

# 模型 ID → 顯示名稱對照表（UI 顯示用，API 呼叫仍使用 ID）
# 動態探索模式下不再使用此對照表，僅保留供 fallback 顯示與舊流程相容
NVIDIA_MODEL_DISPLAY_NAMES = {
    "meta/llama-3.1-70b-instruct": "Llama 3.1 70B Instruct",
    "openai/gpt-oss-120b": "GPT-OSS 120B",
    "moonshotai/kimi-k2.7-code": "Kimi K2.7 Code",
    "z-ai/glm-5.2": "GLM 5.2",
    "google/gemma-4-31b-it": "Gemma 4 31B IT",
    "nvidia/nemotron-3-nano-30b-a3b": "Nemotron 3 Nano 30B A3B",
}


def get_publisher_from_model_id(model_id):
    """從 model_id 拆出 publisher（第一個 '/' 之前的部分）。

    無 '/' 的 model_id 歸類為 "unknown"，確保 UI 仍能分組顯示。
    """
    if not model_id or not isinstance(model_id, str):
        return "unknown"
    if "/" in model_id:
        return model_id.split("/", 1)[0]
    return "unknown"


def group_models_by_publisher(model_ids):
    """將 model_id 清單依 publisher 分組，回傳 {publisher: [model_id, ...]}。

    保持各 publisher 內 model_id 的原始順序。model_id 直接作為顯示名稱，
    不再做重新命名，避免 UI 過度複雜。
    """
    grouped = {}
    for mid in model_ids or []:
        publisher = get_publisher_from_model_id(mid)
        grouped.setdefault(publisher, []).append(mid)
    return grouped


def discover_nim_models(api_key=None, timeout=8):
    """向 NIM 端點 /v1/models 查詢可用模型清單。

    成功時回傳 (True, [model_id, ...])；失敗時回傳 (False, error_message)。
    採短逾時設計，避免阻塞 UI 開窗流程。
    """
    try:
        import requests

        headers = {"Accept": "application/json"}
        normalized = normalize_api_key(api_key) or get_nvidia_api_key()
        if normalized:
            headers["Authorization"] = f"Bearer {normalized}"

        response = requests.get(
            f"{NIM_BASE_URL}/v1/models",
            headers=headers,
            timeout=timeout,
        )
        if response.status_code != 200:
            return (False, f"HTTP {response.status_code}")

        data = response.json()
        # OpenAI 相容格式：{"data": [{"id": "..."}, ...]}
        items = data.get("data", []) if isinstance(data, dict) else []
        model_ids = []
        for item in items:
            if isinstance(item, dict) and item.get("id"):
                model_ids.append(item["id"])
            elif isinstance(item, str):
                model_ids.append(item)

        if not model_ids:
            return (False, "empty model list")
        return (True, model_ids)
    except Exception as e:
        return (False, str(e))


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

    @staticmethod
    def get_model_display_name(model_id):
        # 動態探索模式下直接回傳原始 model_id，不再做重新命名
        return model_id

    def discover_available_models(self):
        """動態探索 NIM 可用模型，失敗時降級至內建清單。

        回傳 (model_ids, used_fallback, error_message)：
          - model_ids：最終使用的 model_id 清單
          - used_fallback：是否使用了內建 fallback
          - error_message：探索失敗時的錯誤訊息（成功時為 None）
        """
        ok, result = discover_nim_models(self.api_key, timeout=8)
        if ok:
            return (result, False, None)
        # 降級至內建清單
        return (NVIDIA_MODELS, True, result)

    def validate_config(self):
        if not self.api_key:
            return (False, self.tr("error.nvidia_api_key_missing_env"))
        if not self.api_key.startswith("nvapi-"):
            return (False, self.tr("error.nvidia_api_key_invalid"))
        return (True, None)

    def set_model(self, model_name):
        self.model_name = model_name
        if self.status_callback:
            self.status_callback(self.tr("status.llm_provider_switched", provider="NVIDIA", model=self.get_model_display_name(model_name)))

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
            if getattr(self, "error_callback", None):
                try:
                    self.error_callback(e, traceback.format_exc())
                except Exception as callback_error:
                    print(f"NVIDIA error callback failed: {callback_error}")
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
        best_moves = data.get("post_mistake_opponent_best_moves") or []
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
