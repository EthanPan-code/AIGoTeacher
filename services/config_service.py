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

    def get_ui_theme(self, default="system"):
        from services.theme_service import normalize_theme
        return normalize_theme(self.get_setting("ui_theme", default))

    def set_ui_theme(self, theme):
        from services.theme_service import normalize_theme
        self.set_setting("ui_theme", normalize_theme(theme))

    def get_analysis_rules(self, default="japanese"):
        from services.rules import normalize_rule_id
        return normalize_rule_id(self.get_setting("analysis_rules", default))

    def set_analysis_rules(self, rules):
        from services.rules import normalize_rule_id
        self.set_setting("analysis_rules", normalize_rule_id(rules))

    def get_analysis_komi(self, default=None):
        from services.rules import DEFAULT_KOMI, validate_komi
        value = self.get_setting("analysis_komi", DEFAULT_KOMI if default is None else default)
        try:
            return validate_komi(value)
        except ValueError:
            return DEFAULT_KOMI if default is None else validate_komi(default)

    def set_analysis_komi(self, komi):
        from services.rules import validate_komi
        self.set_setting("analysis_komi", validate_komi(komi))

    def get_show_teacher(self, default=True):
        return bool(self.get_setting("show_teacher", default))

    def set_show_teacher(self, show):
        self.set_setting("show_teacher", bool(show))

    def migrate_removed_github_provider(self, ollama_default_model):
        """Migrate settings from the removed GitHub Models provider."""
        provider = self.get_setting("llm_provider", "ollama")
        has_legacy_settings = provider == "github" or "github_model" in self._backend.settings
        if not has_legacy_settings:
            return False

        if provider == "github":
            self.set_setting("llm_provider", "ollama")
            if not self.get_setting("ollama_model"):
                self.set_setting("ollama_model", ollama_default_model)

        self._backend.settings.pop("github_model", None)
        self.save()
        return True

    def get_llm_tone(self, default="friendly"):
        return self.get_setting("llm_tone", default)

    def set_llm_tone(self, tone: str):
        self.set_setting("llm_tone", tone)

    def get_custom_prompt(self, default=""):
        return self.get_setting("llm_custom_prompt", default)

    def set_custom_prompt(self, prompt: str):
        self.set_setting("llm_custom_prompt", prompt or "")

    def clear_custom_prompts(self):
        self.set_setting("llm_custom_prompt", "")

    # === Board Image Settings ===

    def get_board_background(self, default=""):
        return self.get_setting("board_background", default)

    def set_board_background(self, path):
        self.set_setting("board_background", path)

    def get_board_frame_background(self, default=""):
        return self.get_setting("board_frame_background", default)

    def set_board_frame_background(self, path):
        self.set_setting("board_frame_background", path)

    def get_black_stone_image(self, default=""):
        return self.get_setting("black_stone_image", default)

    def set_black_stone_image(self, path):
        self.set_setting("black_stone_image", path)

    def get_white_stone_image(self, default=""):
        return self.get_setting("white_stone_image", default)

    def set_white_stone_image(self, path):
        self.set_setting("white_stone_image", path)
