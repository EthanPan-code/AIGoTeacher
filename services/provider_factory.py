from providers.github_provider import GITHUB_MODELS, GITHUB_MODEL_DISPLAY_NAMES, GithubProvider
from providers.nvidia_provider import NVIDIA_MODELS, NVIDIA_MODEL_DISPLAY_NAMES, NvidiaProvider
from providers.ollama_provider import OLLAMA_MODELS, OLLAMA_MODEL_DISPLAY_NAMES, OllamaProvider


class ProviderFactory:
    _providers = {
        "ollama": {
            "class": OllamaProvider,
            "display_name": "Ollama",
            "setting_key": "ollama_model",
            "default_model": OLLAMA_MODELS[0],
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
        "github": {
            "class": GithubProvider,
            "display_name": "GitHub Models",
            "setting_key": "github_model",
            "default_model": GITHUB_MODELS[0],
            "models": GITHUB_MODELS,
            "model_display_names": GITHUB_MODEL_DISPLAY_NAMES,
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
        display_names = provider.get("model_display_names", {})
        for model_id, name in display_names.items():
            if name == display_name:
                return model_id
        # Fallback: maybe the value passed in is already a raw ID
        if display_name in provider["models"]:
            return display_name
        return None

    @classmethod
    def get_available_models_with_names(cls, provider_name):
        """Return [(display_name, model_id), ...] for UI widgets.

        The list follows the same order as get_available_models(). Comboboxes
        can show the display_name while keeping the model_id for persistence.
        """
        provider = cls._providers.get(provider_name, cls._providers["ollama"])
        models = provider["models"]
        display_names = provider.get("model_display_names", {})
        return [(display_names.get(mid, mid), mid) for mid in models]
