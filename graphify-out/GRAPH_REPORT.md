# Graph Report - AIGoTeacher  (2026-10-23)

## Corpus Check
- 36 files · ~71,079 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: .gz 2, .spec 1, (none) 1)

## Summary
- 1282 nodes · 2645 edges · 91 communities (76 shown, 15 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 161 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f580d705`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- GoBoard
- AI 圍棋老師 / AI Go Teacher
- OllamaProvider
- ProviderFactory
- Contributing to AI Go Teacher / 為 AI Go Teacher 貢獻
- LLM 提供來源遷移指南 / LLM Provider Migration Guide
- ._start_generation
- ConfigService
- nvidia_provider.py
- refresh_tab_bar
- _clear_selected_runtime_data
- get_runtime_data_root
- .on_state_change
- find_service.py
- LLMProvider
- chat_sandbox.py
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
- rules.py
- GUI Screenshot
- katago_model_manager.py
- show_analysis_log_dialog
- show_system_info_dialog
- resource_path
- version_info.txt - PyInstaller VSVersionInfo
- _handle_score_estimate_result
- main_v3.py
- ._active_conversation
- ._refresh_conversation_list
- build_menu_bar
- show_game_info_dialog
- .__init__
- ._build_ui
- t
- _ask_sgf_link
- show_ollama_install_dialog
- update_ui_with_data
- KataGoAnalyzer
- create_path_row
- ._apply_chat_palette_swap
- show_find_dialog
- ImeFontManager
- KataGoModelBrowserFrame
- _show_llm_selection_dialog
- materialize_bundled_runtime_file
- start_analyzer_async
- config_service.py
- .apply_markup
- I Want to Contribute
- GameNode
- .refresh_display
- .__init__
- 我想貢獻
- serialize_game_context
- _build_diagnostic_report_text
- save_and_apply_settings
- KataGoModelManager
- show_katago_online_models_dialog
- get_active_analysis_settings
- task
- show_first_run_onboarding_dialog
- refresh_language
- KataGoModelFormatError
- update_ui
- Technical Architecture
- 技術架構
- Quick Start
- 快速開始
- .__init__
- Features
- Development Commands
- 開發指令
- LLM 整合
- .discover_nim_models

## God Nodes (most connected - your core abstractions)
1. `t()` - 122 edges
2. `LLMChatWindow` - 86 edges
3. `GoBoard` - 82 edges
4. `ConfigService` - 44 edges
5. `build_menu_bar()` - 38 edges
6. `_show_llm_selection_dialog()` - 35 edges
7. `ProviderFactory` - 31 edges
8. `resource_path()` - 31 edges
9. `KataGoModelBrowserFrame` - 28 edges
10. `LLMProvider` - 24 edges

## Surprising Connections (you probably didn't know these)
- `ProviderFactory` --uses--> `NvidiaProvider`  [INFERRED]
  services/provider_factory.py → providers/nvidia_provider.py
- `ProviderFactory` --uses--> `OllamaProvider`  [INFERRED]
  services/provider_factory.py → providers/ollama_provider.py
- `ProviderFactory` --uses--> `OpenRouterProvider`  [INFERRED]
  services/provider_factory.py → providers/openrouter_provider.py
- `KataGoModelBrowserFrame` --uses--> `KataGoModel`  [INFERRED]
  ui/katago_model_browser.py → services/katago_model_manager.py
- `show_katago_online_models_dialog()` --uses--> `KataGoModel`  [INFERRED]
  ui/main_v3.py → services/katago_model_manager.py

## Import Cycles
- None detected.

## Communities (91 total, 15 thin omitted)

### Community 0 - "GoBoard"
Cohesion: 0.12
Nodes (5): GoBoard, 動態生成歷史落子紀錄，不會再因為提子而消失，確保 AI 判斷正確, Return 1-based move index where the current branch starts, or None on main line., 點目時暫時隱藏推薦手；結束後依據最後一次分析結果恢復顯示。, Return whether applying a legal move removes any opponent stones.

### Community 1 - "AI 圍棋老師 / AI Go Teacher"
Cohesion: 0.14
Nodes (14): AI 圍棋老師 / AI Go Teacher, Contents, Custom Teaching Tones, i18n, License, LLM Integration, LLM 提供商支援, Python Dependencies (+6 more)

### Community 2 - "OllamaProvider"
Cohesion: 0.07
Nodes (12): OllamaProvider, get_ollama_manager(), OllamaManager, download_task(), emit_complete(), emit_progress(), OllamaModelInfo, Return (models, error), retaining the last good catalog on failure. (+4 more)

### Community 3 - "ProviderFactory"
Cohesion: 0.15
Nodes (11): ProviderFactory, Reverse lookup: display name → model ID. Returns None when the display name is…, Return [(display_name, model_id), ...] for UI widgets. The list follows the…, 從 model_id 清單取出 publisher 清單（已排序、去重）。, get_board_context_text(), 安全取得目前 AI 提供商、模型與語言設定。, 回傳目前棋盤局面的文字快照，供 LLM Chat Sandbox 附加為上下文。, Open the LLM Chat Sandbox window for provider connectivity testing. (+3 more)

### Community 4 - "Contributing to AI Go Teacher / 為 AI Go Teacher 貢獻"
Cohesion: 0.13
Nodes (14): Acknowledgments, Commit Messages, Commit 訊息, Contributing to AI Go Teacher / 為 AI Go Teacher 貢獻, I Have a Question, Style Guides, Table of Contents, 我有問題 (+6 more)

### Community 5 - "LLM 提供來源遷移指南 / LLM Provider Migration Guide"
Cohesion: 0.07
Nodes (27): API Key Security, API key 安全性, Automatic Migration of Legacy Settings, Available Alternatives, Frequently Asked Questions, GitHub Models Still Appears After Startup, LLM 提供來源遷移指南 / LLM Provider Migration Guide, OpenRouter Returns HTTP 402 (+19 more)

### Community 6 - "._start_generation"
Cohesion: 0.16
Nodes (4): on_error(), run(), 使用者按下停止：要求 provider 中止串流，並立即收尾。, 回傳 (顯示文字, 送給 LLM 的完整文字)。附件只附在完整文字中。

### Community 7 - "ConfigService"
Cohesion: 0.09
Nodes (3): ConfigService, Small wrapper around persisted UI settings., Migrate settings from the removed GitHub Models provider.

### Community 8 - "nvidia_provider.py"
Cohesion: 0.25
Nodes (11): json, opencc, get_publisher_from_model_id(), group_models_by_publisher(), 從 model_id 拆出 publisher（第一個 '/' 之前的部分）。 無 '/' 的 model_id 歸類為 "unknown"，確保 UI…, 將 model_id 清單依 publisher 分組，回傳 {publisher: [model_id, ...]}。 保持各 publisher 內…, get_publisher_from_model_id(), group_models_by_publisher() (+3 more)

### Community 9 - "refresh_tab_bar"
Cohesion: 0.11
Nodes (33): _capture_board_snapshot(), _close_tab_silently(), hydrate_active_session(), load_sgf_file(), on_close_tab_click(), on_copy_tab_click(), on_cycle_tab(), _on_find_tab_changed() (+25 more)

### Community 10 - "_clear_selected_runtime_data"
Cohesion: 0.20
Nodes (10): _delete_api_key(), delete_nvidia_api_key(), delete_openrouter_api_key(), Delete one application credential, treating a missing credential as success., Delete the NVIDIA API key owned by this application., Delete the OpenRouter API key owned by this application., _clear_selected_runtime_data(), _delete_runtime_path() (+2 more)

### Community 11 - "get_runtime_data_root"
Cohesion: 0.26
Nodes (13): ensure_runtime_dir(), get_executable_dir(), get_katago_runtime_overrides(), get_runtime_data_root(), get_runtime_file_path(), is_frozen_app(), iter_dotenv_paths(), _iter_log_candidates() (+5 more)

### Community 12 - ".on_state_change"
Cohesion: 0.12
Nodes (9): play_move_sound(), Capture an independent tree state for per-tab edit undo/redo., Move through the existing variation tree without editing it., 切換同一手棋的不同變化圖 (direction: 1 或 -1), Play the sound for a successfully applied board move. Sound playback is…, Append a pass as a real game-tree node without changing the board., 修正：提子只清空視覺棋盤(board)，絕不能刪除歷史紀錄(stones), 跳轉到樹上的任意節點，並回填各層 active_child_idx。 (+1 more)

### Community 13 - "find_service.py"
Cohesion: 0.20
Nodes (13): _branch_label(), find(), FindResult, _iter_all_paths(), parse_coordinate(), 尋找功能（Ctrl+F）的核心搜尋邏輯。 依設計規劃： - 純函式模組，不含任何 UI 依賴，方便單元測試。 - 支援以「手數（數字）」或「座標（GTP…, 依路徑索引從 root 取回節點；路徑失效（樹已變動）時回傳 None。, 解析 GTP 座標輸入（如 'Q16'、'pd'、'q4'）。 回傳 (x, y)，其中 x 欄 0 起、y 由上往下 0 起；無法解析回傳 None。 (+5 more)

### Community 14 - "LLMProvider"
Cohesion: 0.11
Nodes (6): LLMProvider, Return a human-readable display name for the given model ID. Subclasses should…, Return (is_valid, error_message)., Send a raw prompt to the LLM for a plain chat conversation. This is used by the…, Base class for streaming LLM commentary providers., Build the final prompt sent to the model from plain user text plus data.

### Community 15 - "chat_sandbox.py"
Cohesion: 0.07
Nodes (27): copy, pil, detect_system_theme(), Application color themes and Windows system-theme resolution., Return the Windows theme at process startup; safely fall back to light., resolve_theme(), time, _insert_inline_markdown() (+19 more)

### Community 16 - "TabManager"
Cohesion: 0.08
Nodes (9): 多分頁文件管理器：維護所有 TabSession 並提供 active session 切換。, 建立第一個分頁並設為 active。供 main 流程開機時呼叫一次。, 建立新分頁。若已達 MAX_TABS，回傳 None。, 關閉指定分頁；回傳 (success, reason)。 規則： - 至少保留一個分頁。 - 若傳入 index 為 active，自動切到鄰近分頁。, Move one session and preserve which session is active., Restore the most recently closed session at the end of the list., 支援 tab_manager[idx] 取第 idx 個分頁。, TabManager (+1 more)

### Community 18 - "BranchTreeView"
Cohesion: 0.07
Nodes (13): BranchCanvas, BranchTreeView, assign(), build_branch_section(), is_pass_move(), LLMSelectionDialog, load_ctk_image(), MarkupToolbar (+5 more)

### Community 19 - "version.py"
Cohesion: 0.27
Nodes (11): argparse, main(), Path, Application version helpers for AI Go Teacher. Run this file to update every…, Return the numeric tuple used by PyInstaller's VSVersionInfo., _replace_once(), sync_version(), update_version_info() (+3 more)

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
Cohesion: 0.19
Nodes (16): keyring, discover_nim_models(), 向 NIM 端點 /v1/models 查詢可用模型清單。 成功時回傳 (True, [model_id, ...])；失敗時回傳 (False,…, get_nvidia_api_key(), get_openrouter_api_key(), normalize_api_key(), Trim whitespace and common quote wrappers from API key values., Read NVIDIA API key from keyring first, then environment variables. (+8 more)

### Community 26 - "Security Policy"
Cohesion: 0.10
Nodes (19): Accepted Reports, Declined Reports, In-Scope, Information to Include, Out-of-Scope, Reporting a Vulnerability, Response & Resolution Process, Scope (+11 more)

### Community 28 - "plot_window"
Cohesion: 0.17
Nodes (20): add_full_game_commentary_to_cache(), get_full_game_commentary_from_cache(), plot_window(), apply_chart_mode(), build_full_game_summary_data(), collect_top_moves(), copy_summary_text(), format_move_summary() (+12 more)

### Community 29 - "requirements.txt - Python Dependencies"
Cohesion: 0.29
Nodes (7): requirements.txt - Python Dependencies, httpx HTTP Client, keyring Package, matplotlib Package, ollama Python Package, opencc Chinese Conversion, Pillow (PIL) Package

### Community 30 - "_legacy_show_system_info_dialog"
Cohesion: 0.22
Nodes (6): _create_info_section(), _create_katago_section(), _create_labeled_row(), _legacy_show_system_info_dialog(), 建立診斷資訊視窗中的單列 label/value。, setup_system_info_styles()

### Community 31 - "rules.py"
Cohesion: 0.16
Nodes (15): dataclasses, math, get_display_komi_from_sgf(), get_katago_komi(), get_rule_preset(), normalize_analysis_settings(), normalize_rule_id(), Supported KataGo rules and per-game analysis setting helpers. (+7 more)

### Community 33 - "katago_model_manager.py"
Cohesion: 0.12
Nodes (17): customtkinter, hashlib, os, pathlib, re, requests, RuntimeError, DownloadProgress (+9 more)

### Community 34 - "show_analysis_log_dialog"
Cohesion: 0.22
Nodes (11): create_dev_menu(), export_diagnostic_report(), _open_folder(), 顯示診斷報告匯出完成訊息與開啟資料夾按鈕。, 匯出診斷報告到 diagnostics/diagnostic_report.txt。, Return Dev menu items for the themeable menu bar., show_analysis_log_dialog(), apply_highlighting() (+3 more)

### Community 35 - "show_system_info_dialog"
Cohesion: 0.22
Nodes (10): Return a safe RAM usage ratio for the dashboard progress meter., Create a theme-aware dashboard card containing labelled values., Show the theme-aware CustomTkinter system diagnostics dashboard., show_system_info_dialog(), close_dialog(), render_dashboard(), _system_info_card(), _system_info_metric() (+2 more)

### Community 36 - "resource_path"
Cohesion: 0.14
Nodes (14): _confirm_and_download_ollama_model(), _create_ollama_model_row(), on_row_click(), _download_ollama_model(), on_download_complete(), update_progress(), _load_markup_labels(), _load_ollama_icon() (+6 more)

### Community 38 - "_handle_score_estimate_result"
Cohesion: 0.17
Nodes (14): calculate_area_score(), Calculate area scores with dead stones awarded to the opponent., count_captured_prisoners(), _handle_score_estimate_result(), is_markup_node_active(), on_close_score_estimate_click(), on_score_estimate_click(), 依歷史落子順序重播棋局，計算雙方已提取的對方棋子數。 回傳 {"black": 黑方提掉的白子數, "white": 白方提掉的黑子數}。 (+6 more)

### Community 39 - "main_v3.py"
Cohesion: 0.06
Nodes (32): collections, dotenv, itertools, matplotlib, matplotlib_backends_backend_tkagg, matplotlib_figure, matplotlib_pyplot, platform (+24 more)

### Community 41 - "._refresh_conversation_list"
Cohesion: 0.21
Nodes (3): _select(), on_change(), on_close()

### Community 43 - "build_menu_bar"
Cohesion: 0.13
Nodes (8): build_menu_bar(), on_closing(), Show a guarded, itemized dialog for deleting application runtime data., save_game_as_json(), save_game_as_json_dialog(), show_about(), show_delete_data_dialog(), confirm_and_delete()

### Community 44 - "show_game_info_dialog"
Cohesion: 0.15
Nodes (15): datetime, get_game_info(), Helpers for editable SGF game-information properties., Return a normalized date or raise ValueError for a non-SGF date., Read the editable game-info fields without exposing the metadata dict., Update editable fields in place while preserving every other property., update_game_info(), validate_game_date() (+7 more)

### Community 47 - "t"
Cohesion: 0.21
Nodes (16): change_config_path(), change_katago_path(), change_model_path(), create_katago_startup_popup(), update_elapsed(), new_game(), open_feedback_form(), 重新初始化分析器（關閉舊進程，建立新進程） (+8 more)

### Community 48 - "_ask_sgf_link"
Cohesion: 0.20
Nodes (7): _ask_sgf_link(), _fetch_sgf_content_from_url(), on_load_sgf_click_through_link(), download_task(), Load an SGF from a URL, or ask the user for one from the File menu., Fetch SGF bytes into memory and return decoded SGF text., Show a URL input dialog with a real placeholder entry.

### Community 49 - "show_ollama_install_dialog"
Cohesion: 0.22
Nodes (8): detect_ollama_installed(), 在 Windows 上抑制子進程彈出的主控台視窗。 隱藏終端機 (windowed) 模式下，子進程預設會繼承一個可見的主控台， 即使…, 檢查系統是否能執行 `ollama --version`，回傳 (installed: bool, version_or_none), 顯示簡單的 Ollama 安裝引導對話框（包含開啟下載頁與重新檢測）。, update_ollama_install_status_label(), show_ollama_install_dialog(), recheck(), _silent_subprocess_kwargs()

### Community 50 - "update_ui_with_data"
Cohesion: 0.22
Nodes (9): add_to_commentary_cache(), _commentary_cache_key(), get_commentary_from_cache(), on_commentary_generation_complete(), poll_ai(), 【Phase 1】LLM 生成完成後的回呼 — 將完整的解說存儲到快取, 將解說文本新增到快取 (執行緒安全，儲存全部手數), 直接使用記憶體中的數據更新 UI，並將所有分析結果保存到快取以供後續比較使用 (+1 more)

### Community 51 - "KataGoAnalyzer"
Cohesion: 0.14
Nodes (5): KataGoAnalyzer, 將當前棋譜轉換成唯一的字串，作為快取的 Key, 用一致的 KataGo moves 格式生成快取 key，避免 stones/list 格式不一致造成 miss。, Ask KataGo to stop an analysis query immediately, then detach it., Remove already-queued responses belonging to a cancelled query.

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
Nodes (12): ctypes, logging, _font_height_from_tk_size(), ImeFontManager, LOGFONTW, Synchronize Windows IME composition fonts with focused Tk widgets. Tk delegates…, Remove only this manager's binding., Apply the current focused widget's font to its IME context. (+4 more)

### Community 56 - "KataGoModelBrowserFrame"
Cohesion: 0.15
Nodes (3): Exception, KataGoModelBrowserFrame, Browse, download, and apply KataGo neural-network models.

### Community 57 - "_show_llm_selection_dialog"
Cohesion: 0.23
Nodes (9): _show_llm_selection_dialog(), bind_ollama_mousewheel(), refresh_ollama_models(), task(), render_ollama_models(), add_section(), scroll_ollama_models(), show_ollama_models_loading() (+1 more)

### Community 58 - "materialize_bundled_runtime_file"
Cohesion: 0.16
Nodes (18): get_config_path(), get_katago_path(), get_model_path(), hide_path_on_windows(), _load_runtime_manifest(), materialize_bundled_runtime_file(), Copy bundled KataGo runtime files out of PyInstaller's _MEI directory. The…, 安全取得 KataGo 執行檔、設定檔、模型檔路徑與存在狀態。 (+10 more)

### Community 59 - "start_analyzer_async"
Cohesion: 0.15
Nodes (20): auto_analyze(), get_config_display_name(), get_model_display_name(), is_analyzer_ready(), on_analyze_button_click(), 分析整盤棋並回傳每手的勝率列表 (複用全局 KataGo analyzer，支援取消與進度回報), run_full_game_analysis(), set_analysis_controls_state() (+12 more)

### Community 61 - ".apply_markup"
Cohesion: 0.20
Nodes (4): is_markup_node(), Return whether a node stores board annotations instead of a move., Apply one annotation and keep consecutive annotations in one node., Remove every annotation at one coordinate.

### Community 62 - "I Want to Contribute"
Cohesion: 0.17
Nodes (12): Before Submitting a Bug Report, Before Submitting an Enhancement, Development Environment Setup, How Do I Submit a Good Bug Report?, How Do I Submit a Good Enhancement Proposal?, I Want to Contribute, IDE Configuration, Improving the Documentation (+4 more)

### Community 63 - "GameNode"
Cohesion: 0.15
Nodes (6): _copy_game_tree(), GameNode, parse_sequence(), 遞迴複製 GameNode 樹，不複製 parent（避免循環引用）。 回傳新樹的 root，所有節點的 parent 在複製後重新串接。, 讀取 SGF 並正確建立分支樹狀結構，同時恢復註解到快取【Phase 3】修正版本, Parse SGF text directly without creating a local SGF file.

### Community 65 - ".__init__"
Cohesion: 0.29
Nodes (3): load_tk_image(), Load an image as a Tk image, preferring Pillow for broad format support., 依 board_shell 實際尺寸重新縮放外框背景圖片（cover 模式：填滿裁切）。 由 board_shell 的 <Configure>…

### Community 66 - "我想貢獻"
Cohesion: 0.17
Nodes (12): IDE 設定, 回報錯誤（Bug）, 如何提交一份好的 Bug 回報？, 如何提交一份好的功能建議？, 我想貢獻, 提交 Bug 回報前, 提交功能建議前, 提出功能建議 (+4 more)

### Community 68 - "serialize_game_context"
Cohesion: 0.27
Nodes (11): _analysis_lines(), _gtp(), _move_text(), Compact, factual Go-game context for LLM teaching prompts. This module…, Serialize only the selected mainline and explicitly named snapshots., serialize_board(), serialize_game_context(), serialize_mainline() (+3 more)

### Community 71 - "_build_diagnostic_report_text"
Cohesion: 0.40
Nodes (5): _build_diagnostic_report_text(), _get_newest_log_file(), 讀取最新 log 的最後 max_lines 行；沒有 log 時回傳提示文字。, 組合 diagnostic_report.txt 的完整內容。, _read_recent_log_lines()

### Community 72 - "save_and_apply_settings"
Cohesion: 0.23
Nodes (10): Return the human-readable display name for a model ID. Falls back to the raw…, Compatibility callback for components that report transient status., 只更新老師解說區，不改動生成中的快取狀態。, LLM Provider 的串流回呼；累積全文但在回放時不覆蓋既有解說。, render_teacher_ui(), apply_settings(), save_and_apply_settings(), update_selected_indicator() (+2 more)

### Community 73 - "KataGoModelManager"
Cohesion: 0.33
Nodes (5): ProgressCallback, KataGoModel, KataGoModelManager, Path, Fetch and safely download models from katagotraining.org.

### Community 74 - "show_katago_online_models_dialog"
Cohesion: 0.18
Nodes (6): KataGoModelBrowserWindow, Path, Window wrapper for the online model browser frame., Open the CustomTkinter KataGo Training API model browser., show_katago_online_models_dialog(), apply_model()

### Community 75 - "get_active_analysis_settings"
Cohesion: 0.27
Nodes (6): get_active_analysis_settings(), escape_sgf(), get_node_turn_number(), write_node(), GoDataFilter, 【改進】從快取中查詢上一手 (turn-1) 的分析結果，取出勝率和目數作為基準 Args: turn: 當前手數 analyzer:…

### Community 76 - "task"
Cohesion: 0.25
Nodes (4): refresh_openrouter_model_combo(), refresh_openrouter_models_async(), task(), update_ui()

### Community 77 - "show_first_run_onboarding_dialog"
Cohesion: 0.29
Nodes (4): 首次啟動時彈出的強制 Modal Onboarding 視窗。 內容： - 語言選擇（必填，Radiobutton 兩選一） - LLM…, show_first_run_onboarding_dialog(), _on_language_select(), _refresh_dialog_strings()

### Community 78 - "refresh_language"
Cohesion: 0.29
Nodes (8): toggle_dev(), Refresh a known static teacher prompt without touching LLM output., Refresh controls that expose the continuous-analysis state., rebuild_menu_bar(), refresh_language(), refresh_teacher_static_message(), render_winrate_text(), update_continuous_analysis_ui()

### Community 79 - "KataGoModelFormatError"
Cohesion: 0.33
Nodes (4): Any, KataGoModelFormatError, KataGoModelPage, Raised when the API response is missing required model fields.

### Community 80 - "update_ui"
Cohesion: 0.29
Nodes (5): 取得指定 publisher 下的 model_id 清單（保持原始順序）。, 從 model_id 拆出 publisher（供 UI 還原選擇用）。, on_nvidia_publisher_changed(), update_ui(), refresh_nvidia_model_combo()

### Community 81 - "Technical Architecture"
Cohesion: 0.40
Nodes (5): Communication Protocols, Core Modules, Frontend and Application Layer, Go Engine, Technical Architecture

### Community 82 - "技術架構"
Cohesion: 0.40
Nodes (5): 前端與應用程式層, 圍棋引擎, 技術架構, 核心模組, 通訊協定

### Community 83 - "Quick Start"
Cohesion: 0.50
Nodes (4): Download the Executable (Windows), Installation Steps, Prerequisites, Quick Start

### Community 84 - "快速開始"
Cohesion: 0.50
Nodes (4): 下載執行檔（Windows）, 前置需求, 安裝步驟, 快速開始

### Community 86 - "Features"
Cohesion: 0.67
Nodes (3): Core Capabilities, Features, Supported LLM Providers

### Community 87 - "Development Commands"
Cohesion: 0.67
Nodes (3): Development Commands, KataGo Engine Commands, Python Commands

### Community 88 - "開發指令"
Cohesion: 0.67
Nodes (3): KataGo 引擎指令, Python 指令, 開發指令

### Community 89 - "LLM 整合"
Cohesion: 0.67
Nodes (3): LLM 整合, 自訂教學語氣, 設定 API 金鑰

## Knowledge Gaps
- **102 isolated node(s):** `Table of Contents`, `I Have a Question`, `Before Submitting a Bug Report`, `How Do I Submit a Good Bug Report?`, `Before Submitting an Enhancement` (+97 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 445 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMChatWindow` connect `LLMChatWindow` to `ProviderFactory`, `._start_generation`, `main_v3.py`, `._active_conversation`, `._refresh_conversation_list`, `._tr`, `.__init__`, `._build_ui`, `chat_sandbox.py`, `._apply_chat_palette_swap`?**
  _High betweenness centrality (0.126) - this node is a cross-community bridge._
- **Why does `GoBoard` connect `GoBoard` to `.refresh_display`, `.__init__`, `main_v3.py`, `get_active_analysis_settings`, `.on_state_change`, `.apply_markup`, `GameNode`?**
  _High betweenness centrality (0.093) - this node is a cross-community bridge._
- **Why does `t()` connect `t` to `ProviderFactory`, `refresh_tab_bar`, `_clear_selected_runtime_data`, `get_runtime_data_root`, `TabManager`, `BranchTreeView`, `show_appearance_settings_dialog`, `I18n`, `normalize_api_key`, `plot_window`, `_legacy_show_system_info_dialog`, `rules.py`, `show_analysis_log_dialog`, `show_system_info_dialog`, `resource_path`, `_handle_score_estimate_result`, `main_v3.py`, `build_menu_bar`, `show_game_info_dialog`, `_ask_sgf_link`, `show_ollama_install_dialog`, `create_path_row`, `show_find_dialog`, `_show_llm_selection_dialog`, `materialize_bundled_runtime_file`, `start_analyzer_async`, `.refresh_display`, `serialize_game_context`, `save_and_apply_settings`, `show_katago_online_models_dialog`, `get_active_analysis_settings`, `task`, `show_first_run_onboarding_dialog`, `refresh_language`, `update_ui`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `t()` (e.g. with `set_llm_tone()` and `show_chat_sandbox()`) actually correct?**
  _`t()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `build_menu_bar()` (e.g. with `palette()` and `toggle_branch_panel()`) actually correct?**
  _`build_menu_bar()` has 28 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Table of Contents`, `I Have a Question`, `Before Submitting a Bug Report` to the rest of the system?**
  _102 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `GoBoard` be split into smaller, more focused modules?**
  _Cohesion score 0.12477718360071301 - nodes in this community are weakly interconnected._