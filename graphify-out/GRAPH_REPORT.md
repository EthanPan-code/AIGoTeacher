# Graph Report - AIGoTeacher  (2026-08-05)

## Corpus Check
- 24 files · ~41,204 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 616 nodes · 1162 edges · 38 communities (28 shown, 10 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 75 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d083c711`
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
- resource_path
- Ollama 模型目錄最佳化計畫
- NvidiaProvider
- .on_state_change
- _handle_score_estimate_result
- materialize_bundled_runtime_file
- Cloud API Illustration
- GitHub Models Provider
- Interactive Board Feature
- Live Analysis Feature
- LLM Commentary Feature
- SGF Support Feature
- show_system_info_dialog
- add_to_commentary_cache

## God Nodes (most connected - your core abstractions)
1. `GoBoard` - 56 edges
2. `t()` - 51 edges
3. `LLMChatWindow` - 41 edges
4. `ProviderFactory` - 32 edges
5. `ConfigService` - 30 edges
6. `LLMProvider` - 24 edges
7. `build_menu_bar()` - 24 edges
8. `OllamaProvider` - 23 edges
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

## Communities (38 total, 10 thin omitted)

### Community 0 - "t"
Cohesion: 0.13
Nodes (25): build_menu_bar(), change_config_path(), change_katago_path(), change_model_path(), create_katago_startup_popup(), get_config_display_name(), get_model_display_name(), on_load_sgf_click() (+17 more)

### Community 1 - "GoBoard"
Cohesion: 0.06
Nodes (15): BranchCanvas, GameNode, GoBoard, load_tk_image(), _on_board_shell_configure(), on_mouse_wheel(), 依 board_shell 實際尺寸重新縮放外框背景圖片（cover 模式：填滿裁切）。          由 board_shell 的 <Configu, 動態生成歷史落子紀錄，不會再因為提子而消失，確保 AI 判斷正確 (+7 more)

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
Cohesion: 0.14
Nodes (24): _build_diagnostic_report_text(), create_dev_menu(), ensure_runtime_dir(), export_diagnostic_report(), get_executable_dir(), get_katago_runtime_overrides(), _get_newest_log_file(), get_runtime_data_root() (+16 more)

### Community 8 - "KataGoAnalyzer"
Cohesion: 0.09
Nodes (16): get_commentary_from_cache(), GoDataFilter, KataGoAnalyzer, on_closing(), poll_ai(), 分析整盤棋並回傳每手的勝率列表 (複用全局 KataGo analyzer，支援取消與進度回報), 直接使用記憶體中的數據更新 UI，並將所有分析結果保存到快取以供後續比較使用, 將當前棋譜轉換成唯一的字串，作為快取的 Key (+8 more)

### Community 9 - "ConfigService"
Cohesion: 0.15
Nodes (3): ConfigService, Migrate settings from the removed GitHub Models provider., Small wrapper around persisted UI settings.

### Community 10 - "safe_get_system_info"
Cohesion: 0.15
Nodes (16): _format_bytes_as_gb(), _get_cpu_name(), _get_gpu_info(), _get_physical_core_count(), _get_ram_info(), _get_windows_display_version(), 把位元組數轉成 GB 字串；輸入不可用時回傳 Unknown。, 執行 PowerShell 並解析 JSON，失敗時回傳 None。      這裡只用於診斷資訊的 best-effort 查詢，任何錯誤都不能影響主 U (+8 more)

### Community 11 - "ProviderFactory"
Cohesion: 0.10
Nodes (10): ProviderFactory, Return the human-readable display name for a model ID.          Falls back to, Reverse lookup: display name → model ID.          Returns None when the displa, Return [(display_name, model_id), ...] for UI widgets.          The list follo, 向 NIM 端點探索可用模型，失敗時降級至內建清單。          回傳 (model_ids, used_fallback, error_messag, 從 model_id 清單取出 publisher 清單（已排序、去重）。, 取得指定 publisher 下的 model_id 清單（保持原始順序）。, 安全取得目前 AI 提供商、模型與語言設定。 (+2 more)

### Community 12 - "AI 圍棋老師 / AI Go Teacher"
Cohesion: 0.04
Nodes (45): AI 圍棋老師 / AI Go Teacher, Communication Protocols, Contents, Core Capabilities, Core Modules, Custom Teaching Tones, Development Commands, Download the Executable (Windows) (+37 more)

### Community 13 - "add_to_commentary_cache"
Cohesion: 0.13
Nodes (14): API key 安全性, LLM 提供來源遷移指南, OpenRouter 回傳 402, OpenRouter 回傳 429 或 503, OpenRouter 模型清單是空的, 可用的替代來源, 啟動後仍看到 GitHub Models 設定, 常見問題 (+6 more)

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
Nodes (12): get_nvidia_api_key(), get_openrouter_api_key(), normalize_api_key(), Trim whitespace and common quote wrappers from API key values., Read NVIDIA API key from keyring first, then environment variables., Store NVIDIA API key in the OS keyring. Does not write to .env., Read OpenRouter API key from keyring first, then environment variables., Store OpenRouter API key in the OS keyring. Does not write to .env. (+4 more)

### Community 21 - "version.py"
Cohesion: 0.15
Nodes (12): Path, I18n, resource_path(), main(), Application version helpers for AI Go Teacher.  Run this file to update every, Return the numeric tuple used by PyInstaller's VSVersionInfo., _replace_once(), sync_version() (+4 more)

### Community 22 - "github_provider.py"
Cohesion: 0.26
Nodes (7): get_publisher_from_model_id(), group_models_by_publisher(), 從 model_id 拆出 publisher（第一個 '/' 之前的部分）。      無 '/' 的 model_id 歸類為 "unknown"，確保, 將 model_id 清單依 publisher 分組，回傳 {publisher: [model_id, ...]}。      保持各 publishe, get_publisher_from_model_id(), group_models_by_publisher(), 從 model_id 拆出 publisher（供 UI 還原選擇用）。

### Community 24 - "resource_path"
Cohesion: 0.12
Nodes (17): _confirm_and_download_ollama_model(), _create_ollama_model_row(), detect_ollama_installed(), _download_ollama_model(), _load_ollama_icon(), _open_folder(), plot_window(), 檢查系統是否能執行 `ollama --version`，回傳 (installed: bool, version_or_none) (+9 more)

### Community 25 - "Ollama 模型目錄最佳化計畫"
Cohesion: 0.13
Nodes (14): i18n、文件與診斷, Ollama 模型目錄最佳化計畫, `providers/ollama_provider.py` 與 Factory, `services/ollama_manager.py`, `ui/main_v3.py`, 動態模型目錄, 實作變更, 本機與雲端模型的使用規則 (+6 more)

### Community 26 - "NvidiaProvider"
Cohesion: 0.20
Nodes (4): discover_nim_models(), NvidiaProvider, 動態探索 NIM 可用模型，失敗時降級至內建清單。          回傳 (model_ids, used_fallback, error_message, 向 NIM 端點 /v1/models 查詢可用模型清單。      成功時回傳 (True, [model_id, ...])；失敗時回傳 (False,

### Community 27 - ".on_state_change"
Cohesion: 0.40
Nodes (7): auto_analyze(), is_analyzer_ready(), new_game(), on_analyze_button_click(), set_winrate_text(), show_analyzer_not_ready(), show_winrate_chart()

### Community 28 - "_handle_score_estimate_result"
Cohesion: 0.29
Nodes (9): _handle_score_estimate_result(), on_close_score_estimate_click(), on_score_estimate_click(), show_score_estimate_popup(), start_score_analyzer_async(), _start_score_estimate_query(), summarize_score_estimate(), update_score_estimate_button_label() (+1 more)

### Community 29 - "materialize_bundled_runtime_file"
Cohesion: 0.31
Nodes (8): get_config_path(), get_katago_path(), get_model_path(), materialize_bundled_runtime_file(), Copy bundled KataGo runtime files out of PyInstaller's _MEI directory.      Th, 安全取得 KataGo 執行檔、設定檔、模型檔路徑與存在狀態。, safe_get_katago_info(), ScoreAnalyzer

### Community 36 - "show_system_info_dialog"
Cohesion: 0.33
Nodes (6): _create_info_section(), _create_katago_section(), _create_labeled_row(), 建立診斷資訊視窗中的單列 label/value。, setup_system_info_styles(), show_system_info_dialog()

### Community 37 - "add_to_commentary_cache"
Cohesion: 0.50
Nodes (4): add_to_commentary_cache(), on_commentary_generation_complete(), 將解說文本新增到快取 (執行緒安全，儲存全部手數), 【Phase 1】LLM 生成完成後的回呼 — 將完整的解說存儲到快取

## Knowledge Gaps
- **104 isolated node(s):** `Table of Contents`, `I Have a Question`, `Before Submitting a Bug Report`, `How Do I Submit a Good Bug Report?`, `Before Submitting an Enhancement` (+99 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ProviderFactory` connect `ProviderFactory` to `GoBoard`, `OllamaProvider`, `get_runtime_data_root`, `BranchTreeView`, `KataGoAnalyzer`, `main_v3.py`, `_show_llm_selection_dialog`, `github_provider.py`, `NvidiaProvider`, `materialize_bundled_runtime_file`?**
  _High betweenness centrality (0.120) - this node is a cross-community bridge._
- **Why does `GoBoard` connect `GoBoard` to `t`, `LLMChatWindow`, `get_runtime_data_root`, `BranchTreeView`, `ConfigService`, `ProviderFactory`, `version.py`, `.on_state_change`, `_handle_score_estimate_result`?**
  _High betweenness centrality (0.118) - this node is a cross-community bridge._
- **Why does `LLMChatWindow` connect `LLMChatWindow` to `GoBoard`, `get_runtime_data_root`, `BranchTreeView`, `KataGoAnalyzer`, `_show_llm_selection_dialog`, `materialize_bundled_runtime_file`?**
  _High betweenness centrality (0.082) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `GoBoard` (e.g. with `ConfigService` and `ProviderFactory`) actually correct?**
  _`GoBoard` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `LLMChatWindow` (e.g. with `BranchCanvas` and `BranchTreeView`) actually correct?**
  _`LLMChatWindow` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `ProviderFactory` (e.g. with `NvidiaProvider` and `OllamaProvider`) actually correct?**
  _`ProviderFactory` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `ConfigService` (e.g. with `BranchCanvas` and `BranchTreeView`) actually correct?**
  _`ConfigService` has 8 INFERRED edges - model-reasoned connections that need verification._