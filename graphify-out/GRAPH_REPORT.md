# Graph Report - AIGoTeacher  (2026-11-03)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1316 nodes · 2727 edges · 84 communities (70 shown, 14 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 162 edges (avg confidence: 0.86)
- Token cost: 6,403 input · 966 output

## Graph Freshness
- Built from commit: `d11595eb`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Board Interaction Helpers
- Project Features Overview
- Ollama Provider Integration
- LLM Provider Factory
- Contribution Guidelines
- Migration and FAQ Guide
- Chat Message Handling
- Configuration Service
- Provider Model Grouping
- Tab and Session Management
- Credential and Data Cleanup
- Runtime Environment Utilities
- Game Tree Navigation
- Game Tree Search Service
- LLM Provider Base Class
- Chat Bubble UI Component
- Multi-Tab Session Manager
- Menu Bar UI
- Branch Tree Visualization
- Version Management Utilities
- Developer Contribution Guide
- System Hardware Diagnostics
- AI Teacher Tone Templates
- OpenRouter Provider Integration
- LLM Chat Interface
- API Key Security Service
- Security Policy Documentation
- NVIDIA NIM Provider
- Game Analysis and Summary
- Python Package Requirements
- Diagnostic View Layout
- Developer Setup Guide (ZH)
- GUI Screenshots
- KataGo Model Downloader
- System Configuration Dialogs
- System Info Dashboard
- Full Game Analysis Controls
- PyInstaller Version Info
- Score Estimation Logic
- External Library Dependencies
- Conversation Editing Logic
- Conversation History Management
- Menu Bar Commands
- SGF Metadata Editor
- Appearance and Sound Settings
- Chat Input Configuration
- Model Catalog Synchronization
- SGF URL Loader
- Ollama Model Download UI
- Commentary Cache Management
- Go Game Context Serialization
- Settings Dialog Management
- Theme and Icon Management
- Find Dialog UI
- IME and Font Management
- KataGo Model Browser UI
- Theme Application Logic
- KataGo Runtime Path Resolution
- Async Task UI Updates
- Markdown Rendering Engine
- Game Node Logic
- Conversation Persistence
- Go Board Rendering
- Ollama Installation Helper
- Board Background Rendering
- Tab Closing Workflow
- Technical Architecture Overview
- Technical Architecture (ZH)
- Diagnostic Report Generation
- KataGo Model Manager
- KataGo Online Model Window
- Installation Guide
- Installation Guide (ZH)
- SGF Parsing and Export
- Core Capabilities Overview
- Development and Engine Commands
- Development Commands (ZH)
- LLM and API Setup (ZH)
- Move History Tracking
- Session Type Definitions

## God Nodes (most connected - your core abstractions)
1. `t()` - 123 edges
2. `LLMChatWindow` - 86 edges
3. `GoBoard` - 82 edges
4. `ConfigService` - 44 edges
5. `build_menu_bar()` - 38 edges
6. `_show_llm_selection_dialog()` - 35 edges
7. `KataGoModelBrowserFrame` - 32 edges
8. `resource_path()` - 32 edges
9. `ProviderFactory` - 31 edges
10. `LLMProvider` - 24 edges

## Surprising Connections (you probably didn't know these)
- `ProviderFactory` --uses--> `OllamaProvider`  [INFERRED]
  services/provider_factory.py → providers/ollama_provider.py
- `ProviderFactory` --uses--> `OpenRouterProvider`  [INFERRED]
  services/provider_factory.py → providers/openrouter_provider.py
- `ProviderFactory` --uses--> `NvidiaProvider`  [INFERRED]
  services/provider_factory.py → providers/nvidia_provider.py
- `_download_ollama_model()` --uses--> `ProviderFactory`  [INFERRED]
  ui/main_v3.py → services/provider_factory.py
- `plot_window()` --uses--> `ProviderFactory`  [INFERRED]
  ui/main_v3.py → services/provider_factory.py

## Import Cycles
- None detected.

## Communities (84 total, 14 thin omitted)

### Community 0 - "Board Interaction Helpers"
Cohesion: 0.13
Nodes (3): Return 1-based move index where the current branch starts, or None on main line., 點目時暫時隱藏推薦手；結束後依據最後一次分析結果恢復顯示。, Return whether applying a legal move removes any opponent stones.

