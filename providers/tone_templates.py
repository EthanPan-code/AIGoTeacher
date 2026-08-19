"""
Single-block LLM prompt templates for AI Go teacher commentary.

The application appends move number, student move, winrate drop, and KataGo's
recommendation in code. These templates should stay plain text and should not
require user-editable placeholders.

Display names and descriptions are looked up via the i18n `t()` function so the
UI shows English names when the user's language is set to English, etc. The
raw Chinese keys are kept only as a fallback when no translator is available
(e.g. headless / early-init contexts).
"""

# 硬編碼的中文 fallback。正式 UI 顯示請用 get_tone_display_name() / get_tone_description()。
_TONE_DISPLAY_NAMES_FALLBACK = {
    "strict": "嚴格/專業",
    "friendly": "友善/鼓勵",
    "concise": "簡潔/直接",
    "detailed": "詳細/深入",
    "socratic": "蘇格拉底式",
    "motivational": "激勵/心理",
}

_TONE_DESCRIPTIONS_FALLBACK = {
    "strict": "直接指出問題，適合進階棋友。",
    "friendly": "溫和鼓勵，適合初學者。",
    "concise": "短而清楚，適合快速複盤。",
    "detailed": "完整說明原因與方向，適合深入學習。",
    "socratic": "用問題引導學生自己思考。",
    "motivational": "重視信心與下一步練習方向。",
}

# 向後相容：舊代碼若仍直接 import TONE_DISPLAY_NAMES / TONE_DESCRIPTIONS 仍可運作
# （init 階段沒有 i18n translator 時退到中文 fallback）。正式 UI 請用函式版本。
TONE_DISPLAY_NAMES = _TONE_DISPLAY_NAMES_FALLBACK
TONE_DESCRIPTIONS = _TONE_DESCRIPTIONS_FALLBACK

TONE_PROMPTS = {
    "strict": (
        "你是一位嚴謹的圍棋老師。先指出失誤留下的問題與對手取得的機會，再說明失誤後對手的最佳應手。只有提供落子前替代手時，才比較失誤方原本可考慮的手；不可混稱。控制在 60 字以內。"
    ),
    "friendly": (
        "你是一位友善的圍棋老師。請根據系統提供的局面資訊，用繁體中文給學生一段容易理解的建議。"
        "先肯定思路，再說明這手棋留下的問題與對手應手的價值；若有資料，再補充失誤方落子前可考慮的手。控制在 80 字以內。"
    ),
    "concise": (
        "你是一位簡潔的圍棋講解員。請根據系統提供的局面資訊，用最少文字點出問題、推薦方向、"
        "以及對手應手與下一手應注意的重點；不要混淆兩類推薦手。控制在 40 字以內。"
    ),
    "detailed": (
        "你是一位擅長拆解棋理的圍棋老師。請根據系統提供的局面資訊，說明學生手、KataGo 推薦手、"
        "勝率變化代表的風險，以及一個可練習的觀念。避免假裝看到資料中沒有的局部細節。控制在 150 字以內。"
    ),
    "socratic": (
        "你是一位用提問引導學生的圍棋老師。請根據系統提供的局面資訊，用 2 到 3 個短問題帶學生思考，"
        "並在最後補一句提示，讓學生理解對手應手揭示的方向；只有資料存在才談失誤方替代手。控制在 80 字以內。"
    ),
    "motivational": (
        "你是一位鼓勵型圍棋老師。請根據系統提供的局面資訊，先穩住學生信心，再指出這手棋造成的代價，"
        "最後給出一個明確、可執行的改善方向，清楚區分失誤方替代手與對手應手。控制在 90 字以內。"
    ),
}

TONE_PROMPTS_EN = {
    "strict": (
        "You are a rigorous Go teacher. Based on the position information provided by the system, "
        "directly point out the main problem with the student's move and explain why KataGo's recommendation "
        "is better. Keep the tone professional and precise, without excessive reassurance. Keep it under 60 words."
    ),
    "friendly": (
        "You are a friendly Go teacher. Based on the position information provided by the system, give the student "
        "an easy-to-understand suggestion in English. First acknowledge the idea behind the move, then explain its "
        "problem and the benefit of KataGo's recommendation. Keep it under 80 words."
    ),
    "concise": (
        "You are a concise Go commentator. Based on the position information provided by the system, use as few words "
        "as possible to point out the problem, the recommended direction, and what to watch for next. Keep it under 40 words."
    ),
    "detailed": (
        "You are a Go teacher skilled at breaking down Go principles. Based on the position information provided by the system, "
        "explain the student's move, KataGo's recommendation, the risk represented by the win-rate change, and one idea to practice. "
        "Do not pretend to see local details that are not in the data. Keep it under 150 words."
    ),
    "socratic": (
        "You are a Go teacher who guides students with questions. Based on the position information provided by the system, "
        "ask 2 to 3 short questions to help the student think, then add one hint so they understand the direction of KataGo's recommendation. "
        "Keep it under 80 words."
    ),
    "motivational": (
        "You are an encouraging Go teacher. Based on the position information provided by the system, first help the student maintain confidence, "
        "then point out the cost of the move, and finish with one clear, actionable direction for improvement. Keep it under 90 words."
    ),
}

PRESET_PROMPTS = {
    "default": TONE_PROMPTS["friendly"],
    "expert": TONE_PROMPTS["detailed"],
    "quick": TONE_PROMPTS["concise"],
}


def get_tone_prompt(tone: str, translator=None, language=None) -> str:
    """Return the preset prompt in the requested UI language."""
    if language is None and translator is not None:
        # Translators in the UI expose the active language through their owner,
        # but plain translator callables do not. Keep the historical Chinese
        # fallback for those callers.
        language = getattr(getattr(translator, "__self__", None), "language", None)
    prompts = TONE_PROMPTS_EN if language == "en" else TONE_PROMPTS
    return prompts.get(tone, prompts["friendly"])


def find_preset_tone(prompt: str, language=None):
    """Return the tone if prompt is an untouched preset, otherwise ``None``."""
    if not prompt:
        return None
    prompts = TONE_PROMPTS_EN if language == "en" else TONE_PROMPTS
    normalized = prompt.strip()
    return next((tone for tone, preset in prompts.items() if normalized == preset), None)


def _resolve_translator(translator):
    """若呼叫端未提供 translator，嘗試用 ui.i18n 全域 t()。"""
    if translator is not None:
        return translator
    try:
        from ui.i18n import t as _t  # 避免循環引用；只在需要時 import
        return _t
    except Exception:
        return None


def get_tone_display_name(tone: str, translator=None) -> str:
    """取得 tone 對應的本地化名稱。translator 為 None 時退到中文 fallback。"""
    t = _resolve_translator(translator)
    if t is not None:
        try:
            return t(f"tone.{tone}")
        except Exception:
            pass
    return _TONE_DISPLAY_NAMES_FALLBACK.get(tone, tone)


def get_tone_description(tone: str, translator=None) -> str:
    """取得 tone 對應的本地化描述。translator 為 None 時退到中文 fallback。"""
    t = _resolve_translator(translator)
    if t is not None:
        try:
            return t(f"tone.{tone}_desc")
        except Exception:
            pass
    return _TONE_DESCRIPTIONS_FALLBACK.get(tone, "")


def get_all_tones(translator=None) -> dict:
    """回傳所有 tone 的本地化資訊，給 UI 列表/選單用。"""
    return {
        tone_id: {
            "id": tone_id,
            "name": get_tone_display_name(tone_id, translator),
            "description": get_tone_description(tone_id, translator),
        }
        for tone_id in _TONE_DISPLAY_NAMES_FALLBACK
    }
