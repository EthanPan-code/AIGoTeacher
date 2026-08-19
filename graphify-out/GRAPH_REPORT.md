# Graph Report - AIGoTeacher  (2026-08-19)

## Corpus Check
- 26 files · ~53,563 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 743 nodes · 1386 edges · 38 communities (30 shown, 8 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 44 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `dc17074c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- GoBoard
- AI 圍棋老師 / AI Go Teacher
- OllamaProvider
- ProviderFactory
- Contributing to AI Go Teacher / 為 AI Go Teacher 貢獻
- LLM 提供來源遷移指南 / LLM Provider Migration Guide
- LLMChatWindow
- ConfigService
- get_runtime_data_root
- refresh_tab_bar
- t
- main_v3.py
- I18n
- refresh_language
- LLMProvider
- KataGoAnalyzer
- TabManager
- FakeMenuBar
- BranchTreeView
- keyring_service.py
- serialize_game_context
- safe_get_system_info
- tone_templates.py
- provider_factory.py
- stop_continuous_analysis
- normalize_api_key
- Security Policy
- NvidiaProvider
- OpenRouterProvider
- requirements.txt - Python Dependencies
- reinitialize_analyzer
- detect_ollama_installed
- GUI Screenshot
- Available Status Screenshot
- Cloud API Illustration
- Download UI Screenshot
- version_info.txt - PyInstaller VSVersionInfo

## God Nodes (most connected - your core abstractions)
1. `t()` - 65 edges
2. `GoBoard` - 55 edges
3. `LLMChatWindow` - 33 edges
4. `ProviderFactory` - 31 edges
5. `LLMProvider` - 24 edges
6. `ConfigService` - 24 edges
7. `build_menu_bar()` - 24 edges
8. `OllamaProvider` - 23 edges
9. `resource_path()` - 20 edges
10. `BranchTreeView` - 20 edges

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

## Communities (38 total, 8 thin omitted)

### Community 0 - "GoBoard"
Cohesion: 0.07
Nodes (12): GameNode, GoBoard, load_tk_image(), Load an image as a Tk image, preferring Pillow for broad format support., 依 board_shell 實際尺寸重新縮放外框背景圖片（cover 模式：填滿裁切）。 由 board_shell 的 <Configure>…, 動態生成歷史落子紀錄，不會再因為提子而消失，確保 AI 判斷正確, Return 1-based move index where the current branch starts, or None on main line., 切換同一手棋的不同變化圖 (direction: 1 或 -1) (+4 more)

### Community 1 - "AI 圍棋老師 / AI Go Teacher"
Cohesion: 0.05
Nodes (44): AI 圍棋老師 / AI Go Teacher, Communication Protocols, Contents, Core Capabilities, Core Modules, Custom Teaching Tones, Development Commands, Download the Executable (Windows) (+36 more)

### Community 2 - "OllamaProvider"
Cohesion: 0.08
Nodes (9): OllamaProvider, get_ollama_manager(), OllamaManager, OllamaModelInfo, Return (models, error), retaining the last good catalog on failure., Read a model without triggering network I/O., Start a streaming REST pull for a local model., REST client and catalog cache for the local Ollama service. (+1 more)

### Community 3 - "ProviderFactory"
Cohesion: 0.07
Nodes (22): Store NVIDIA API key in the OS keyring. Does not write to .env., Store OpenRouter API key in the OS keyring. Does not write to .env., set_nvidia_api_key(), set_openrouter_api_key(), ProviderFactory, Return the human-readable display name for a model ID. Falls back to the raw…, Reverse lookup: display name → model ID. Returns None when the display name is…, Return [(display_name, model_id), ...] for UI widgets. The list follows the… (+14 more)

### Community 4 - "Contributing to AI Go Teacher / 為 AI Go Teacher 貢獻"
Cohesion: 0.05
Nodes (38): Acknowledgments, Before Submitting a Bug Report, Before Submitting an Enhancement, Commit Messages, Commit 訊息, Contributing to AI Go Teacher / 為 AI Go Teacher 貢獻, Development Environment Setup, How Do I Submit a Good Bug Report? (+30 more)

### Community 5 - "LLM 提供來源遷移指南 / LLM Provider Migration Guide"
Cohesion: 0.07
Nodes (27): API Key Security, API key 安全性, Automatic Migration of Legacy Settings, Available Alternatives, Frequently Asked Questions, GitHub Models Still Appears After Startup, LLM 提供來源遷移指南 / LLM Provider Migration Guide, OpenRouter Returns HTTP 402 (+19 more)

### Community 6 - "LLMChatWindow"
Cohesion: 0.11
Nodes (3): LLMChatWindow, 輸入框獲得焦點時清除 placeholder。, 輸入框失去焦點時恢復 placeholder。

### Community 7 - "ConfigService"
Cohesion: 0.11
Nodes (8): ConfigService, Small wrapper around persisted UI settings., Migrate settings from the removed GitHub Models provider., detect_system_theme(), normalize_theme(), Application color themes and Windows system-theme resolution., Return the Windows theme at process startup; safely fall back to light., resolve_theme()

### Community 8 - "get_runtime_data_root"
Cohesion: 0.09
Nodes (29): _build_diagnostic_report_text(), _delete_runtime_path(), ensure_runtime_dir(), get_config_path(), get_executable_dir(), get_katago_path(), get_katago_runtime_overrides(), get_model_path() (+21 more)

### Community 9 - "refresh_tab_bar"
Cohesion: 0.11
Nodes (28): _capture_board_snapshot(), _close_tab_silently(), _copy_game_tree(), hydrate_active_session(), on_close_tab_click(), on_copy_tab_click(), on_load_sgf_click(), on_new_tab_click() (+20 more)

### Community 10 - "t"
Cohesion: 0.12
Nodes (30): build_branch_section(), build_menu_bar(), _confirm_and_download_ollama_model(), create_dev_menu(), _download_ollama_model(), export_diagnostic_report(), get_config_display_name(), get_model_display_name() (+22 more)

### Community 11 - "main_v3.py"
Cohesion: 0.09
Nodes (26): add_to_commentary_cache(), _commentary_cache_key(), _create_info_section(), _create_katago_section(), _create_labeled_row(), _create_ollama_model_row(), get_commentary_from_cache(), _handle_score_estimate_result() (+18 more)

### Community 12 - "I18n"
Cohesion: 0.16
Nodes (12): Path, I18n, resource_path(), main(), Application version helpers for AI Go Teacher. Run this file to update every…, Return the numeric tuple used by PyInstaller's VSVersionInfo., _replace_once(), sync_version() (+4 more)

### Community 13 - "refresh_language"
Cohesion: 0.13
Nodes (15): apply_theme(), new_game(), Expose semantic theme tokens to legacy drawing code in this module., 只更新老師解說區，不改動生成中的快取狀態。, LLM Provider 的串流回呼；累積全文但在回放時不覆蓋既有解說。, Apply a configured theme to existing widgets without restarting., Refresh a known static teacher prompt without touching LLM output., rebuild_menu_bar() (+7 more)

### Community 14 - "LLMProvider"
Cohesion: 0.11
Nodes (6): LLMProvider, Return a human-readable display name for the given model ID. Subclasses should…, Return (is_valid, error_message)., Send a raw prompt to the LLM for a plain chat conversation. This is used by the…, Base class for streaming LLM commentary providers., Build the final prompt sent to the model from plain user text plus data.

### Community 15 - "KataGoAnalyzer"
Cohesion: 0.16
Nodes (5): KataGoAnalyzer, 將當前棋譜轉換成唯一的字串，作為快取的 Key, 用一致的 KataGo moves 格式生成快取 key，避免 stones/list 格式不一致造成 miss。, Ask KataGo to stop an analysis query immediately, then detach it., Remove already-queued responses belonging to a cancelled query.

### Community 16 - "TabManager"
Cohesion: 0.10
Nodes (7): 多分頁文件管理器：維護所有 TabSession 並提供 active session 切換。, 建立第一個分頁並設為 active。供 main 流程開機時呼叫一次。, 建立新分頁。若已達 MAX_TABS，回傳 None。, 關閉指定分頁；回傳 (success, reason)。 規則： - 至少保留一個分頁。 - 若傳入 index 為 active，自動切到鄰近分頁。, 支援 tab_manager[idx] 取第 idx 個分頁。, TabManager, TabSession

### Community 17 - "FakeMenuBar"
Cohesion: 0.23
Nodes (3): FakeMenuBar, Themeable, Tk-only application menu bar. This deliberately does not use native…, A small menu system built from Frames and Buttons. Menu definitions are plain…

### Community 19 - "keyring_service.py"
Cohesion: 0.31
Nodes (8): _delete_api_key(), delete_nvidia_api_key(), delete_openrouter_api_key(), Delete one application credential, treating a missing credential as success., Delete the NVIDIA API key owned by this application., Delete the OpenRouter API key owned by this application., _clear_selected_runtime_data(), Stop engine processes and clear selected data, returning result rows.

### Community 20 - "serialize_game_context"
Cohesion: 0.19
Nodes (11): _analysis_lines(), _gtp(), _move_text(), Compact, factual Go-game context for LLM teaching prompts. This module…, Serialize only the selected mainline and explicitly named snapshots., serialize_board(), serialize_game_context(), serialize_mainline() (+3 more)

### Community 21 - "safe_get_system_info"
Cohesion: 0.15
Nodes (16): _format_bytes_as_gb(), _get_cpu_name(), _get_gpu_info(), _get_physical_core_count(), _get_ram_info(), _get_windows_display_version(), 把位元組數轉成 GB 字串；輸入不可用時回傳 Unknown。, 執行 PowerShell 並解析 JSON，失敗時回傳 None。 這裡只用於診斷資訊的 best-effort 查詢，任何錯誤都不能影響主 UI。 (+8 more)

### Community 22 - "tone_templates.py"
Cohesion: 0.17
Nodes (15): find_preset_tone(), get_all_tones(), get_tone_description(), get_tone_display_name(), get_tone_prompt(), Single-block LLM prompt templates for AI Go teacher commentary. The application…, Return the preset prompt in the requested UI language., Return the tone if prompt is an untouched preset, otherwise ``None``. (+7 more)

### Community 23 - "provider_factory.py"
Cohesion: 0.32
Nodes (6): get_publisher_from_model_id(), group_models_by_publisher(), 從 model_id 拆出 publisher（第一個 '/' 之前的部分）。 無 '/' 的 model_id 歸類為 "unknown"，確保 UI…, 將 model_id 清單依 publisher 分組，回傳 {publisher: [model_id, ...]}。 保持各 publisher 內…, get_publisher_from_model_id(), group_models_by_publisher()

### Community 24 - "stop_continuous_analysis"
Cohesion: 0.17
Nodes (16): auto_analyze(), is_analyzer_ready(), on_analyze_button_click(), on_closing(), poll_ai(), 分析整盤棋並回傳每手的勝率列表 (複用全局 KataGo analyzer，支援取消與進度回報), 直接使用記憶體中的數據更新 UI，並將所有分析結果保存到快取以供後續比較使用, Stop the active continuous query and clear its routing state. (+8 more)

### Community 25 - "normalize_api_key"
Cohesion: 0.21
Nodes (10): discover_nim_models(), 向 NIM 端點 /v1/models 查詢可用模型清單。 成功時回傳 (True, [model_id, ...])；失敗時回傳 (False,…, discover_openrouter_models(), Return (True, model_ids) or (False, error_message)., get_nvidia_api_key(), get_openrouter_api_key(), normalize_api_key(), Trim whitespace and common quote wrappers from API key values. (+2 more)

### Community 26 - "Security Policy"
Cohesion: 0.18
Nodes (10): Accepted Reports, Declined Reports, In-Scope, Information to Include, Out-of-Scope, Reporting a Vulnerability, Response & Resolution Process, Scope (+2 more)

### Community 29 - "requirements.txt - Python Dependencies"
Cohesion: 0.29
Nodes (7): requirements.txt - Python Dependencies, httpx HTTP Client, keyring Package, matplotlib Package, ollama Python Package, opencc Chinese Conversion, Pillow (PIL) Package

### Community 30 - "reinitialize_analyzer"
Cohesion: 0.25
Nodes (8): change_config_path(), change_katago_path(), change_model_path(), create_katago_startup_popup(), 重新初始化分析器（關閉舊進程，建立新進程）, reinitialize_analyzer(), set_analysis_controls_state(), start_analyzer_async()

### Community 31 - "detect_ollama_installed"
Cohesion: 0.50
Nodes (4): detect_ollama_installed(), 在 Windows 上抑制子進程彈出的主控台視窗。 隱藏終端機 (windowed) 模式下，子進程預設會繼承一個可見的主控台， 即使…, 檢查系統是否能執行 `ollama --version`，回傳 (installed: bool, version_or_none), _silent_subprocess_kwargs()

## Knowledge Gaps
- **99 isolated node(s):** `Table of Contents`, `I Have a Question`, `Before Submitting a Bug Report`, `How Do I Submit a Good Bug Report?`, `Before Submitting an Enhancement` (+94 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `GoBoard` connect `GoBoard` to `main_v3.py`?**
  _High betweenness centrality (0.109) - this node is a cross-community bridge._
- **Why does `ProviderFactory` connect `ProviderFactory` to `OllamaProvider`, `t`, `main_v3.py`, `serialize_game_context`, `provider_factory.py`, `NvidiaProvider`, `OpenRouterProvider`?**
  _High betweenness centrality (0.074) - this node is a cross-community bridge._
- **Why does `LLMChatWindow` connect `LLMChatWindow` to `ProviderFactory`, `main_v3.py`?**
  _High betweenness centrality (0.071) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `t()` (e.g. with `set_llm_tone()` and `show_chat_sandbox()`) actually correct?**
  _`t()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `ProviderFactory` (e.g. with `NvidiaProvider` and `OllamaProvider`) actually correct?**
  _`ProviderFactory` has 10 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Table of Contents`, `I Have a Question`, `Before Submitting a Bug Report` to the rest of the system?**
  _99 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `GoBoard` be split into smaller, more focused modules?**
  _Cohesion score 0.06512890094979647 - nodes in this community are weakly interconnected._