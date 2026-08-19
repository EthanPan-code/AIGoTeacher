# Graph Report - AIGoTeacher  (2026-08-15)

## Corpus Check
- 25 files · ~49,012 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 740 nodes · 1475 edges · 54 communities (41 shown, 13 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 96 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5b7b8f26`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- t
- GoBoard
- LLMProvider
- requirements.txt - Python Dependencies
- LLMChatWindow
- OllamaProvider
- get_runtime_data_root
- BranchTreeView
- KataGoAnalyzer
- ConfigService
- safe_get_system_info
- ProviderFactory
- AI 圍棋老師 / AI Go Teacher
- add_to_commentary_cache
- Available Status Screenshot
- Download UI Screenshot
- Contributing to AI Go Teacher / 為 AI Go Teacher 貢獻
- main_v3.py
- OllamaManager
- _show_llm_selection_dialog
- version.py
- github_provider.py
- materialize_bundled_runtime_file
- main_v3.py
- version.py
- NvidiaProvider
- set_winrate_text
- _build_diagnostic_report_text
- materialize_bundled_runtime_file
- Cloud API Illustration
- GitHub Models Provider
- Interactive Board Feature
- Live Analysis Feature
- LLM Commentary Feature
- SGF Support Feature
- _handle_score_estimate_result
- show_first_run_onboarding_dialog
- add_to_commentary_cache
- detect_ollama_installed
- show_first_run_onboarding_dialog
- refresh_language
- render_teacher_ui
- add_to_commentary_cache
- _close_tab_silently
- OllamaProvider
- .rebuild_board
- .on_state_change
- GameNode
- _show_llm_selection_dialog
- show_first_run_onboarding_dialog
- get_publisher_from_model_id
- ._resize_frame_background
- on_closing

## God Nodes (most connected - your core abstractions)
1. `t()` - 66 edges
2. `GoBoard` - 60 edges
3. `LLMChatWindow` - 43 edges
4. `ConfigService` - 34 edges
5. `ProviderFactory` - 34 edges
6. `FakeMenuBar` - 29 edges
7. `build_menu_bar()` - 27 edges
8. `LLMProvider` - 24 edges
9. `OllamaProvider` - 23 edges
10. `BranchTreeView` - 23 edges

## Surprising Connections (you probably didn't know these)
- `Framework Architecture Diagram` --conceptually_related_to--> `KataGo v1.16.4 Engine`  [INFERRED]
  README_img/framework.png → README.md
- `ollama Python Package` --semantically_similar_to--> `Ollama Provider`  [INFERRED] [semantically similar]
  requirements.txt → README.md
- `Cloud API Illustration` --conceptually_related_to--> `NVIDIA NIM Provider`  [INFERRED]
  image/cloud.png → README.md
- `version_info.txt - PyInstaller VSVersionInfo` --semantically_similar_to--> `PyInstaller Packaging`  [INFERRED] [semantically similar]
  version_info.txt → README.md
- `matplotlib Package` --semantically_similar_to--> `Matplotlib Visualization`  [INFERRED] [semantically similar]
  requirements.txt → README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Multi-Provider LLM System** — readme_llm_commentary, readme_ollama_provider, readme_nvidia_nim_provider, readme_github_models_provider [EXTRACTED 1.00]

## Communities (54 total, 13 thin omitted)

### Community 0 - "t"
Cohesion: 0.15
Nodes (24): build_menu_bar(), _confirm_and_download_ollama_model(), _download_ollama_model(), get_config_display_name(), get_model_display_name(), open_feedback_form(), plot_window(), 顯示簡單的 Ollama 安裝引導對話框（包含開啟下載頁與重新檢測）。 (+16 more)

### Community 1 - "GoBoard"
Cohesion: 0.18
Nodes (3): GoBoard, 動態生成歷史落子紀錄，不會再因為提子而消失，確保 AI 判斷正確, Return 1-based move index where the current branch starts, or None on main line.

### Community 2 - "LLMProvider"
Cohesion: 0.11
Nodes (6): LLMProvider, Return a human-readable display name for the given model ID.          Subclasses, Return (is_valid, error_message)., Send a raw prompt to the LLM for a plain chat conversation.          This is use, Base class for streaming LLM commentary providers., Build the final prompt sent to the model from plain user text plus data.

### Community 3 - "requirements.txt - Python Dependencies"
Cohesion: 0.18
Nodes (11): Matplotlib Visualization, Ollama Provider, PyInstaller Packaging, requirements.txt - Python Dependencies, httpx HTTP Client, keyring Package, matplotlib Package, ollama Python Package (+3 more)

### Community 4 - "LLMChatWindow"
Cohesion: 0.11
Nodes (3): LLMChatWindow, 輸入框獲得焦點時清除 placeholder。, 輸入框失去焦點時恢復 placeholder。

### Community 5 - "OllamaProvider"
Cohesion: 0.13
Nodes (7): OllamaManager, OllamaModelInfo, Return (models, error), retaining the last good catalog on failure., Read a model without triggering network I/O., Start a streaming REST pull for a local model., REST client and catalog cache for the local Ollama service., Return (available, version_or_error) without changing the catalog.

### Community 6 - "get_runtime_data_root"
Cohesion: 0.18
Nodes (17): _delete_runtime_path(), ensure_runtime_dir(), get_executable_dir(), get_katago_runtime_overrides(), get_runtime_data_root(), get_runtime_file_path(), hide_path_on_windows(), is_frozen_app() (+9 more)

### Community 8 - "KataGoAnalyzer"
Cohesion: 0.13
Nodes (7): GoDataFilter, KataGoAnalyzer, 將當前棋譜轉換成唯一的字串，作為快取的 Key, 用一致的 KataGo moves 格式生成快取 key，避免 stones/list 格式不一致造成 miss。, Ask KataGo to stop an analysis query immediately, then detach it., Remove already-queued responses belonging to a cancelled query., 【改進】從快取中查詢上一手 (turn-1) 的分析結果，取出勝率和目數作為基準                  Args:             t

### Community 9 - "ConfigService"
Cohesion: 0.11
Nodes (8): ConfigService, Small wrapper around persisted UI settings., Migrate settings from the removed GitHub Models provider., detect_system_theme(), normalize_theme(), Application color themes and Windows system-theme resolution., Return the Windows theme at process startup; safely fall back to light., resolve_theme()

### Community 10 - "safe_get_system_info"
Cohesion: 0.13
Nodes (18): _build_diagnostic_report_text(), _format_bytes_as_gb(), _get_cpu_name(), _get_gpu_info(), _get_physical_core_count(), _get_ram_info(), _get_windows_display_version(), 把位元組數轉成 GB 字串；輸入不可用時回傳 Unknown。 (+10 more)

### Community 11 - "ProviderFactory"
Cohesion: 0.13
Nodes (6): ProviderFactory, Reverse lookup: display name → model ID.          Returns None when the displa, Return [(display_name, model_id), ...] for UI widgets.          The list follo, 向 NIM 端點探索可用模型，失敗時降級至內建清單。          回傳 (model_ids, used_fallback, error_messag, 從 model_id 清單取出 publisher 清單（已排序、去重）。, 取得指定 publisher 下的 model_id 清單（保持原始順序）。

### Community 12 - "AI 圍棋老師 / AI Go Teacher"
Cohesion: 0.04
Nodes (45): AI 圍棋老師 / AI Go Teacher, Communication Protocols, Contents, Core Capabilities, Core Modules, Custom Teaching Tones, Development Commands, Download the Executable (Windows) (+37 more)

### Community 13 - "add_to_commentary_cache"
Cohesion: 0.07
Nodes (27): API Key Security, API key 安全性, Automatic Migration of Legacy Settings, Available Alternatives, Frequently Asked Questions, GitHub Models Still Appears After Startup, LLM 提供來源遷移指南 / LLM Provider Migration Guide, OpenRouter Returns HTTP 402 (+19 more)

### Community 17 - "Contributing to AI Go Teacher / 為 AI Go Teacher 貢獻"
Cohesion: 0.05
Nodes (37): Acknowledgments, Before Submitting a Bug Report, Before Submitting an Enhancement, Commit Messages, Commit 訊息, Contributing to AI Go Teacher / 為 AI Go Teacher 貢獻, Development Environment Setup, How Do I Submit a Good Bug Report? (+29 more)

### Community 19 - "OllamaManager"
Cohesion: 0.18
Nodes (10): Accepted Reports, Declined Reports, In-Scope, Information to Include, Out-of-Scope, Reporting a Vulnerability, Response & Resolution Process, Scope (+2 more)

### Community 20 - "_show_llm_selection_dialog"
Cohesion: 0.27
Nodes (8): discover_nim_models(), 向 NIM 端點 /v1/models 查詢可用模型清單。      成功時回傳 (True, [model_id, ...])；失敗時回傳 (False,, get_nvidia_api_key(), get_openrouter_api_key(), normalize_api_key(), Trim whitespace and common quote wrappers from API key values., Read NVIDIA API key from keyring first, then environment variables., Read OpenRouter API key from keyring first, then environment variables.

### Community 21 - "version.py"
Cohesion: 0.16
Nodes (12): Path, I18n, resource_path(), main(), Application version helpers for AI Go Teacher.  Run this file to update every, Return the numeric tuple used by PyInstaller's VSVersionInfo., _replace_once(), sync_version() (+4 more)

### Community 22 - "github_provider.py"
Cohesion: 0.31
Nodes (4): discover_openrouter_models(), get_publisher_from_model_id(), group_models_by_publisher(), Return (True, model_ids) or (False, error_message).

### Community 23 - "materialize_bundled_runtime_file"
Cohesion: 0.15
Nodes (13): create_dev_menu(), _create_info_section(), _create_katago_section(), _create_labeled_row(), export_diagnostic_report(), _open_folder(), 建立診斷資訊視窗中的單列 label/value。, 顯示診斷報告匯出完成訊息與開啟資料夾按鈕。 (+5 more)

### Community 24 - "main_v3.py"
Cohesion: 0.25
Nodes (8): change_config_path(), change_katago_path(), change_model_path(), create_katago_startup_popup(), 重新初始化分析器（關閉舊進程，建立新進程）, reinitialize_analyzer(), set_analysis_controls_state(), start_analyzer_async()

### Community 25 - "version.py"
Cohesion: 0.08
Nodes (12): on_close_tab_click(), 關閉分頁：dirty 時彈出 三選一（儲存 / 不儲存 / 取消）。      為了在關閉流程內支援 "儲存" 動作，會先暫時把這個分頁切為 active，, 彈出儲存 / 不儲存 / 取消 三選一對話框，回傳 'save' / 'discard' / 'cancel'。, 多分頁文件管理器：維護所有 TabSession 並提供 active session 切換。, 建立第一個分頁並設為 active。供 main 流程開機時呼叫一次。, 關閉指定分頁；回傳 (success, reason)。          規則：           - 至少保留一個分頁。           -, 支援 tab_manager[idx] 取第 idx 個分頁。, _show_close_tab_dialog() (+4 more)

### Community 27 - "set_winrate_text"
Cohesion: 0.23
Nodes (3): FakeMenuBar, Themeable, Tk-only application menu bar.  This deliberately does not use native, A small menu system built from Frames and Buttons.      Menu definitions are pla

### Community 28 - "_build_diagnostic_report_text"
Cohesion: 0.19
Nodes (13): find_preset_tone(), get_all_tones(), get_tone_description(), get_tone_display_name(), get_tone_prompt(), Single-block LLM prompt templates for AI Go teacher commentary.  The application, Return the preset prompt in the requested UI language., Return the tone if prompt is an untouched preset, otherwise ``None``. (+5 more)

### Community 29 - "materialize_bundled_runtime_file"
Cohesion: 0.36
Nodes (7): get_config_path(), get_katago_path(), get_model_path(), materialize_bundled_runtime_file(), Copy bundled KataGo runtime files out of PyInstaller's _MEI directory.      Th, 安全取得 KataGo 執行檔、設定檔、模型檔路徑與存在狀態。, safe_get_katago_info()

### Community 36 - "_handle_score_estimate_result"
Cohesion: 0.11
Nodes (23): _create_ollama_model_row(), _get_newest_log_file(), _handle_score_estimate_result(), _load_ollama_icon(), needs_first_run_onboarding(), on_close_score_estimate_click(), on_score_estimate_click(), Switch language and migrate only an untouched preset custom prompt. (+15 more)

### Community 37 - "show_first_run_onboarding_dialog"
Cohesion: 0.31
Nodes (8): _delete_api_key(), delete_nvidia_api_key(), delete_openrouter_api_key(), Delete one application credential, treating a missing credential as success., Delete the NVIDIA API key owned by this application., Delete the OpenRouter API key owned by this application., _clear_selected_runtime_data(), Stop engine processes and clear selected data, returning result rows.

### Community 38 - "add_to_commentary_cache"
Cohesion: 0.50
Nodes (4): detect_ollama_installed(), 在 Windows 上抑制子進程彈出的主控台視窗。      隱藏終端機 (windowed) 模式下，子進程預設會繼承一個可見的主控台，     即使, 檢查系統是否能執行 `ollama --version`，回傳 (installed: bool, version_or_none), _silent_subprocess_kwargs()

### Community 39 - "detect_ollama_installed"
Cohesion: 0.24
Nodes (10): auto_analyze(), is_analyzer_ready(), on_analyze_button_click(), poll_ai(), 分析整盤棋並回傳每手的勝率列表 (複用全局 KataGo analyzer，支援取消與進度回報), run_full_game_analysis(), ScoreAnalyzer, set_winrate_text() (+2 more)

### Community 40 - "show_first_run_onboarding_dialog"
Cohesion: 0.29
Nodes (6): Return the human-readable display name for a model ID.          Falls back to, 安全取得目前 AI 提供商、模型與語言設定。, Open the LLM Chat Sandbox window for provider connectivity testing., safe_get_ai_config(), show_chat_sandbox(), update_llm_model_label()

### Community 41 - "refresh_language"
Cohesion: 0.33
Nodes (7): Refresh controls that expose the continuous-analysis state., Refresh a known static teacher prompt without touching LLM output., rebuild_menu_bar(), refresh_language(), refresh_teacher_static_message(), render_winrate_text(), update_continuous_analysis_ui()

### Community 42 - "render_teacher_ui"
Cohesion: 0.21
Nodes (6): get_commentary_from_cache(), new_game(), 直接使用記憶體中的數據更新 UI，並將所有分析結果保存到快取以供後續比較使用, 只更新老師解說區，不改動生成中的快取狀態。, render_teacher_ui(), update_ui_with_data()

### Community 43 - "add_to_commentary_cache"
Cohesion: 0.50
Nodes (4): add_to_commentary_cache(), on_commentary_generation_complete(), 【Phase 1】LLM 生成完成後的回呼 — 將完整的解說存儲到快取, 將解說文本新增到快取 (執行緒安全，儲存全部手數)

### Community 44 - "_close_tab_silently"
Cohesion: 0.13
Nodes (22): _capture_board_snapshot(), _close_tab_silently(), _copy_game_tree(), hydrate_active_session(), on_copy_tab_click(), on_new_tab_click(), on_tab_click(), Stop the active continuous query and clear its routing state. (+14 more)

### Community 47 - ".on_state_change"
Cohesion: 0.22
Nodes (4): on_mouse_wheel(), 切換同一手棋的不同變化圖 (direction: 1 或 -1), 跳轉到樹上的任意節點，並回填各層 active_child_idx。, 【修復】回放模式下，從快取顯示當前手數的解說；無快取則清空。                  此方法統一處理 undo / redo / switch_b

### Community 48 - "GameNode"
Cohesion: 0.20
Nodes (5): apply_theme(), GameNode, on_load_sgf_click(), 讀取 SGF 並正確建立分支樹狀結構，同時恢復註解到快取【Phase 3】修正版本, Apply a configured theme to existing widgets without restarting.

### Community 49 - "_show_llm_selection_dialog"
Cohesion: 0.25
Nodes (3): BranchCanvas, LLMSelectionDialog, _show_llm_selection_dialog()

### Community 50 - "show_first_run_onboarding_dialog"
Cohesion: 0.29
Nodes (6): Store NVIDIA API key in the OS keyring. Does not write to .env., Store OpenRouter API key in the OS keyring. Does not write to .env., set_nvidia_api_key(), set_openrouter_api_key(), 首次啟動時彈出的強制 Modal Onboarding 視窗。      內容：     - 語言選擇（必填，Radiobutton 兩選一）, show_first_run_onboarding_dialog()

### Community 51 - "get_publisher_from_model_id"
Cohesion: 0.33
Nodes (5): get_publisher_from_model_id(), group_models_by_publisher(), 從 model_id 拆出 publisher（第一個 '/' 之前的部分）。      無 '/' 的 model_id 歸類為 "unknown"，確保, 將 model_id 清單依 publisher 分組，回傳 {publisher: [model_id, ...]}。      保持各 publishe, 從 model_id 拆出 publisher（供 UI 還原選擇用）。

### Community 52 - "._resize_frame_background"
Cohesion: 0.40
Nodes (4): load_tk_image(), _on_board_shell_configure(), Load an image as a Tk image, preferring Pillow for broad format support., 依 board_shell 實際尺寸重新縮放外框背景圖片（cover 模式：填滿裁切）。          由 board_shell 的 <Configu

### Community 53 - "on_closing"
Cohesion: 0.50
Nodes (3): on_closing(), Start a fresh application instance, then close the current one., restart_application()

## Knowledge Gaps
- **105 isolated node(s):** `Table of Contents`, `I Have a Question`, `Before Submitting a Bug Report`, `How Do I Submit a Good Bug Report?`, `Before Submitting an Enhancement` (+100 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ProviderFactory` connect `ProviderFactory` to `GoBoard`, `_handle_score_estimate_result`, `BranchTreeView`, `show_first_run_onboarding_dialog`, `KataGoAnalyzer`, `detect_ollama_installed`, `OllamaProvider`, `GameNode`, `_show_llm_selection_dialog`, `main_v3.py`, `show_first_run_onboarding_dialog`, `get_publisher_from_model_id`, `github_provider.py`, `version.py`, `NvidiaProvider`?**
  _High betweenness centrality (0.106) - this node is a cross-community bridge._
- **Why does `GoBoard` connect `GoBoard` to `t`, `_handle_score_estimate_result`, `LLMChatWindow`, `BranchTreeView`, `ConfigService`, `render_teacher_ui`, `ProviderFactory`, `.rebuild_board`, `.on_state_change`, `GameNode`, `._resize_frame_background`, `version.py`, `set_winrate_text`?**
  _High betweenness centrality (0.104) - this node is a cross-community bridge._
- **Why does `LLMChatWindow` connect `LLMChatWindow` to `GoBoard`, `_handle_score_estimate_result`, `BranchTreeView`, `KataGoAnalyzer`, `detect_ollama_installed`, `show_first_run_onboarding_dialog`, `GameNode`, `_show_llm_selection_dialog`, `version.py`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `t()` (e.g. with `set_llm_tone()` and `show_chat_sandbox()`) actually correct?**
  _`t()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `GoBoard` (e.g. with `ConfigService` and `ProviderFactory`) actually correct?**
  _`GoBoard` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `LLMChatWindow` (e.g. with `BranchCanvas` and `BranchTreeView`) actually correct?**
  _`LLMChatWindow` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `ConfigService` (e.g. with `BranchCanvas` and `BranchTreeView`) actually correct?**
  _`ConfigService` has 10 INFERRED edges - model-reasoned connections that need verification._