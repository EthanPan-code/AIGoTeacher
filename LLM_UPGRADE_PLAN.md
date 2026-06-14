# LLM 功能升級規劃
## AI 圍棋老師 v0.2.0

### 📋 概述

本升級計畫將增強 LLM 回應的個性化程度，包括：
1. **多種回應語氣選項** - 讓用戶選擇教學風格
2. **自訂提示詞功能** - 讓用戶編寫自己的提示詞模板

---

## 🎯 功能需求

### 1. 回應語氣選項 (Voice/Tone Settings)

#### 目標
- 提供 5-6 種預定義的教學語氣
- 用戶可在運行時切換語氣
- 語氣設定保存到 `ui_settings.json`
- 支援多語言 (繁體中文、英文)

#### 語氣類型定義

| 語氣 | 中文名稱 | 特徵 | 使用場景 |
|------|--------|------|--------|
| `strict` | 嚴格/專業 | 直指問題、邏輯嚴謹、無寒暄 | 高級棋手、棋賽前準備 |
| `friendly` | 友善/鼓勵 | 溫暖、鼓勵、簡單易懂 | 初級棋手、學習過程 |
| `concise` | 簡潔/直接 | 要點明確、字數少 | 快速回顧、移動設備 |
| `detailed` | 詳細/深入 | 完整分析、有理由、有例子 | 深度學習、教學模式 |
| `socratic` | 蘇格拉底法 | 提出問題、引導思考、少給答案 | 自主學習、棋力提升 |
| `motivational` | 激勵/心理 | 強調潛力、正向反饋、建立信心 | 兒童、興趣培養 |

---

### 2. 自訂提示詞 (Custom Prompts)

#### 目標
- UI 對話框允許編輯系統提示詞和用戶提示詞
- 支援提示詞模板與佔位符
- 預置提示詞預設 (presets)
- 驗證提示詞的有效性

#### 必要佔位符

**系統提示詞 (System Prompt)**:
- 無強制佔位符（可自由定義 LLM 角色）

**用戶提示詞 (User Prompt)** 須包含：
- `{turn}` — 手數
- `{user_move}` — 用戶的著法 (如"D4")
- `{best_move}` — AI 推薦著法
- `{winrate_drop}` — 勝率下降百分比
- (選項) `{current_best_moves}` — 前N個候選手列表

---

## 🏗 實現方案

### 階段 1: 後端架構升級 (Phase 1)

#### 1.1 擴展 `ConfigService` (services/config_service.py)

```python
# 新增設定項
"llm_tone": "friendly",  # 預設語氣
"llm_custom_prompts": {  # 自訂提示詞預設
    "default": {
        "system": "你是一位專業圍棋老師...",
        "user": "目前是第 {turn} 手..."
    },
    "user_custom_1": {...}
}
```

#### 1.2 在提供商基類新增語氣支援 (providers/base.py)

```python
class LLMProvider:
    def __init__(self, ..., tone="friendly", custom_prompts=None):
        self.tone = tone
        self.custom_prompts = custom_prompts or {}
    
    def apply_tone(self, content: str) -> str:
        """根據語氣調整輸出內容"""
        # 在 generate_commentary() 輸出後應用
        ...
    
    def get_prompt_template(self, prompt_type="user"):
        """取得當前選定的提示詞模板"""
        ...
```

#### 1.3 更新每個提供商實現

- **ollama_provider.py**: 在 `_generate_task()` 中應用語氣
- **nvidia_provider.py**: 同上
- **github_provider.py**: 同上

**修改模式**:
```python
def start_commentary(self, critical_data):
    # 應用自訂提示詞或語氣特定提示詞
    if self.custom_prompts.get("user"):
        user_prompt = self._format_custom_prompt(
            self.custom_prompts["user"],
            critical_data
        )
    else:
        user_prompt = self._get_tone_specific_prompt(
            self.tone,
            critical_data
        )
    
    # 發送 LLM 查詢...
```

---

### 階段 2: UI 層升級 (Phase 2)

#### 2.1 新增語氣選擇菜單 (ui/main_v3.py)

位置: `菜單 > 分析 > LLM 語氣` 或 `菜單 > 設定 > LLM 設定`

