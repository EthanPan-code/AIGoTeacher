class LLMProvider:
    """Base class for streaming LLM commentary providers."""

    def __init__(self, ui_callback, status_callback=None, translator=None, language_getter=None, on_complete_callback=None, tone="friendly", custom_prompts=None):
        self.ui_callback = ui_callback
        self.status_callback = status_callback
        self.translator = translator or (lambda key, **kwargs: key)
        self.language_getter = language_getter or (lambda: "zh_TW")
        self.is_generating = False
        self.on_complete_callback = on_complete_callback  # 【Phase 1】生成完成時的回呼
        
        # 【Phase 2】LLM 語氣和自訂提示詞支援
        self.tone = tone  # 語氣類型 (friendly, strict, concise 等)
        self.custom_prompts = custom_prompts or {}  # 自訂提示詞: {"system": "...", "user": "..."}

    def tr(self, key, **kwargs):
        return self.translator(key, **kwargs)

    def set_tone(self, tone: str):
        """設定回應語氣"""
        self.tone = tone
    
    def get_tone(self) -> str:
        """取得目前語氣"""
        return self.tone
    
    def set_custom_prompts(self, system_prompt: str = None, user_prompt: str = None):
        """
        設定自訂提示詞
        
        Args:
            system_prompt: 系統提示詞，None 則不更新
            user_prompt: 用戶提示詞，None 則不更新
        """
        if system_prompt is not None:
            self.custom_prompts["system"] = system_prompt
        if user_prompt is not None:
            self.custom_prompts["user"] = user_prompt
    
    def get_custom_prompts(self) -> dict:
        """取得自訂提示詞"""
        return self.custom_prompts
    
    def clear_custom_prompts(self):
        """清除自訂提示詞"""
        self.custom_prompts = {}
    
    def get_prompt_template(self, prompt_type: str = "user"):
        """
        取得當前應使用的提示詞模板
        
        優先順序:
        1. 自訂提示詞 (若已設定)
        2. 語氣特定提示詞 (依 tone 從 tone_templates 取得)
        3. 預設提示詞 (從 i18n 系統取得)
        
        Args:
            prompt_type: "user" 或 "system"
        
        Returns:
            提示詞模板字符串
        """
        # 先檢查自訂提示詞
        if self.custom_prompts.get(prompt_type):
            return self.custom_prompts[prompt_type]
        
        # 否則從 tone_templates 中取得
        from . import tone_templates
        if prompt_type == "system":
            return tone_templates.get_tone_system_prompt(self.tone)
        else:  # user
            return tone_templates.get_tone_user_prompt_template(self.tone)

    def set_model(self, model_name):
        raise NotImplementedError("Subclass must implement set_model()")

    def start_commentary(self, critical_data):
        raise NotImplementedError("Subclass must implement start_commentary()")

    def get_available_models(self):
        raise NotImplementedError("Subclass must implement get_available_models()")

    def validate_config(self):
        """Return (is_valid, error_message)."""
        raise NotImplementedError("Subclass must implement validate_config()")
