"""
LLM 提示詞模板系統 - 支援多種教學語氣
定義了 6 種預設語氣的系統提示詞和用戶提示詞模板
"""

# 語氣 ID 與顯示名稱對應
TONE_DISPLAY_NAMES = {
    "strict": "嚴格/專業",
    "friendly": "友善/鼓勵",
    "concise": "簡潔/直接",
    "detailed": "詳細/深入",
    "socratic": "蘇格拉底法",
    "motivational": "激勵/心理",
}

# 語氣描述
TONE_DESCRIPTIONS = {
    "strict": "直指問題，邏輯嚴謹，適合高級棋手",
    "friendly": "溫暖鼓勵，簡單易懂，適合初學者",
    "concise": "要點明確，字數少，適合快速回顧",
    "detailed": "完整分析，邏輯完整，適合深度學習",
    "socratic": "提出問題，引導思考，適合自主學習",
    "motivational": "強調潛力，建立信心，適合兒童教學",
}

# 提示詞模板 - 包含系統提示詞和用戶提示詞
TONE_PROMPTS = {
    "strict": {
        "system": "你是一位嚴謹的職業圍棋教練。用精確的棋理術語和邏輯清晰地分析問題。不需要寒暄，直指核心要點。",
        "user": "第 {turn} 手，學生下在 {user_move}，導致勝率下降 {winrate_drop:.1f}%。AI 最佳手為 {best_move}。請簡明扼要指出這步棋的主要問題所在，以及 {best_move} 為何更優。控制在 60 字以內。",
    },
    "friendly": {
        "system": "你是一位親切、鼓勵學生的圍棋老師。用簡單清晰的語言解釋棋理，強調學習過程而非完美棋手。",
        "user": "第 {turn} 手時，學生選擇下在 {user_move}，結果勝率掉了 {winrate_drop:.1f}%。AI 建議的最佳著法是 {best_move}。請溫和地解釋為什麼 {best_move} 更好，以及 {user_move} 可以如何改進。字數 80 以內，語氣友善鼓勵。",
    },
    "concise": {
        "system": "你是圍棋分析師。用極簡的風格給出分析——直接說重點，不要廢話。",
        "user": "第 {turn} 手：{user_move} 不如 {best_move}（勝率差 {winrate_drop:.1f}%）。原因？最多 40 字。",
    },
    "detailed": {
        "system": "你是深度圍棋教練。用完整的分析框架回答，包括局面背景、問題診斷、解決方案、學習建議。",
        "user": "第 {turn} 手分析：學生下在 {user_move}（勝率下降 {winrate_drop:.1f}%），AI 推薦 {best_move}。請從以下角度詳細說明：(1) {user_move} 的具體問題；(2) {best_move} 為何更優；(3) 這步棋體現的大局觀差異；(4) 如何避免類似失誤。字數 150-200 字。",
    },
    "socratic": {
        "system": "你是蘇格拉底式教練。通過提問引導學生思考，少給直接答案，多啟發思維。",
        "user": "第 {turn} 手，學生下了 {user_move}，但勝率掉了 {winrate_drop:.1f}%。AI 提出 {best_move} 更優。不要直接告訴答案，而是用 2-3 個引導式問題，幫助學生自己發現 {best_move} 的優勢與 {user_move} 的不足。字數 60 以內。",
    },
    "motivational": {
        "system": "你是兒童棋類教練。在指正錯誤時，強調學習機會、建立信心、鼓勵成長。",
        "user": "第 {turn} 手，小棋手下在 {user_move}，結果勝率下降 {winrate_drop:.1f}%。AI 建議 {best_move}。請用鼓勵和正向的語調，讚美學習的進步，指出 {user_move} 的學習點，解釋 {best_move} 的精妙之處。字數 70-90。",
    },
}

# 預設提示詞集合 - 支援多預設，方便擴展
PRESET_PROMPTS = {
    "default": TONE_PROMPTS["friendly"],  # 預設使用友善風格
    "expert": TONE_PROMPTS["detailed"],
    "quick": TONE_PROMPTS["concise"],
}


def get_tone_system_prompt(tone: str, translator=None) -> str:
    """
    取得指定語氣的系統提示詞
    
    Args:
        tone: 語氣類型 (如 'friendly', 'strict')
        translator: 翻譯函數（用於 fallback，目前暫未使用）
    
    Returns:
        系統提示詞字符串
    """
    if tone not in TONE_PROMPTS:
        return TONE_PROMPTS["friendly"]["system"]
    return TONE_PROMPTS[tone]["system"]


def get_tone_user_prompt_template(tone: str, translator=None) -> str:
    """
    取得指定語氣的用戶提示詞模板
    
    Args:
        tone: 語氣類型
        translator: 翻譯函數（備用）
    
    Returns:
        用戶提示詞模板字符串，包含佔位符
    """
    if tone not in TONE_PROMPTS:
        return TONE_PROMPTS["friendly"]["user"]
    return TONE_PROMPTS[tone]["user"]


def validate_user_prompt_template(prompt: str) -> tuple[bool, list[str]]:
    """
    驗證用戶提示詞模板是否包含必要的佔位符
    
    Args:
        prompt: 要驗證的提示詞模板
    
    Returns:
        (is_valid, missing_placeholders)
        - is_valid: True 表示有效，False 表示缺少必要佔位符
        - missing_placeholders: 缺少的佔位符列表
    """
    required_placeholders = {"turn", "user_move", "best_move", "winrate_drop"}
    missing = []
    
    for placeholder in required_placeholders:
        # 支援帶格式的佔位符，例如 {winrate_drop:.1f}
        pattern = "{" + placeholder
        if pattern not in prompt:
            missing.append(placeholder)
    
    return len(missing) == 0, missing


def format_prompt(template: str, critical_data: dict) -> str:
    """
    使用 critical_data 中的值替換提示詞模板中的佔位符
    
    Args:
        template: 提示詞模板字符串
        critical_data: 包含 turn, user_move, best_move, winrate_drop 等的字典
    
    Returns:
        格式化後的提示詞字符串
    
    Raises:
        KeyError: 如果缺少必要的數據
        ValueError: 如果佔位符無法替換
    """
    try:
        # 準備替換數據
        best_move = critical_data.get("current_best_moves", [{}])[0].get("move", "?")
        if isinstance(best_move, dict):
            best_move = best_move.get("move", "?")
        
        format_data = {
            "turn": critical_data.get("turn", "?"),
            "user_move": critical_data.get("user_move", "?"),
            "best_move": best_move,
            "winrate_drop": critical_data.get("winrate_drop", 0) * 100,  # 轉換為百分比
        }
        
        return template.format(**format_data)
    except KeyError as e:
        raise KeyError(f"缺少必要的數據欄位: {e}")
    except Exception as e:
        raise ValueError(f"提示詞格式化失敗: {e}")


def get_all_tones() -> dict:
    """
    取得所有可用語氣的資訊
    
    Returns:
        字典，格式: {tone_id: {"name": str, "description": str, ...}}
    """
    result = {}
    for tone_id in TONE_DISPLAY_NAMES:
        result[tone_id] = {
            "id": tone_id,
            "name": TONE_DISPLAY_NAMES[tone_id],
            "description": TONE_DESCRIPTIONS.get(tone_id, ""),
        }
    return result
