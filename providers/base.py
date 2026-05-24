class LLMProvider:
    """Base class for streaming LLM commentary providers."""

    def __init__(self, ui_callback, status_callback=None, translator=None, language_getter=None, on_complete_callback=None):
        self.ui_callback = ui_callback
        self.status_callback = status_callback
        self.translator = translator or (lambda key, **kwargs: key)
        self.language_getter = language_getter or (lambda: "zh_TW")
        self.is_generating = False
        self.on_complete_callback = on_complete_callback  # 【Phase 1】生成完成時的回呼

    def tr(self, key, **kwargs):
        return self.translator(key, **kwargs)

    def set_model(self, model_name):
        raise NotImplementedError("Subclass must implement set_model()")

    def start_commentary(self, critical_data):
        raise NotImplementedError("Subclass must implement start_commentary()")

    def get_available_models(self):
        raise NotImplementedError("Subclass must implement get_available_models()")

    def validate_config(self):
        """Return (is_valid, error_message)."""
        raise NotImplementedError("Subclass must implement validate_config()")
