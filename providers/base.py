class LLMProvider:
    """Base class for streaming LLM commentary providers."""

    def __init__(
        self,
        ui_callback,
        status_callback=None,
        translator=None,
        language_getter=None,
        on_complete_callback=None,
        tone="friendly",
        custom_prompt=None,
    ):
        self.ui_callback = ui_callback
        self.status_callback = status_callback
        self.translator = translator or (lambda key, **kwargs: key)
        self.language_getter = language_getter or (lambda: "zh_TW")
        self.is_generating = False
        self.on_complete_callback = on_complete_callback
        self.tone = tone
        self.custom_prompt = custom_prompt or ""

    def tr(self, key, **kwargs):
        return self.translator(key, **kwargs)

    def set_tone(self, tone: str):
        self.tone = tone

    def get_tone(self) -> str:
        return self.tone

    def set_custom_prompt(self, prompt: str):
        self.custom_prompt = prompt or ""

    def get_custom_prompt(self) -> str:
        return self.custom_prompt

    def clear_custom_prompts(self):
        self.custom_prompt = ""

    def get_prompt_template(self):
        if self.custom_prompt:
            return self.custom_prompt

        from . import tone_templates

        return tone_templates.get_tone_prompt(self.tone)

    def build_commentary_prompt(self, data: dict) -> str:
        """Build the final prompt sent to the model from plain user text plus data."""
        if data.get("full_prompt"):
            return data["full_prompt"]

        user_prompt = data.get("user_prompt")
        system_prompt = data.get("system_prompt")
        if user_prompt or system_prompt:
            return "\n\n".join(part.strip() for part in (system_prompt, user_prompt) if part and part.strip())

        base_prompt = self.get_prompt_template().strip()
        turn = data.get("turn", "?")
        user_move = data.get("user_move", "?")
        winrate_drop = data.get("winrate_drop", 0) * 100
        best_moves = data.get("current_best_moves") or []
        best_move = self.tr("teacher.best_unknown")
        if best_moves:
            best_move = best_moves[0].get("move", best_move)

        if self.language_getter() == "en":
            info_block = (
                "=== Position Information ===\n"
                f"Move: {turn}\n"
                f"Student move: {user_move}\n"
                f"Winrate drop: {winrate_drop:.1f}%\n"
                f"KataGo recommendation: {best_move}\n"
                "Please give teaching feedback based on the information above."
            )
        else:
            info_block = (
                "=== 局面資訊 ===\n"
                f"第 {turn} 手\n"
                f"學生下在：{user_move}\n"
                f"勝率下降：{winrate_drop:.1f}%\n"
                f"KataGo 推薦：{best_move}\n"
                "請根據以上資訊給出教學解說。"
            )

        return f"{base_prompt}\n\n{info_block}" if base_prompt else info_block

    def set_model(self, model_name):
        raise NotImplementedError("Subclass must implement set_model()")

    def start_commentary(self, critical_data):
        raise NotImplementedError("Subclass must implement start_commentary()")

    def get_available_models(self):
        raise NotImplementedError("Subclass must implement get_available_models()")

    def validate_config(self):
        """Return (is_valid, error_message)."""
        raise NotImplementedError("Subclass must implement validate_config()")