### Community 1 - "Project Features Overview"
Cohesion: 0.14
Nodes (14): AI 圍棋老師 / AI Go Teacher, Contents, Custom Teaching Tones, i18n, License, LLM Integration, LLM 提供商支援, Python Dependencies (+6 more)

### Community 2 - "Ollama Provider Integration"
Cohesion: 0.07
Nodes (12): OllamaProvider, get_ollama_manager(), OllamaManager, download_task(), emit_complete(), emit_progress(), OllamaModelInfo, Return (models, error), retaining the last good catalog on failure. (+4 more)

### Community 3 - "LLM Provider Factory"
Cohesion: 0.06
Nodes (40): ProviderFactory, Return the human-readable display name for a model ID. Falls back to the raw…, Reverse lookup: display name → model ID. Returns None when the display name is…, Return [(display_name, model_id), ...] for UI widgets. The list follows the…, 向 NIM 端點探索可用模型；失敗時回傳空清單與錯誤。 回傳 (model_ids, used_fallback, error_message)： -…, 從 model_id 清單取出 publisher 清單（已排序、去重）。, 取得指定 publisher 下的 model_id 清單（保持原始順序）。, 從 model_id 拆出 publisher（供 UI 還原選擇用）。 (+32 more)

### Community 4 - "Contribution Guidelines"
Cohesion: 0.13
Nodes (14): Acknowledgments, Commit Messages, Commit 訊息, Contributing to AI Go Teacher / 為 AI Go Teacher 貢獻, I Have a Question, Style Guides, Table of Contents, 我有問題 (+6 more)

### Community 5 - "Migration and FAQ Guide"
Cohesion: 0.07
Nodes (27): API Key Security, API key 安全性, Automatic Migration of Legacy Settings, Available Alternatives, Frequently Asked Questions, GitHub Models Still Appears After Startup, LLM 提供來源遷移指南 / LLM Provider Migration Guide, OpenRouter Returns HTTP 402 (+19 more)

### Community 6 - "Chat Message Handling"
Cohesion: 0.16
Nodes (4): on_error(), run(), 使用者按下停止：要求 provider 中止串流，並立即收尾。, 回傳 (顯示文字, 送給 LLM 的完整文字)。附件只附在完整文字中。

### Community 7 - "Configuration Service"
Cohesion: 0.07
Nodes (13): ConfigService, Small wrapper around persisted UI settings., Migrate settings from the removed GitHub Models provider., get_display_komi_from_sgf(), normalize_rule_id(), Convert an SGF KM value to the application's displayed komi unit., validate_komi(), detect_system_theme() (+5 more)

### Community 8 - "Provider Model Grouping"
Cohesion: 0.26
Nodes (10): opencc, get_publisher_from_model_id(), group_models_by_publisher(), 從 model_id 拆出 publisher（第一個 '/' 之前的部分）。 無 '/' 的 model_id 歸類為 "unknown"，確保 UI…, 將 model_id 清單依 publisher 分組，回傳 {publisher: [model_id, ...]}。 保持各 publisher 內…, get_publisher_from_model_id(), group_models_by_publisher(), threading (+2 more)

### Community 9 - "Tab and Session Management"
Cohesion: 0.12
Nodes (28): _capture_board_snapshot(), _close_tab_silently(), _copy_game_tree(), hydrate_active_session(), load_sgf_file(), on_copy_tab_click(), _on_find_tab_changed(), on_load_sgf_click() (+20 more)

### Community 10 - "Credential and Data Cleanup"
Cohesion: 0.20
Nodes (10): _delete_api_key(), delete_nvidia_api_key(), delete_openrouter_api_key(), Delete one application credential, treating a missing credential as success., Delete the NVIDIA API key owned by this application., Delete the OpenRouter API key owned by this application., _clear_selected_runtime_data(), _delete_runtime_path() (+2 more)

### Community 11 - "Runtime Environment Utilities"
Cohesion: 0.14
Nodes (21): create_dev_menu(), ensure_runtime_dir(), export_diagnostic_report(), get_executable_dir(), get_katago_runtime_overrides(), get_runtime_data_root(), get_runtime_file_path(), is_frozen_app() (+13 more)

