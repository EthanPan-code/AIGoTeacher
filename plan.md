# Ollama 模型目錄最佳化計畫

## 目標

將 Ollama 從「固定推薦模型清單」改為「依 Ollama 服務實際回傳的模型目錄」運作，並在 UI、下載、驗證與錯誤處理中明確區分本機模型與雲端模型。

本次不改變 Ollama 作為單一 provider 的設定鍵：`llm_provider: "ollama"` 與 `ollama_model` 仍保持相容；也不影響 NVIDIA NIM、OpenRouter 或 KataGo 的流程。

## 現況與問題

目前 `providers/ollama_provider.py` 以 `OLLAMA_LOCAL_MODELS`、`OLLAMA_CLOUD_MODELS` 與 `OLLAMA_PAID_MODELS` 寫死可用模型，並以模型名稱是否包含 `cloud` 判斷類型。`services/ollama_manager.py` 則以 `ollama list`、`ollama show`、`ollama pull` CLI 管理模型。

這會造成：

- 使用者自行下載的本機模型不會自然出現在可選清單中。
- 新增、移除或改名的 Ollama 雲端模型必須改程式才能支援。
- `:cloud`、`-cloud` 等名稱慣例不適合作為可用性或類型的唯一判斷依據。
- 目前模型重新掃描與資訊讀取可能執行 CLI，增加 UI 阻塞與格式相依風險。

Ollama 的 `GET /api/tags` 回應會同時提供本機模型與雲端模型的 metadata；雲端項目包含 `remote_model`、`remote_host`，本機模型則具實際檔案大小、format、quantization 等資訊。此 metadata 是分類與呈現的唯一來源。

## 設計決策

### 動態模型目錄

- 在 `OllamaManager` 新增以 `http://localhost:11434` 為基礎的 REST client，使用 `GET /api/version` 健康檢查、`GET /api/tags` 取得模型目錄、`POST /api/pull` 下載本機模型。
- 定義 `OllamaModelInfo` 資料物件，至少包含：`name`、`model`、`kind`（`local` / `cloud`）、`remote_model`、`remote_host`、`size_bytes`、`modified_at`、`details`、`capabilities`。
- `kind` 僅依 tags metadata 的 `remote_model` 或 `remote_host` 判定；不再以模型字串是否有 `cloud`/`paid` 分類。
- Manager 以 10 秒 TTL 快取成功取得的 catalog，避免頻繁重繪造成多次 API 呼叫；使用者按「重新掃描」時強制略過快取。失敗時保留上一次成功資料並回傳可顯示的錯誤狀態。
- 保留 `DEFAULT_OLLAMA_MODEL = "qwen2.5:3b"` 作為首次安裝或舊設定缺少模型時的預設值，但不再把它當作可用模型清單。

### 本機與雲端模型的使用規則

| 類型 | 來源 | UI 顯示 | 可下載 | 可選取條件 |
|---|---|---|---|---|
| 本機模型 | `/api/tags` 中無 remote metadata 的項目 | 本機模型區，顯示大小、量化與能力 | 可；使用 `/api/pull` | 已出現在 tags 中 |
| 雲端模型 | `/api/tags` 中有 `remote_model` 或 `remote_host` 的項目 | 雲端模型區，顯示遠端模型與主機 | 不可 | 已由本機 Ollama 服務列出且帳號可使用 |

- 保留原先清單的模型並保留是否下載狀態顯示，目的僅為推薦。
- 雲端模型不顯示下載按鈕，也不由應用程式處理登入；登入、授權與雲端額度由 Ollama service/使用者帳號處理。
- 選取雲端模型時，若 API 回傳授權、額度或服務錯誤，沿用 provider fallback 講解，並顯示「發生錯誤，請確認 Ollama 登入、雲端模型權限或服務狀態」的專屬提示。
- 選取的 `ollama_model` 即使暫時未出現在 catalog 中，也必須在 UI 顯示為「目前設定／不可用」，不能靜默改成其他模型；使用者套用新模型後才覆寫設定。

## 實作變更

### `services/ollama_manager.py`

- 以 `requests` REST 呼叫取代模型列舉、模型資訊與下載流程的 CLI 依賴；保留 CLI 偵測僅供安裝指南/相容性顯示，不作為 catalog 來源。
- 提供 `check_service()`、`refresh_model_catalog(force=False)`、`get_local_models()`、`get_cloud_models()`、`get_model(name)`、`pull_model_async(name, ...)`。
- `/api/pull` 使用 streaming JSON 讀取進度，將 `status`、completed/total bytes 轉為既有下載進度 callback；下載完成後強制刷新 catalog。
- 對連線拒絕、逾時、無效 JSON、非 2xx 與 API error 建立結構化錯誤，避免把例外文字直接當成 UI 邏輯。

