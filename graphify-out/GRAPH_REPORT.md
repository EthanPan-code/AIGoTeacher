# Graph Report - AIGoTeacher  (2026-10-13)

## Corpus Check
- 30 files · ~66,009 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: .gz 2, .spec 1, (none) 1)

## Summary
- 1171 nodes · 2384 edges · 63 communities (55 shown, 8 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 153 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1ffd0aba`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- GoBoard
- AI 圍棋老師 / AI Go Teacher
- OllamaManager
- ProviderFactory
- Contributing to AI Go Teacher / 為 AI Go Teacher 貢獻
- LLM 提供來源遷移指南 / LLM Provider Migration Guide
- ._start_generation
- ConfigService
- nvidia_provider.py
- refresh_tab_bar
- _clear_selected_runtime_data
- materialize_bundled_runtime_file
- chat_sandbox.py
- find_service.py
- LLMProvider
- OllamaProvider
- TabManager
- MenuBar
- BranchTreeView
- version.py
- show_appearance_settings_dialog
- safe_get_system_info
- I18n
- OpenRouterProvider
- LLMChatWindow
- normalize_api_key
- Security Policy
- NvidiaProvider
- plot_window
- requirements.txt - Python Dependencies
- _legacy_show_system_info_dialog
- get_runtime_data_root
- GUI Screenshot
- _show_llm_selection_dialog
- show_analysis_log_dialog
- show_system_info_dialog
- _download_ollama_model
- version_info.txt - PyInstaller VSVersionInfo
- start_analyzer_async
- main_v3.py
- ._active_conversation
- ._refresh_conversation_list
- build_menu_bar
- get_active_analysis_settings
- .__init__
- ._build_ui
- t
- _ask_sgf_link
- resource_path
- update_ui_with_data
- KataGoAnalyzer
- create_path_row
- ._apply_chat_palette_swap
- show_find_dialog
- ImeFontManager
- MessageBubble
- save_and_apply_settings
- task
- set_winrate_text
- update_ui
- _build_diagnostic_report_text
- .discover_nim_models

## God Nodes (most connected - your core abstractions)
1. `t()` - 119 edges
2. `LLMChatWindow` - 86 edges
3. `GoBoard` - 65 edges
4. `ConfigService` - 38 edges
5. `build_menu_bar()` - 37 edges
6. `_show_llm_selection_dialog()` - 35 edges
7. `ProviderFactory` - 31 edges
8. `resource_path()` - 29 edges
9. `LLMProvider` - 24 edges
10. `plot_window()` - 24 edges

## Surprising Connections (you probably didn't know these)
- `ProviderFactory` --uses--> `NvidiaProvider`  [INFERRED]
  services/provider_factory.py → providers/nvidia_provider.py
- `OllamaProvider` --uses--> `OllamaModelInfo`  [INFERRED]
  providers/ollama_provider.py → services/ollama_manager.py
- `ProviderFactory` --uses--> `OllamaProvider`  [INFERRED]
  services/provider_factory.py → providers/ollama_provider.py
- `ProviderFactory` --uses--> `OpenRouterProvider`  [INFERRED]
  services/provider_factory.py → providers/openrouter_provider.py
- `_download_ollama_model()` --uses--> `ProviderFactory`  [INFERRED]
  ui/main_v3.py → services/provider_factory.py

## Import Cycles
- None detected.

## Communities (63 total, 8 thin omitted)

### Community 0 - "GoBoard"
Cohesion: 0.06
Nodes (21): _copy_game_tree(), GameNode, GoBoard, parse_sequence(), load_tk_image(), Load an image as a Tk image, preferring Pillow for broad format support., 依 board_shell 實際尺寸重新縮放外框背景圖片（cover 模式：填滿裁切）。 由 board_shell 的 <Configure>…, 動態生成歷史落子紀錄，不會再因為提子而消失，確保 AI 判斷正確 (+13 more)

### Community 1 - "AI 圍棋老師 / AI Go Teacher"
Cohesion: 0.05
Nodes (44): AI 圍棋老師 / AI Go Teacher, Communication Protocols, Contents, Core Capabilities, Core Modules, Custom Teaching Tones, Development Commands, Download the Executable (Windows) (+36 more)

### Community 2 - "OllamaManager"
Cohesion: 0.12
Nodes (10): OllamaManager, download_task(), emit_complete(), emit_progress(), OllamaModelInfo, Return (models, error), retaining the last good catalog on failure., Read a model without triggering network I/O., Start a streaming REST pull for a local model. (+2 more)

### Community 3 - "ProviderFactory"
Cohesion: 0.13
Nodes (13): ProviderFactory, Return the human-readable display name for a model ID. Falls back to the raw…, Reverse lookup: display name → model ID. Returns None when the display name is…, Return [(display_name, model_id), ...] for UI widgets. The list follows the…, 從 model_id 清單取出 publisher 清單（已排序、去重）。, get_board_context_text(), 安全取得目前 AI 提供商、模型與語言設定。, 回傳目前棋盤局面的文字快照，供 LLM Chat Sandbox 附加為上下文。 (+5 more)

### Community 4 - "Contributing to AI Go Teacher / 為 AI Go Teacher 貢獻"
Cohesion: 0.05
Nodes (38): Acknowledgments, Before Submitting a Bug Report, Before Submitting an Enhancement, Commit Messages, Commit 訊息, Contributing to AI Go Teacher / 為 AI Go Teacher 貢獻, Development Environment Setup, How Do I Submit a Good Bug Report? (+30 more)

### Community 5 - "LLM 提供來源遷移指南 / LLM Provider Migration Guide"
Cohesion: 0.07
Nodes (27): API Key Security, API key 安全性, Automatic Migration of Legacy Settings, Available Alternatives, Frequently Asked Questions, GitHub Models Still Appears After Startup, LLM 提供來源遷移指南 / LLM Provider Migration Guide, OpenRouter Returns HTTP 402 (+19 more)

### Community 6 - "._start_generation"
Cohesion: 0.16
Nodes (4): on_error(), run(), 使用者按下停止：要求 provider 中止串流，並立即收尾。, 回傳 (顯示文字, 送給 LLM 的完整文字)。附件只附在完整文字中。

### Community 7 - "ConfigService"
Cohesion: 0.05
Nodes (27): dataclasses, math, ConfigService, Small wrapper around persisted UI settings., Migrate settings from the removed GitHub Models provider., calculate_area_score(), get_display_komi_from_sgf(), get_katago_komi() (+19 more)

### Community 8 - "nvidia_provider.py"
Cohesion: 0.27
Nodes (9): opencc, get_publisher_from_model_id(), group_models_by_publisher(), 從 model_id 拆出 publisher（第一個 '/' 之前的部分）。 無 '/' 的 model_id 歸類為 "unknown"，確保 UI…, 將 model_id 清單依 publisher 分組，回傳 {publisher: [model_id, ...]}。 保持各 publisher 內…, get_publisher_from_model_id(), group_models_by_publisher(), threading (+1 more)

### Community 9 - "refresh_tab_bar"
Cohesion: 0.09
Nodes (38): apply_theme(), recolor(), _capture_board_snapshot(), _close_tab_silently(), hydrate_active_session(), load_sgf_file(), on_close_tab_click(), on_copy_tab_click() (+30 more)

### Community 10 - "_clear_selected_runtime_data"
Cohesion: 0.20
Nodes (10): _delete_api_key(), delete_nvidia_api_key(), delete_openrouter_api_key(), Delete one application credential, treating a missing credential as success., Delete the NVIDIA API key owned by this application., Delete the OpenRouter API key owned by this application., _clear_selected_runtime_data(), _delete_runtime_path() (+2 more)

### Community 11 - "materialize_bundled_runtime_file"
Cohesion: 0.22
Nodes (12): get_config_path(), get_katago_path(), get_model_path(), hide_path_on_windows(), _load_runtime_manifest(), materialize_bundled_runtime_file(), Copy bundled KataGo runtime files out of PyInstaller's _MEI directory. The…, 安全取得 KataGo 執行檔、設定檔、模型檔路徑與存在狀態。 (+4 more)

### Community 12 - "chat_sandbox.py"
Cohesion: 0.12
Nodes (17): copy, json, pathlib, pil, sys, time, traceback, _insert_inline_markdown() (+9 more)

### Community 13 - "find_service.py"
Cohesion: 0.20
Nodes (13): _branch_label(), find(), FindResult, _iter_all_paths(), parse_coordinate(), 尋找功能（Ctrl+F）的核心搜尋邏輯。 依設計規劃： - 純函式模組，不含任何 UI 依賴，方便單元測試。 - 支援以「手數（數字）」或「座標（GTP…, 依路徑索引從 root 取回節點；路徑失效（樹已變動）時回傳 None。, 解析 GTP 座標輸入（如 'Q16'、'pd'、'q4'）。 回傳 (x, y)，其中 x 欄 0 起、y 由上往下 0 起；無法解析回傳 None。 (+5 more)

### Community 14 - "LLMProvider"
Cohesion: 0.11
Nodes (6): LLMProvider, Return a human-readable display name for the given model ID. Subclasses should…, Return (is_valid, error_message)., Send a raw prompt to the LLM for a plain chat conversation. This is used by the…, Base class for streaming LLM commentary providers., Build the final prompt sent to the model from plain user text plus data.

### Community 16 - "TabManager"
Cohesion: 0.08
Nodes (9): 建立第一個分頁並設為 active。供 main 流程開機時呼叫一次。, 建立新分頁。若已達 MAX_TABS，回傳 None。, 關閉指定分頁；回傳 (success, reason)。 規則： - 至少保留一個分頁。 - 若傳入 index 為 active，自動切到鄰近分頁。, Move one session and preserve which session is active., Restore the most recently closed session at the end of the list., 支援 tab_manager[idx] 取第 idx 個分頁。, 多分頁文件管理器：維護所有 TabSession 並提供 active session 切換。, TabManager (+1 more)

### Community 17 - "MenuBar"
Cohesion: 0.21
Nodes (4): tkinter, MenuBar, Themeable, Tk-only application menu bar. This deliberately does not use native…, A small menu system built from Frames and Buttons. Menu definitions are plain…

### Community 18 - "BranchTreeView"
Cohesion: 0.08
Nodes (12): BranchCanvas, BranchTreeView, assign(), build_branch_section(), get_node_turn_number(), write_node(), is_pass_move(), LLMSelectionDialog (+4 more)

### Community 19 - "version.py"
Cohesion: 0.24
Nodes (12): argparse, Path, re, main(), Application version helpers for AI Go Teacher. Run this file to update every…, Return the numeric tuple used by PyInstaller's VSVersionInfo., _replace_once(), sync_version() (+4 more)

### Community 20 - "show_appearance_settings_dialog"
Cohesion: 0.21
Nodes (9): show_appearance_settings_dialog(), apply_changes(), create_image_row(), browse_image(), use_default(), update_preview(), show_sound_settings_dialog(), create_sound_row() (+1 more)

### Community 21 - "safe_get_system_info"
Cohesion: 0.15
Nodes (16): _format_bytes_as_gb(), _get_cpu_name(), _get_gpu_info(), _get_physical_core_count(), _get_ram_info(), _get_windows_display_version(), 把位元組數轉成 GB 字串；輸入不可用時回傳 Unknown。, 執行 PowerShell 並解析 JSON，失敗時回傳 None。 這裡只用於診斷資訊的 best-effort 查詢，任何錯誤都不能影響主 UI。 (+8 more)

### Community 22 - "I18n"
Cohesion: 0.10
Nodes (19): find_preset_tone(), get_all_tones(), get_tone_description(), get_tone_display_name(), get_tone_prompt(), Single-block LLM prompt templates for AI Go teacher commentary. The application…, Return the preset prompt in the requested UI language., Return the tone if prompt is an untouched preset, otherwise ``None``. (+11 more)

### Community 23 - "OpenRouterProvider"
Cohesion: 0.20
Nodes (3): discover_openrouter_models(), OpenRouterProvider, Return (True, model_ids) or (False, error_message).

### Community 24 - "LLMChatWindow"
Cohesion: 0.09
Nodes (5): LLMChatWindow, 把使用者訊息回填輸入框，並截斷該則之後的所有對話。, 遞迴綁定滾輪事件，讓游標在卡片上也能捲動聊天區。, 輸入框獲得焦點時清除 placeholder。, 輸入框失去焦點時恢復 placeholder。

### Community 25 - "normalize_api_key"
Cohesion: 0.14
Nodes (18): keyring, get_nvidia_api_key(), get_openrouter_api_key(), normalize_api_key(), Trim whitespace and common quote wrappers from API key values., Read NVIDIA API key from keyring first, then environment variables., Store NVIDIA API key in the OS keyring. Does not write to .env., Read OpenRouter API key from keyring first, then environment variables. (+10 more)

### Community 26 - "Security Policy"
Cohesion: 0.10
Nodes (19): Accepted Reports, Declined Reports, In-Scope, Information to Include, Out-of-Scope, Reporting a Vulnerability, Response & Resolution Process, Scope (+11 more)

### Community 27 - "NvidiaProvider"
Cohesion: 0.18
Nodes (4): discover_nim_models(), NvidiaProvider, 動態探索 NIM 可用模型。 回傳 (model_ids, used_fallback, error_message)： -…, 向 NIM 端點 /v1/models 查詢可用模型清單。 成功時回傳 (True, [model_id, ...])；失敗時回傳 (False,…

### Community 28 - "plot_window"
Cohesion: 0.15
Nodes (23): add_full_game_commentary_to_cache(), get_full_game_commentary_from_cache(), plot_window(), apply_chart_mode(), build_full_game_summary_data(), build_summary_prompt(), get_player_from_move(), get_player_name() (+15 more)

### Community 29 - "requirements.txt - Python Dependencies"
Cohesion: 0.29
Nodes (7): requirements.txt - Python Dependencies, httpx HTTP Client, keyring Package, matplotlib Package, ollama Python Package, opencc Chinese Conversion, Pillow (PIL) Package

### Community 30 - "_legacy_show_system_info_dialog"
Cohesion: 0.22
Nodes (6): _create_info_section(), _create_katago_section(), _create_labeled_row(), _legacy_show_system_info_dialog(), 建立診斷資訊視窗中的單列 label/value。, setup_system_info_styles()

### Community 31 - "get_runtime_data_root"
Cohesion: 0.17
Nodes (17): ensure_runtime_dir(), get_executable_dir(), get_katago_runtime_overrides(), get_runtime_data_root(), get_runtime_file_path(), is_frozen_app(), iter_dotenv_paths(), _iter_log_candidates() (+9 more)

### Community 33 - "_show_llm_selection_dialog"
Cohesion: 0.22
Nodes (10): _show_llm_selection_dialog(), bind_ollama_mousewheel(), download_named_ollama_model(), refresh_ollama_models(), task(), render_ollama_models(), add_section(), scroll_ollama_models() (+2 more)

### Community 34 - "show_analysis_log_dialog"
Cohesion: 0.22
Nodes (11): create_dev_menu(), export_diagnostic_report(), _open_folder(), 顯示診斷報告匯出完成訊息與開啟資料夾按鈕。, 匯出診斷報告到 diagnostics/diagnostic_report.txt。, Return Dev menu items for the themeable menu bar., show_analysis_log_dialog(), apply_highlighting() (+3 more)

### Community 35 - "show_system_info_dialog"
Cohesion: 0.22
Nodes (10): Return a safe RAM usage ratio for the dashboard progress meter., Create a theme-aware dashboard card containing labelled values., Show the theme-aware CustomTkinter system diagnostics dashboard., show_system_info_dialog(), close_dialog(), render_dashboard(), _system_info_card(), _system_info_metric() (+2 more)

### Community 36 - "_download_ollama_model"
Cohesion: 0.22
Nodes (9): _confirm_and_download_ollama_model(), _create_ollama_model_row(), on_row_click(), _download_ollama_model(), on_download_complete(), update_progress(), _load_ollama_icon(), 為 Ollama 模型創建一個選擇行。 - 已下載（available）：點擊直接選中 - 雲端（cloud）：點擊直接選中，不顯示下載 -… (+1 more)

### Community 38 - "start_analyzer_async"
Cohesion: 0.22
Nodes (13): get_config_display_name(), get_model_display_name(), set_analysis_controls_state(), start_analyzer_async(), finish_failure(), finish_success(), task(), update_startup_message() (+5 more)

### Community 39 - "main_v3.py"
Cohesion: 0.06
Nodes (35): collections, customtkinter, dotenv, hashlib, itertools, matplotlib, matplotlib_backends_backend_tkagg, matplotlib_figure (+27 more)

### Community 41 - "._refresh_conversation_list"
Cohesion: 0.21
Nodes (3): _select(), on_change(), on_close()

### Community 43 - "build_menu_bar"
Cohesion: 0.12
Nodes (12): build_menu_bar(), toggle_dev(), Refresh a known static teacher prompt without touching LLM output., Refresh controls that expose the continuous-analysis state., rebuild_menu_bar(), refresh_language(), refresh_teacher_static_message(), render_winrate_text() (+4 more)

### Community 44 - "get_active_analysis_settings"
Cohesion: 0.06
Nodes (36): datetime, _analysis_lines(), _gtp(), _move_text(), Compact, factual Go-game context for LLM teaching prompts. This module…, Serialize only the selected mainline and explicitly named snapshots., serialize_board(), serialize_game_context() (+28 more)

### Community 47 - "t"
Cohesion: 0.21
Nodes (16): change_config_path(), change_katago_path(), change_model_path(), create_katago_startup_popup(), update_elapsed(), new_game(), open_feedback_form(), 重新初始化分析器（關閉舊進程，建立新進程） (+8 more)

### Community 48 - "_ask_sgf_link"
Cohesion: 0.20
Nodes (7): _ask_sgf_link(), _fetch_sgf_content_from_url(), on_load_sgf_click_through_link(), download_task(), Load an SGF from a URL, or ask the user for one from the File menu., Fetch SGF bytes into memory and return decoded SGF text., Show a URL input dialog with a real placeholder entry.

### Community 49 - "resource_path"
Cohesion: 0.17
Nodes (11): detect_ollama_installed(), play_move_sound(), Play the sound for a successfully applied board move. Sound playback is…, 檢查系統是否能執行 `ollama --version`，回傳 (installed: bool, version_or_none), 顯示簡單的 Ollama 安裝引導對話框（包含開啟下載頁與重新檢測）。, 彈出儲存 / 不儲存 / 取消 三選一對話框，回傳 'save' / 'discard' / 'cancel'。, resource_path(), _show_close_tab_dialog() (+3 more)

### Community 50 - "update_ui_with_data"
Cohesion: 0.22
Nodes (9): add_to_commentary_cache(), _commentary_cache_key(), get_commentary_from_cache(), on_commentary_generation_complete(), poll_ai(), 【Phase 1】LLM 生成完成後的回呼 — 將完整的解說存儲到快取, 將解說文本新增到快取 (執行緒安全，儲存全部手數), 直接使用記憶體中的數據更新 UI，並將所有分析結果保存到快取以供後續比較使用 (+1 more)

### Community 51 - "KataGoAnalyzer"
Cohesion: 0.13
Nodes (6): KataGoAnalyzer, 將當前棋譜轉換成唯一的字串，作為快取的 Key, 用一致的 KataGo moves 格式生成快取 key，避免 stones/list 格式不一致造成 miss。, Ask KataGo to stop an analysis query immediately, then detach it., Remove already-queued responses belonging to a cancelled query., ScoreAnalyzer

### Community 52 - "create_path_row"
Cohesion: 0.33
Nodes (7): show_settings_dialog(), apply_settings(), create_path_row(), browse_path(), set_entry_value(), show_placeholder(), update_mode()

### Community 53 - "._apply_chat_palette_swap"
Cohesion: 0.29
Nodes (4): recolor(), _remove(), 主題切換：依舊色碼映射到新色碼，重繪整個視窗（含 Text tag 顏色）。, 依主題載入圖示：`_light.png` 用於淺色模式，`_dark.png` 用於深色模式。 若指定主題的圖示不存在，則退回另一主題版本；兩者皆無則設為…

### Community 54 - "show_find_dialog"
Cohesion: 0.29
Nodes (6): 開啟尋找對話框；已存在則聚焦並清空舊結果。, show_find_dialog(), _maybe_show_placeholder(), on_jump(), _show_placeholder(), _sync_query()

### Community 55 - "ImeFontManager"
Cohesion: 0.12
Nodes (13): ctypes, logging, os, _font_height_from_tk_size(), ImeFontManager, LOGFONTW, Synchronize Windows IME composition fonts with focused Tk widgets. Tk delegates…, Remove only this manager's binding. (+5 more)

### Community 56 - "MessageBubble"
Cohesion: 0.32
Nodes (4): MessageBubble, _action_btn(), _action_icon(), 依 wrap 後的 displayline 數調整 Text 高度，消除多餘空白。

### Community 57 - "save_and_apply_settings"
Cohesion: 0.31
Nodes (8): Compatibility callback for components that report transient status., 只更新老師解說區，不改動生成中的快取狀態。, LLM Provider 的串流回呼；累積全文但在回放時不覆蓋既有解說。, render_teacher_ui(), apply_settings(), save_and_apply_settings(), update_status(), update_teacher_ui()

### Community 58 - "task"
Cohesion: 0.25
Nodes (4): refresh_openrouter_model_combo(), refresh_openrouter_models_async(), task(), update_ui()

### Community 59 - "set_winrate_text"
Cohesion: 0.26
Nodes (12): auto_analyze(), is_analyzer_ready(), on_analyze_button_click(), 分析整盤棋並回傳每手的勝率列表 (複用全局 KataGo analyzer，支援取消與進度回報), run_full_game_analysis(), set_winrate_text(), show_analyzer_not_ready(), refresh_nim_models_async() (+4 more)

### Community 60 - "update_ui"
Cohesion: 0.29
Nodes (5): 取得指定 publisher 下的 model_id 清單（保持原始順序）。, 從 model_id 拆出 publisher（供 UI 還原選擇用）。, on_nvidia_publisher_changed(), update_ui(), refresh_nvidia_model_combo()

### Community 61 - "_build_diagnostic_report_text"
Cohesion: 0.40
Nodes (5): _build_diagnostic_report_text(), _get_newest_log_file(), 讀取最新 log 的最後 max_lines 行；沒有 log 時回傳提示文字。, 組合 diagnostic_report.txt 的完整內容。, _read_recent_log_lines()

## Knowledge Gaps
- **102 isolated node(s):** `Table of Contents`, `I Have a Question`, `Before Submitting a Bug Report`, `How Do I Submit a Good Bug Report?`, `Before Submitting an Enhancement` (+97 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 417 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMChatWindow` connect `LLMChatWindow` to `ProviderFactory`, `._start_generation`, `main_v3.py`, `._active_conversation`, `._refresh_conversation_list`, `._tr`, `chat_sandbox.py`, `.__init__`, `._build_ui`, `._apply_chat_palette_swap`?**
  _High betweenness centrality (0.152) - this node is a cross-community bridge._
- **Why does `t()` connect `t` to `GoBoard`, `ProviderFactory`, `ConfigService`, `refresh_tab_bar`, `_clear_selected_runtime_data`, `TabManager`, `BranchTreeView`, `show_appearance_settings_dialog`, `I18n`, `normalize_api_key`, `plot_window`, `_legacy_show_system_info_dialog`, `get_runtime_data_root`, `_show_llm_selection_dialog`, `show_analysis_log_dialog`, `show_system_info_dialog`, `_download_ollama_model`, `start_analyzer_async`, `main_v3.py`, `build_menu_bar`, `get_active_analysis_settings`, `_ask_sgf_link`, `resource_path`, `create_path_row`, `show_find_dialog`, `save_and_apply_settings`, `task`, `set_winrate_text`, `update_ui`?**
  _High betweenness centrality (0.099) - this node is a cross-community bridge._
- **Why does `GoBoard` connect `GoBoard` to `BranchTreeView`, `main_v3.py`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `t()` (e.g. with `set_llm_tone()` and `show_chat_sandbox()`) actually correct?**
  _`t()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `build_menu_bar()` (e.g. with `palette()` and `toggle_branch_panel()`) actually correct?**
  _`build_menu_bar()` has 27 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Table of Contents`, `I Have a Question`, `Before Submitting a Bug Report` to the rest of the system?**
  _102 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `GoBoard` be split into smaller, more focused modules?**
  _Cohesion score 0.057703081232493 - nodes in this community are weakly interconnected._