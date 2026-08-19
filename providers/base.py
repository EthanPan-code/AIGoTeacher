class LLMProvider:
    """Base class for streaming LLM commentary providers."""

    def __init__(
        self,
        ui_callback,
        status_callback=None,
        translator=None,
        language_getter=None,
        on_complete_callback=None,
        error_callback=None,
        tone="friendly",
        custom_prompt=None,
    ):
        self.ui_callback = ui_callback
        self.status_callback = status_callback
        self.translator = translator or (lambda key, **kwargs: key)
        self.language_getter = language_getter or (lambda: "zh_TW")
        self.is_generating = False
        self.on_complete_callback = on_complete_callback
        self.error_callback = error_callback
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

        return tone_templates.get_tone_prompt(self.tone, language=self.language_getter())

    def build_commentary_prompt(self, data: dict) -> str:
        """Build the final prompt sent to the model from plain user text plus data."""
        if data.get("full_prompt"):
            return data["full_prompt"]

        user_prompt = data.get("user_prompt")
        system_prompt = data.get("system_prompt")
        context = data.get("game_context", "")
        semantic_rules = (
            "FACTUAL DATA RULES: Keep mistake_move and mistake_player as the move/player that made the mistake. "
            "pre_move_best_moves are alternatives available to the mistake player BEFORE that move. "
            "post_mistake_opponent_best_moves are responses available to the opponent AFTER the mistake. "
            "Never describe the latter as the mistake player's alternative. If a field is unavailable, say so; "
            "do not substitute another player's recommendation or invent a move, reading, life-and-death result, joseki, or variation."
        )
        if user_prompt or system_prompt:
            return "\n\n".join(part.strip() for part in (system_prompt, semantic_rules, user_prompt, context) if part and part.strip())

        base_prompt = self.get_prompt_template().strip()
        turn = data.get("turn", "?")
        user_move = data.get("user_move", "?")
        winrate_drop = data.get("winrate_drop", 0) * 100
        player = data.get("player", "")  # "Black" or "White"
        pre_moves = data.get("pre_move_best_moves") or []
        post_moves = data.get("post_mistake_opponent_best_moves") or []
        best_move = self.tr("teacher.best_unknown")
        pre_text = ", ".join(item.get("move", str(item)) if isinstance(item, dict) else str(item) for item in pre_moves) or "unavailable"
        post_text = ", ".join(item.get("move", str(item)) if isinstance(item, dict) else str(item) for item in post_moves) or "unavailable"

        # Get localized player name (stone.black or stone.white)
        player_name = ""
        if player:
            if player == "Black":
                player_name = self.tr("stone.black")
            elif player == "White":
                player_name = self.tr("stone.white")

        if self.language_getter() == "en":
            info_block = (
                "=== Position Information ===\n"
                f"Move: {turn}\n"
                f"Mistake move: {user_move}\n"
                f"Winrate drop: {winrate_drop:.1f}%\n"
            )
            if player_name:
                info_block += f"Mistake by: {player_name}\n"
            info_block += (
                f"Mistake player's alternatives before the move: {pre_text}\n"
                f"Opponent's best responses after the mistake: {post_text}\n"
                "Explain the problem created by the mistake first, then the opponent's opportunity.\n"
                "Please give teaching feedback based on the information above."
            )
        else:
            info_block = (
                "=== 局面資訊 ===\n"
                f"第 {turn} 手\n"
                f"失誤手：{user_move}\n"
                f"勝率下降：{winrate_drop:.1f}%\n"
            )
            if player_name:
                info_block += f"失誤方：{player_name}\n"
            info_block += (
                f"失誤方落子前可考慮：{pre_text}\n"
                f"失誤後對手最佳應手：{post_text}\n"
                "先解釋失誤留下的問題，再解釋對手應手的價值；兩者不可混稱。\n"
                "請根據以上資訊給出教學解說。"
            )
        context = data.get("game_context", "")
        return "\n\n".join(part for part in (base_prompt, semantic_rules, info_block, context) if part)

    def set_model(self, model_name):
        raise NotImplementedError("Subclass must implement set_model()")

    @staticmethod
    def get_model_display_name(model_id):
        """Return a human-readable display name for the given model ID.

        Subclasses should override this with a provider-specific lookup table.
        The default implementation returns the raw ID so that unknown /
        user-installed models still display gracefully.
        """
        return model_id

    def start_commentary(self, critical_data):
        raise NotImplementedError("Subclass must implement start_commentary()")

    def get_available_models(self):
        raise NotImplementedError("Subclass must implement get_available_models()")

    def validate_config(self):
        """Return (is_valid, error_message)."""
        raise NotImplementedError("Subclass must implement validate_config()")

    def chat_stream(self, prompt: str, conversation: list = None):
        """Send a raw prompt to the LLM for a plain chat conversation.

        This is used by the LLM Chat Sandbox to test provider connectivity
        without any Go-specific prompt engineering.

        Args:
            prompt: The raw user message to send.
            conversation: Optional list of prior messages in format
                [{"role": "user"/"assistant", "content": "..."}].

        The default implementation wraps the prompt in a minimal data dict
        and calls start_commentary, relying on build_commentary_prompt's
        full_prompt bypass. Subclasses may override for provider-specific
        chat implementations.
        """
        data = {
            "full_prompt": prompt,
            "thinking_text": self.tr("chat.thinking", default="Assistant is thinking..."),
            "conversation": conversation,
        }
        self.start_commentary(data)