```python
def create_llm_tone_submenu(parent_menu):
    """建立語氣選擇菜單"""
    tone_menu = tk.Menu(parent_menu, tearoff=0)
    for tone_id, tone_name in TONE_NAMES.items():
        tone_menu.add_command(
            label=tone_name,
            command=lambda t=tone_id: set_llm_tone(t)
        )
    parent_menu.add_cascade(label="LLM 語氣", menu=tone_menu)
```

#### 2.2 新增「自訂提示詞」對話框 (ui/main_v3.py)

新建函數: `_create_custom_prompt_dialog()`

功能:
- 兩個文本區域 (系統提示詞 + 用戶提示詞)
- 佔位符提示 & 驗證
- 保存/取消/重設按鈕
- 預設提示詞模板選擇下拉菜單
- 實時預覽

**對話框佈局**:
```
┌─────────────────────────────────┐
│ 自訂提示詞設定                      │
├─────────────────────────────────┤
│ 預設模板: [友善模板 ▼]              │
├─────────────────────────────────┤
│ 系統提示詞 (System Prompt):       │
│ ┌───────────────────────────────┐ │
│ │ 你是一位專業圍棋老師...     │ │
│ └───────────────────────────────┘ │
├─────────────────────────────────┤
│ 用戶提示詞 (User Prompt):        │
│ ┌───────────────────────────────┐ │
│ │ 目前是第 {turn} 手...         │ │
│ │ 必要佔位符:                    │ │
│ │ • {turn}、{user_move}         │ │
│ │ • {best_move}、{winrate_drop} │ │
│ └───────────────────────────────┘ │
├─────────────────────────────────┤
│ [保存] [取消] [重設為預設]         │
└─────────────────────────────────┘
```

#### 2.3 擴展 LLM 設定對話框

菜單路徑: `分析 > LLM 模型 > 設定`

新增標籤頁:
- 「提供商 & 模型」(既有)
- 「語氣選擇」(新增)
- 「自訂提示詞」(新增)

---

### 階段 3: 翻譯 & 設定 (Phase 3)

#### 3.1 擴展 `i18n/zh_TW.json` 和 `i18n/en.json`

**新增鍵值**:

```json
{
  "menu.llm_tone": "LLM 語氣",
  "menu.custom_prompts": "自訂提示詞",
  
  "tone.strict": "嚴格/專業",
  "tone.strict_desc": "直指問題，邏輯嚴謹，適合高級棋手",
  "tone.friendly": "友善/鼓勵",
  "tone.friendly_desc": "溫暖鼓勵，簡單易懂，適合初學者",
  "tone.concise": "簡潔/直接",
  "tone.concise_desc": "要點明確，字數少，適合快速回顧",
  "tone.detailed": "詳細/深入",
  "tone.detailed_desc": "完整分析，邏輯完整，適合深度學習",
  "tone.socratic": "蘇格拉底法",
  "tone.socratic_desc": "提出問題，引導思考，適合自主學習",
  "tone.motivational": "激勵/心理",
  "tone.motivational_desc": "強調潛力，建立信心，適合兒童教學",
  
  "dialog.custom_prompts_title": "自訂提示詞",
  "dialog.system_prompt_label": "系統提示詞 (System Prompt)",
  "dialog.user_prompt_label": "用戶提示詞 (User Prompt)",
  "dialog.prompt_template": "預設模板",
  "dialog.prompt_required_placeholders": "必要佔位符",
  "dialog.prompt_preview": "預覽",
  "button.save_prompts": "保存提示詞",
  "button.reset_prompts": "重設為預設",
  "status.tone_changed": "語氣已切換為：{tone}",
  "status.custom_prompts_saved": "自訂提示詞已保存",
  "error.prompt_missing_placeholder": "提示詞缺少必要佔位符：{placeholder}",
  "error.prompt_empty": "提示詞不能為空"
}
```

#### 3.2 定義語氣提示詞模板

新建檔案: `providers/tone_templates.py`

```python
TONE_PROMPTS = {
    "strict": {
        "system": "你是一位嚴謹的職業圍棋教練。用精確的棋理術語回答...",
        "user": "第{turn}手，學生下{user_move}導致勝率下降{winrate_drop:.1f}%。AI最佳手為{best_move}。請簡明指出問題所在。控制在60字以內。"
    },
    "friendly": {
        "system": "你是一位親切的圍棋老師，善於鼓勵學生...",
        "user": "..."
    },
    # ... 其他語氣
}
```

