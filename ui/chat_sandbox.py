from __future__ import annotations

import copy
import threading
import traceback
import tkinter as tk
from tkinter import ttk, font as tkfont

# --- 深色主題配色方案 (移植自 llm_chat_gui_tkinter.py) ---
_CHAT_BG = "#0f172a"          # slate-950  主背景
_CHAT_PANEL = "#1e293b"       # slate-800  側邊欄/輸入框背景
_CHAT_BORDER = "#334155"      # slate-700  邊框
_CHAT_TEXT = "#f8fafc"        # slate-50   主文字
_CHAT_MUTED = "#94a3b8"       # slate-400  次要文字
_CHAT_DIM = "#64748b"         # slate-500  暗淡文字
_CHAT_ACCENT = "#2563eb"      # blue-600   主調（發送按鈕）
_CHAT_ACCENT_D = "#3b82f6"    # blue-500   hover
_CHAT_ACCENT_HOVER = "#3b82f6"  # blue-500

_USER_BUBBLE_BG = "#1e293b"   # slate-800  使用者氣泡
_ASSISTANT_BUBBLE = "#1e293b" # slate-800  助手氣泡
_ERROR_BUBBLE = "#7f1d1d"     # red-900    錯誤氣泡
_THINKING_BG = "#1e293b"      # slate-800  思考中氣泡
_AVATAR_USER = "#334155"      # slate-700  使用者頭像
_AVATAR_AI = "#2563eb"        # blue-600   AI 頭像
_BULLET = "#60a5fa"           # blue-400   列表項目符號

_FONT_MAIN = ("Segoe UI", 10)
_FONT_BOLD = ("Segoe UI", 10, "bold")
_FONT_SMALL = ("Segoe UI", 8)
_FONT_TITLE = ("Segoe UI", 14, "bold")
_FONT_TINY = ("Segoe UI", 7)