### Community 12 - "Game Tree Navigation"
Cohesion: 0.15
Nodes (7): is_markup_node(), Return whether a node stores board annotations instead of a move., Capture an independent tree state for per-tab edit undo/redo., Move through the existing variation tree without editing it., 切換同一手棋的不同變化圖 (direction: 1 或 -1), 跳轉到樹上的任意節點，並回填各層 active_child_idx。, 【修復】回放模式下，從快取顯示當前手數的解說；無快取則清空。 此方法統一處理 undo / redo / switch_branch /…

### Community 13 - "Game Tree Search Service"
Cohesion: 0.20
Nodes (13): _branch_label(), find(), FindResult, _iter_all_paths(), parse_coordinate(), 尋找功能（Ctrl+F）的核心搜尋邏輯。 依設計規劃： - 純函式模組，不含任何 UI 依賴，方便單元測試。 - 支援以「手數（數字）」或「座標（GTP…, 依路徑索引從 root 取回節點；路徑失效（樹已變動）時回傳 None。, 解析 GTP 座標輸入（如 'Q16'、'pd'、'q4'）。 回傳 (x, y)，其中 x 欄 0 起、y 由上往下 0 起；無法解析回傳 None。 (+5 more)

### Community 14 - "LLM Provider Base Class"
Cohesion: 0.11
Nodes (6): LLMProvider, Return a human-readable display name for the given model ID. Subclasses should…, Return (is_valid, error_message)., Send a raw prompt to the LLM for a plain chat conversation. This is used by the…, Base class for streaming LLM commentary providers., Build the final prompt sent to the model from plain user text plus data.

### Community 15 - "Chat Bubble UI Component"
Cohesion: 0.32
Nodes (4): MessageBubble, _action_btn(), _action_icon(), 依 wrap 後的 displayline 數調整 Text 高度，消除多餘空白。

### Community 16 - "Multi-Tab Session Manager"
Cohesion: 0.08
Nodes (9): 多分頁文件管理器：維護所有 TabSession 並提供 active session 切換。, 建立第一個分頁並設為 active。供 main 流程開機時呼叫一次。, 建立新分頁。若已達 MAX_TABS，回傳 None。, 關閉指定分頁；回傳 (success, reason)。 規則： - 至少保留一個分頁。 - 若傳入 index 為 active，自動切到鄰近分頁。, Move one session and preserve which session is active., Restore the most recently closed session at the end of the list., 支援 tab_manager[idx] 取第 idx 個分頁。, TabManager (+1 more)

### Community 18 - "Branch Tree Visualization"
Cohesion: 0.07
Nodes (13): BranchCanvas, BranchTreeView, assign(), build_branch_section(), is_pass_move(), LLMSelectionDialog, load_ctk_image(), MarkupToolbar (+5 more)

### Community 19 - "Version Management Utilities"
Cohesion: 0.24
Nodes (12): argparse, re, main(), Path, Application version helpers for AI Go Teacher. Run this file to update every…, Return the numeric tuple used by PyInstaller's VSVersionInfo., _replace_once(), sync_version() (+4 more)

### Community 20 - "Developer Contribution Guide"
Cohesion: 0.17
Nodes (12): Before Submitting a Bug Report, Before Submitting an Enhancement, Development Environment Setup, How Do I Submit a Good Bug Report?, How Do I Submit a Good Enhancement Proposal?, I Want to Contribute, IDE Configuration, Improving the Documentation (+4 more)

### Community 21 - "System Hardware Diagnostics"
Cohesion: 0.15
Nodes (16): _format_bytes_as_gb(), _get_cpu_name(), _get_gpu_info(), _get_physical_core_count(), _get_ram_info(), _get_windows_display_version(), 把位元組數轉成 GB 字串；輸入不可用時回傳 Unknown。, 執行 PowerShell 並解析 JSON，失敗時回傳 None。 這裡只用於診斷資訊的 best-effort 查詢，任何錯誤都不能影響主 UI。 (+8 more)

### Community 22 - "AI Teacher Tone Templates"
Cohesion: 0.10
Nodes (18): find_preset_tone(), get_all_tones(), get_tone_description(), get_tone_display_name(), get_tone_prompt(), Single-block LLM prompt templates for AI Go teacher commentary. The application…, Return the preset prompt in the requested UI language., Return the tone if prompt is an untouched preset, otherwise ``None``. (+10 more)

