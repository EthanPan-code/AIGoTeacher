
# LLM 提供來源遷移指南 / LLM Provider Migration Guide

[English](#English) [繁體中文](#Chinese)

---

<a id="English"></a>

This document explains how to migrate your existing settings to other LLM providers after AI Go Teacher removed GitHub Models, and how to configure the newly added OpenRouter provider.

## Why GitHub Models Was Removed

The GitHub Models API service has been discontinued. As a result, the original GitHub Models provider can no longer reliably perform model discovery or generate chat responses. Keeping the provider would lead to the following issues:

* API requests fail after selecting GitHub Models in the settings.
* Startup errors may occur if the GitHub token is unavailable.
* The legacy model list and GitHub API status are no longer meaningful.
* Maintaining obsolete tokens, model lists, and fallback logic increases configuration complexity.

Therefore, GitHub Models has been removed from the provider list, settings interface, API calls, keyring access, translations, and user documentation.

Links to the GitHub repository and release pages remain available. These links are only used for accessing the project source code and downloading releases, and are unrelated to the GitHub Models API.

## Automatic Migration of Legacy Settings

If `ui_settings.json` still contains the following legacy configuration:

```json
{
  "llm_provider": "github",
  "github_model": "openai/gpt-4o-mini"
}
```

The application will automatically perform the following steps on startup:

1. Change `llm_provider` to `ollama`.
2. If `ollama_model` is missing, use the default Ollama model.
3. Remove the obsolete `github_model` field.
4. Save the migrated configuration back to `ui_settings.json`.

Existing Ollama and NVIDIA NIM model settings are preserved. If the configuration already uses `ollama` or `nvidia`, only the obsolete `github_model` field is removed; the current provider is left unchanged.

GitHub tokens are not automatically deleted. The application no longer reads from or writes to GitHub tokens, `GITHUB_TOKEN`, or `KATAGO_GITHUB_TOKEN`. If these still exist in your operating system's keyring or environment variables, you may remove them manually if desired.

## Available Alternatives

The following LLM providers are currently supported:

| Provider   | Recommended For                                                    | API Key                                                                              |
| ---------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| Ollama     | Local models or cloud models available through your Ollama account | Not required for local models; cloud access is managed by the Ollama service/account |
| NVIDIA NIM | NVIDIA-hosted cloud models                                         | `NVIDIA_API_KEY`                                                                     |
| OpenRouter | Accessing models from multiple providers through a single API      | `OPENROUTER_API_KEY`                                                                 |

## Option 1: Using Ollama

Local Ollama models run through the local Ollama service and do not require an application API key. Cloud models depend on your Ollama service login status, permissions, and quota.

1. Install Ollama.

2. Download a model, for example:

   ```bash
   ollama pull qwen2.5:3b
   ```

3. Open **Settings > LLM Model** in AI Go Teacher.

4. Select **Ollama**, choose a downloaded model, and apply the settings.

If the selected model has not yet been downloaded, the settings page provides options to download it or continue saving the configuration.

## Option 2: Using NVIDIA NIM

NVIDIA NIM uses a cloud-based API. You can provide the API key by:

* Entering it in the application's **LLM Model** settings page, where it will be securely stored in your operating system's keyring.

After selecting **NVIDIA NIM**, the application automatically discovers available models in the background. Models are selected using the **Publisher → Model** hierarchy. If discovery fails, the built-in fallback model list is used and a fallback notification is displayed.

## Option 3: Using OpenRouter

OpenRouter provides an OpenAI-compatible API that allows access to models from multiple providers through a unified endpoint. You can provide the API key by:

* Entering it in the application's **LLM Model** settings page, where it will be securely stored in your operating system's keyring.

The setup process is the same as NVIDIA NIM:

1. Open **Analysis > LLM Model**.
2. Select **OpenRouter**.
3. Enter your API key.
4. Wait for model discovery to complete.
5. Select a **Publisher** and then a **Model**.
6. Click **Apply**.

OpenRouter uses the following APIs:

* Model discovery: `GET https://openrouter.ai/api/v1/models`
* Chat completion: `POST https://openrouter.ai/api/v1/chat/completions`

Chat responses are streamed using SSE. If the API returns HTTP 402, 429, or 503, or an error event occurs during streaming, the application displays a fallback explanation while continuing to operate normally.

If model discovery fails, the built-in fallback list is used. When discovery succeeds, the model IDs returned by OpenRouter are used directly. For example:

```json
{
  "llm_provider": "openrouter",
  "openrouter_model": "openai/gpt-oss-20b:free"
}
```

## API Key Security

API keys are not stored in `ui_settings.json` and are never written to the project's `.env` file. The application reads credentials from the operating system keyring whenever possible, using environment variables only as a fallback.

Avoid the following:

* Storing API keys in Git-tracked files.
* Uploading `.env` files containing API keys to GitHub.
* Including API keys in diagnostic reports, issues, or public logs.

If an API key has been exposed, revoke it immediately through the corresponding service dashboard and generate a new one.

## Verifying the Migration

After switching providers, verify the configuration by checking the following:

1. The LLM Model settings page only lists Ollama, NVIDIA NIM, and OpenRouter.
2. The settings label displays the selected provider and model.
3. Trigger a move that requires AI commentary and confirm that streamed text is received.
4. Temporarily enter an invalid API key and verify that the application falls back gracefully instead of terminating the UI.
5. Restart the application and confirm that the selected provider and model are still saved.
6. If using Ollama, verify that the local service is running and that cloud model users have signed in to Ollama.

## Frequently Asked Questions

### GitHub Models Still Appears After Startup

Make sure you are using the latest source code or a newly packaged executable. New versions no longer create GitHub Models configuration sections.

### The OpenRouter Model List Is Empty

Verify that your API key is valid, your network connection is working, and the OpenRouter model service is available. If discovery temporarily fails, the application automatically switches to the built-in fallback model list.

### OpenRouter Returns HTTP 402

This usually indicates that your account balance or API key quota has been exhausted. Check your credits and key limits in the OpenRouter dashboard, or switch to a local Ollama model.

### OpenRouter Returns HTTP 429 or 503

This usually indicates rate limiting or that no provider is currently available for the selected model. Try again later, choose a different model, or switch to NVIDIA NIM or Ollama.

---

<a id="Chinese"></a>

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
| Ollama | 本機模型或 Ollama 帳號可用的雲端模型 | 本機不需要；雲端由 Ollama service/account 管理 |
| NVIDIA NIM | 使用 NVIDIA 提供的雲端模型 | `NVIDIA_API_KEY` |
| OpenRouter | 透過單一 API 存取多家模型 | `OPENROUTER_API_KEY` |

## 方式一：使用 Ollama

Ollama 的本機模型透過本機 service 執行，不需要應用程式 API key；雲端模型則由 Ollama service 的登入狀態、權限與額度決定。

1. 安裝 Ollama。
2. 下載模型，例如：

   ```bash
   ollama pull qwen2.5:3b
   ```

3. 開啟 AI Go Teacher 的「設定 > LLM 模型」。
4. 選擇 `Ollama`，選取已下載的模型後套用。

如果模型尚未下載，設定畫面會提供下載或繼續保存設定的選項。

## 方式二：使用 NVIDIA NIM

NVIDIA NIM 使用雲端 API。API key 可透過下列方式提供：

- 在程式的 LLM 模型設定畫面輸入，程式會保存到作業系統 keyring。


在設定畫面選擇 `NVIDIA NIM` 後，程式會背景探索可用模型，並以 `Publisher` → `Model` 的方式選取。探索失敗時會使用內建模型清單，並顯示 fallback 提示。

## 方式三：使用 OpenRouter

OpenRouter 使用 OpenAI 相容的 API，能透過統一端點存取多家模型。API key 可透過以下提供：

- 在程式的 LLM 模型設定畫面輸入，程式會保存到作業系統 keyring。

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
6. 若使用 Ollama，確認本機 service 可回應，且雲端模型使用者已完成 Ollama 登入。

## 常見問題

### 啟動後仍看到 GitHub Models 設定

請確認使用的是最新的 source code 或重新打包後的 executable。新版程式不會再建立 GitHub Models 設定區塊。

### OpenRouter 模型清單是空的

請先確認 API key 正確、網路可連線，並檢查 OpenRouter 的模型服務狀態。短時間探索失敗時，程式會自動切換到內建 fallback 清單。

### OpenRouter 回傳 402

通常代表帳戶餘額或 API key 使用額度不足，請在 OpenRouter 控制台確認 credits 與 key limits，或改用本機 Ollama 模型。

### OpenRouter 回傳 429 或 503

通常代表速率限制或暫時沒有可用的模型供應商。可稍後重試、選擇其他模型，或切換至 NVIDIA NIM/Ollama。

