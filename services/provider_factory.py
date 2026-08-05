from providers.nvidia_provider import (
    NVIDIA_MODELS,
    NVIDIA_MODEL_DISPLAY_NAMES,
    NvidiaProvider,
    discover_nim_models,
    group_models_by_publisher,
)
from providers.openrouter_provider import (
    OPENROUTER_MODELS,
    OpenRouterProvider,
    discover_openrouter_models,
    group_models_by_publisher as group_openrouter_models_by_publisher,
)
from providers.ollama_provider import OLLAMA_MODELS, OLLAMA_MODEL_DISPLAY_NAMES, OllamaProvider
from services.ollama_manager import DEFAULT_OLLAMA_MODEL


class ProviderFactory:
    _providers = {
        "ollama": {
            "class": OllamaProvider,
            "display_name": "Ollama",
            "setting_key": "ollama_model",
            "default_model": DEFAULT_OLLAMA_MODEL,
            "models": OLLAMA_MODELS,
            "model_display_names": OLLAMA_MODEL_DISPLAY_NAMES,
        },
        "nvidia": {
            "class": NvidiaProvider,
            "display_name": "NVIDIA NIM",
            "setting_key": "nvidia_model",
            "default_model": NVIDIA_MODELS[0],
            "models": NVIDIA_MODELS,
            "model_display_names": NVIDIA_MODEL_DISPLAY_NAMES,
        },
        "openrouter": {
            "class": OpenRouterProvider,
            "display_name": "OpenRouter",
            "setting_key": "openrouter_model",
            "default_model": OPENROUTER_MODELS[0],
            "models": OPENROUTER_MODELS,
            "model_display_names": {},
        },
    }

    @classmethod
    def create_provider(
        cls,
        provider_name,
        ui_callback,
        status_callback=None,
        model_name=None,
        translator=None,
        language_getter=None,
        **kwargs,
    ):
        provider_info = cls._providers.get(provider_name)
        if provider_info is None:
            provider_name = "ollama"
            provider_info = cls._providers[provider_name]

        return provider_info["class"](
            ui_callback=ui_callback,
            status_callback=status_callback,
            model_name=model_name or provider_info["default_model"],
            translator=translator,
            language_getter=language_getter,
            **kwargs,
        )

    @classmethod
    def create_from_config(cls, config_service, ui_callback, status_callback=None, translator=None, language_getter=None, **kwargs):
        provider_name = config_service.get_setting("llm_provider", "ollama")
        model_name = cls.get_configured_model(config_service, provider_name)
        kwargs.setdefault("tone", config_service.get_llm_tone("friendly"))
        kwargs.setdefault("custom_prompt", config_service.get_custom_prompt(""))
        return cls.create_provider(
            provider_name,
            ui_callback=ui_callback,
            status_callback=status_callback,
            model_name=model_name,
            translator=translator,
            language_getter=language_getter,
            **kwargs,
        )

    @classmethod
    def get_available_providers(cls):
        return tuple(cls._providers.keys())

    @classmethod
    def get_display_name(cls, provider_name):
        return cls._providers.get(provider_name, cls._providers["ollama"])["display_name"]

    @classmethod
    def get_model_setting_key(cls, provider_name):
        return cls._providers.get(provider_name, cls._providers["ollama"])["setting_key"]

    @classmethod
    def get_default_model(cls, provider_name):
        return cls._providers.get(provider_name, cls._providers["ollama"])["default_model"]

    @classmethod
    def get_configured_model(cls, config_service, provider_name):
        return config_service.get_setting(
            cls.get_model_setting_key(provider_name),
            cls.get_default_model(provider_name),
        )

    @classmethod
    def get_available_models(cls, provider_name):
        if provider_name == "ollama":
            return cls._providers["ollama"]["class"](
                ui_callback=lambda _message: None
            ).get_available_models()
        provider = cls._providers.get(provider_name, cls._providers["ollama"])
        return provider["models"]

    @classmethod
    def get_model_display_name(cls, provider_name, model_id):
        """Return the human-readable display name for a model ID.

        Falls back to the raw model_id when the provider or model is unknown,
        so user-installed Ollama models still display gracefully.
        """
        provider = cls._providers.get(provider_name, cls._providers["ollama"])
        display_names = provider.get("model_display_names", {})
        return display_names.get(model_id, model_id)

    @classmethod
    def get_model_id_by_display_name(cls, provider_name, display_name):
        """Reverse lookup: display name → model ID.

        Returns None when the display name is not found. Useful for Combobox
        widgets that show display names but need to persist the underlying ID.
        """
        provider = cls._providers.get(provider_name, cls._providers["ollama"])
        models = cls.get_available_models(provider_name) if provider_name == "ollama" else provider["models"]
        display_names = provider.get("model_display_names", {})
        for model_id, name in display_names.items():
            if name == display_name:
                return model_id
        # Fallback: maybe the value passed in is already a raw ID
        if display_name in models:
            return display_name
        return None

    @classmethod
    def get_available_models_with_names(cls, provider_name):
        """Return [(display_name, model_id), ...] for UI widgets.

        The list follows the same order as get_available_models(). Comboboxes
        can show the display_name while keeping the model_id for persistence.
        """
        provider = cls._providers.get(provider_name, cls._providers["ollama"])
        models = cls.get_available_models(provider_name) if provider_name == "ollama" else provider["models"]
        display_names = provider.get("model_display_names", {})
        return [(display_names.get(mid, mid), mid) for mid in models]

    # ===== NIM 動態模型探索專用 helper =====
    # 僅供 NVIDIA NIM 使用，其他 provider 不受影響。
    # 動態模式下 model_id 直接作為顯示名稱，不再做重新命名。

    @classmethod
    def discover_nim_models(cls, api_key=None):
        """向 NIM 端點探索可用模型，失敗時降級至內建清單。

        回傳 (model_ids, used_fallback, error_message)：
          - model_ids：最終使用的 model_id 清單
          - used_fallback：是否使用了內建 fallback
          - error_message：探索失敗時的錯誤訊息（成功時為 None）
        """
        ok, result = discover_nim_models(api_key, timeout=8)
        if ok:
            return (result, False, None)
        return (NVIDIA_MODELS, True, result)

    @classmethod
    def get_nim_publishers(cls, model_ids):
        """從 model_id 清單取出 publisher 清單（已排序、去重）。"""
        grouped = group_models_by_publisher(model_ids)
        return sorted(grouped.keys())

    @classmethod
    def get_nim_models_by_publisher(cls, model_ids, publisher):
        """取得指定 publisher 下的 model_id 清單（保持原始順序）。"""
        grouped = group_models_by_publisher(model_ids)
        return grouped.get(publisher, [])

    @classmethod
    def get_nim_publisher_for_model(cls, model_id):
        """從 model_id 拆出 publisher（供 UI 還原選擇用）。"""
        from providers.nvidia_provider import get_publisher_from_model_id
        return get_publisher_from_model_id(model_id)

    @classmethod
    def discover_openrouter_models(cls, api_key=None):
        ok, result = discover_openrouter_models(api_key, timeout=8)
        if ok:
            return (result, False, None)
        return (OPENROUTER_MODELS, True, result)

    @classmethod
    def get_openrouter_publishers(cls, model_ids):
        return sorted(group_openrouter_models_by_publisher(model_ids).keys())

    @classmethod
    def get_openrouter_models_by_publisher(cls, model_ids, publisher):
        return group_openrouter_models_by_publisher(model_ids).get(publisher, [])

    @classmethod
    def get_openrouter_publisher_for_model(cls, model_id):
        if not model_id or "/" not in model_id:
            return "unknown"
        return model_id.split("/", 1)[0]
