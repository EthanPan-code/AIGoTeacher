# Graph Report - AIGoTeacher  (2026-10-20)

## Corpus Check
- 34 files · ~69,425 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: .gz 2, .spec 1, (none) 1)

## Summary
- 1209 nodes · 2487 edges · 71 communities (56 shown, 15 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 154 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `35889421`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- GoBoard
- AI 圍棋老師 / AI Go Teacher
- OllamaProvider
- _show_llm_selection_dialog
- Contributing to AI Go Teacher / 為 AI Go Teacher 貢獻
- LLM 提供來源遷移指南 / LLM Provider Migration Guide
- ._start_generation
- ConfigService
- nvidia_provider.py
- refresh_tab_bar
- _clear_selected_runtime_data
- KataGoAnalyzer
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
- create_dev_menu
- show_system_info_dialog
- _download_ollama_model
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
- resource_path
- add_to_commentary_cache
- get_active_analysis_settings
- create_path_row
- ._apply_chat_palette_swap
- show_find_dialog
- ImeFontManager
- MessageBubble
- refresh_language
- write_node
- set_winrate_text
- theme_service.py
- .apply_markup
- show_first_run_onboarding_dialog
- GameNode
- .refresh_display
- .__init__
- _confirm_and_download_ollama_model

## God Nodes (most connected - your core abstractions)
1. `t()` - 121 edges
2. `LLMChatWindow` - 86 edges
3. `GoBoard` - 82 edges
4. `ConfigService` - 40 edges
5. `build_menu_bar()` - 38 edges
6. `_show_llm_selection_dialog()` - 35 edges
7. `ProviderFactory` - 31 edges
8. `resource_path()` - 31 edges
9. `LLMProvider` - 24 edges
10. `plot_window()` - 24 edges

## Surprising Connections (you probably didn't know these)
- `ProviderFactory` --uses--> `NvidiaProvider`  [INFERRED]
  services/provider_factory.py → providers/nvidia_provider.py
- `ProviderFactory` --uses--> `OllamaProvider`  [INFERRED]
  services/provider_factory.py → providers/ollama_provider.py
- `ProviderFactory` --uses--> `OpenRouterProvider`  [INFERRED]
  services/provider_factory.py → providers/openrouter_provider.py
- `_download_ollama_model()` --uses--> `ProviderFactory`  [INFERRED]
  ui/main_v3.py → services/provider_factory.py
- `plot_window()` --uses--> `ProviderFactory`  [INFERRED]
  ui/main_v3.py → services/provider_factory.py

## Import Cycles
- None detected.

## Communities (71 total, 15 thin omitted)

### Community 0 - "GoBoard"
Cohesion: 0.14
Nodes (5): GoBoard, 動態生成歷史落子紀錄，不會再因為提子而消失，確保 AI 判斷正確, Return 1-based move index where the current branch starts, or None on main line., 點目時暫時隱藏推薦手；結束後依據最後一次分析結果恢復顯示。, Return whether applying a legal move removes any opponent stones.

### Community 1 - "AI 圍棋老師 / AI Go Teacher"
Cohesion: 0.05
Nodes (44): AI 圍棋老師 / AI Go Teacher, Communication Protocols, Contents, Core Capabilities, Core Modules, Custom Teaching Tones, Development Commands, Download the Executable (Windows) (+36 more)

### Community 2 - "OllamaProvider"
Cohesion: 0.07
Nodes (12): OllamaProvider, get_ollama_manager(), OllamaManager, download_task(), emit_complete(), emit_progress(), OllamaModelInfo, Return (models, error), retaining the last good catalog on failure. (+4 more)

### Community 3 - "_show_llm_selection_dialog"
Cohesion: 0.06
Nodes (39): ProviderFactory, Return the human-readable display name for a model ID. Falls back to the raw…, Reverse lookup: display name → model ID. Returns None when the display name is…, Return [(display_name, model_id), ...] for UI widgets. The list follows the…, 向 NIM 端點探索可用模型；失敗時回傳空清單與錯誤。 回傳 (model_ids, used_fallback, error_message)： -…, 從 model_id 清單取出 publisher 清單（已排序、去重）。, 取得指定 publisher 下的 model_id 清單（保持原始順序）。, 從 model_id 拆出 publisher（供 UI 還原選擇用）。 (+31 more)

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
Cohesion: 0.16
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

### Community 11 - "KataGoAnalyzer"
Cohesion: 0.06
Nodes (40): ensure_runtime_dir(), get_config_path(), get_executable_dir(), get_katago_path(), get_katago_runtime_overrides(), get_model_path(), get_runtime_data_root(), get_runtime_file_path() (+32 more)

### Community 12 - ".on_state_change"
Cohesion: 0.14
Nodes (7): Capture an independent tree state for per-tab edit undo/redo., Move through the existing variation tree without editing it., 切換同一手棋的不同變化圖 (direction: 1 或 -1), Append a pass as a real game-tree node without changing the board., 修正：提子只清空視覺棋盤(board)，絕不能刪除歷史紀錄(stones), 跳轉到樹上的任意節點，並回填各層 active_child_idx。, 【修復】回放模式下，從快取顯示當前手數的解說；無快取則清空。 此方法統一處理 undo / redo / switch_branch /…

### Community 13 - "find_service.py"
Cohesion: 0.20
Nodes (13): _branch_label(), find(), FindResult, _iter_all_paths(), parse_coordinate(), 尋找功能（Ctrl+F）的核心搜尋邏輯。 依設計規劃： - 純函式模組，不含任何 UI 依賴，方便單元測試。 - 支援以「手數（數字）」或「座標（GTP…, 依路徑索引從 root 取回節點；路徑失效（樹已變動）時回傳 None。, 解析 GTP 座標輸入（如 'Q16'、'pd'、'q4'）。 回傳 (x, y)，其中 x 欄 0 起、y 由上往下 0 起；無法解析回傳 None。 (+5 more)

### Community 14 - "LLMProvider"
Cohesion: 0.11
Nodes (6): LLMProvider, Return a human-readable display name for the given model ID. Subclasses should…, Return (is_valid, error_message)., Send a raw prompt to the LLM for a plain chat conversation. This is used by the…, Base class for streaming LLM commentary providers., Build the final prompt sent to the model from plain user text plus data.

### Community 15 - "chat_sandbox.py"
Cohesion: 0.13
Nodes (15): copy, os, pathlib, pil, re, sys, time, tkinter (+7 more)

### Community 16 - "TabManager"
Cohesion: 0.08
Nodes (9): 多分頁文件管理器：維護所有 TabSession 並提供 active session 切換。, 建立第一個分頁並設為 active。供 main 流程開機時呼叫一次。, 建立新分頁。若已達 MAX_TABS，回傳 None。, 關閉指定分頁；回傳 (success, reason)。 規則： - 至少保留一個分頁。 - 若傳入 index 為 active，自動切到鄰近分頁。, Move one session and preserve which session is active., Restore the most recently closed session at the end of the list., 支援 tab_manager[idx] 取第 idx 個分頁。, TabManager (+1 more)

### Community 18 - "BranchTreeView"
Cohesion: 0.17
Nodes (4): BranchTreeView, assign(), build_branch_section(), Update only current-path colors after navigation. Node coordinates and static…

### Community 19 - "version.py"
Cohesion: 0.27
Nodes (11): argparse, Path, main(), Application version helpers for AI Go Teacher. Run this file to update every…, Return the numeric tuple used by PyInstaller's VSVersionInfo., _replace_once(), sync_version(), update_version_info() (+3 more)

### Community 20 - "show_appearance_settings_dialog"
Cohesion: 0.21
Nodes (9): show_appearance_settings_dialog(), apply_changes(), create_image_row(), browse_image(), use_default(), update_preview(), show_sound_settings_dialog(), create_sound_row() (+1 more)

### Community 21 - "safe_get_system_info"
Cohesion: 0.11
Nodes (21): _build_diagnostic_report_text(), _format_bytes_as_gb(), _get_cpu_name(), _get_gpu_info(), _get_newest_log_file(), _get_physical_core_count(), _get_ram_info(), _get_windows_display_version() (+13 more)

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
Cohesion: 0.10
Nodes (33): _analysis_lines(), _gtp(), _move_text(), Compact, factual Go-game context for LLM teaching prompts. This module…, Serialize only the selected mainline and explicitly named snapshots., serialize_board(), serialize_game_context(), serialize_mainline() (+25 more)

### Community 29 - "requirements.txt - Python Dependencies"
Cohesion: 0.29
Nodes (7): requirements.txt - Python Dependencies, httpx HTTP Client, keyring Package, matplotlib Package, ollama Python Package, opencc Chinese Conversion, Pillow (PIL) Package

### Community 30 - "_legacy_show_system_info_dialog"
Cohesion: 0.22
Nodes (6): _create_info_section(), _create_katago_section(), _create_labeled_row(), _legacy_show_system_info_dialog(), 建立診斷資訊視窗中的單列 label/value。, setup_system_info_styles()

### Community 31 - "rules.py"
Cohesion: 0.18
Nodes (11): dataclasses, math, get_display_komi_from_sgf(), get_katago_komi(), get_rule_preset(), normalize_rule_id(), Supported KataGo rules and per-game analysis setting helpers., Convert the displayed score unit to KataGo's half-point komi unit. (+3 more)

### Community 34 - "create_dev_menu"
Cohesion: 0.29
Nodes (7): create_dev_menu(), export_diagnostic_report(), _open_folder(), 顯示診斷報告匯出完成訊息與開啟資料夾按鈕。, 匯出診斷報告到 diagnostics/diagnostic_report.txt。, Return Dev menu items for the themeable menu bar., _show_diagnostic_export_success()

### Community 35 - "show_system_info_dialog"
Cohesion: 0.22
Nodes (10): Return a safe RAM usage ratio for the dashboard progress meter., Create a theme-aware dashboard card containing labelled values., Show the theme-aware CustomTkinter system diagnostics dashboard., show_system_info_dialog(), close_dialog(), render_dashboard(), _system_info_card(), _system_info_metric() (+2 more)

### Community 36 - "_download_ollama_model"
Cohesion: 0.32
Nodes (7): _download_ollama_model(), on_download_complete(), update_progress(), show_winrate_chart(), on_cancel(), task(), update_progress()

### Community 38 - "_handle_score_estimate_result"
Cohesion: 0.18
Nodes (13): calculate_area_score(), Calculate area scores with dead stones awarded to the opponent., count_captured_prisoners(), _handle_score_estimate_result(), on_close_score_estimate_click(), on_score_estimate_click(), 依歷史落子順序重播棋局，計算雙方已提取的對方棋子數。 回傳 {"black": 黑方提掉的白子數, "white": 白方提掉的黑子數}。, show_score_estimate_popup() (+5 more)

### Community 39 - "main_v3.py"
Cohesion: 0.06
Nodes (33): collections, customtkinter, dotenv, hashlib, itertools, matplotlib, matplotlib_backends_backend_tkagg, matplotlib_figure (+25 more)

### Community 41 - "._refresh_conversation_list"
Cohesion: 0.21
Nodes (3): _select(), on_change(), on_close()

### Community 43 - "build_menu_bar"
Cohesion: 0.13
Nodes (8): build_menu_bar(), on_closing(), Show a guarded, itemized dialog for deleting application runtime data., save_game_as_json(), save_game_as_json_dialog(), show_about(), show_delete_data_dialog(), confirm_and_delete()

### Community 44 - "show_game_info_dialog"
Cohesion: 0.16
Nodes (14): datetime, get_game_info(), Helpers for editable SGF game-information properties., Return a normalized date or raise ValueError for a non-SGF date., Read the editable game-info fields without exposing the metadata dict., Update editable fields in place while preserving every other property., update_game_info(), validate_game_date() (+6 more)

### Community 47 - "t"
Cohesion: 0.14
Nodes (24): change_config_path(), change_katago_path(), change_model_path(), create_katago_startup_popup(), update_elapsed(), get_config_display_name(), get_model_display_name(), new_game() (+16 more)

### Community 48 - "_ask_sgf_link"
Cohesion: 0.20
Nodes (7): _ask_sgf_link(), _fetch_sgf_content_from_url(), on_load_sgf_click_through_link(), download_task(), Load an SGF from a URL, or ask the user for one from the File menu., Fetch SGF bytes into memory and return decoded SGF text., Show a URL input dialog with a real placeholder entry.

### Community 49 - "resource_path"
Cohesion: 0.13
Nodes (14): detect_ollama_installed(), _load_markup_labels(), play_move_sound(), 彈出儲存 / 不儲存 / 取消 三選一對話框，回傳 'save' / 'discard' / 'cancel'。, Play the sound for a successfully applied board move. Sound playback is…, 在 Windows 上抑制子進程彈出的主控台視窗。 隱藏終端機 (windowed) 模式下，子進程預設會繼承一個可見的主控台， 即使…, 檢查系統是否能執行 `ollama --version`，回傳 (installed: bool, version_or_none), 顯示簡單的 Ollama 安裝引導對話框（包含開啟下載頁與重新檢測）。 (+6 more)

### Community 50 - "add_to_commentary_cache"
Cohesion: 0.33
Nodes (6): add_to_commentary_cache(), _commentary_cache_key(), get_commentary_from_cache(), on_commentary_generation_complete(), 【Phase 1】LLM 生成完成後的回呼 — 將完整的解說存儲到快取, 將解說文本新增到快取 (執行緒安全，儲存全部手數)

### Community 51 - "get_active_analysis_settings"
Cohesion: 0.22
Nodes (8): normalize_analysis_settings(), get_active_analysis_settings(), GoDataFilter, 【改進】從快取中查詢上一手 (turn-1) 的分析結果，取出勝率和目數作為基準 Args: turn: 當前手數 analyzer:…, Edit the active tab's rules and the default for newly created tabs., open_rules_settings(), show_rules_settings_dialog(), apply_rules()

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

### Community 56 - "MessageBubble"
Cohesion: 0.18
Nodes (8): _insert_inline_markdown(), MessageBubble, _action_btn(), _action_icon(), 把單行文字插入 Text widget，支援 **粗體**、*斜體*、`行內程式碼`。, 把 Markdown 內容渲染到 Text widget：標題 / 列表 / 粗斜體 / 行程式碼 / 程式碼區塊。, 依 wrap 後的 displayline 數調整 Text 高度，消除多餘空白。, render_markdown()

### Community 57 - "refresh_language"
Cohesion: 0.17
Nodes (13): apply_theme(), recolor(), toggle_dev(), Apply a configured theme to existing widgets without restarting., Refresh a known static teacher prompt without touching LLM output., Refresh controls that expose the continuous-analysis state., Expose semantic theme tokens to legacy drawing code in this module., rebuild_menu_bar() (+5 more)

### Community 58 - "write_node"
Cohesion: 0.21
Nodes (9): escape_sgf(), get_node_turn_number(), write_node(), is_markup_node(), is_pass_move(), move_to_gtp(), Return whether a node stores board annotations instead of a move., Return whether a move tuple represents a pass (SGF B[]/W[]). (+1 more)

### Community 59 - "set_winrate_text"
Cohesion: 0.27
Nodes (11): auto_analyze(), is_analyzer_ready(), is_markup_node_active(), on_analyze_button_click(), poll_ai(), 分析整盤棋並回傳每手的勝率列表 (複用全局 KataGo analyzer，支援取消與進度回報), 直接使用記憶體中的數據更新 UI，並將所有分析結果保存到快取以供後續比較使用, run_full_game_analysis() (+3 more)

### Community 60 - "theme_service.py"
Cohesion: 0.32
Nodes (6): detect_system_theme(), normalize_theme(), Application color themes and Windows system-theme resolution., Return the Windows theme at process startup; safely fall back to light., resolve_theme(), winreg

### Community 62 - "show_first_run_onboarding_dialog"
Cohesion: 0.29
Nodes (4): 首次啟動時彈出的強制 Modal Onboarding 視窗。 內容： - 語言選擇（必填，Radiobutton 兩選一） - LLM…, show_first_run_onboarding_dialog(), _on_language_select(), _refresh_dialog_strings()

### Community 63 - "GameNode"
Cohesion: 0.15
Nodes (6): _copy_game_tree(), GameNode, parse_sequence(), 遞迴複製 GameNode 樹，不複製 parent（避免循環引用）。 回傳新樹的 root，所有節點的 parent 在複製後重新串接。, 讀取 SGF 並正確建立分支樹狀結構，同時恢復註解到快取【Phase 3】修正版本, Parse SGF text directly without creating a local SGF file.

### Community 65 - ".__init__"
Cohesion: 0.14
Nodes (6): BranchCanvas, LLMSelectionDialog, load_tk_image(), MarkupToolbar, Load an image as a Tk image, preferring Pillow for broad format support., 依 board_shell 實際尺寸重新縮放外框背景圖片（cover 模式：填滿裁切）。 由 board_shell 的 <Configure>…

### Community 66 - "_confirm_and_download_ollama_model"
Cohesion: 0.29
Nodes (7): _confirm_and_download_ollama_model(), _create_ollama_model_row(), on_row_click(), _load_ollama_icon(), 為 Ollama 模型創建一個選擇行。 - 已下載（available）：點擊直接選中 - 雲端（cloud）：點擊直接選中，不顯示下載 -…, 顯示下載確認對話框並開始下載 Args: parent: 父窗口 model_name: 要下載的模型名稱 provider: OllamaProvider…, download_named_ollama_model()

## Knowledge Gaps
- **102 isolated node(s):** `Table of Contents`, `I Have a Question`, `Before Submitting a Bug Report`, `How Do I Submit a Good Bug Report?`, `Before Submitting an Enhancement` (+97 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 426 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMChatWindow` connect `LLMChatWindow` to `_show_llm_selection_dialog`, `._start_generation`, `main_v3.py`, `._active_conversation`, `._refresh_conversation_list`, `._tr`, `.__init__`, `._build_ui`, `chat_sandbox.py`, `._apply_chat_palette_swap`?**
  _High betweenness centrality (0.131) - this node is a cross-community bridge._
- **Why does `t()` connect `t` to `_show_llm_selection_dialog`, `refresh_tab_bar`, `_clear_selected_runtime_data`, `KataGoAnalyzer`, `TabManager`, `BranchTreeView`, `show_appearance_settings_dialog`, `I18n`, `normalize_api_key`, `plot_window`, `_legacy_show_system_info_dialog`, `create_dev_menu`, `show_system_info_dialog`, `_download_ollama_model`, `_handle_score_estimate_result`, `main_v3.py`, `build_menu_bar`, `show_game_info_dialog`, `_ask_sgf_link`, `resource_path`, `get_active_analysis_settings`, `create_path_row`, `show_find_dialog`, `refresh_language`, `write_node`, `show_first_run_onboarding_dialog`, `.refresh_display`, `.__init__`, `_confirm_and_download_ollama_model`?**
  _High betweenness centrality (0.113) - this node is a cross-community bridge._
- **Why does `GoBoard` connect `GoBoard` to `.refresh_display`, `.__init__`, `.is_welcome_mode`, `main_v3.py`, `.on_state_change`, `write_node`, `.apply_markup`, `GameNode`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `t()` (e.g. with `set_llm_tone()` and `show_chat_sandbox()`) actually correct?**
  _`t()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `build_menu_bar()` (e.g. with `palette()` and `toggle_branch_panel()`) actually correct?**
  _`build_menu_bar()` has 28 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Table of Contents`, `I Have a Question`, `Before Submitting a Bug Report` to the rest of the system?**
  _102 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `GoBoard` be split into smaller, more focused modules?**
  _Cohesion score 0.1402116402116402 - nodes in this community are weakly interconnected._