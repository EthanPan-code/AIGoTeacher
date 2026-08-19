# Graph Report - AIGoTeacher  (2026-08-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 743 nodes · 1383 edges · 38 communities (30 shown, 8 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 46 edges (avg confidence: 0.54)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2396ae38`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- GoBoard
- AI 圍棋老師 / AI Go Teacher
- OllamaProvider
- ProviderFactory
- Contributing to AI Go Teacher / 為 AI Go Teacher 貢獻
- LLM 提供來源遷移指南 / LLM Provider Migration Guide
- LLMChatWindow
- ConfigService
- KataGoAnalyzer
- refresh_tab_bar
- t
- main_v3.py
- I18n
- refresh_language
- LLMProvider
- update_score_estimate_button_label
- TabManager
- FakeMenuBar
- BranchTreeView
- keyring_service.py
- serialize_game_context
- safe_get_system_info
- tone_templates.py
- provider_factory.py
- create_dev_menu
- normalize_api_key
- Security Policy
- NvidiaProvider
- OpenRouterProvider
- requirements.txt - Python Dependencies
- render_teacher_ui
- detect_ollama_installed
- GUI Screenshot
- Available Status Screenshot
- Cloud API Illustration
- Download UI Screenshot
- version_info.txt - PyInstaller VSVersionInfo

## God Nodes (most connected - your core abstractions)
1. `t()` - 67 edges
2. `GoBoard` - 55 edges
3. `LLMChatWindow` - 33 edges
4. `ProviderFactory` - 31 edges
5. `LLMProvider` - 24 edges
6. `ConfigService` - 24 edges
7. `build_menu_bar()` - 24 edges
8. `OllamaProvider` - 23 edges
9. `resource_path()` - 20 edges
10. `FakeMenuBar` - 19 edges

## Surprising Connections (you probably didn't know these)
- `README` --references--> `i18n System`  [EXTRACTED]
  README.md → i18n.py