### `providers/ollama_provider.py` 與 Factory

- 移除固定 local/cloud/paid 模型清單與名稱字串分類；僅保留 `DEFAULT_OLLAMA_MODEL` 及 model display fallback。
- `get_model_status()` 改回傳動態 catalog 的 model info/status；`is_cloud_model()`、`is_model_available()`、`get_model_size()` 依 catalog metadata 判定。
- `validate_config()` 改為驗證 Ollama service 可回應，而非僅確認 Python `ollama` 套件可 import。
- 保留 `ollama.chat(..., stream=True)` 的既有講解串流行為；若後續 client 版本無法正確處理雲端 metadata，再統一改用 `/api/chat`，但本次不混用兩條生成路徑。
- `ProviderFactory` 的 Ollama default 改引用 `DEFAULT_OLLAMA_MODEL`；NVIDIA NIM、OpenRouter 註冊與模型探索 helper 不調整。

### `ui/main_v3.py`

- 將現有單一 Ollama 固定模型清單保留，`本機模型`、`雲端模型`會和原本一樣在圖示做出區隔。
- 開啟設定視窗時在背景執行緒取得 catalog，成功後更新兩區；按「重新掃描」強制更新，不阻塞 Tkinter 主執行緒。
- 本機列顯示：模型名稱、大小、參數/量化（資料存在時）、下載狀態、選取按鈕；未安裝不再從固定清單列出。
- 雲端列顯示：模型名稱、remote model、remote host（資料存在時）、選取按鈕與雲端標籤；不顯示下載控制。
- 保留現有設定套用、worker 重建、語氣/custom prompt、聊天沙盒與設定保存行為。

### i18n、文件與診斷

- 新增中英文翻譯：本機/雲端模型、雲端模型登入/權限提示、服務未啟動、catalog 讀取失敗、無可用本機模型、下載模型名稱輸入、遠端主機與目前設定不可用。
- 更新 README 與 `docs/migration-v1.0.md`：Ollama 同時支援本機與雲端模型；雲端模型是否可見與可使用由 Ollama account/service 決定，不要宣稱 Ollama 一律離線或無帳號需求。
- 診斷報告只輸出 Ollama service 可用性、版本、模型名稱與分類/數量；不得輸出帳號資訊、token 或完整遠端回應。

## 相容性與遷移

- 已保存的 `ollama_model` 保持原值，不做批次改名或刪除。
- 若舊模型可在新 catalog 找到，正常歸入本機或雲端區。
- 若舊模型不存在，保留設定並標示不可用；使用者可下載該本機模型、登入 Ollama 後取得雲端存取，或選擇其他模型。
- 移除 `OLLAMA_PAID_MODELS` 的硬編碼封鎖，因費率與可用性由 Ollama 動態回應與使用者帳號決定。

## 測試與驗收

- 使用 mock 的 `/api/version`、`/api/tags`、`/api/pull` 測試 Manager，不使用真實 Ollama service。
- 驗證 tags 範例可正確分出：
  - 本機 GGUF 模型（含 size/details/capabilities）。
  - 具 `remote_model`、`remote_host` 的雲端模型。
  - 缺少選填 metadata 的模型不會造成 crash。
- 驗證 10 秒快取、強制刷新、服務離線、逾時、無效 JSON、非 2xx 與保留上次成功 catalog 的行為。
- 驗證 `/api/pull` 進度解析、已下載刷新、單一下載鎖，以及雲端模型不可進入 pull 流程。
- 驗證設定畫面：本機/雲端分區、未知舊設定、雲端模型無下載按鈕、重新掃描非阻塞、選取後能保存 `ollama_model`。
- 回歸驗證：Ollama 本機模型與雲端模型都可完成 commentary streaming；NVIDIA NIM、OpenRouter provider、GitHub Models 遷移與 KataGo 分析流程保持通過。
- 執行 Python 編譯、JSON 檢查、既有 provider 測試與新增 Ollama catalog 單元測試；最後建立 PyInstaller 產物並確認 `requests` 與新的 Manager 模組被包含。

## 非目標

- 不在應用程式內建立 Ollama 帳號登入、付款或雲端額度管理。
- 不新增 Ollama 模型市集搜尋或價格比較；下載功能只接受使用者明確輸入的模型名稱。
- 不變更 NIM/OpenRouter 的 publisher/model 選擇 UI。