class LLMChatWindow(tk.Toplevel):
    def __init__(
        self,
        parent,
        provider,
        provider_name=None,
        provider_display_name=None,
        model_display_name=None,
        translator=None,
        language_getter=None,
    ):
        super().__init__(parent)
        self.provider = provider
        self.provider_name = provider_name or ""
        self.provider_display_name = provider_display_name or self._guess_provider_display_name()
        self.model_display_name = model_display_name or getattr(provider, "model_name", "") or self._tr("chat.unknown_model", default="Unknown model")
        self.translator = translator or (lambda key, **kwargs: key)
        self.language_getter = language_getter or (lambda: "zh_TW")

        self._busy = False
        self._stream_text = ""
        self._assistant_started = False
        self._thinking_start = None
        self._thinking_text = self._tr("chat.thinking", default="Assistant is thinking...")

        self._conversation = []
        self._max_messages = 40 

        self.title(f"{self._tr('chat.title', default='LLM Chat Sandbox')} - {self.model_display_name}")
        self.geometry("1100x720")  # 配合側邊欄加寬
        self.minsize(900, 600)    # 限制最小尺寸
        self.configure(bg=_CHAT_BG)

        # 設定 ttk 按鈕樣式（深色主題）
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(
            "Send.TButton",
            font=_FONT_BOLD,
            background=_CHAT_ACCENT,
            foreground="white",
            borderwidth=0,
            focuscolor="none",
            padding=(20, 6),
        )
        self.style.map(
            "Send.TButton",
            background=[("active", _CHAT_ACCENT_D), ("disabled", _CHAT_BORDER)],
            foreground=[("disabled", _CHAT_MUTED)]
        )
        # 捲軸樣式（深色）
        self.style.configure(
            "Dark.Vertical.TScrollbar",
            background=_CHAT_BORDER,
            troughcolor=_CHAT_PANEL,
            borderwidth=0,
            arrowcolor=_CHAT_MUTED,
        )

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _tr(self, key, **kwargs):
        return self.translator(key, **kwargs)

    def _guess_provider_display_name(self):
        class_name = self.provider.__class__.__name__.lower()
        if "ollama" in class_name:
            return "Ollama"
        if "nvidia" in class_name:
            return "NVIDIA NIM"
        if "github" in class_name:
            return "GitHub Models"
        return self.provider.__class__.__name__.replace("Provider", "") or "LLM"

    def _build_ui(self):
        # 外層水平容器：側邊欄 + 主內容區
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=0)  # 側邊欄固定寬度
        self.columnconfigure(1, weight=1)  # 主內容區縮放

        # ---- 側邊欄 ----
        self._build_sidebar()

        # ---- 主內容區 ----
        main = tk.Frame(self, bg=_CHAT_BG)
        main.grid(row=0, column=1, sticky="nsew")
        main.rowconfigure(0, weight=0)   # Header
        main.rowconfigure(1, weight=1)   # 聊天區
        main.rowconfigure(2, weight=0)   # 輸入區
        main.columnconfigure(0, weight=1)

        self._build_header(main)
        self._build_chat_area(main)
        self._build_input_area(main)

    # ============================================================
    # 側邊欄（靜態介面，暫不啟用功能）
    # ============================================================
    def _build_sidebar(self):
        sidebar = tk.Frame(self, bg=_CHAT_PANEL, width=288)
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.pack_propagate(False)
        sidebar.grid_propagate(False)

        # ---- Logo & New Chat ----
        top_frame = tk.Frame(sidebar, bg=_CHAT_PANEL)
        top_frame.pack(fill=tk.X, padx=16, pady=16)

        logo_label = tk.Label(
            top_frame,
            text="LLM Chat",
            bg=_CHAT_PANEL,
            fg=_CHAT_TEXT,
            font=_FONT_TITLE,
            anchor="w",
        )
        logo_label.pack(anchor="w")

        # New Chat 按鈕（靜態，暫不啟用）
        new_chat_btn = tk.Label(
            top_frame,
            text="  +  New Chat",
            bg=_CHAT_ACCENT,
            fg="white",
            font=_FONT_MAIN,
            padx=16,
            pady=8,
            cursor="hand2",
        )
        new_chat_btn.pack(fill=tk.X, pady=(16, 0))

        # ---- Recent Conversations ----
        recent_header = tk.Frame(sidebar, bg=_CHAT_PANEL)
        recent_header.pack(fill=tk.X, padx=12, pady=(24, 4))

        recent_label = tk.Label(
            recent_header,
            text="RECENT CONVERSATIONS",
            bg=_CHAT_PANEL,
            fg=_CHAT_DIM,
            font=_FONT_SMALL,
        )
        recent_label.pack(side=tk.LEFT)

        search_icon = tk.Label(
            recent_header,
            text="🔍",
            bg=_CHAT_PANEL,
            fg=_CHAT_DIM,
            font=_FONT_SMALL,
            cursor="hand2",
        )
        search_icon.pack(side=tk.RIGHT)

        # 對話列表容器（靜態，暫不啟用）
        list_container = tk.Frame(sidebar, bg=_CHAT_PANEL)
        list_container.pack(fill=tk.BOTH, expand=True, padx=12)

        conversations = [
            ("Understanding Quantum Computing", "2 min ago", True),
            ("Python Function Optimization", "1 hour ago", False),
            ("Creative Story Ideas", "3 hours ago", False),
            ("Marketing Strategy Brainstorm", "Yesterday", False),
            ("Daily Task Automation", "2 days ago", False),
        ]
        for title, time_str, is_active in conversations:
            self._build_conversation_item(list_container, title, time_str, is_active)

        # ---- Footer / Settings ----
        border_line = tk.Frame(sidebar, bg=_CHAT_BORDER, height=1)
        border_line.pack(fill=tk.X, side=tk.BOTTOM)

        settings_frame = tk.Frame(sidebar, bg=_CHAT_PANEL)
        settings_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=16, pady=16)

        settings_icon = tk.Label(
            settings_frame,
            text="⚙",
            bg=_CHAT_PANEL,
            fg=_CHAT_DIM,
            font=_FONT_MAIN,
            cursor="hand2",
        )
        settings_icon.pack(anchor="w")

    def _build_conversation_item(self, parent, title, time_str, is_active):
        """建立單一對話項目（靜態，暫不啟用）。"""
        bg = "#0f172a" if is_active else _CHAT_PANEL  # 選中項用深色
        fg = _CHAT_TEXT if is_active else _CHAT_MUTED

        item = tk.Frame(parent, bg=bg, padx=12, pady=8, cursor="hand2")
        item.pack(fill=tk.X, pady=2)

        title_label = tk.Label(
            item,
            text=title,
            bg=bg,
            fg=fg,
            font=_FONT_MAIN,
            anchor="w",
        )
        title_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        time_label = tk.Label(
            item,
            text=time_str,
            bg=bg,
            fg=_CHAT_DIM,
            font=_FONT_TINY,
        )
        time_label.pack(side=tk.RIGHT)

    # ============================================================
    # Header
    # ============================================================
    def _build_header(self, parent):
        header = tk.Frame(parent, bg=_CHAT_PANEL, height=64)
        header.grid(row=0, column=0, sticky="ew")
        header.pack_propagate(False)
        header.columnconfigure(0, weight=1)

        # 左側：下拉箭頭 + 標題 + 模型/提供商資訊
        left = tk.Frame(header, bg=_CHAT_PANEL)
        left.grid(row=0, column=0, sticky="w", padx=24, pady=16)

        chevron = tk.Label(
            left,
            text="▾",
            bg=_CHAT_PANEL,
            fg=_CHAT_MUTED,
            font=_FONT_SMALL,
        )
        chevron.pack(side=tk.LEFT, padx=(0, 8))

        title_text = tk.Label(
            left,
            text=self._tr("chat.title", default="LLM Chat Sandbox"),
            bg=_CHAT_PANEL,
            fg=_CHAT_TEXT,
            font=_FONT_BOLD,
        )
        title_text.pack(side=tk.LEFT)

        # 模型與提供商資訊（次要文字）
        info_label = tk.Label(
            left,
            text=f"  ·  {self.model_display_name}  ·  {self.provider_display_name}",
            bg=_CHAT_PANEL,
            fg=_CHAT_DIM,
            font=_FONT_SMALL,
        )
        info_label.pack(side=tk.LEFT, padx=(8, 0))

        # 右側：更多按鈕（靜態，暫不啟用）
        right = tk.Frame(header, bg=_CHAT_PANEL)
        right.grid(row=0, column=1, sticky="e", padx=24, pady=16)

        more_btn = tk.Label(
            right,
            text="⋮",
            bg=_CHAT_PANEL,
            fg=_CHAT_MUTED,
            font=_FONT_MAIN,
            cursor="hand2",
            padx=8,
        )
        more_btn.pack()

        # 底部邊框線
        border = tk.Frame(parent, bg=_CHAT_BORDER, height=1)
        border.grid(row=0, column=0, sticky="ews")

    # ============================================================
    # 聊天區
    # ============================================================
    def _build_chat_area(self, parent):
        history_wrap = tk.Frame(parent, bg=_CHAT_BG)
        history_wrap.grid(row=1, column=0, sticky="nsew", padx=24, pady=12)

        self._history_text = tk.Text(
            history_wrap,
            wrap="word",
            font=_FONT_MAIN,
            bg=_CHAT_BG,
            fg=_CHAT_TEXT,
            insertbackground=_CHAT_ACCENT,
            relief="flat",
            bd=0,
            highlightthickness=0,
            padx=16,
            pady=16,
            state="disabled",
        )
        history_scroll = ttk.Scrollbar(
            history_wrap,
            command=self._history_text.yview,
            style="Dark.Vertical.TScrollbar",
        )
        self._history_text.configure(yscrollcommand=history_scroll.set)

        self._history_text.pack(side="left", fill="both", expand=True)
        history_scroll.pack(side="right", fill="y")

        # --- 深色主題對話標籤與氣泡 ---
        # 使用者訊息靠右
        self._history_text.tag_configure(
            "user_role",
            foreground=_CHAT_DIM,
            font=_FONT_SMALL,
            spacing1=15,
            spacing3=2,
            justify="right",
        )
        self._history_text.tag_configure(
            "user_body",
            foreground="#e2e8f0",
            background=_USER_BUBBLE_BG,
            spacing3=5,
            justify="right",
            rmargin=10,
            lmargin1=150,
            lmargin2=150,
        )

        # 助手訊息靠左
        self._history_text.tag_configure(
            "assistant_role",
            foreground=_CHAT_DIM,
            font=_FONT_SMALL,
            spacing1=15,
            spacing3=2,
            justify="left",
        )
        self._history_text.tag_configure(
            "assistant_body",
            foreground="#e2e8f0",
            background=_ASSISTANT_BUBBLE,
            spacing3=5,
            justify="left",
            lmargin1=25,
            lmargin2=25,
            rmargin=150,
        )

        # 錯誤訊息
        self._history_text.tag_configure(
            "error_role",
            foreground="#fca5a5",
            font=_FONT_BOLD,
            spacing1=15,
            spacing3=2,
            justify="left",
        )
        self._history_text.tag_configure(
            "error_body",
            foreground="#fecaca",
            background=_ERROR_BUBBLE,
            spacing3=5,
            justify="left",
            lmargin1=10,
            lmargin2=10,
            rmargin=10,
        )

        self._history_text.tag_configure(
            "thinking",
            foreground=_CHAT_MUTED,
            font=("Segoe UI", 10, "italic"),
            spacing1=10,
            spacing3=10,
        )

        self._history_text.bind("<MouseWheel>", self._on_mousewheel)
        self._history_text.bind("<Button-4>", self._on_mousewheel_linux)
        self._history_text.bind("<Button-5>", self._on_mousewheel_linux)

    # ============================================================
    # 輸入區
    # ============================================================
    def _build_input_area(self, parent):
        input_container = tk.Frame(parent, bg=_CHAT_BG)
        input_container.grid(row=2, column=0, sticky="ew", padx=24, pady=24)

        # 輸入框外框（深色圓角風格）
        input_frame = tk.Frame(
            input_container,
            bg=_CHAT_PANEL,
            highlightbackground=_CHAT_BORDER,
            highlightthickness=1,
        )
        input_frame.pack(fill=tk.X)
        input_frame.columnconfigure(0, weight=1)

        self._input_text = tk.Text(
            input_frame,
            height=4,
            wrap="word",
            font=_FONT_MAIN,
            bg=_CHAT_PANEL,
            fg=_CHAT_TEXT,
            insertbackground=_CHAT_TEXT,
            relief="flat",
            bd=0,
            highlightthickness=0,
            padx=12,
            pady=12,
        )
        self._input_text.grid(row=0, column=0, sticky="ew")
        self._input_text.bind("<Return>", self._on_enter)
        self._input_text.bind("<Shift-Return>", self._on_shift_enter)

        # Placeholder 行為
        self._placeholder_text = self._tr("chat.placeholder", default="Message LLM Chat...")
        self._input_text.insert("1.0", self._placeholder_text)
        self._input_text.config(fg=_CHAT_DIM)
        self._input_text.bind("<FocusIn>", self._on_input_focus_in)
        self._input_text.bind("<FocusOut>", self._on_input_focus_out)

        # 底部按鈕列
        button_bar = tk.Frame(input_frame, bg=_CHAT_PANEL)
        button_bar.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 8))

        # 分隔線
        sep = tk.Frame(button_bar, bg=_CHAT_BORDER, height=1)
        sep.pack(fill=tk.X, side=tk.TOP, pady=(0, 8))

        button_row = tk.Frame(button_bar, bg=_CHAT_PANEL)
        button_row.pack(fill=tk.X)
        button_row.columnconfigure(0, weight=1)

        # 左側 + 按鈕（靜態，暫不啟用）
        plus_btn = tk.Label(
            button_row,
            text="  +  ",
            bg=_CHAT_BG,
            fg=_CHAT_MUTED,
            font=_FONT_SMALL,
            padx=12,
            pady=4,
            cursor="hand2",
        )
        plus_btn.pack(side=tk.LEFT)

        # 右側 Send 按鈕
        self.send_btn = ttk.Button(
            button_row,
            text=f"  {self._tr('chat.send', default='Send')}  ➤  ",
            command=self._on_send,
            style="Send.TButton",
        )
        self.send_btn.pack(side=tk.RIGHT)

    def _on_input_focus_in(self, event):
        """輸入框獲得焦點時清除 placeholder。"""
        current = self._input_text.get("1.0", "end-1c")
        if current == self._placeholder_text:
            self._input_text.delete("1.0", "end")
            self._input_text.config(fg=_CHAT_TEXT)

    def _on_input_focus_out(self, event):
        """輸入框失去焦點時恢復 placeholder。"""
        current = self._input_text.get("1.0", "end-1c").strip()
        if not current:
            self._input_text.delete("1.0", "end")
            self._input_text.insert("1.0", self._placeholder_text)
            self._input_text.config(fg=_CHAT_DIM)

    def _on_enter(self, event):
        self._on_send()
        return "break"

    def _on_shift_enter(self, event):
        self._input_text.insert("insert", "\n")
        return "break"

    def _on_send(self):
        if self._busy:
            return

        raw = self._input_text.get("1.0", "end-1c").strip()
        if not raw:
            return

        self._input_text.delete("1.0", "end")
        self._remember("user", raw)
        self._add_message("user", raw)
        self._start_generation(raw)

    def _on_close(self):
        self.destroy()

    def _append_history(self, role_text, content, tag):
        self._history_text.configure(state="normal")
        padding_content = f"{content.strip()}  "
        
        self._history_text.insert("end", f"{role_text}\n", f"{tag}_role")
        self._history_text.insert("end", f"{padding_content}\n\n", f"{tag}_body")
        self._history_text.configure(state="disabled")
        self._history_text.see("end")

    def _schedule(self, callback):
        try:
            if self.winfo_exists():
                self.after(0, callback)
        except tk.TclError:
            pass

    def _add_message(self, role, content, is_error=False):
        tag = "error" if is_error else role
        role_text = self._tr("chat.role_user", default="User") if role == "user" else self._tr("chat.role_assistant", default="Assistant")
        self._append_history(role_text, content, tag)

    def _show_thinking(self):
        if self._thinking_start is not None:
            return
        self._history_text.configure(state="normal")
        self._thinking_start = self._history_text.index("end-1c")
        self._history_text.insert("end", f"💬 {self._thinking_text}\n\n", "thinking")
        self._history_text.configure(state="disabled")
        self._history_text.see("end")

    def _hide_thinking(self):
        if self._thinking_start is None:
            return
        self._history_text.configure(state="normal")
        try:
            self._history_text.delete(self._thinking_start, "end")
        except Exception:
            pass
        self._history_text.configure(state="disabled")
        self._thinking_start = None
        self._history_text.see("end")

    def _begin_assistant_message(self):
        if self._assistant_started:
            return
        self._hide_thinking()
        self._history_text.configure(state="normal")
        self._history_text.insert("end", f"{self._tr('chat.role_assistant', default='Assistant')}\n", "assistant_role")
        self._history_text.insert("end", "  \n\n", "assistant_body") 
        self._history_text.configure(state="disabled")
        self._assistant_started = True
        self._history_text.see("end")

    def _append_assistant_delta(self, chunk_text):
        if not chunk_text:
            return

        if chunk_text == self._thinking_text:
            return

        self._begin_assistant_message()

        if self._stream_text and chunk_text.startswith(self._stream_text):
            delta = chunk_text[len(self._stream_text):]
        else:
            delta = chunk_text

        if not delta:
            return

        self._history_text.configure(state="normal")
        # 由於串流是一字字塞入，我們移除結尾換行，交給完成時處理
        self._history_text.insert("end-2c", delta, "assistant_body")
        self._history_text.configure(state="disabled")
        self._stream_text = chunk_text
        self._history_text.see("end")

    def _finish_generation(self):

        if self._stream_text.strip():
            self._remember(
                "assistant",
                self._stream_text,
            )
        # 補上最後的對話尾隨換行
        self._history_text.configure(state="normal")
        self._history_text.insert("end", "  \n\n", "assistant_body")
        self._history_text.configure(state="disabled")
        
        self._busy = False
        self._hide_thinking()
        self._assistant_started = False
        self._stream_text = ""

    def _show_error(self, error, trace_text):
        error_message = [
            self._tr("chat.error_prefix", default="發生錯誤："),
            str(error),
            "",
            self._tr("chat.error_log", default="完整 Exception Log："),
            trace_text.strip(),
        ]
        self._remember("assistant", "\n".join(error_message))
        self._add_message("assistant", "\n".join(error_message), is_error=True)

    def _create_sandbox_provider(self, ui_callback, on_complete, on_error):
        provider = copy.copy(self.provider)
        provider.ui_callback = ui_callback
        provider.status_callback = None
        provider.on_complete_callback = on_complete
        provider.error_callback = on_error
        provider.is_generating = False
        return provider

    def _handle_provider_error(self, provider, error, trace_text):
        provider.ui_callback = lambda *_args, **_kwargs: None
        self._show_error(error, trace_text)
        self._finish_generation()

    def _start_generation(self, user_text):
        self._busy = True
        self._show_thinking()

        provider = None

        def on_error(error, trace_text):
            if provider is not None:
                provider.ui_callback = lambda *_args, **_kwargs: None
            self._schedule(lambda: self._handle_provider_error(provider, error, trace_text))

        provider = self._create_sandbox_provider(
            ui_callback=lambda text: self._schedule(lambda: self._append_assistant_delta(text)),
            on_complete=lambda: self._schedule(self._finish_generation),
            on_error=on_error,
        )

        def run():
            try:
                provider.chat_stream(user_text, conversation=self._conversation)
            except Exception:
                self._schedule(lambda: self._show_error(Exception("Unexpected provider failure"), traceback.format_exc()))
                self._schedule(self._finish_generation)

        threading.Thread(target=run, daemon=True).start()

    def _on_mousewheel(self, event):
        try:
            self._history_text.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except Exception:
            pass
        return "break"

    def _on_mousewheel_linux(self, event):
        try:
            delta = -1 if event.num == 5 else 1
            self._history_text.yview_scroll(delta, "units")
        except Exception:
            pass
        return "break"
    
    def _remember(self, role, content):
        """加入聊天記憶"""

        self._conversation.append({
            "role": role,
            "content": content,
        })

        # 超過限制時，只保留最新 N 則
        if len(self._conversation) > self._max_messages:
            self._conversation = self._conversation[-self._max_messages:]