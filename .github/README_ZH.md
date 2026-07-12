# AI 圍棋老師

[![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![KataGo](https://img.shields.io/badge/KataGo-v1.16.4-2EA043)](https://katagotraining.org/)
[![Windows](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows)](https://www.microsoft.com/)
![License](https://img.shields.io/badge/License-MIT-red)
![Version](https://img.shields.io/badge/Version-0.3.0--beta-blue)

## 目錄
- 功能特色
- 快速開始
- 技術架構
- LLM 整合
- i18n
- 開發指令

---

## Features
### Core Capabilities
| Feature | Description |
|------|------|
| **Interactive Board** | Tkinter-based visualized Go board supporting click-to-play, dragging, and zooming |
| **Real-time Analysis** | Synchronously displays AI-recommended moves, win rates, and predicted variations |
| **Full-game Analysis** | Win rate curve chart for the entire game |
| **SGF Support** | Import/Export game records (SGF) with support for branch navigation |
| **LLM Commentary** | Multi-provider AI Go commentary and explanations |
### Supported LLM Providers
| Provider | Type | Default Model |
|--------|------|----------|
| **Ollama** | Local / Cloud API | `qwen2.5:3b` |
| **NVIDIA NIM** | Cloud API | `meta/llama-3.1-8b-instruct` |
| **GitHub Models** | Cloud API | `GPT-4o` |

---

## Quick Start
### Prerequisites
- Windows Operating System
- Python 3.14+
- KataGo Model File (Requires download from [katagotraining.org](https://katagotraining.org/))
### Installation Steps
```bash
# 1. Clone the repository
git clone [https://github.com/EthanPan-code/AIGoTeacher.git](https://github.com/EthanPan-code/AIGoTeacher.git)
cd AIGoTeacher
# 2. Install dependencies
pip install -r requirements.txt
# 3. Download KataGo model
'''
Go to [https://katagotraining.org/](https://katagotraining.org/) to download the neural network weight file.
Place it inside the 'models/' directory.
'''
# 4. Run the application
python ui/main_v3.py
```

---

## Technical Architecture
### Go Engine
| Technology | Description |
| ------------------ | --------------------- |
| **KataGo v1.16.4** | State-of-the-art neural network Go engine |
| **Neural Network Weights** | Policy and value networks supporting GPU/CPU acceleration |
### Frontend and Application Layer
| Technology | Purpose |
| ------------------ | ----------- |
| **Python 3.14** | Primary development language |
| **Python 3.13 & PyInstaller** | Packaging into a standalone executable file |
| **Tkinter / ttk** | Cross-platform desktop GUI framework |
| **Matplotlib** | Visualization for win rate and score lead (Komi/Point differential) charts |
| **Pillow (PIL)** | Image asset processing and board textures |
### Core Modules
| Module | Responsibilities |
|------|------|
| `main_v3.py` | Main application: Board rendering, analysis engine integration, and event handling |
| `providers/*.py` | LLM provider implementations (Ollama/NVIDIA/GitHub) |
| `services/` | Configuration management and secure API key storage |
| `i18n.py` | Internationalization (i18n) system |
### Communication Protocols
- **Asynchronous JSON Protocol**: Communicates with the KataGo engine via stdin/stdout.
- **Response Matching**: Uses a unique `id` field to match requests with corresponding responses.
- **Thread Safety**: Employs `queue.Queue` for safe inter-thread communication.

## Python Dependencies
```text
matplotlib >= 3.7
pillow >= 10.0
python-dotenv >= 1.0
keyring >= 24.0
requests >= 2.31
opencc-python-reimplemented
```

---

## LLM Integration
### Setting Up API Keys
**Ollama(Local)**
```bash
# Automatically detected after installation; no API key required
ollama pull qwen2.5:3b
```
**NVIDIA NIM**
api key：
```
nvapi-xxxxx
```
**GitHub Models**
api key：
```
github_pat_xxxxx
```

### Custom Teaching Tones
The LLM commentary feature supports multiple tone templates, allowing the depth and style of explanations to be adjusted based on the learner's skill level.

---

## i18n
| Language | File |
|------|------|
| Traditional Chinese | zh_TW.json |
| English | en.json |
**Switch Language**: Instantly switch languages via the UI menu `Settings` > `Language`.

---

## Development Commands
### KataGo Engine Commands
| Command | Purpose |
|------|------|
| `katago.exe benchmark -model <model>.bin.gz` | Test GPU performance |
| `katago.exe analysis -model <model>.bin.gz -config analysis.cfg` | Launch analysis mode |
| `katago.exe gtp -model <model>.bin.gz -config gtp.cfg` | Launch GTP mode |
### Python Commands
```bash
py ui/main_v3.py           # Launch the main application
py version.py 0.3.0-beta   # Update the version number

---

## License
This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.