---

## 📊 實現步驟順序

### 優先級
1. **高** — 後端: 提示詞模板 + 語氣結構
2. **高** — UI: 語氣菜單 + 對話框
3. **中** — 翻譯 & 驗證
4. **低** — 新增語氣預設模板

### 建議實現順序

```
步驟 1: 建立 tone_templates.py (5 分鐘)
       ↓
步驟 2: 擴展 ConfigService (10 分鐘)
       ↓
步驟 3: 擴展 LLMProvider 基類 (15 分鐘)
       ↓
步驟 4: 更新 ollama_provider.py + 其他提供商 (20 分鐘)
       ↓
步驟 5: 添加 UI 語氣菜單 (15 分鐘)
       ↓
步驟 6: 建立自訂提示詞對話框 (30 分鐘)
       ↓
步驟 7: 添加 i18n 翻譯 (15 分鐘)
       ↓
步驟 8: 測試 & 除錯 (30 分鐘)
```

**總計**: ~140 分鐘 (約 2.5 小時)

---

## 🔧 技術細節

### 4.1 提示詞變量替換邏輯

```python
def _format_custom_prompt(template: str, critical_data: dict) -> str:
    """替換提示詞中的佔位符"""
    replacements = {
        "turn": critical_data.get("turn", "?"),
        "user_move": critical_data.get("user_move", "?"),
        "best_move": critical_data["current_best_moves"][0]["move"] 
                     if critical_data.get("current_best_moves") else "?",
        "winrate_drop": critical_data.get("winrate_drop", 0) * 100,
    }
    return template.format(**replacements)
```

### 4.2 驗證提示詞有效性

```python
REQUIRED_PLACEHOLDERS = {"turn", "user_move", "best_move", "winrate_drop"}

def validate_user_prompt(prompt: str) -> tuple[bool, str]:
    """驗證提示詞包含必要佔位符"""
    for placeholder in REQUIRED_PLACEHOLDERS:
        if f"{{{placeholder}}}" not in prompt:
            return False, f"缺少必要佔位符: {placeholder}"
    return True, ""
```

### 4.3 語氣應用邏輯

```python
def apply_tone(llm_response: str, tone: str) -> str:
    """在 LLM 回應後調整語氣（可選）"""
    # 方案 A: 在提示詞中嵌入語氣指令
    #   (推薦，無需後處理)
    
    # 方案 B: 用另一個 LLM 查詢調整既有回應
    #   (成本高，不推薦)
    
    return llm_response  # 預設不需要後處理
```

---

## 📝 使用流程 (用戶視角)

### 用例 1: 切換到嚴格語氣

```
1. 菜單 > 分析 > LLM 語氣 > 嚴格/專業
2. 確認對話框
3. 下一次 LLM 回應自動使用嚴格語氣
```

### 用例 2: 自訂提示詞

```
1. 菜單 > 分析 > LLM 模型 > [設定]
2. 切換到「自訂提示詞」標籤頁
3. 編輯系統提示詞和用戶提示詞
4. 驗證必要佔位符
5. 保存
6. 下一次 LLM 回應使用自訂提示詞
```

---

## ✅ 測試檢查清單

- [ ] 語氣切換生效 (LLM 回應改變)
- [ ] 自訂提示詞保存到 `ui_settings.json`
- [ ] 提示詞佔位符驗證正常
- [ ] 多語言翻譯完整 (zh_TW + en)
- [ ] 提示詞修改後立即生效
- [ ] 三個提供商 (Ollama、NVIDIA、GitHub) 都支援
- [ ] 回滾到預設提示詞正常
- [ ] UI 無明顯卡頓

---

## 🚀 後期擴展 (v0.3.0+)

- [ ] 雲端提示詞社群庫
- [ ] 提示詞版本管理 & Git 同步
- [ ] A/B 測試語氣效果
- [ ] 機器學習自動優化提示詞
- [ ] 用戶反饋迴圈

---

## 📚 參考資料

- 現有實現: `providers/ollama_provider.py` L110-150
- 設定系統: `services/config_service.py`
- UI 架構: `ui/main_v3.py`
- i18n 系統: `i18n/` 目錄

