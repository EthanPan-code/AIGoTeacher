class ConfigService:
    """Small wrapper around persisted UI settings."""

    def __init__(self, settings_backend):
        self._backend = settings_backend

    def get_setting(self, key, default=None):
        return self._backend.settings.get(key, default)

    def set_setting(self, key, value):
        self._backend.settings[key] = value

    def save(self):
        self._backend.save_settings()

    # ========== LLM 設定便利方法 ==========
    
    def get_llm_tone(self, default="friendly"):
        """取得 LLM 回應語氣 (friendly, strict, concise, detailed, socratic, motivational)"""
        return self.get_setting("llm_tone", default)
    
    def set_llm_tone(self, tone: str):
        """設定 LLM 回應語氣"""
        self.set_setting("llm_tone", tone)
    
    def get_custom_prompts(self, default=None):
        """
        取得自訂提示詞設定
        
        Returns:
            格式: {"user": "...", "system": "..."}
            若未設定則返回 default (通常為 None)
        """
        if default is None:
            default = {}
        return self.get_setting("llm_custom_prompts", default)
    
    def set_custom_prompts(self, system_prompt: str = None, user_prompt: str = None):
        """
        設定自訂提示詞
        
        Args:
            system_prompt: 系統提示詞，None 則不更新此項
            user_prompt: 用戶提示詞，None 則不更新此項
        """
        current = self.get_custom_prompts()
        if system_prompt is not None:
            current["system"] = system_prompt
        if user_prompt is not None:
            current["user"] = user_prompt
        self.set_setting("llm_custom_prompts", current)
    
    def clear_custom_prompts(self):
        """清除自訂提示詞設定（回到預設）"""
        self.set_setting("llm_custom_prompts", {})
