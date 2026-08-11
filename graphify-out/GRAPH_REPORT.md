# Graph Report - AIGoTeacher  (2026-08-10)

## Corpus Check
- 25 files · ~46,138 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 690 nodes · 1345 edges · 41 communities (29 shown, 12 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 93 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2bcec5d5`
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
- .get_nim_publisher_for_model

## God Nodes (most connected - your core abstractions)
1. `GoBoard` - 57 edges
2. `t()` - 54 edges
3. `LLMChatWindow` - 43 edges
4. `ConfigService` - 34 edges
5. `ProviderFactory` - 34 edges
6. `FakeMenuBar` - 29 edges
7. `build_menu_bar()` - 26 edges
8. `LLMProvider` - 24 edges
9. `OllamaProvider` - 23 edges
10. `BranchTreeView` - 22 edges

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

## Communities (41 total, 12 thin omitted)

### Community 0 - "t"
Cohesion: 0.18
Nodes (16): change_config_path(), change_katago_path(), change_model_path(), create_katago_startup_popup(), get_config_display_name(), get_model_display_name(), _open_folder(), 重新初始化分析器（關閉舊進程，建立新進程） (+8 more)

### Community 1 - "GoBoard"
Cohesion: 0.06
Nodes (14): GameNode, GoBoard, load_tk_image(), _on_board_shell_configure(), on_mouse_wheel(), 依 board_shell 實際尺寸重新縮放外框背景圖片（cover 模式：填滿裁切）。          由 board_shell 的 <Configu, 動態生成歷史落子紀錄，不會再因為提子而消失，確保 AI 判斷正確, Return 1-based move index where the current branch starts, or None on main line. (+6 more)

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
Cohesion: 0.10
Nodes (30): _build_diagnostic_report_text(), create_dev_menu(), ensure_runtime_dir(), export_diagnostic_report(), get_config_path(), get_executable_dir(), get_katago_path(), get_katago_runtime_overrides() (+22 more)

### Community 8 - "KataGoAnalyzer"
Cohesion: 0.14
Nodes (8): get_commentary_from_cache(), GoDataFilter, KataGoAnalyzer, 將當前棋譜轉換成唯一的字串，作為快取的 Key, 用一致的 KataGo moves 格式生成快取 key，避免 stones/list 格式不一致造成 miss。, 【改進】從快取中查詢上一手 (turn-1) 的分析結果，取出勝率和目數作為基準                  Args:             t, 直接使用記憶體中的數據更新 UI，並將所有分析結果保存到快取以供後續比較使用, update_ui_with_data()

### Community 9 - "ConfigService"
Cohesion: 0.11
Nodes (8): ConfigService, Small wrapper around persisted UI settings., Migrate settings from the removed GitHub Models provider., detect_system_theme(), normalize_theme(), Application color themes and Windows system-theme resolution., Return the Windows theme at process startup; safely fall back to light., resolve_theme()

### Community 10 - "safe_get_system_info"
Cohesion: 0.15
Nodes (16): _format_bytes_as_gb(), _get_cpu_name(), _get_gpu_info(), _get_physical_core_count(), _get_ram_info(), _get_windows_display_version(), 把位元組數轉成 GB 字串；輸入不可用時回傳 Unknown。, 執行 PowerShell 並解析 JSON，失敗時回傳 None。      這裡只用於診斷資訊的 best-effort 查詢，任何錯誤都不能影響主 U (+8 more)

### Community 11 - "ProviderFactory"
Cohesion: 0.09
Nodes (12): ProviderFactory, Return the human-readable display name for a model ID.          Falls back to, Reverse lookup: display name → model ID.          Returns None when the displa, Return [(display_name, model_id), ...] for UI widgets.          The list follo, 向 NIM 端點探索可用模型，失敗時降級至內建清單。          回傳 (model_ids, used_fallback, error_messag, 從 model_id 清單取出 publisher 清單（已排序、去重）。, 取得指定 publisher 下的 model_id 清單（保持原始順序）。, 安全取得目前 AI 提供商、模型與語言設定。 (+4 more)

### Community 12 - "AI 圍棋老師 / AI Go Teacher"
Cohesion: 0.04
Nodes (45): AI 圍棋老師 / AI Go Teacher, Communication Protocols, Contents, Core Capabilities, Core Modules, Custom Teaching Tones, Development Commands, Download the Executable (Windows) (+37 more)

### Community 13 - "add_to_commentary_cache"
Cohesion: 0.07
Nodes (27): API Key Security, API key 安全性, Automatic Migration of Legacy Settings, Available Alternatives, Frequently Asked Questions, GitHub Models Still Appears After Startup, LLM 提供來源遷移指南 / LLM Provider Migration Guide, OpenRouter Returns HTTP 402 (+19 more)

### Community 17 - "Contributing to AI Go Teacher / 為 AI Go Teacher 貢獻"
Cohesion: 0.05
Nodes (37): Acknowledgments, Before Submitting a Bug Report, Before Submitting an Enhancement, Commit Messages, Commit 訊息, Contributing to AI Go Teacher / 為 AI Go Teacher 貢獻, Development Environment Setup, How Do I Submit a Good Bug Report? (+29 more)

### Community 18 - "main_v3.py"
Cohesion: 0.22
Nodes (3): discover_openrouter_models(), OpenRouterProvider, Return (True, model_ids) or (False, error_message).

### Community 19 - "OllamaManager"
Cohesion: 0.18
Nodes (10): Accepted Reports, Declined Reports, In-Scope, Information to Include, Out-of-Scope, Reporting a Vulnerability, Response & Resolution Process, Scope (+2 more)

### Community 20 - "_show_llm_selection_dialog"
Cohesion: 0.20
Nodes (15): discover_nim_models(), 向 NIM 端點 /v1/models 查詢可用模型清單。      成功時回傳 (True, [model_id, ...])；失敗時回傳 (False,, get_nvidia_api_key(), get_openrouter_api_key(), normalize_api_key(), Trim whitespace and common quote wrappers from API key values., Read NVIDIA API key from keyring first, then environment variables., Store NVIDIA API key in the OS keyring. Does not write to .env. (+7 more)

### Community 21 - "version.py"
Cohesion: 0.12
Nodes (14): Path, I18n, resource_path(), BranchCanvas, LLMSelectionDialog, main(), Application version helpers for AI Go Teacher.  Run this file to update every, Return the numeric tuple used by PyInstaller's VSVersionInfo. (+6 more)

### Community 22 - "github_provider.py"
Cohesion: 0.29
Nodes (6): get_publisher_from_model_id(), group_models_by_publisher(), 從 model_id 拆出 publisher（第一個 '/' 之前的部分）。      無 '/' 的 model_id 歸類為 "unknown"，確保, 將 model_id 清單依 publisher 分組，回傳 {publisher: [model_id, ...]}。      保持各 publishe, get_publisher_from_model_id(), group_models_by_publisher()

### Community 24 - "main_v3.py"
Cohesion: 0.10
Nodes (27): _confirm_and_download_ollama_model(), _create_info_section(), _create_katago_section(), _create_labeled_row(), _create_ollama_model_row(), detect_ollama_installed(), _download_ollama_model(), _load_ollama_icon() (+19 more)

### Community 25 - "version.py"
Cohesion: 0.11
Nodes (7): 多分頁文件管理器：維護所有 TabSession 並提供 active session 切換。, 建立第一個分頁並設為 active。供 main 流程開機時呼叫一次。, 建立新分頁。若已達 MAX_TABS，回傳 None。, 關閉指定分頁；回傳 (success, reason)。          規則：           - 至少保留一個分頁。           -, 支援 tab_manager[idx] 取第 idx 個分頁。, TabManager, TabSession

### Community 27 - "set_winrate_text"
Cohesion: 0.23
Nodes (3): FakeMenuBar, Themeable, Tk-only application menu bar.  This deliberately does not use native, A small menu system built from Frames and Buttons.      Menu definitions are pla

### Community 28 - "_build_diagnostic_report_text"
Cohesion: 0.15
Nodes (16): _capture_board_snapshot(), _close_tab_silently(), hydrate_active_session(), new_game(), on_new_tab_click(), on_tab_click(), 切換到指定分頁。會先把當前棋盤存回離開的 session，再從目標 session 還原。, 實際執行關閉流程（含棋盤快照處理、hydrate 與 bar 重繪）。 (+8 more)

### Community 29 - "materialize_bundled_runtime_file"
Cohesion: 0.24
Nodes (10): _close_tab_button(), on_close_tab_click(), on_load_sgf_click(), 依 tab_manager 狀態重繪分頁列。, 關閉分頁：dirty 時彈出 三選一（儲存 / 不儲存 / 取消）。      為了在關閉流程內支援 "儲存" 動作，會先暫時把這個分頁切為 active，, 彈出儲存 / 不儲存 / 取消 三選一對話框，回傳 'save' / 'discard' / 'cancel'。, refresh_tab_bar(), save_game_as_sgf() (+2 more)

### Community 36 - "_handle_score_estimate_result"
Cohesion: 0.29
Nodes (9): _handle_score_estimate_result(), on_close_score_estimate_click(), on_score_estimate_click(), show_score_estimate_popup(), start_score_analyzer_async(), _start_score_estimate_query(), summarize_score_estimate(), update_score_estimate_button_label() (+1 more)

### Community 37 - "show_first_run_onboarding_dialog"
Cohesion: 0.20
Nodes (11): apply_theme(), build_menu_bar(), on_closing(), Expose semantic theme tokens to legacy drawing code in this module., Apply a configured theme to existing widgets without restarting., rebuild_menu_bar(), save_game_as_json(), save_game_as_json_dialog() (+3 more)

### Community 38 - "add_to_commentary_cache"
Cohesion: 0.50
Nodes (4): add_to_commentary_cache(), on_commentary_generation_complete(), 【Phase 1】LLM 生成完成後的回呼 — 將完整的解說存儲到快取, 將解說文本新增到快取 (執行緒安全，儲存全部手數)

### Community 39 - "detect_ollama_installed"
Cohesion: 0.27
Nodes (9): auto_analyze(), is_analyzer_ready(), on_analyze_button_click(), poll_ai(), 分析整盤棋並回傳每手的勝率列表 (複用全局 KataGo analyzer，支援取消與進度回報), run_full_game_analysis(), set_winrate_text(), show_analyzer_not_ready() (+1 more)

## Knowledge Gaps
- **105 isolated node(s):** `Table of Contents`, `I Have a Question`, `Before Submitting a Bug Report`, `How Do I Submit a Good Bug Report?`, `Before Submitting an Enhancement` (+100 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ProviderFactory` connect `ProviderFactory` to `GoBoard`, `OllamaProvider`, `get_runtime_data_root`, `BranchTreeView`, `.get_nim_publisher_for_model`, `KataGoAnalyzer`, `main_v3.py`, `version.py`, `github_provider.py`, `main_v3.py`, `version.py`, `NvidiaProvider`?**
  _High betweenness centrality (0.114) - this node is a cross-community bridge._
- **Why does `GoBoard` connect `GoBoard` to `LLMChatWindow`, `_handle_score_estimate_result`, `show_first_run_onboarding_dialog`, `BranchTreeView`, `ConfigService`, `ProviderFactory`, `version.py`, `main_v3.py`, `set_winrate_text`, `_build_diagnostic_report_text`, `materialize_bundled_runtime_file`?**
  _High betweenness centrality (0.107) - this node is a cross-community bridge._
- **Why does `LLMChatWindow` connect `LLMChatWindow` to `GoBoard`, `get_runtime_data_root`, `BranchTreeView`, `KataGoAnalyzer`, `ProviderFactory`, `version.py`, `main_v3.py`, `version.py`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `GoBoard` (e.g. with `ConfigService` and `ProviderFactory`) actually correct?**
  _`GoBoard` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `LLMChatWindow` (e.g. with `BranchCanvas` and `BranchTreeView`) actually correct?**
  _`LLMChatWindow` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `ConfigService` (e.g. with `BranchCanvas` and `BranchTreeView`) actually correct?**
  _`ConfigService` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `ProviderFactory` (e.g. with `NvidiaProvider` and `OllamaProvider`) actually correct?**
  _`ProviderFactory` has 13 INFERRED edges - model-reasoned connections that need verification._