- `README` --references--> `LLM Providers`  [EXTRACTED]
  README.md → providers/*.py
- `ProviderFactory` --uses--> `OllamaProvider`  [INFERRED]
  services/provider_factory.py → providers/ollama_provider.py
- `ProviderFactory` --uses--> `NvidiaProvider`  [INFERRED]
  services/provider_factory.py → providers/nvidia_provider.py
- `ProviderFactory` --uses--> `OpenRouterProvider`  [INFERRED]
  services/provider_factory.py → providers/openrouter_provider.py

## Import Cycles
- None detected.

## Communities (38 total, 8 thin omitted)

### Community 0 - "GoBoard"
Cohesion: 0.07
Nodes (12): GameNode, GoBoard, load_tk_image(), Load an image as a Tk image, preferring Pillow for broad format support., 依 board_shell 實際尺寸重新縮放外框背景圖片（cover 模式：填滿裁切）。 由 board_shell 的 <Configure>…, 動態生成歷史落子紀錄，不會再因為提子而消失，確保 AI 判斷正確, Return 1-based move index where the current branch starts, or None on main line., 切換同一手棋的不同變化圖 (direction: 1 或 -1) (+4 more)

### Community 1 - "AI 圍棋老師 / AI Go Teacher"
Cohesion: 0.05
Nodes (44): AI 圍棋老師 / AI Go Teacher, Communication Protocols, Contents, Core Capabilities, Core Modules, Custom Teaching Tones, Development Commands, Download the Executable (Windows) (+36 more)

### Community 2 - "OllamaProvider"
Cohesion: 0.08
Nodes (9): OllamaProvider, get_ollama_manager(), OllamaManager, OllamaModelInfo, Return (models, error), retaining the last good catalog on failure., Read a model without triggering network I/O., Start a streaming REST pull for a local model., REST client and catalog cache for the local Ollama service. (+1 more)

### Community 3 - "ProviderFactory"
Cohesion: 0.08
Nodes (16): ProviderFactory, Return the human-readable display name for a model ID. Falls back to the raw…, Reverse lookup: display name → model ID. Returns None when the display name is…, Return [(display_name, model_id), ...] for UI widgets. The list follows the…, 向 NIM 端點探索可用模型，失敗時降級至內建清單。 回傳 (model_ids, used_fallback, error_message)： -…, 從 model_id 清單取出 publisher 清單（已排序、去重）。, 取得指定 publisher 下的 model_id 清單（保持原始順序）。, 從 model_id 拆出 publisher（供 UI 還原選擇用）。 (+8 more)

### Community 4 - "Contributing to AI Go Teacher / 為 AI Go Teacher 貢獻"
Cohesion: 0.06
Nodes (35): Acknowledgments, Before Submitting a Bug Report, Before Submitting an Enhancement, Commit Messages, Commit 訊息, Contributing to AI Go Teacher / 為 AI Go Teacher 貢獻, Development Environment Setup, How Do I Submit a Good Bug Report? (+27 more)

### Community 5 - "LLM 提供來源遷移指南 / LLM Provider Migration Guide"
Cohesion: 0.06
Nodes (32): API Key Security, API key 安全性, Automatic Migration of Legacy Settings, Available Alternatives, Frequently Asked Questions, GitHub Models Still Appears After Startup, LLM 提供來源遷移指南 / LLM Provider Migration Guide, OpenRouter Returns HTTP 402 (+24 more)

### Community 6 - "LLMChatWindow"
Cohesion: 0.11
Nodes (3): LLMChatWindow, 輸入框獲得焦點時清除 placeholder。, 輸入框失去焦點時恢復 placeholder。

### Community 7 - "ConfigService"
Cohesion: 0.11
Nodes (8): ConfigService, Small wrapper around persisted UI settings., Migrate settings from the removed GitHub Models provider., detect_system_theme(), normalize_theme(), Application color themes and Windows system-theme resolution., Return the Windows theme at process startup; safely fall back to light., resolve_theme()

### Community 8 - "KataGoAnalyzer"
Cohesion: 0.06
Nodes (35): _build_diagnostic_report_text(), _delete_runtime_path(), ensure_runtime_dir(), get_config_path(), get_executable_dir(), get_katago_path(), get_katago_runtime_overrides(), get_model_path() (+27 more)

### Community 9 - "refresh_tab_bar"
Cohesion: 0.11
Nodes (28): _capture_board_snapshot(), _close_tab_silently(), _copy_game_tree(), hydrate_active_session(), on_close_tab_click(), on_copy_tab_click(), on_load_sgf_click(), on_new_tab_click() (+20 more)

### Community 10 - "t"
Cohesion: 0.13
Nodes (29): get_tone_prompt(), Return the preset prompt in the requested UI language., build_menu_bar(), change_config_path(), change_katago_path(), change_model_path(), _confirm_and_download_ollama_model(), _download_ollama_model() (+21 more)

### Community 11 - "main_v3.py"
Cohesion: 0.09
Nodes (24): add_to_commentary_cache(), auto_analyze(), _commentary_cache_key(), _create_info_section(), _create_katago_section(), _create_labeled_row(), _create_ollama_model_row(), get_commentary_from_cache() (+16 more)

### Community 12 - "I18n"
Cohesion: 0.15
Nodes (12): Path, I18n, resource_path(), main(), Application version helpers for AI Go Teacher. Run this file to update every…, Return the numeric tuple used by PyInstaller's VSVersionInfo., _replace_once(), sync_version() (+4 more)

### Community 13 - "refresh_language"
Cohesion: 0.13
Nodes (19): apply_theme(), create_katago_startup_popup(), on_analyze_button_click(), on_closing(), Stop the active continuous query and clear its routing state., Refresh controls that expose the continuous-analysis state., Expose semantic theme tokens to legacy drawing code in this module., Apply a configured theme to existing widgets without restarting. (+11 more)

### Community 14 - "LLMProvider"
Cohesion: 0.11
Nodes (6): LLMProvider, Return a human-readable display name for the given model ID. Subclasses should…, Return (is_valid, error_message)., Send a raw prompt to the LLM for a plain chat conversation. This is used by the…, Base class for streaming LLM commentary providers., Build the final prompt sent to the model from plain user text plus data.

### Community 15 - "update_score_estimate_button_label"
Cohesion: 0.28
Nodes (9): _handle_score_estimate_result(), on_close_score_estimate_click(), on_score_estimate_click(), show_score_estimate_popup(), start_score_analyzer_async(), _start_score_estimate_query(), summarize_score_estimate(), update_score_estimate_button_label() (+1 more)

### Community 16 - "TabManager"
Cohesion: 0.10
Nodes (7): 多分頁文件管理器：維護所有 TabSession 並提供 active session 切換。, 建立第一個分頁並設為 active。供 main 流程開機時呼叫一次。, 建立新分頁。若已達 MAX_TABS，回傳 None。, 關閉指定分頁；回傳 (success, reason)。 規則： - 至少保留一個分頁。 - 若傳入 index 為 active，自動切到鄰近分頁。, 支援 tab_manager[idx] 取第 idx 個分頁。, TabManager, TabSession

### Community 17 - "FakeMenuBar"
Cohesion: 0.23
Nodes (3): FakeMenuBar, Themeable, Tk-only application menu bar. This deliberately does not use native…, A small menu system built from Frames and Buttons. Menu definitions are plain…

### Community 19 - "keyring_service.py"
Cohesion: 0.16
Nodes (14): _delete_api_key(), delete_nvidia_api_key(), delete_openrouter_api_key(), Store NVIDIA API key in the OS keyring. Does not write to .env., Store OpenRouter API key in the OS keyring. Does not write to .env., Delete one application credential, treating a missing credential as success., Delete the NVIDIA API key owned by this application., Delete the OpenRouter API key owned by this application. (+6 more)

### Community 20 - "serialize_game_context"
Cohesion: 0.19
Nodes (11): _analysis_lines(), _gtp(), _move_text(), Compact, factual Go-game context for LLM teaching prompts. This module…, Serialize only the selected mainline and explicitly named snapshots., serialize_board(), serialize_game_context(), serialize_mainline() (+3 more)

### Community 21 - "safe_get_system_info"
Cohesion: 0.15
Nodes (16): _format_bytes_as_gb(), _get_cpu_name(), _get_gpu_info(), _get_physical_core_count(), _get_ram_info(), _get_windows_display_version(), 把位元組數轉成 GB 字串；輸入不可用時回傳 Unknown。, 執行 PowerShell 並解析 JSON，失敗時回傳 None。 這裡只用於診斷資訊的 best-effort 查詢，任何錯誤都不能影響主 UI。 (+8 more)

### Community 22 - "tone_templates.py"
Cohesion: 0.17
Nodes (14): find_preset_tone(), get_all_tones(), get_tone_description(), get_tone_display_name(), Single-block LLM prompt templates for AI Go teacher commentary. The application…, Return the tone if prompt is an untouched preset, otherwise ``None``., 若呼叫端未提供 translator，嘗試用 ui.i18n 全域 t()。, 取得 tone 對應的本地化名稱。translator 為 None 時退到中文 fallback。 (+6 more)

### Community 23 - "provider_factory.py"
Cohesion: 0.26
Nodes (8): discover_nim_models(), get_publisher_from_model_id(), group_models_by_publisher(), 從 model_id 拆出 publisher（第一個 '/' 之前的部分）。 無 '/' 的 model_id 歸類為 "unknown"，確保 UI…, 將 model_id 清單依 publisher 分組，回傳 {publisher: [model_id, ...]}。 保持各 publisher 內…, 向 NIM 端點 /v1/models 查詢可用模型清單。 成功時回傳 (True, [model_id, ...])；失敗時回傳 (False,…, get_publisher_from_model_id(), group_models_by_publisher()

### Community 24 - "create_dev_menu"
Cohesion: 0.29
Nodes (7): create_dev_menu(), export_diagnostic_report(), _open_folder(), 顯示診斷報告匯出完成訊息與開啟資料夾按鈕。, 匯出診斷報告到 diagnostics/diagnostic_report.txt。, Return Dev menu items for the themeable menu bar., _show_diagnostic_export_success()

### Community 25 - "normalize_api_key"
Cohesion: 0.24
Nodes (8): discover_openrouter_models(), Return (True, model_ids) or (False, error_message)., get_nvidia_api_key(), get_openrouter_api_key(), normalize_api_key(), Trim whitespace and common quote wrappers from API key values., Read NVIDIA API key from keyring first, then environment variables., Read OpenRouter API key from keyring first, then environment variables.

### Community 26 - "Security Policy"
Cohesion: 0.18
Nodes (10): Accepted Reports, Declined Reports, In-Scope, Information to Include, Out-of-Scope, Reporting a Vulnerability, Response & Resolution Process, Scope (+2 more)

### Community 29 - "requirements.txt - Python Dependencies"
Cohesion: 0.29
Nodes (7): requirements.txt - Python Dependencies, httpx HTTP Client, keyring Package, matplotlib Package, ollama Python Package, opencc Chinese Conversion, Pillow (PIL) Package

### Community 30 - "render_teacher_ui"
Cohesion: 0.33
Nodes (6): new_game(), 只更新老師解說區，不改動生成中的快取狀態。, LLM Provider 的串流回呼；累積全文但在回放時不覆蓋既有解說。, render_teacher_ui(), start_new_game_from_welcome(), update_teacher_ui()

### Community 31 - "detect_ollama_installed"
Cohesion: 0.50
Nodes (4): detect_ollama_installed(), 在 Windows 上抑制子進程彈出的主控台視窗。 隱藏終端機 (windowed) 模式下，子進程預設會繼承一個可見的主控台， 即使…, 檢查系統是否能執行 `ollama --version`，回傳 (installed: bool, version_or_none), _silent_subprocess_kwargs()

## Knowledge Gaps
- **100 isolated node(s):** `Communication Protocols`, `Contents`, `Core Capabilities`, `Core Modules`, `Custom Teaching Tones` (+95 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `GoBoard` connect `GoBoard` to `main_v3.py`?**
  _High betweenness centrality (0.108) - this node is a cross-community bridge._
- **Why does `ProviderFactory` connect `ProviderFactory` to `OllamaProvider`, `t`, `main_v3.py`, `keyring_service.py`, `serialize_game_context`, `provider_factory.py`, `NvidiaProvider`, `OpenRouterProvider`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Why does `LLMChatWindow` connect `LLMChatWindow` to `ProviderFactory`, `main_v3.py`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `t()` (e.g. with `get_tone_description()` and `get_tone_display_name()`) actually correct?**
  _`t()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `ProviderFactory` (e.g. with `NvidiaProvider` and `OllamaProvider`) actually correct?**
  _`ProviderFactory` has 10 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Communication Protocols`, `Contents`, `Core Capabilities` to the rest of the system?**
  _100 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `GoBoard` be split into smaller, more focused modules?**
  _Cohesion score 0.06512890094979647 - nodes in this community are weakly interconnected._