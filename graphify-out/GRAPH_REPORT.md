# Graph Report - AIGoTeacher  (2026-07-20)

## Corpus Check
- 21 files · ~38,147 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 538 nodes · 1051 edges · 36 communities (23 shown, 13 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 74 edges (avg confidence: 0.54)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `00c4e882`
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
- _handle_score_estimate_result
- GithubProvider
- NvidiaProvider
- _build_diagnostic_report_text
- create_dev_menu
- show_system_info_dialog
- Cloud API Illustration
- GitHub Models Provider
- Interactive Board Feature
- Live Analysis Feature
- LLM Commentary Feature
- SGF Support Feature

## God Nodes (most connected - your core abstractions)
1. `GoBoard` - 56 edges
2. `t()` - 50 edges
3. `LLMChatWindow` - 41 edges
4. `ConfigService` - 29 edges
5. `LLMProvider` - 24 edges
6. `ProviderFactory` - 24 edges
7. `build_menu_bar()` - 24 edges
8. `OllamaProvider` - 21 edges
9. `BranchTreeView` - 21 edges
10. `KataGoAnalyzer` - 19 edges

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

## Communities (36 total, 13 thin omitted)

### Community 0 - "t"
Cohesion: 0.17
Nodes (22): build_menu_bar(), _confirm_and_download_ollama_model(), create_katago_startup_popup(), _download_ollama_model(), open_feedback_form(), plot_window(), 顯示簡單的 Ollama 安裝引導對話框（包含開啟下載頁與重新檢測）。, 顯示下載確認對話框並開始下載          Args:         parent: 父窗口         model_name: 要下載的模型 (+14 more)

### Community 1 - "GoBoard"
Cohesion: 0.06
Nodes (20): GameNode, GoBoard, load_tk_image(), new_game(), _on_board_shell_configure(), on_load_sgf_click(), on_mouse_wheel(), 依 board_shell 實際尺寸重新縮放外框背景圖片（cover 模式：填滿裁切）。          由 board_shell 的 <Configu (+12 more)

### Community 2 - "LLMProvider"
Cohesion: 0.11
Nodes (6): LLMProvider, Return a human-readable display name for the given model ID.          Subclasses, Return (is_valid, error_message)., Send a raw prompt to the LLM for a plain chat conversation.          This is use, Base class for streaming LLM commentary providers., Build the final prompt sent to the model from plain user text plus data.

### Community 3 - "requirements.txt - Python Dependencies"
Cohesion: 0.18
Nodes (11): Matplotlib Visualization, Ollama Provider, PyInstaller Packaging, requirements.txt - Python Dependencies, httpx HTTP Client, keyring Package, matplotlib Package, ollama Python Package (+3 more)

### Community 4 - "LLMChatWindow"
Cohesion: 0.11
Nodes (3): LLMChatWindow, 輸入框獲得焦點時清除 placeholder。, 輸入框失去焦點時恢復 placeholder。

### Community 6 - "get_runtime_data_root"
Cohesion: 0.27
Nodes (12): ensure_runtime_dir(), get_executable_dir(), get_katago_runtime_overrides(), get_runtime_data_root(), get_runtime_file_path(), is_frozen_app(), iter_dotenv_paths(), _iter_log_candidates() (+4 more)

### Community 7 - "BranchTreeView"
Cohesion: 0.09
Nodes (5): I18n, resource_path(), BranchCanvas, BranchTreeView, LLMSelectionDialog

### Community 8 - "KataGoAnalyzer"
Cohesion: 0.09
Nodes (19): auto_analyze(), get_commentary_from_cache(), GoDataFilter, is_analyzer_ready(), KataGoAnalyzer, on_analyze_button_click(), on_closing(), poll_ai() (+11 more)

### Community 10 - "safe_get_system_info"
Cohesion: 0.15
Nodes (16): _format_bytes_as_gb(), _get_cpu_name(), _get_gpu_info(), _get_physical_core_count(), _get_ram_info(), _get_windows_display_version(), 把位元組數轉成 GB 字串；輸入不可用時回傳 Unknown。, 執行 PowerShell 並解析 JSON，失敗時回傳 None。      這裡只用於診斷資訊的 best-effort 查詢，任何錯誤都不能影響主 U (+8 more)

### Community 11 - "ProviderFactory"
Cohesion: 0.13
Nodes (10): ProviderFactory, Return the human-readable display name for a model ID.          Falls back to th, Reverse lookup: display name → model ID.          Returns None when the display, Return [(display_name, model_id), ...] for UI widgets.          The list follows, _create_ollama_model_row(), _load_ollama_icon(), 為 Ollama 模型創建一個選擇行。     - 已下載（available）：點擊直接選中     - 雲端（cloud）：點擊直接選中，不顯示下載, Open the LLM Chat Sandbox window for provider connectivity testing. (+2 more)

### Community 12 - "AI 圍棋老師 / AI Go Teacher"
Cohesion: 0.04
Nodes (45): AI 圍棋老師 / AI Go Teacher, Communication Protocols, Contents, Core Capabilities, Core Modules, Custom Teaching Tones, Development Commands, Download the Executable (Windows) (+37 more)

### Community 13 - "add_to_commentary_cache"
Cohesion: 0.50
Nodes (4): add_to_commentary_cache(), on_commentary_generation_complete(), 將解說文本新增到快取 (執行緒安全，儲存全部手數), 【Phase 1】LLM 生成完成後的回呼 — 將完整的解說存儲到快取

### Community 17 - "Contributing to AI Go Teacher / 為 AI Go Teacher 貢獻"
Cohesion: 0.05
Nodes (37): Acknowledgments, Before Submitting a Bug Report, Before Submitting an Enhancement, Commit Messages, Commit 訊息, Contributing to AI Go Teacher / 為 AI Go Teacher 貢獻, Development Environment Setup, How Do I Submit a Good Bug Report? (+29 more)

### Community 18 - "main_v3.py"
Cohesion: 0.16
Nodes (14): change_config_path(), change_katago_path(), change_model_path(), detect_ollama_installed(), get_config_display_name(), get_model_display_name(), 重新初始化分析器（關閉舊進程，建立新進程）, 檢查系統是否能執行 `ollama --version`，回傳 (installed: bool, version_or_none) (+6 more)

### Community 19 - "OllamaManager"
Cohesion: 0.18
Nodes (5): OllamaManager, Start `ollama pull` in a background thread., Return local model names from `ollama list`., Best-effort model size lookup for downloaded and remote models., Small wrapper around the Ollama CLI for local model management.

### Community 20 - "_show_llm_selection_dialog"
Cohesion: 0.25
Nodes (11): get_github_token(), get_nvidia_api_key(), normalize_api_key(), Trim whitespace and common quote wrappers from API key values., Read NVIDIA API key from keyring first, then environment variables., Store NVIDIA API key in the OS keyring. Does not write to .env., Read GitHub Models token from keyring first, then environment variables., Store GitHub Models token in the OS keyring. Does not write to .env. (+3 more)

### Community 21 - "version.py"
Cohesion: 0.33
Nodes (10): Path, main(), Application version helpers for AI Go Teacher.  Run this file to update every, Return the numeric tuple used by PyInstaller's VSVersionInfo., _replace_once(), sync_version(), update_version_info(), update_version_module() (+2 more)

### Community 23 - "materialize_bundled_runtime_file"
Cohesion: 0.31
Nodes (8): get_config_path(), get_katago_path(), get_model_path(), hide_path_on_windows(), materialize_bundled_runtime_file(), Copy bundled KataGo runtime files out of PyInstaller's _MEI directory.      Th, 安全取得 KataGo 執行檔、設定檔、模型檔路徑與存在狀態。, safe_get_katago_info()

### Community 24 - "_handle_score_estimate_result"
Cohesion: 0.33
Nodes (8): _handle_score_estimate_result(), on_close_score_estimate_click(), on_score_estimate_click(), start_score_analyzer_async(), _start_score_estimate_query(), summarize_score_estimate(), update_score_estimate_button_label(), _wait_for_score_estimate_response()

### Community 27 - "_build_diagnostic_report_text"
Cohesion: 0.29
Nodes (7): _build_diagnostic_report_text(), _get_newest_log_file(), 安全取得目前 AI 提供商、模型與語言設定。, 讀取最新 log 的最後 max_lines 行；沒有 log 時回傳提示文字。, 組合 diagnostic_report.txt 的完整內容。, _read_recent_log_lines(), safe_get_ai_config()

### Community 28 - "create_dev_menu"
Cohesion: 0.29
Nodes (7): create_dev_menu(), export_diagnostic_report(), _open_folder(), 顯示診斷報告匯出完成訊息與開啟資料夾按鈕。, 匯出診斷報告到 diagnostics/diagnostic_report.txt。, 建立 Dev 選單；初始建置與語言重建共用同一份項目。, _show_diagnostic_export_success()

### Community 29 - "show_system_info_dialog"
Cohesion: 0.33
Nodes (6): _create_info_section(), _create_katago_section(), _create_labeled_row(), 建立診斷資訊視窗中的單列 label/value。, setup_system_info_styles(), show_system_info_dialog()

## Knowledge Gaps
- **75 isolated node(s):** `Table of Contents`, `I Have a Question`, `Before Submitting a Bug Report`, `How Do I Submit a Good Bug Report?`, `Before Submitting an Enhancement` (+70 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `GoBoard` connect `GoBoard` to `t`, `LLMChatWindow`, `BranchTreeView`, `ConfigService`, `ProviderFactory`, `main_v3.py`, `_handle_score_estimate_result`?**
  _High betweenness centrality (0.142) - this node is a cross-community bridge._
- **Why does `ProviderFactory` connect `ProviderFactory` to `GoBoard`, `OllamaProvider`, `BranchTreeView`, `KataGoAnalyzer`, `main_v3.py`, `github_provider.py`, `GithubProvider`, `NvidiaProvider`?**
  _High betweenness centrality (0.134) - this node is a cross-community bridge._
- **Why does `LLMChatWindow` connect `LLMChatWindow` to `GoBoard`, `BranchTreeView`, `KataGoAnalyzer`, `ProviderFactory`, `main_v3.py`?**
  _High betweenness centrality (0.099) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `GoBoard` (e.g. with `ConfigService` and `ProviderFactory`) actually correct?**
  _`GoBoard` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `LLMChatWindow` (e.g. with `BranchCanvas` and `BranchTreeView`) actually correct?**
  _`LLMChatWindow` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `ConfigService` (e.g. with `BranchCanvas` and `BranchTreeView`) actually correct?**
  _`ConfigService` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `LLMProvider` (e.g. with `GithubProvider` and `NvidiaProvider`) actually correct?**
  _`LLMProvider` has 3 INFERRED edges - model-reasoned connections that need verification._