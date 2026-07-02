# AI 圍棋老師 / AI Go Teacher

[![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![KataGo](https://img.shields.io/badge/KataGo-v1.16.4-2EA043)](https://katagotraining.org/)
[![Windows](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows)](https://www.microsoft.com/)
![License](https://img.shields.io/badge/License-MIT-red)
![Version](https://img.shields.io/badge/Version-0.3.0--beta-blue)

**AI 圍棋老師 v0.3.0-beta** 是一個互動式圍棋教學系統，由 **KataGo v1.16.4** 神經網路引擎驅動，結合 Python Tkinter 圖形介面與多提供商 LLM 評論功能。

English | 中文

---

## 目錄

- 功能特色
- 快速開始
- 技術架構
- LLM 整合
- i18n
- 開發指令

---

## 功能特色

### 核心功能

| 功能 | 說明 |
|------|------|
| **互動棋盤** | Tkinter 視覺化棋盤，支援點擊下棋、拖曳、縮放 |
| **即時分析** | 同步顯示 AI 推薦手、勝率、預測變化 |
| **全局分析** | 整盤棋局勝率曲線圖 |
| **SGF 支援** | 匯入/匯出棋譜，支援分支導航 |
| **LLM 評論** | 多提供商 AI 圍棋解說 |

### LLM 提供商支援

| 提供商 | 類型 | 預設模型 |
|--------|------|----------|
| **Ollama** | 本機 / 雲端 API | `qwen2.5:3b` |
| **NVIDIA NIM** | 雲端 API | `meta/llama-3.1-8b-instruct` |
| **GitHub Models** | 雲端 API | `GPT-4o` |

---

## 快速開始

### 前置需求

- Windows 作業系統
- Python 3.14+
- KataGo 模型檔案（需從 [katagotraining.org](https://katagotraining.org/) 下載）

### 安裝步驟

```bash
# 1. 複製專案
git clone https://github.com/EthanPan-code/AIGoTeacher.git
cd AIGoTeacher

# 2. 安裝依賴
pip install -r requirements.txt

# 3. 下載 KataGo 模型
'''
前往 https://katagotraining.org/ 下載神經網路權重檔案
放置於 models/ 目錄下
'''

# 4. 執行
py ui/main_v3.py
```


---

## 技術架構
### 圍棋引擎

| 技術                 | 說明                    |
| ------------------ | --------------------- |
| **KataGo v1.16.4** | 頂尖神經網路圍棋引擎            |
| **神經網路權重模型**       | 支援 GPU／CPU 加速的策略與價值網路 |
### 前端與應用程式層

| 技術                | 用途          |
| ----------------- | ----------- |
| **Python 3.14**   | 主要開發語言      |
| **Python 3.13 & PyInstaller**   |  打包成單一執行檔  |
| **Tkinter / ttk** | 跨平台桌面圖形介面框架 |
| **Matplotlib**    | 勝率與目差圖表視覺化  |
| **Pillow (PIL)**  | 棋盤材質與圖片資源處理 |


### 核心模組

| 模組 | 職責 |
|------|------|
| `main_v3.py` | 主程式：棋盤渲染、分析引擎、事件處理 |
| `providers/*.py` | LLM 提供商實作（Ollama/NVIDIA/GitHub） |
| services | 設定管理、API 金鑰安全儲存 |
| `i18n.py` | 國際化系統 |

### 通訊協定

- **非同步 JSON 協定**：透過 stdin/stdout 與 KataGo 引擎溝通
- **響應匹配**：使用 unique `id` 欄位匹配請求與回應
- **執行緒安全**：使用 `queue.Queue` 進行執行緒間通訊

## Python 相依套件

```text
matplotlib >= 3.7
pillow >= 10.0
python-dotenv >= 1.0
keyring >= 24.0
requests >= 2.31
opencc-python-reimplemented
```

---

## LLM 整合

### 設定 API 金鑰

**Ollama（本地）**
```bash
# 安裝後自動偵測，無需 API 金鑰
ollama pull qwen2.5:3b
```

**NVIDIA NIM**

api key：
```
nvapi-xxxxx
```

**GitHub Models**

api key：
```
github_pat_xxxxx
```

### 自訂教學語氣

LLM 評論支援多種語氣模板，可根據學習者程度調整解說深度。

---

## i18n

| 語言 | 檔案 |
|------|------|
| 繁體中文 | zh_TW.json |
| English | en.json |

**切換語言**：透過 UI 選單 `設定` > `語言` 即時切換

---

## 開發指令

### KataGo 引擎指令

| 指令 | 用途 |
|------|------|
| `katago.exe benchmark -model <model>.bin.gz` | 測試 GPU 效能 |
| `katago.exe analysis -model <model>.bin.gz -config analysis.cfg` | 啟動分析模式 |
| `katago.exe gtp -model <model>.bin.gz -config gtp.cfg` | 啟動 GTP 模式 |

### Python 指令

```bash
py ui/main_v3.py           # 啟動主程式
py version.py 0.3.0-beta   # 更新版本號
```


---

## 授權

本專案採用 MIT 授權條款。詳見 [LICENSE](LICENSE) 檔案。