### Community 23 - "OpenRouter Provider Integration"
Cohesion: 0.16
Nodes (5): discover_openrouter_models(), OpenRouterProvider, Return (True, model_ids) or (False, error_message)., get_openrouter_api_key(), Read OpenRouter API key from keyring first, then environment variables.

### Community 24 - "LLM Chat Interface"
Cohesion: 0.09
Nodes (5): LLMChatWindow, 把使用者訊息回填輸入框，並截斷該則之後的所有對話。, 遞迴綁定滾輪事件，讓游標在卡片上也能捲動聊天區。, 輸入框獲得焦點時清除 placeholder。, 輸入框失去焦點時恢復 placeholder。

### Community 25 - "API Key Security Service"
Cohesion: 0.14
Nodes (18): keyring, discover_nim_models(), 向 NIM 端點 /v1/models 查詢可用模型清單。 成功時回傳 (True, [model_id, ...])；失敗時回傳 (False,…, get_nvidia_api_key(), normalize_api_key(), Trim whitespace and common quote wrappers from API key values., Read NVIDIA API key from keyring first, then environment variables., Store NVIDIA API key in the OS keyring. Does not write to .env. (+10 more)

### Community 26 - "Security Policy Documentation"
Cohesion: 0.10
Nodes (19): Accepted Reports, Declined Reports, In-Scope, Information to Include, Out-of-Scope, Reporting a Vulnerability, Response & Resolution Process, Scope (+11 more)

### Community 28 - "Game Analysis and Summary"
Cohesion: 0.15
Nodes (23): add_full_game_commentary_to_cache(), get_full_game_commentary_from_cache(), plot_window(), apply_chart_mode(), build_full_game_summary_data(), build_summary_prompt(), get_player_from_move(), get_player_name() (+15 more)

### Community 29 - "Python Package Requirements"
Cohesion: 0.29
Nodes (7): requirements.txt - Python Dependencies, httpx HTTP Client, keyring Package, matplotlib Package, ollama Python Package, opencc Chinese Conversion, Pillow (PIL) Package

### Community 30 - "Diagnostic View Layout"
Cohesion: 0.22
Nodes (6): _create_info_section(), _create_katago_section(), _create_labeled_row(), _legacy_show_system_info_dialog(), 建立診斷資訊視窗中的單列 label/value。, setup_system_info_styles()

### Community 31 - "Developer Setup Guide (ZH)"
Cohesion: 0.17
Nodes (12): IDE 設定, 回報錯誤（Bug）, 如何提交一份好的 Bug 回報？, 如何提交一份好的功能建議？, 我想貢獻, 提交 Bug 回報前, 提交功能建議前, 提出功能建議 (+4 more)

### Community 33 - "KataGo Model Downloader"
Cohesion: 0.11
Nodes (23): concurrent_futures, customtkinter, gzip, hashlib, os, pathlib, requests, RuntimeError (+15 more)

### Community 34 - "System Configuration Dialogs"
Cohesion: 0.19
Nodes (17): change_config_path(), change_katago_path(), change_model_path(), create_katago_startup_popup(), update_elapsed(), open_feedback_form(), _open_folder(), 重新初始化分析器（關閉舊進程，建立新進程） (+9 more)

### Community 35 - "System Info Dashboard"
Cohesion: 0.22
Nodes (10): Return a safe RAM usage ratio for the dashboard progress meter., Create a theme-aware dashboard card containing labelled values., Show the theme-aware CustomTkinter system diagnostics dashboard., show_system_info_dialog(), close_dialog(), render_dashboard(), _system_info_card(), _system_info_metric() (+2 more)

### Community 36 - "Full Game Analysis Controls"
Cohesion: 0.17
Nodes (15): auto_analyze(), toggle_dev(), is_analyzer_ready(), on_analyze_button_click(), Refresh a known static teacher prompt without touching LLM output., 分析整盤棋並回傳每手的勝率列表 (複用全局 KataGo analyzer，支援取消與進度回報), Refresh controls that expose the continuous-analysis state., rebuild_menu_bar() (+7 more)

### Community 38 - "Score Estimation Logic"
Cohesion: 0.17
Nodes (14): calculate_area_score(), Calculate area scores with dead stones awarded to the opponent., count_captured_prisoners(), _handle_score_estimate_result(), is_markup_node_active(), on_close_score_estimate_click(), on_score_estimate_click(), 依歷史落子順序重播棋局，計算雙方已提取的對方棋子數。 回傳 {"black": 黑方提掉的白子數, "white": 白方提掉的黑子數}。 (+6 more)

### Community 39 - "External Library Dependencies"
Cohesion: 0.06
Nodes (32): collections, dotenv, itertools, matplotlib, matplotlib_backends_backend_tkagg, matplotlib_figure, matplotlib_pyplot, platform (+24 more)

### Community 41 - "Conversation History Management"
Cohesion: 0.21
Nodes (3): _select(), on_change(), on_close()

### Community 43 - "Menu Bar Commands"
Cohesion: 0.13
Nodes (8): build_menu_bar(), on_closing(), Show a guarded, itemized dialog for deleting application runtime data., save_game_as_json(), save_game_as_json_dialog(), show_about(), show_delete_data_dialog(), confirm_and_delete()

### Community 44 - "SGF Metadata Editor"
Cohesion: 0.16
Nodes (14): datetime, get_game_info(), Helpers for editable SGF game-information properties., Return a normalized date or raise ValueError for a non-SGF date., Read the editable game-info fields without exposing the metadata dict., Update editable fields in place while preserving every other property., update_game_info(), validate_game_date() (+6 more)

### Community 45 - "Appearance and Sound Settings"
Cohesion: 0.21
Nodes (9): show_appearance_settings_dialog(), apply_changes(), create_image_row(), browse_image(), use_default(), update_preview(), show_sound_settings_dialog(), create_sound_row() (+1 more)

### Community 47 - "Model Catalog Synchronization"
Cohesion: 0.24
Nodes (4): KataGoModel, Fetch every paginated model page for local search and filtering., Refresh the catalog while reusing the local cache. Page 1 is always the only…, Atomically persist catalog progress; a partial write never becomes cache.

### Community 48 - "SGF URL Loader"
Cohesion: 0.20
Nodes (7): _ask_sgf_link(), _fetch_sgf_content_from_url(), on_load_sgf_click_through_link(), download_task(), Load an SGF from a URL, or ask the user for one from the File menu., Fetch SGF bytes into memory and return decoded SGF text., Show a URL input dialog with a real placeholder entry.

### Community 49 - "Ollama Model Download UI"
Cohesion: 0.20
Nodes (10): _confirm_and_download_ollama_model(), _create_ollama_model_row(), on_row_click(), _download_ollama_model(), on_download_complete(), update_progress(), _load_ollama_icon(), 為 Ollama 模型創建一個選擇行。 - 已下載（available）：點擊直接選中 - 雲端（cloud）：點擊直接選中，不顯示下載 -… (+2 more)

### Community 50 - "Commentary Cache Management"
Cohesion: 0.12
Nodes (19): add_to_commentary_cache(), _build_manual_teacher_event(), _commentary_cache_key(), get_commentary_from_cache(), _get_valid_teacher_analysis(), invalidate_teacher_analysis(), on_commentary_generation_complete(), on_teacher_generate_click() (+11 more)

### Community 51 - "Go Game Context Serialization"
Cohesion: 0.05
Nodes (31): dataclasses, math, _analysis_lines(), _gtp(), _move_text(), Compact, factual Go-game context for LLM teaching prompts. This module…, Serialize only the selected mainline and explicitly named snapshots., serialize_board() (+23 more)

### Community 52 - "Settings Dialog Management"
Cohesion: 0.33
Nodes (7): show_settings_dialog(), apply_settings(), create_path_row(), browse_path(), set_entry_value(), show_placeholder(), update_mode()

### Community 53 - "Theme and Icon Management"
Cohesion: 0.29
Nodes (4): recolor(), _remove(), 主題切換：依舊色碼映射到新色碼，重繪整個視窗（含 Text tag 顏色）。, 依主題載入圖示：`_light.png` 用於淺色模式，`_dark.png` 用於深色模式。 若指定主題的圖示不存在，則退回另一主題版本；兩者皆無則設為…

### Community 54 - "Find Dialog UI"
Cohesion: 0.29
Nodes (6): 開啟尋找對話框；已存在則聚焦並清空舊結果。, show_find_dialog(), _maybe_show_placeholder(), on_jump(), _show_placeholder(), _sync_query()

### Community 55 - "IME and Font Management"
Cohesion: 0.12
Nodes (12): ctypes, logging, _font_height_from_tk_size(), ImeFontManager, LOGFONTW, Synchronize Windows IME composition fonts with focused Tk widgets. Tk delegates…, Remove only this manager's binding., Apply the current focused widget's font to its IME context. (+4 more)

### Community 56 - "KataGo Model Browser UI"
Cohesion: 0.13
Nodes (4): Exception, KataGoModelBrowserFrame, Path, Browse, download, and apply KataGo neural-network models.

### Community 57 - "Theme Application Logic"
Cohesion: 0.33
Nodes (6): apply_theme(), recolor(), _load_teacher_generate_images(), Apply a configured theme to existing widgets without restarting., Expose semantic theme tokens to legacy drawing code in this module., _set_theme_palette()

### Community 58 - "KataGo Runtime Path Resolution"
Cohesion: 0.15
Nodes (15): migrate_mislabeled_text_model(), Repair an older download incorrectly saved with a .bin.gz suffix., get_config_path(), get_katago_path(), get_model_path(), hide_path_on_windows(), _load_runtime_manifest(), materialize_bundled_runtime_file() (+7 more)

### Community 59 - "Async Task UI Updates"
Cohesion: 0.16
Nodes (18): get_config_display_name(), get_model_display_name(), set_analysis_controls_state(), refresh_nim_models_async(), show_winrate_chart(), on_cancel(), task(), update_progress() (+10 more)

### Community 60 - "Markdown Rendering Engine"
Cohesion: 0.13
Nodes (16): copy, json, pil, sys, time, _insert_inline_markdown(), 主題切換時由主程式呼叫：重繪所有開著的聊天視窗。, 把單行文字插入 Text widget，支援 **粗體**、*斜體*、`行內程式碼`。 (+8 more)

### Community 61 - "Game Node Logic"
Cohesion: 0.14
Nodes (9): GameNode, new_game(), play_move_sound(), Play the sound for a successfully applied board move. Sound playback is…, Append a pass as a real game-tree node without changing the board., 修正：提子只清空視覺棋盤(board)，絕不能刪除歷史紀錄(stones), 讀取 SGF 並正確建立分支樹狀結構，同時恢復註解到快取【Phase 3】修正版本, Parse SGF text directly without creating a local SGF file. (+1 more)

### Community 63 - "Go Board Rendering"
Cohesion: 0.15
Nodes (4): GoBoard, point_from_key(), Apply one annotation and keep consecutive annotations in one node., Remove every annotation at one coordinate.

### Community 64 - "Ollama Installation Helper"
Cohesion: 0.20
Nodes (10): detect_ollama_installed(), _load_markup_labels(), 在 Windows 上抑制子進程彈出的主控台視窗。 隱藏終端機 (windowed) 模式下，子進程預設會繼承一個可見的主控台， 即使…, 檢查系統是否能執行 `ollama --version`，回傳 (installed: bool, version_or_none), 顯示簡單的 Ollama 安裝引導對話框（包含開啟下載頁與重新檢測）。, resource_path(), update_ollama_install_status_label(), show_ollama_install_dialog() (+2 more)

### Community 65 - "Board Background Rendering"
Cohesion: 0.29
Nodes (3): load_tk_image(), Load an image as a Tk image, preferring Pillow for broad format support., 依 board_shell 實際尺寸重新縮放外框背景圖片（cover 模式：填滿裁切）。 由 board_shell 的 <Configure>…

### Community 66 - "Tab Closing Workflow"
Cohesion: 0.25
Nodes (8): on_close_tab_click(), 關閉分頁：dirty 時彈出 三選一（儲存 / 不儲存 / 取消）。 為了在關閉流程內支援 "儲存" 動作，會先暫時把這個分頁切為 active， 讓既有的…, 彈出儲存 / 不儲存 / 取消 三選一對話框，回傳 'save' / 'discard' / 'cancel'。, save_game_as_sgf(), save_game_as_sgf_dialog(), _show_close_tab_dialog(), _show_tab_options_menu(), _tab_options_button()

### Community 68 - "Technical Architecture Overview"
Cohesion: 0.40
Nodes (5): Communication Protocols, Core Modules, Frontend and Application Layer, Go Engine, Technical Architecture

### Community 71 - "Technical Architecture (ZH)"
Cohesion: 0.40
Nodes (5): 前端與應用程式層, 圍棋引擎, 技術架構, 核心模組, 通訊協定

### Community 72 - "Diagnostic Report Generation"
Cohesion: 0.40
Nodes (5): _build_diagnostic_report_text(), _get_newest_log_file(), 讀取最新 log 的最後 max_lines 行；沒有 log 時回傳提示文字。, 組合 diagnostic_report.txt 的完整內容。, _read_recent_log_lines()

### Community 73 - "KataGo Model Manager"
Cohesion: 0.18
Nodes (9): Any, ProgressCallback, KataGoModelFormatError, KataGoModelManager, Path, Fetch and safely download models from katagotraining.org., Load the last catalog without contacting the network. A damaged or old cache is…, Raised when the API response is missing required model fields. (+1 more)

### Community 74 - "KataGo Online Model Window"
Cohesion: 0.25
Nodes (6): KataGoModelBrowserWindow, Window wrapper for the online model browser frame., resource_path(), Open the CustomTkinter KataGo Training API model browser., show_katago_online_models_dialog(), apply_model()

### Community 75 - "Installation Guide"
Cohesion: 0.50
Nodes (4): Download the Executable (Windows), Installation Steps, Prerequisites, Quick Start

### Community 76 - "Installation Guide (ZH)"
Cohesion: 0.50
Nodes (4): 下載執行檔（Windows）, 前置需求, 安裝步驟, 快速開始

### Community 78 - "Core Capabilities Overview"
Cohesion: 0.67
Nodes (3): Core Capabilities, Features, Supported LLM Providers

### Community 79 - "Development and Engine Commands"
Cohesion: 0.67
Nodes (3): Development Commands, KataGo Engine Commands, Python Commands

### Community 80 - "Development Commands (ZH)"
Cohesion: 0.67
Nodes (3): KataGo 引擎指令, Python 指令, 開發指令

### Community 81 - "LLM and API Setup (ZH)"
Cohesion: 0.67
Nodes (3): LLM 整合, 自訂教學語氣, 設定 API 金鑰

## Knowledge Gaps
- **102 isolated node(s):** `Contents`, `Custom Teaching Tones`, `i18n`, `License`, `LLM 提供商支援` (+97 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 460 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMChatWindow` connect `LLM Chat Interface` to `LLM Provider Factory`, `Chat Message Handling`, `External Library Dependencies`, `Conversation Editing Logic`, `Conversation History Management`, `Chat Context Menus`, `Chat Input Configuration`, `Theme and Icon Management`, `Markdown Rendering Engine`, `Conversation Persistence`?**
  _High betweenness centrality (0.132) - this node is a cross-community bridge._
- **Why does `GoBoard` connect `Go Board Rendering` to `Board Interaction Helpers`, `Board Background Rendering`, `External Library Dependencies`, `Game Tree Navigation`, `SGF Parsing and Export`, `Move History Tracking`, `Go Game Context Serialization`, `Game Node Logic`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Why does `t()` connect `System Configuration Dialogs` to `LLM Provider Factory`, `Tab and Session Management`, `Credential and Data Cleanup`, `Runtime Environment Utilities`, `Multi-Tab Session Manager`, `Branch Tree Visualization`, `AI Teacher Tone Templates`, `API Key Security Service`, `Game Analysis and Summary`, `Diagnostic View Layout`, `System Info Dashboard`, `Full Game Analysis Controls`, `Score Estimation Logic`, `External Library Dependencies`, `Menu Bar Commands`, `SGF Metadata Editor`, `Appearance and Sound Settings`, `SGF URL Loader`, `Ollama Model Download UI`, `Commentary Cache Management`, `Go Game Context Serialization`, `Settings Dialog Management`, `Find Dialog UI`, `Async Task UI Updates`, `Game Node Logic`, `Ollama Installation Helper`, `Tab Closing Workflow`, `KataGo Online Model Window`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `t()` (e.g. with `set_llm_tone()` and `show_chat_sandbox()`) actually correct?**
  _`t()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `build_menu_bar()` (e.g. with `palette()` and `toggle_branch_panel()`) actually correct?**
  _`build_menu_bar()` has 28 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Contents`, `Custom Teaching Tones`, `i18n` to the rest of the system?**
  _102 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Board Interaction Helpers` be split into smaller, more focused modules?**
  _Cohesion score 0.1341991341991342 - nodes in this community are weakly interconnected._