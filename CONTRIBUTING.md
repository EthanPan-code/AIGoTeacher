<!-- omit in toc -->
# Contributing to AI Go Teacher / 為 AI Go Teacher 貢獻

<a href="#English">English</a>　<a href="#Chinese">繁體中文</a>

---

<a id="English"></a>


First off, thanks for taking the time to contribute! ❤️

All types of contributions are encouraged and valued. See the [Table of Contents](#table-of-contents) for different ways to help and details about how this project handles them. Please make sure to read the relevant section before making your contribution. It will make it a lot easier for us maintainers and smooth out the experience for all involved. The community looks forward to your contributions. 🎉

> And if you like the project, but just don't have time to contribute, that's fine. There are other easy ways to support the project and show your appreciation, which we would also be very happy about:
> - Star the project
> - Refer this project in your project's README
> - Mention the project at local meetups and tell your friends/colleagues

<!-- omit in toc -->
## Table of Contents

- [I Have a Question](#i-have-a-question)
- [I Want to Contribute](#i-want-to-contribute)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Your First Code Contribution](#your-first-code-contribution)
- [Improving the Documentation](#improving-the-documentation)
- [Style Guides](#style-guides)
- [Commit Messages](#commit-messages)
- [Join the Project Team](#join-the-project-team)

## I Have a Question

> If you want to ask a question, we assume that you have read the [README](README.md).

If you need help, we recommend the following approach:

- Create a new [Feedback Form](https://forms.gle/DkHPzEUCHx1NdKjE8).
- Provide as much relevant background information as possible about the issue you are experiencing.
- Include your project and platform version information whenever applicable.

We'll do our best to help you as soon as possible.

## I Want to Contribute

> ### Legal Notice <!-- omit in toc -->
>
> By submitting a contribution to this project, you agree that:
>
> - You are the original author of the submitted content.
> - You have all necessary rights to contribute the content.
> - Your contribution will be distributed under the project's license.

### Reporting Bugs

<!-- omit in toc -->
#### Before Submitting a Bug Report

A good bug report should contain enough information that maintainers do not need to ask for additional details.

Before submitting a report, please investigate the issue, gather the necessary information, and provide a clear description. The following checklist will help us resolve the issue more efficiently:

- Make sure you are using the latest version.
- Confirm that the issue is actually a bug and not caused by your local environment, such as incompatible components or versions. (Please read the [README](README.md) first. If you simply need usage assistance, see [I Have a Question](#i-have-a-question).)
- Collect the following information:
  - Operating system, platform, and architecture (Windows, Linux, macOS, x86, ARM, etc.)
  - Input and output related to the issue (if applicable)
  - Whether the issue can be reproduced consistently

<!-- omit in toc -->
#### How Do I Submit a Good Bug Report?

> **Please do not** report security vulnerabilities, sensitive information, or other security-related issues through the public issue tracker or any other public channel.
>
> Instead, please submit the [Feedback Form](https://forms.gle/DkHPzEUCHx1NdKjE8).

### Suggesting Enhancements

This section explains how to suggest improvements for AI Go Teacher, **including both new features and enhancements to existing functionality**.

Following these guidelines helps maintainers and the community understand your proposal and determine whether a similar suggestion already exists.

<!-- omit in toc -->
#### Before Submitting an Enhancement

- Make sure you are using the latest version.
- Read the [README](README.md) carefully to verify that the feature does not already exist or cannot be achieved through configuration.
- Consider whether your proposal aligns with the project's goals and scope. Please explain the value of the feature and why it should be included. We prefer features that benefit the majority of users rather than a small niche. If your idea only applies to a limited audience, consider implementing it as a plugin or extension instead.

<!-- omit in toc -->
#### How Do I Submit a Good Enhancement Proposal?

Enhancement requests are also managed through the [Feedback Form](https://forms.gle/DkHPzEUCHx1NdKjE8).

- Describe your proposal in as much detail as possible, including step-by-step explanations where appropriate.
- Explain the **current behavior**, the **expected behavior**, and why the change is needed. If alternative solutions are insufficient, please explain why.
- Describe how the feature would benefit the majority of AI Go Teacher users. If another project has implemented a similar idea particularly well, feel free to include it as a reference.

### Your First Code Contribution

The following instructions assume a Windows development environment. On other platforms, replace `py` with the appropriate Python command.

#### Development Environment Setup

1. Install Git, Python 3.14, and a KataGo runtime with OpenCL support. For packaging, Python 3.13 and PyInstaller are also required.
2. Clone the repository and create a virtual environment from the project root:

   ```powershell
   py -3.14 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   py -m pip install -r requirements.txt
   ```

3. Download a compatible KataGo model into the `models/` directory. Ensure that `katago.exe`, the model file, and the analysis configuration file are all available. Store cloud LLM API keys in environment variables or your system keyring—**never commit them to Git**.

#### IDE Configuration

- Open the project root as your workspace and select `.venv` as the Python interpreter.
- Use UTF-8 encoding and preserve Traditional Chinese content where applicable. Python files should use four spaces for indentation.
- When running or debugging, use the project root as the working directory and `ui/main_v3.py` as the entry point.

#### Quick Start

```powershell
# Launch the interactive UI
py ui/main_v3.py

# Check the syntax of modified Python files
py -m py_compile ui/main_v3.py
```

When modifying the analysis pipeline, make sure asynchronous responses are matched using their `id`, and that live analysis results are never applied to an outdated board state.

To test the packaging process, run the following with Python 3.13:

```powershell
py pyinstaller.py
```

The packaged application will be generated in `dist/GoTeacher/`.

### Improving the Documentation

Documentation is an essential part of the project. Contributions such as fixing typos, improving usage instructions, updating outdated information, or making the project easier for newcomers to understand are all welcome.

- Before making changes, verify that the documentation matches the current application behavior. If the implementation has changed, update the relevant documentation in the same commit.
- Write clear and concise English. Keep technical terms, commands, file paths, configuration keys, and source code in their original form.
- When adding or updating commands, verify that they work from the project root and specify any required Python, KataGo, model, or operating system requirements.
- If your changes involve the UI, configuration options, or error messages, also check whether `README.md`, `i18n/zh_TW.json`, and `i18n/en.json` need to be updated.
- Ensure that links, file names, section headings, and examples are correct and usable. Never include personal file paths, API keys, or other sensitive information.
- Before submitting, verify Markdown heading levels, list indentation, fenced code block language tags, and internal links.

Recommended documentation workflow:

1. Verify the current behavior using the README, source code, or the application itself.
2. Update the document that is most closely related to the topic, avoiding duplicate documentation across multiple files.
3. Run the documented commands or examples whenever possible. If you cannot verify them, explain why in your commit message.
4. Briefly describe your documentation changes in the commit message, including any affected versions, platforms, or user groups.

## Style Guides

### Commit Messages

Commit messages should clearly communicate the purpose of a change and make the project history easy to search.

- Write a short, descriptive imperative subject line, ideally within 72 characters. Avoid vague verbs such as "Update" or "Modify" that provide little context.
- Each commit should represent a single logical change. Documentation, tests, or required translation updates related to that change may be included in the same commit.
- If additional context is needed, leave a blank line after the subject and include a body explaining the motivation, impact, and validation performed.
- If the commit relates to a Feedback Form submission, Issue, or Pull Request, include the corresponding link or reference number in the body.
- Never include API keys, personal file paths, model download credentials, or any other sensitive information in commit messages or committed files.

Recommended format:

```text
<Verb> <what changed>

<Optional: motivation, impact, and testing>
```

Example:

```text
Fix live analysis results being applied to stale board states

Validate responses using the query id and turnNumber, and verify ui/main_v3.py with py_compile.
```

## Acknowledgments

This guide is adapted from [contributing.md](https://contributing.md/generator).

---

<a id="Chinese"></a>


首先，感謝您願意花時間為本專案做出貢獻！❤️

我們歡迎並重視各種形式的貢獻。請參閱下方的[目錄](#table-of-contents)，了解不同的參與方式，以及本專案如何處理各類貢獻。在提交貢獻之前，請務必閱讀相關章節，這將能大幅減輕維護者的工作，也讓所有參與者都能擁有更順暢的協作體驗。

我們的社群期待您的加入與貢獻！🎉

> 如果您喜歡這個專案，但目前沒有時間參與開發，也沒關係。您仍然可以透過以下方式支持本專案，我們同樣會非常感謝：
>
> - 為本專案按下 Star 
> - 在您的專案 README 中推薦本專案
> - 在聚會中介紹本專案，或分享給朋友與同事

<!-- omit in toc -->
## 目錄

- [我有問題](#i-have-a-question)
- [我想貢獻](#i-want-to-contribute)
- [回報錯誤](#reporting-bugs)
- [提出功能建議](#suggesting-enhancements)
- [第一次提交程式碼](#your-first-code-contribution)
- [改善文件](#improving-the-documentation)
- [程式風格指南](#styleguides)
- [Commit 訊息](#commit-messages)
- [加入專案團隊](#join-the-project-team)


## 我有問題

> 如果您想提出問題，我們假設您已閱讀相關的[ README 文件](README.md)。


如果您需要協助，建議依照以下方式提問：

- 建立一個新的 [回饋表單](https://forms.gle/DkHPzEUCHx1NdKjE8)。
- 盡可能提供完整的背景資訊，說明您遇到的問題。
- 提供相關的專案與平台版本資訊，依實際情況提供即可。

我們會盡快協助處理您的問題。


## 我想貢獻

> ### 法律聲明 <!-- omit in toc -->
>
> 當您為本專案提交貢獻時，即表示您同意：
>
> - 您是所提交內容的原始作者。
> - 您擁有提交該內容所需的一切權利。
> - 您同意您的貢獻將依照本專案的授權條款（License）發布。

### 回報錯誤（Bug）

<!-- omit in toc -->
#### 提交 Bug 回報前

一份好的 Bug 回報，不應該讓其他人還需要再向您索取更多資訊。

因此，我們希望您在提交前先進行充分調查、蒐集資訊，並詳細描述問題。請先完成以下事項，以協助我們更快修復問題：

- 確認您使用的是最新版本。
- 確認問題確實是 Bug，而非您的環境設定造成，例如不相容的元件或版本。（請先閱讀[ README 文件](README.md)；若您只是需要使用上的協助，請參閱[我有問題](#i-have-a-question)。）
- 蒐集以下資訊：
  - 作業系統、平台及版本（Windows、Linux、macOS、x86、ARM 等）
  - 問題輸入與輸出（若適用）
  - 是否能穩定重現此問題？

<!-- omit in toc -->
#### 如何提交一份好的 Bug 回報？

> **請勿**在公開的 Issue Tracker 或其他公開場所回報任何涉及安全漏洞、敏感資訊或資安問題。
>
> 請填寫[回饋表單](https://forms.gle/DkHPzEUCHx1NdKjE8)。


### 提出功能建議

本章節說明如何向 AI Go Teacher 提出改善建議，**包括全新的功能以及既有功能的改善**。

遵循以下建議，有助於維護者及社群理解您的想法，並找出是否已有相關提案。

<!-- omit in toc -->
#### 提交功能建議前

- 確認您使用的是最新版本。
- 仔細閱讀[ README 文件](README.md)，確認此功能是否已存在，或可透過設定完成。
- 評估您的提案是否符合本專案的目標與定位。請盡可能說明此功能的價值，說服開發者其必要性。我們希望新增的功能能夠造福大多數使用者，而非僅少數特定族群。若僅適用少數人，建議考慮開發額外的外掛（Plugin）或擴充套件。

<!-- omit in toc -->
#### 如何提交一份好的功能建議？

功能建議同樣透過[回饋表單](https://forms.gle/DkHPzEUCHx1NdKjE8)管理。

- 盡可能詳細描述建議內容，並提供逐步說明。
- 說明**目前的行為**，以及**您希望看到的行為**，並解釋原因。如有其他替代方案無法滿足需求，也可一併說明。
- 說明此功能為何能讓大多數 AI Go Teacher 使用者受益。若其他專案已有類似且更完善的設計，也歡迎提供作為參考。


### 第一次提交程式碼

以下流程適用於 Windows 開發環境；其他平台請將 `py` 替換成可用的 Python 指令。

#### 開發環境設定

1. 安裝 Git、Python 3.14，以及支援 OpenCL 的 KataGo 執行環境。打包時另需 Python 3.13 與 PyInstaller。
2. 將專案複製到本機，並從專案根目錄建立虛擬環境：

   ```powershell
   py -3.14 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   py -m pip install -r requirements.txt
   ```

3. 下載相容的 KataGo 模型並放入 `models/`，確認 `katago.exe`、模型檔及分析設定檔可用。雲端 LLM 的 API 金鑰請放在環境變數或 keyring，勿提交至 Git。

#### IDE 設定

- 將專案根目錄開啟為 workspace，並選取 `.venv` 作為 Python interpreter。
- 使用 UTF-8 編碼，保留繁體中文檔案內容；Python 檔案以 4 個空白縮排。
- 執行或偵錯時以專案根目錄作為 working directory，入口檔使用 `ui/main_v3.py`。

#### 新手快速開始

```powershell
# 啟動互動式 UI
py ui/main_v3.py

# 檢查修改過的 Python 檔案語法
py -m py_compile ui/main_v3.py
```

修改分析流程時，請特別確認非同步回應以 `id` 配對，且即時結果不會套用到過期棋盤狀態。若要測試打包流程，使用 Python 3.13 執行 `py pyinstaller.py`，輸出位於 `dist/GoTeacher/`。

### 改善文件

文件同樣是專案功能的一部分。歡迎修正錯字、補充使用說明、更新過時資訊，或改善新手理解專案所需的背景資料。

- 修改前請先確認內容與目前程式行為一致；若程式行為已變更，請在同一個提交中同步更新相關文件。
- 使用清楚、簡潔的繁體中文；技術名稱、指令、檔案路徑、設定鍵及程式碼請保留其原文。
- 新增或修改指令時，請從專案根目錄確認指令可執行，並標明必要的 Python、KataGo、模型或作業系統條件。
- 涉及 UI 功能、設定或錯誤訊息時，請同時檢查 `README.md`、`i18n/zh_TW.json` 及 `i18n/en.json` 是否需要更新。
- 文件中的連結、檔名、章節標題與範例應可直接使用；避免提交個人路徑、API 金鑰或其他敏感資訊。
- 提交前請檢查 Markdown 標題層級、清單縮排、程式碼區塊語言標記，以及內部連結是否正確。

建議的文件修改流程：

1. 從 README、程式碼或實際操作確認目前行為。
2. 直接修改最接近主題的文件，避免在多個文件重複維護同一份說明。
3. 執行文件中的相關指令或範例；若無法驗證，請在提交描述中說明原因。
4. 在提交訊息中簡述修改內容，以及可能影響的版本、平台或使用者。

## 程式風格指南

### Commit 訊息

Commit 訊息應讓維護者能快速理解變更目的，並方便日後搜尋歷史紀錄。

- 主旨使用簡短、明確的祈使句，建議控制在 72 個字元內；避免使用「更新」「修改」等無法描述內容的文字。
- 一個 commit 聚焦一項邏輯變更；文件、測試或必要的翻譯更新可與該變更一起提交。
- 需要補充背景或取捨時，在主旨後空一行加入本文，說明原因、影響範圍及驗證方式。
- 若有對應的回饋表單、Issue 或 Pull Request，於本文附上連結或編號。
- 不要在訊息或提交檔案中放入 API 金鑰、個人路徑、模型下載憑證或其他敏感資料。

建議格式：

```text
<動詞> <變更內容>

<可選：原因、影響與測試方式>
```

範例：

```text
修正即時分析結果套用到過期棋盤

以 query id 與 turnNumber 驗證回應，並以 py_compile 檢查 ui/main_v3.py。
```


## 致謝

本指南改編自 [contributing.md](https://contributing.md/generator)。

