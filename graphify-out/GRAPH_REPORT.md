# Graph Report - AIGoTeacher  (2026-08-14)

## Corpus Check
- 25 files · ~48,871 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 737 nodes · 1467 edges · 44 communities (33 shown, 11 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 96 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0fe76d02`
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

## God Nodes (most connected - your core abstractions)
1. `t()` - 64 edges
2. `GoBoard` - 60 edges
3. `LLMChatWindow` - 43 edges
4. `ConfigService` - 34 edges
5. `ProviderFactory` - 34 edges
6. `FakeMenuBar` - 29 edges
7. `build_menu_bar()` - 27 edges
8. `LLMProvider` - 24 edges
9. `OllamaProvider` - 23 edges
10. `KataGoAnalyzer` - 22 edges

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

## Communities (44 total, 11 thin omitted)

### Community 0 - "t"
Cohesion: 0.14
Nodes (25): build_menu_bar(), _confirm_and_download_ollama_model(), _download_ollama_model(), get_config_display_name(), get_model_display_name(), new_game(), on_closing(), open_feedback_form() (+17 more)

### Community 1 - "GoBoard"
Cohesion: 0.07
Nodes (13): GoBoard, load_tk_image(), _on_board_shell_configure(), on_mouse_wheel(), Load an image as a Tk image, preferring Pillow for broad format support., 依 board_shell 實際尺寸重新縮放外框背景圖片（cover 模式：填滿裁切）。          由 board_shell 的 <Configu, 動態生成歷史落子紀錄，不會再因為提子而消失，確保 AI 判斷正確, Return 1-based move index where the current branch starts, or None on main line. (+5 more)

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
Cohesion: 0.08
Nodes (9): OllamaProvider, get_ollama_manager(), OllamaManager, OllamaModelInfo, Return (models, error), retaining the last good catalog on failure., Read a model without triggering network I/O., Start a streaming REST pull for a local model., REST client and catalog cache for the local Ollama service. (+1 more)

### Community 6 - "get_runtime_data_root"
Cohesion: 0.22
Nodes (14): _delete_runtime_path(), get_executable_dir(), get_runtime_data_root(), get_runtime_file_path(), is_frozen_app(), iter_dotenv_paths(), _iter_log_candidates(), load_runtime_dotenv() (+6 more)

### Community 8 - "KataGoAnalyzer"
Cohesion: 0.11
Nodes (11): get_commentary_from_cache(), GoDataFilter, KataGoAnalyzer, poll_ai(), 將當前棋譜轉換成唯一的字串，作為快取的 Key, 用一致的 KataGo moves 格式生成快取 key，避免 stones/list 格式不一致造成 miss。, Ask KataGo to stop an analysis query immediately, then detach it., Remove already-queued responses belonging to a cancelled query. (+3 more)

### Community 9 - "ConfigService"
Cohesion: 0.11
Nodes (8): ConfigService, Small wrapper around persisted UI settings., Migrate settings from the removed GitHub Models provider., detect_system_theme(), normalize_theme(), Application color themes and Windows system-theme resolution., Return the Windows theme at process startup; safely fall back to light., resolve_theme()

### Community 10 - "safe_get_system_info"
Cohesion: 0.15
Nodes (16): _format_bytes_as_gb(), _get_cpu_name(), _get_gpu_info(), _get_physical_core_count(), _get_ram_info(), _get_windows_display_version(), 把位元組數轉成 GB 字串；輸入不可用時回傳 Unknown。, 執行 PowerShell 並解析 JSON，失敗時回傳 None。      這裡只用於診斷資訊的 best-effort 查詢，任何錯誤都不能影響主 U (+8 more)

### Community 11 - "ProviderFactory"
Cohesion: 0.09
Nodes (11): ProviderFactory, Return the human-readable display name for a model ID.          Falls back to, Reverse lookup: display name → model ID.          Returns None when the displa, Return [(display_name, model_id), ...] for UI widgets.          The list follo, 向 NIM 端點探索可用模型，失敗時降級至內建清單。          回傳 (model_ids, used_fallback, error_messag, 從 model_id 清單取出 publisher 清單（已排序、去重）。, 取得指定 publisher 下的 model_id 清單（保持原始順序）。, 從 model_id 拆出 publisher（供 UI 還原選擇用）。 (+3 more)

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
Cohesion: 0.18
Nodes (12): discover_openrouter_models(), Return (True, model_ids) or (False, error_message)., get_nvidia_api_key(), get_openrouter_api_key(), normalize_api_key(), Trim whitespace and common quote wrappers from API key values., Read NVIDIA API key from keyring first, then environment variables., Store NVIDIA API key in the OS keyring. Does not write to .env. (+4 more)

### Community 21 - "version.py"
Cohesion: 0.16
Nodes (12): Path, I18n, resource_path(), main(), Application version helpers for AI Go Teacher.  Run this file to update every, Return the numeric tuple used by PyInstaller's VSVersionInfo., _replace_once(), sync_version() (+4 more)

### Community 22 - "github_provider.py"
Cohesion: 0.26
Nodes (8): discover_nim_models(), get_publisher_from_model_id(), group_models_by_publisher(), 從 model_id 拆出 publisher（第一個 '/' 之前的部分）。      無 '/' 的 model_id 歸類為 "unknown"，確保, 將 model_id 清單依 publisher 分組，回傳 {publisher: [model_id, ...]}。      保持各 publishe, 向 NIM 端點 /v1/models 查詢可用模型清單。      成功時回傳 (True, [model_id, ...])；失敗時回傳 (False,, get_publisher_from_model_id(), group_models_by_publisher()

### Community 23 - "materialize_bundled_runtime_file"
Cohesion: 0.29
Nodes (7): create_dev_menu(), export_diagnostic_report(), _open_folder(), 顯示診斷報告匯出完成訊息與開啟資料夾按鈕。, 匯出診斷報告到 diagnostics/diagnostic_report.txt。, Return Dev menu items for the themeable menu bar., _show_diagnostic_export_success()

### Community 24 - "main_v3.py"
Cohesion: 0.11
Nodes (23): change_config_path(), change_katago_path(), change_model_path(), _create_info_section(), _create_katago_section(), create_katago_startup_popup(), _create_labeled_row(), _create_ollama_model_row() (+15 more)

### Community 25 - "version.py"
Cohesion: 0.06
Nodes (33): _capture_board_snapshot(), _close_tab_silently(), _copy_game_tree(), GameNode, hydrate_active_session(), on_close_tab_click(), on_copy_tab_click(), on_new_tab_click() (+25 more)

### Community 27 - "set_winrate_text"
Cohesion: 0.23
Nodes (3): FakeMenuBar, Themeable, Tk-only application menu bar.  This deliberately does not use native, A small menu system built from Frames and Buttons.      Menu definitions are pla

### Community 28 - "_build_diagnostic_report_text"
Cohesion: 0.19
Nodes (13): find_preset_tone(), get_all_tones(), get_tone_description(), get_tone_display_name(), get_tone_prompt(), Single-block LLM prompt templates for AI Go teacher commentary.  The application, Return the preset prompt in the requested UI language., Return the tone if prompt is an untouched preset, otherwise ``None``. (+5 more)

### Community 29 - "materialize_bundled_runtime_file"
Cohesion: 0.21
Nodes (11): ensure_runtime_dir(), get_config_path(), get_katago_path(), get_katago_runtime_overrides(), get_model_path(), hide_path_on_windows(), materialize_bundled_runtime_file(), Copy bundled KataGo runtime files out of PyInstaller's _MEI directory.      Th (+3 more)

### Community 36 - "_handle_score_estimate_result"
Cohesion: 0.29
Nodes (9): _handle_score_estimate_result(), on_close_score_estimate_click(), on_score_estimate_click(), show_score_estimate_popup(), start_score_analyzer_async(), _start_score_estimate_query(), summarize_score_estimate(), update_score_estimate_button_label() (+1 more)

### Community 37 - "show_first_run_onboarding_dialog"
Cohesion: 0.29
Nodes (8): _delete_api_key(), delete_nvidia_api_key(), delete_openrouter_api_key(), Delete one application credential, treating a missing credential as success., Delete the NVIDIA API key owned by this application., Delete the OpenRouter API key owned by this application., _clear_selected_runtime_data(), Stop engine processes and clear selected data, returning result rows.

### Community 38 - "add_to_commentary_cache"
Cohesion: 0.50
Nodes (4): detect_ollama_installed(), 在 Windows 上抑制子進程彈出的主控台視窗。      隱藏終端機 (windowed) 模式下，子進程預設會繼承一個可見的主控台，     即使, 檢查系統是否能執行 `ollama --version`，回傳 (installed: bool, version_or_none), _silent_subprocess_kwargs()

### Community 39 - "detect_ollama_installed"
Cohesion: 0.36
Nodes (8): auto_analyze(), is_analyzer_ready(), on_analyze_button_click(), 分析整盤棋並回傳每手的勝率列表 (複用全局 KataGo analyzer，支援取消與進度回報), run_full_game_analysis(), set_winrate_text(), show_analyzer_not_ready(), show_winrate_chart()

### Community 40 - "show_first_run_onboarding_dialog"
Cohesion: 0.15
Nodes (12): _build_diagnostic_report_text(), _get_newest_log_file(), 首次啟動時彈出的強制 Modal Onboarding 視窗。      內容：     - 語言選擇（必填，Radiobutton 兩選一）, 安全取得目前 AI 提供商、模型與語言設定。, 讀取最新 log 的最後 max_lines 行；沒有 log 時回傳提示文字。, 組合 diagnostic_report.txt 的完整內容。, Open the LLM Chat Sandbox window for provider connectivity testing., _read_recent_log_lines() (+4 more)

### Community 41 - "refresh_language"
Cohesion: 0.20
Nodes (12): apply_theme(), on_load_sgf_click(), Refresh controls that expose the continuous-analysis state., Expose semantic theme tokens to legacy drawing code in this module., 歡迎頁隱藏棋局操作能力，但保留檔案選單與中央兩個入口。, Apply a configured theme to existing widgets without restarting., rebuild_menu_bar(), refresh_language() (+4 more)

### Community 42 - "render_teacher_ui"
Cohesion: 0.33
Nodes (6): 只更新老師解說區，不改動生成中的快取狀態。, LLM Provider 的串流回呼；累積全文但在回放時不覆蓋既有解說。, Refresh a known static teacher prompt without touching LLM output., refresh_teacher_static_message(), render_teacher_ui(), update_teacher_ui()

### Community 43 - "add_to_commentary_cache"
Cohesion: 0.50
Nodes (4): add_to_commentary_cache(), on_commentary_generation_complete(), 【Phase 1】LLM 生成完成後的回呼 — 將完整的解說存儲到快取, 將解說文本新增到快取 (執行緒安全，儲存全部手數)

## Knowledge Gaps
- **105 isolated node(s):** `Table of Contents`, `I Have a Question`, `Before Submitting a Bug Report`, `How Do I Submit a Good Bug Report?`, `Before Submitting an Enhancement` (+100 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ProviderFactory` connect `ProviderFactory` to `GoBoard`, `OllamaProvider`, `BranchTreeView`, `show_first_run_onboarding_dialog`, `KataGoAnalyzer`, `main_v3.py`, `github_provider.py`, `main_v3.py`, `version.py`, `NvidiaProvider`, `materialize_bundled_runtime_file`?**
  _High betweenness centrality (0.107) - this node is a cross-community bridge._
- **Why does `GoBoard` connect `GoBoard` to `t`, `LLMChatWindow`, `_handle_score_estimate_result`, `BranchTreeView`, `ConfigService`, `ProviderFactory`, `version.py`, `main_v3.py`, `version.py`, `set_winrate_text`?**
  _High betweenness centrality (0.105) - this node is a cross-community bridge._
- **Why does `LLMChatWindow` connect `LLMChatWindow` to `GoBoard`, `BranchTreeView`, `KataGoAnalyzer`, `show_first_run_onboarding_dialog`, `ProviderFactory`, `main_v3.py`, `version.py`, `materialize_bundled_runtime_file`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `t()` (e.g. with `set_llm_tone()` and `show_chat_sandbox()`) actually correct?**
  _`t()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `GoBoard` (e.g. with `ConfigService` and `ProviderFactory`) actually correct?**
  _`GoBoard` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `LLMChatWindow` (e.g. with `BranchCanvas` and `BranchTreeView`) actually correct?**
  _`LLMChatWindow` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `ConfigService` (e.g. with `BranchCanvas` and `BranchTreeView`) actually correct?**
  _`ConfigService` has 10 INFERRED edges - model-reasoned connections that need verification._