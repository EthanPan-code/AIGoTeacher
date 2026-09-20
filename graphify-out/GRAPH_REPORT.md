# Graph Report - AIGoTeacher  (2026-09-20)

## Corpus Check
- 29 files · ~77,565 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: .gz 2, .spec 1, (none) 1)

## Summary
- 1110 nodes · 2279 edges · 57 communities (45 shown, 12 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 142 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `dcd0d9ec`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- GoBoard
- AI 圍棋老師 / AI Go Teacher
- OllamaManager
- _show_llm_selection_dialog
- Contributing to AI Go Teacher / 為 AI Go Teacher 貢獻
- LLM 提供來源遷移指南 / LLM Provider Migration Guide
- ._start_generation
- ConfigService
- nvidia_provider.py
- refresh_tab_bar
- _clear_selected_runtime_data
- task
- version.py
- find_service.py
- LLMProvider
- KataGoAnalyzer
- TabManager
- MenuBar
- BranchTreeView
- OllamaProvider
- show_appearance_settings_dialog
- safe_get_system_info
- I18n
- openrouter_provider.py
- LLMChatWindow
- normalize_api_key
- Security Policy
- NvidiaProvider
- plot_window
- requirements.txt - Python Dependencies
- show_system_info_dialog
- get_runtime_data_root
- GUI Screenshot
- Available Status Screenshot
- Cloud API Illustration
- Download UI Screenshot
- chat_sandbox.py
- version_info.txt - PyInstaller VSVersionInfo
- start_analyzer_async
- main_v3.py
- ._active_conversation
- ._refresh_conversation_list
- build_menu_bar
- show_game_info_dialog
- .__init__
- ._build_ui
- t
- MessageBubble
- show_ollama_install_dialog
- materialize_bundled_runtime_file
- _build_diagnostic_report_text
- create_path_row
- ._apply_chat_palette_swap
- show_find_dialog
- show_analysis_log_dialog
- _delete_runtime_path

## God Nodes (most connected - your core abstractions)
1. `t()` - 120 edges
2. `LLMChatWindow` - 86 edges
3. `GoBoard` - 63 edges
4. `_show_llm_selection_dialog()` - 36 edges
5. `build_menu_bar()` - 35 edges
6. `ProviderFactory` - 31 edges
7. `ConfigService` - 30 edges
8. `LLMProvider` - 24 edges
9. `resource_path()` - 24 edges
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
- `plot_window()` --uses--> `ProviderFactory`  [INFERRED]
  ui/main_v3.py → services/provider_factory.py

## Import Cycles
- None detected.

## Communities (57 total, 12 thin omitted)

### Community 0 - "GoBoard"
Cohesion: 0.06
Nodes (20): add_to_commentary_cache(), _commentary_cache_key(), GameNode, get_commentary_from_cache(), GoBoard, parse_sequence(), on_commentary_generation_complete(), 將解說文本新增到快取 (執行緒安全，儲存全部手數) (+12 more)

### Community 1 - "AI 圍棋老師 / AI Go Teacher"
Cohesion: 0.05
Nodes (44): AI 圍棋老師 / AI Go Teacher, Communication Protocols, Contents, Core Capabilities, Core Modules, Custom Teaching Tones, Development Commands, Download the Executable (Windows) (+36 more)

### Community 2 - "OllamaManager"
Cohesion: 0.13
Nodes (9): OllamaManager, download_task(), emit_complete(), emit_progress(), Return (models, error), retaining the last good catalog on failure., Read a model without triggering network I/O., Start a streaming REST pull for a local model., REST client and catalog cache for the local Ollama service. (+1 more)

### Community 3 - "_show_llm_selection_dialog"
Cohesion: 0.05
Nodes (46): ProviderFactory, Return the human-readable display name for a model ID. Falls back to the raw…, Reverse lookup: display name → model ID. Returns None when the display name is…, Return [(display_name, model_id), ...] for UI widgets. The list follows the…, 向 NIM 端點探索可用模型，失敗時降級至內建清單。 回傳 (model_ids, used_fallback, error_message)： -…, 從 model_id 清單取出 publisher 清單（已排序、去重）。, 取得指定 publisher 下的 model_id 清單（保持原始順序）。, 從 model_id 拆出 publisher（供 UI 還原選擇用）。 (+38 more)

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
Nodes (29): math, ConfigService, Small wrapper around persisted UI settings., Migrate settings from the removed GitHub Models provider., get_display_komi_from_sgf(), get_katago_komi(), get_rule_preset(), normalize_analysis_settings() (+21 more)

### Community 8 - "nvidia_provider.py"
Cohesion: 0.23
Nodes (8): opencc, get_publisher_from_model_id(), group_models_by_publisher(), 從 model_id 拆出 publisher（第一個 '/' 之前的部分）。 無 '/' 的 model_id 歸類為 "unknown"，確保 UI…, 將 model_id 清單依 publisher 分組，回傳 {publisher: [model_id, ...]}。 保持各 publisher 內…, OllamaModelInfo, threading, typing

### Community 9 - "refresh_tab_bar"
Cohesion: 0.09
Nodes (39): _capture_board_snapshot(), _close_tab_silently(), _copy_game_tree(), hydrate_active_session(), load_sgf_file(), new_game(), on_close_tab_click(), on_copy_tab_click() (+31 more)

### Community 10 - "_clear_selected_runtime_data"
Cohesion: 0.17
Nodes (12): _delete_api_key(), delete_nvidia_api_key(), delete_openrouter_api_key(), Delete one application credential, treating a missing credential as success., Delete the NVIDIA API key owned by this application., Delete the OpenRouter API key owned by this application., _clear_selected_runtime_data(), on_closing() (+4 more)

### Community 11 - "task"
Cohesion: 0.23
Nodes (11): get_config_path(), get_katago_path(), get_model_path(), 安全取得 KataGo 執行檔、設定檔、模型檔路徑與存在狀態。, safe_get_katago_info(), ScoreAnalyzer, task(), start_score_analyzer_async() (+3 more)

### Community 12 - "version.py"
Cohesion: 0.22
Nodes (13): argparse, Path, pathlib, re, main(), Application version helpers for AI Go Teacher. Run this file to update every…, Return the numeric tuple used by PyInstaller's VSVersionInfo., _replace_once() (+5 more)

### Community 13 - "find_service.py"
Cohesion: 0.18
Nodes (14): dataclasses, _branch_label(), find(), FindResult, _iter_all_paths(), parse_coordinate(), 尋找功能（Ctrl+F）的核心搜尋邏輯。 依設計規劃： - 純函式模組，不含任何 UI 依賴，方便單元測試。 - 支援以「手數（數字）」或「座標（GTP…, 依路徑索引從 root 取回節點；路徑失效（樹已變動）時回傳 None。 (+6 more)

### Community 14 - "LLMProvider"
Cohesion: 0.11
Nodes (6): LLMProvider, Return a human-readable display name for the given model ID. Subclasses should…, Return (is_valid, error_message)., Send a raw prompt to the LLM for a plain chat conversation. This is used by the…, Base class for streaming LLM commentary providers., Build the final prompt sent to the model from plain user text plus data.

### Community 15 - "KataGoAnalyzer"
Cohesion: 0.14
Nodes (5): KataGoAnalyzer, 將當前棋譜轉換成唯一的字串，作為快取的 Key, 用一致的 KataGo moves 格式生成快取 key，避免 stones/list 格式不一致造成 miss。, Ask KataGo to stop an analysis query immediately, then detach it., Remove already-queued responses belonging to a cancelled query.

### Community 16 - "TabManager"
Cohesion: 0.08
Nodes (9): Move one session and preserve which session is active., Restore the most recently closed session at the end of the list., 支援 tab_manager[idx] 取第 idx 個分頁。, 多分頁文件管理器：維護所有 TabSession 並提供 active session 切換。, 建立第一個分頁並設為 active。供 main 流程開機時呼叫一次。, 建立新分頁。若已達 MAX_TABS，回傳 None。, 關閉指定分頁；回傳 (success, reason)。 規則： - 至少保留一個分頁。 - 若傳入 index 為 active，自動切到鄰近分頁。, TabManager (+1 more)

### Community 17 - "MenuBar"
Cohesion: 0.21
Nodes (4): tkinter, MenuBar, Themeable, Tk-only application menu bar. This deliberately does not use native…, A small menu system built from Frames and Buttons. Menu definitions are plain…

### Community 18 - "BranchTreeView"
Cohesion: 0.12
Nodes (5): BranchCanvas, BranchTreeView, assign(), LLMSelectionDialog, Update only current-path colors after navigation. Node coordinates and static…

### Community 20 - "show_appearance_settings_dialog"
Cohesion: 0.22
Nodes (8): load_tk_image(), Load an image as a Tk image, preferring Pillow for broad format support., 依 board_shell 實際尺寸重新縮放外框背景圖片（cover 模式：填滿裁切）。 由 board_shell 的 <Configure>…, show_appearance_settings_dialog(), create_image_row(), browse_image(), use_default(), update_preview()

### Community 21 - "safe_get_system_info"
Cohesion: 0.15
Nodes (16): _format_bytes_as_gb(), _get_cpu_name(), _get_gpu_info(), _get_physical_core_count(), _get_ram_info(), _get_windows_display_version(), 把位元組數轉成 GB 字串；輸入不可用時回傳 Unknown。, 執行 PowerShell 並解析 JSON，失敗時回傳 None。 這裡只用於診斷資訊的 best-effort 查詢，任何錯誤都不能影響主 UI。 (+8 more)

### Community 22 - "I18n"
Cohesion: 0.11
Nodes (17): find_preset_tone(), get_all_tones(), get_tone_description(), get_tone_display_name(), get_tone_prompt(), Single-block LLM prompt templates for AI Go teacher commentary. The application…, Return the preset prompt in the requested UI language., Return the tone if prompt is an untouched preset, otherwise ``None``. (+9 more)

### Community 23 - "openrouter_provider.py"
Cohesion: 0.17
Nodes (7): discover_openrouter_models(), get_publisher_from_model_id(), group_models_by_publisher(), OpenRouterProvider, Return (True, model_ids) or (False, error_message)., get_openrouter_api_key(), Read OpenRouter API key from keyring first, then environment variables.

### Community 24 - "LLMChatWindow"
Cohesion: 0.09
Nodes (5): LLMChatWindow, 把使用者訊息回填輸入框，並截斷該則之後的所有對話。, 遞迴綁定滾輪事件，讓游標在卡片上也能捲動聊天區。, 輸入框獲得焦點時清除 placeholder。, 輸入框失去焦點時恢復 placeholder。

### Community 25 - "normalize_api_key"
Cohesion: 0.13
Nodes (19): keyring, os, discover_nim_models(), 向 NIM 端點 /v1/models 查詢可用模型清單。 成功時回傳 (True, [model_id, ...])；失敗時回傳 (False,…, get_nvidia_api_key(), normalize_api_key(), Trim whitespace and common quote wrappers from API key values., Read NVIDIA API key from keyring first, then environment variables. (+11 more)

### Community 26 - "Security Policy"
Cohesion: 0.10
Nodes (19): Accepted Reports, Declined Reports, In-Scope, Information to Include, Out-of-Scope, Reporting a Vulnerability, Response & Resolution Process, Scope (+11 more)

### Community 28 - "plot_window"
Cohesion: 0.11
Nodes (28): _analysis_lines(), _gtp(), _move_text(), Compact, factual Go-game context for LLM teaching prompts. This module…, Serialize only the selected mainline and explicitly named snapshots., serialize_board(), serialize_game_context(), serialize_mainline() (+20 more)

### Community 29 - "requirements.txt - Python Dependencies"
Cohesion: 0.29
Nodes (7): requirements.txt - Python Dependencies, httpx HTTP Client, keyring Package, matplotlib Package, ollama Python Package, opencc Chinese Conversion, Pillow (PIL) Package

### Community 30 - "show_system_info_dialog"
Cohesion: 0.13
Nodes (12): create_dev_menu(), _create_info_section(), _create_katago_section(), _create_labeled_row(), get_board_context_text(), 建立診斷資訊視窗中的單列 label/value。, 回傳目前棋盤局面的文字快照，供 LLM Chat Sandbox 附加為上下文。, Open the LLM Chat Sandbox window for provider connectivity testing. (+4 more)

### Community 31 - "get_runtime_data_root"
Cohesion: 0.26
Nodes (13): ensure_runtime_dir(), get_executable_dir(), get_katago_runtime_overrides(), get_runtime_data_root(), get_runtime_file_path(), is_frozen_app(), iter_dotenv_paths(), _iter_log_candidates() (+5 more)

### Community 36 - "chat_sandbox.py"
Cohesion: 0.18
Nodes (12): copy, json, pil, sys, time, traceback, 主題切換時由主程式呼叫：重繪所有開著的聊天視窗。, 讀取主程式目前主題（light/dark），失敗時退回 dark。 ConfigService 需要有狀態的 backend，無法獨立重新建立實例，… (+4 more)

### Community 38 - "start_analyzer_async"
Cohesion: 0.17
Nodes (16): auto_analyze(), get_config_display_name(), get_model_display_name(), is_analyzer_ready(), on_analyze_button_click(), poll_ai(), 直接使用記憶體中的數據更新 UI，並將所有分析結果保存到快取以供後續比較使用, set_analysis_controls_state() (+8 more)

### Community 39 - "main_v3.py"
Cohesion: 0.05
Nodes (44): collections, ctypes, dotenv, hashlib, itertools, logging, matplotlib, matplotlib_backends_backend_tkagg (+36 more)

### Community 41 - "._refresh_conversation_list"
Cohesion: 0.21
Nodes (3): _select(), on_change(), on_close()

### Community 43 - "build_menu_bar"
Cohesion: 0.09
Nodes (19): apply_theme(), recolor(), build_menu_bar(), set_language(), toggle_dev(), Refresh controls that expose the continuous-analysis state., Expose semantic theme tokens to legacy drawing code in this module., Apply a configured theme to existing widgets without restarting. (+11 more)

### Community 44 - "show_game_info_dialog"
Cohesion: 0.16
Nodes (14): datetime, get_game_info(), Helpers for editable SGF game-information properties., Return a normalized date or raise ValueError for a non-SGF date., Read the editable game-info fields without exposing the metadata dict., Update editable fields in place while preserving every other property., update_game_info(), validate_game_date() (+6 more)

### Community 47 - "t"
Cohesion: 0.09
Nodes (35): build_branch_section(), change_config_path(), change_katago_path(), change_model_path(), create_katago_startup_popup(), update_elapsed(), _create_ollama_model_row(), on_row_click() (+27 more)

### Community 48 - "MessageBubble"
Cohesion: 0.18
Nodes (8): _insert_inline_markdown(), MessageBubble, _action_btn(), _action_icon(), 把單行文字插入 Text widget，支援 **粗體**、*斜體*、`行內程式碼`。, 把 Markdown 內容渲染到 Text widget：標題 / 列表 / 粗斜體 / 行程式碼 / 程式碼區塊。, 依 wrap 後的 displayline 數調整 Text 高度，消除多餘空白。, render_markdown()

### Community 49 - "show_ollama_install_dialog"
Cohesion: 0.22
Nodes (8): detect_ollama_installed(), 在 Windows 上抑制子進程彈出的主控台視窗。 隱藏終端機 (windowed) 模式下，子進程預設會繼承一個可見的主控台， 即使…, 檢查系統是否能執行 `ollama --version`，回傳 (installed: bool, version_or_none), 顯示簡單的 Ollama 安裝引導對話框（包含開啟下載頁與重新檢測）。, update_ollama_install_status_label(), show_ollama_install_dialog(), recheck(), _silent_subprocess_kwargs()

### Community 50 - "materialize_bundled_runtime_file"
Cohesion: 0.38
Nodes (7): hide_path_on_windows(), _load_runtime_manifest(), materialize_bundled_runtime_file(), Copy bundled KataGo runtime files out of PyInstaller's _MEI directory. The…, _runtime_manifest_path(), _save_runtime_manifest(), _sha256_of_file()

### Community 51 - "_build_diagnostic_report_text"
Cohesion: 0.40
Nodes (5): _build_diagnostic_report_text(), _get_newest_log_file(), 讀取最新 log 的最後 max_lines 行；沒有 log 時回傳提示文字。, 組合 diagnostic_report.txt 的完整內容。, _read_recent_log_lines()

### Community 52 - "create_path_row"
Cohesion: 0.48
Nodes (5): create_path_row(), browse_path(), set_entry_value(), show_placeholder(), update_mode()

### Community 53 - "._apply_chat_palette_swap"
Cohesion: 0.29
Nodes (4): recolor(), _remove(), 主題切換：依舊色碼映射到新色碼，重繪整個視窗（含 Text tag 顏色）。, 依主題載入圖示：`_light.png` 用於淺色模式，`_dark.png` 用於深色模式。 若指定主題的圖示不存在，則退回另一主題版本；兩者皆無則設為…

### Community 54 - "show_find_dialog"
Cohesion: 0.29
Nodes (6): 開啟尋找對話框；已存在則聚焦並清空舊結果。, show_find_dialog(), _maybe_show_placeholder(), on_jump(), _show_placeholder(), _sync_query()

### Community 55 - "show_analysis_log_dialog"
Cohesion: 0.83
Nodes (4): show_analysis_log_dialog(), apply_highlighting(), on_confirm_click(), open_analysis_log_path()

## Knowledge Gaps
- **105 isolated node(s):** `Table of Contents`, `I Have a Question`, `Before Submitting a Bug Report`, `How Do I Submit a Good Bug Report?`, `Before Submitting an Enhancement` (+100 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 391 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMChatWindow` connect `LLMChatWindow` to `chat_sandbox.py`, `._start_generation`, `main_v3.py`, `._active_conversation`, `._refresh_conversation_list`, `._tr`, `.__init__`, `._build_ui`, `._apply_chat_palette_swap`, `show_system_info_dialog`?**
  _High betweenness centrality (0.155) - this node is a cross-community bridge._
- **Why does `GoBoard` connect `GoBoard` to `ConfigService`, `show_appearance_settings_dialog`, `main_v3.py`?**
  _High betweenness centrality (0.116) - this node is a cross-community bridge._
- **Why does `t()` connect `t` to `GoBoard`, `_show_llm_selection_dialog`, `refresh_tab_bar`, `_clear_selected_runtime_data`, `task`, `TabManager`, `BranchTreeView`, `show_appearance_settings_dialog`, `normalize_api_key`, `plot_window`, `show_system_info_dialog`, `get_runtime_data_root`, `start_analyzer_async`, `main_v3.py`, `build_menu_bar`, `show_game_info_dialog`, `show_ollama_install_dialog`, `create_path_row`, `show_find_dialog`, `show_analysis_log_dialog`?**
  _High betweenness centrality (0.081) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `t()` (e.g. with `set_llm_tone()` and `show_chat_sandbox()`) actually correct?**
  _`t()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `_show_llm_selection_dialog()` (e.g. with `ProviderFactory` and `apply_settings()`) actually correct?**
  _`_show_llm_selection_dialog()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 25 inferred relationships involving `build_menu_bar()` (e.g. with `palette()` and `toggle_branch_panel()`) actually correct?**
  _`build_menu_bar()` has 25 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Table of Contents`, `I Have a Question`, `Before Submitting a Bug Report` to the rest of the system?**
  _105 weakly-connected nodes found - possible documentation gaps or missing edges._