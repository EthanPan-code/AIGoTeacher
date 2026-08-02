# LLM 提供來源遷移指南

本文件說明 AI Go Teacher 移除 GitHub Models 後，如何將既有設定轉移至其他 LLM 提供來源，以及如何設定新增的 OpenRouter。

## 為什麼移除 GitHub Models

GitHub Models 的 API 服務已停止提供，原本的 GitHub Models provider 無法再可靠地完成模型探索與對話生成。繼續保留該來源會造成以下問題：

- 使用者在設定畫面選取後無法完成 API 呼叫。
- 啟動時可能因 GitHub token 不可用而顯示錯誤。
- 舊版模型清單與 GitHub API 狀態不再具有參考價值。
- 維護失效的 token、模型清單與 fallback 邏輯會增加設定複雜度。

因此，GitHub Models 已從 provider 清單、設定介面、API 呼叫、keyring 存取、翻譯與使用說明中移除。

GitHub repository 與 release 頁面的連結仍然保留；這些連結只用於專案原始碼與版本下載，與 GitHub Models API 無關。

## 舊版設定的自動遷移

如果 `ui_settings.json` 中仍有舊設定：

```json
{
  "llm_provider": "github",
  "github_model": "openai/gpt-4o-mini"
}
```

程式啟動時會自動：

1. 將 `llm_provider` 改為 `ollama`。
2. 若沒有 `ollama_model`，使用 Ollama 預設模型。
3. 移除不再使用的 `github_model` 欄位。
4. 將遷移後設定保存回 `ui_settings.json`。

既有的 Ollama 與 NVIDIA NIM 模型設定會保留。若設定檔已使用 `ollama` 或 `nvidia`，只會清除殘留的 `github_model` 欄位，不會改變目前 provider。

GitHub token 不會由程式自動刪除。程式已停止讀取或寫入 GitHub token、`GITHUB_TOKEN` 與 `KATAGO_GITHUB_TOKEN`；若仍存在於作業系統 keyring 或環境變數，使用者可依需要自行清理。

## 可用的替代來源

目前可使用以下三種來源：

| Provider | 適用情境 | API Key |
|---|---|---|
| Ollama | 本機執行、離線使用、無雲端 API key | 不需要 |
| NVIDIA NIM | 使用 NVIDIA 提供的雲端模型 | `NVIDIA_API_KEY` |
| OpenRouter | 透過單一 API 存取多家模型 | `OPENROUTER_API_KEY` |

## 方式一：使用 Ollama

Ollama 不需要 API key，模型在本機執行。

1. 安裝 Ollama。
2. 下載模型，例如：

   ```bash
   ollama pull qwen2.5:3b
   ```

3. 開啟 AI Go Teacher 的「分析 > LLM 模型」。
4. 選擇 `Ollama`，選取已下載的模型後套用。

如果模型尚未下載，設定畫面會提供下載或繼續保存設定的選項。

## 方式二：使用 NVIDIA NIM

NVIDIA NIM 使用雲端 API。API key 可透過下列任一方式提供：

- 在程式的 LLM 模型設定畫面輸入，程式會保存到作業系統 keyring。
- 設定環境變數 `NVIDIA_API_KEY`。
- 設定相容環境變數 `KATAGO_NVIDIA_API_KEY`。

PowerShell 範例：

```powershell
$env:NVIDIA_API_KEY = "nvapi-..."
py ui/main_v3.py
```

在設定畫面選擇 `NVIDIA NIM` 後，程式會背景探索可用模型，並以 `Publisher` → `Model` 的方式選取。探索失敗時會使用內建模型清單，並顯示 fallback 提示。

## 方式三：使用 OpenRouter

OpenRouter 使用 OpenAI 相容的 API，能透過統一端點存取多家模型。API key 可透過下列任一方式提供：

- 在程式的 LLM 模型設定畫面輸入，程式會保存到作業系統 keyring。
- 設定環境變數 `OPENROUTER_API_KEY`。
- 設定相容環境變數 `KATAGO_OPENROUTER_API_KEY`。

PowerShell 範例：

```powershell
$env:OPENROUTER_API_KEY = "sk-or-v1-..."
py ui/main_v3.py
```

設定流程與 NVIDIA NIM 一致：

1. 開啟「分析 > LLM 模型」。
2. 選擇 `OpenRouter`。
3. 輸入 API key。
4. 等待模型清單探索完成。
5. 依序選擇 `Publisher` 與 `Model`。
6. 按下套用。

OpenRouter 使用以下 API：

- 模型探索：`GET https://openrouter.ai/api/v1/models`
- 對話生成：`POST https://openrouter.ai/api/v1/chat/completions`

對話使用 SSE 串流。若 API 回傳 HTTP 402、429、503，或串流中途回傳錯誤事件，程式會顯示備用講解並保留應用程式運作。

模型探索失敗時，程式會使用內建 fallback 清單；成功探索後則以 OpenRouter 回傳的模型 ID 為準。模型 ID 會直接保存，例如：

```json
{
  "llm_provider": "openrouter",
  "openrouter_model": "openai/gpt-oss-20b:free"
}
```

## API key 安全性

API key 不會保存到 `ui_settings.json`，也不會寫入專案內的 `.env` 檔。程式會優先讀取作業系統 keyring，環境變數只作為 fallback。

請避免：

- 將 API key 寫入 git 追蹤的檔案。
- 將含有 key 的 `.env` 上傳到 GitHub。
- 將 API key 貼到診斷報告、issue 或公開 log。

若 key 已經外洩，應立即在對應服務的控制台撤銷並重新建立。

## 遷移後驗證

完成切換後，可依下列項目確認設定正常：

1. LLM 模型設定畫面只顯示 Ollama、NVIDIA NIM 與 OpenRouter。
2. 設定標籤顯示所選 provider 與模型。
3. 觸發一個需要教學解說的棋步，確認可收到串流文字。
4. 暫時輸入錯誤 API key，確認程式顯示 fallback，而不是整個 UI 結束。
5. 重新啟動程式，確認 provider 與模型仍被保存。
6. 若使用本機 Ollama，確認 Ollama 服務仍可獨立運作。

## 常見問題

### 啟動後仍看到 GitHub Models 設定

請確認使用的是最新的 source code 或重新打包後的 executable。新版程式不會再建立 GitHub Models 設定區塊。

### OpenRouter 模型清單是空的

請先確認 API key 正確、網路可連線，並檢查 OpenRouter 的模型服務狀態。短時間探索失敗時，程式會自動切換到內建 fallback 清單。

### OpenRouter 回傳 402

通常代表帳戶餘額或 API key 使用額度不足，請在 OpenRouter 控制台確認 credits 與 key limits，或改用 Ollama 等不需要雲端額度的來源。

### OpenRouter 回傳 429 或 503

通常代表速率限制或暫時沒有可用的模型供應商。可稍後重試、選擇其他模型，或切換至 NVIDIA NIM/Ollama。

