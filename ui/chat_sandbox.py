from __future__ import annotations

import copy
import re
import threading
import time
import traceback
import tkinter as tk
from tkinter import ttk, font as tkfont, filedialog, messagebox

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
_FONT_CODE = ("Consolas", 9)
_FONT_ITALIC = ("Segoe UI", 10, "italic")
_FONT_H1 = ("Segoe UI", 13, "bold")
_FONT_H2 = ("Segoe UI", 11, "bold")
_FONT_H3 = ("Segoe UI", 10, "bold")
_CODE_BG = "#0b1220"          # 程式碼區塊背景
_USER_BUBBLE_ACCENT = "#2563eb"  # 使用者氣泡（藍色）


# ============================================================
# 輕量 Markdown 渲染器（Phase 1：無新依賴，純 Text tag 實作）
# ============================================================
_MD_INLINE_RE = re.compile(r"(\*\*.+?\*\*|\*[^*\n]+\*|`[^`\n]+?`)")
_MD_HEADING_RE = re.compile(r"^(#{1,3})\s+(.*)$")
_MD_ORDERED_RE = re.compile(r"^(\d+)[.)]\s+(.*)$")


def _insert_inline_markdown(text_widget, line, base_tag=None):
    """把單行文字插入 Text widget，支援 **粗體**、*斜體*、`行內程式碼`。"""
    for part in _MD_INLINE_RE.split(line):
        if not part:
            continue
        tags = (base_tag,) if base_tag else ()
        if part.startswith("**") and part.endswith("**") and len(part) > 4:
            text_widget.insert("end", part[2:-2], tags + ("md_bold",))
        elif part.startswith("`") and part.endswith("`") and len(part) > 2:
            text_widget.insert("end", part[1:-1], tags + ("md_icode",))
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            text_widget.insert("end", part[1:-1], tags + ("md_italic",))
        else:
            text_widget.insert("end", part, tags)


def render_markdown(text_widget, content):
    """把 Markdown 內容渲染到 Text widget：標題 / 列表 / 粗斜體 / 行程式碼 / 程式碼區塊。"""
    text_widget.configure(state="normal")
    text_widget.delete("1.0", "end")
    in_code = False
    lines = content.split("\n")
    while lines and not lines[-1].strip():
        lines.pop()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            text_widget.insert("end", line + "\n", ("md_code",))
            continue
        m = _MD_HEADING_RE.match(stripped)
        if m:
            level = len(m.group(1))
            line_start = text_widget.index("end-1c")
            _insert_inline_markdown(text_widget, m.group(2))
            text_widget.insert("end", "\n")
            text_widget.tag_add(f"md_h{level}", line_start, "end-1c")
            continue
        if stripped.startswith(("- ", "* ")) and not stripped.startswith("**"):
            text_widget.insert("end", "  \u2022 ", ("md_bullet",))
            _insert_inline_markdown(text_widget, stripped[2:])
            text_widget.insert("end", "\n")
            continue
        ol = _MD_ORDERED_RE.match(stripped)
        if ol:
            text_widget.insert("end", f"  {ol.group(1)}. ", ("md_bullet",))
            _insert_inline_markdown(text_widget, ol.group(2))
            text_widget.insert("end", "\n")
            continue
        _insert_inline_markdown(text_widget, line)
        text_widget.insert("end", "\n")
    text_widget.configure(state="disabled")


# ============================================================
# 訊息卡片（頭像 + 角色名 + 複製按鈕 + Markdown 訊息本體）
# ============================================================
class MessageBubble(tk.Frame):
    def __init__(self, parent, window, role, is_error=False):
        super().__init__(parent, bg=_CHAT_BG)
        self.window = window
        self.role = role
        self.is_error = is_error
        self.raw_content = ""

        is_user = role == "user"
        body_bg = _USER_BUBBLE_ACCENT if is_user else (_ERROR_BUBBLE if is_error else _CHAT_BG)
        body_fg = "white" if is_user else ("#fecaca" if is_error else "#e2e8f0")
        avatar_bg = _AVATAR_USER if is_user else (_ERROR_BUBBLE if is_error else _AVATAR_AI)
        if is_user:
            avatar_text = "你" if str(window.language_getter()).startswith("zh") else "U"
            role_text = window._tr("chat.role_user", default="User")
        else:
            avatar_text = "AI"
            role_text = window._tr("chat.role_assistant", default="Assistant")

        header = tk.Frame(self, bg=_CHAT_BG)
        header.pack(fill=tk.X, padx=2, pady=(6, 2))

        avatar = tk.Label(
            header, text=avatar_text, bg=avatar_bg, fg="white",
            font=_FONT_SMALL, width=3, pady=2,
        )
        avatar.pack(side=tk.LEFT)

        name = tk.Label(
            header, text=f"  {role_text}", bg=_CHAT_BG, fg=_CHAT_MUTED, font=_FONT_SMALL,
        )
        name.pack(side=tk.LEFT)

        copy_btn = tk.Label(
            header, text="\U0001F4CB", bg=_CHAT_BG, fg=_CHAT_DIM,
            font=_FONT_SMALL, cursor="hand2",
        )
        copy_btn.pack(side=tk.RIGHT)
        copy_btn.bind("<Button-1>", self._copy_content)
        copy_btn.bind("<Enter>", lambda _e: copy_btn.config(fg=_CHAT_TEXT))
        copy_btn.bind("<Leave>", lambda _e: copy_btn.config(fg=_CHAT_DIM))
        self._copy_btn = copy_btn

        self.body = tk.Text(
            self, wrap="word", height=1, font=_FONT_MAIN,
            bg=body_bg, fg=body_fg, relief="flat", bd=0,
            highlightthickness=0, padx=14, pady=10,
            spacing1=2, spacing3=2, cursor="arrow", state="disabled",
        )
        self._configure_body_tags()
        self.body.pack(fill=tk.X, expand=True, padx=(38, 2), pady=(0, 6))

        window._bind_wheel(self)

    def _configure_body_tags(self):
        t = self.body
        t.tag_configure("md_bold", font=_FONT_BOLD)
        t.tag_configure("md_italic", font=_FONT_ITALIC)
        t.tag_configure("md_icode", font=_FONT_CODE, background=_CHAT_BORDER)
        t.tag_configure(
            "md_code", font=_FONT_CODE, background=_CODE_BG,
            foreground="#e2e8f0", lmargin1=8, lmargin2=8,
        )
        t.tag_configure("md_h1", font=_FONT_H1, spacing1=6, spacing3=4)
        t.tag_configure("md_h2", font=_FONT_H2, spacing1=5, spacing3=3)
        t.tag_configure("md_h3", font=_FONT_H3, spacing1=4, spacing3=2)
        t.tag_configure("md_bullet", foreground=_BULLET)

    def _copy_content(self, event=None):
        try:
            self.window.clipboard_clear()
            self.window.clipboard_append(self.raw_content)
        except tk.TclError:
            pass

    def set_content(self, content):
        self.raw_content = content
        render_markdown(self.body, content)
        self.window.after_idle(self._fix_height)

    def _fix_height(self):
        """依 wrap 後的 displayline 數調整 Text 高度，消除多餘空白。"""
        if not self.winfo_exists():
            return
        try:
            self.window.update_idletasks()
            result = self.body.count("1.0", "end-1c", "displaylines")
            if result:
                self.body.configure(height=max(1, int(result[0])))
        except tk.TclError:
            pass


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
        self._thinking_text = self._tr("chat.thinking", default="Assistant is thinking...")

        self._max_messages = 40
        self._search_query = ""
        self._conversations = [self._make_conversation()]
        self._active_conv_index = 0
        self._conversation = self._conversations[0]["messages"]

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
        if "openrouter" in class_name:
            return "OpenRouter"
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
    # 側邊欄（對話列表 / New Chat / 搜尋 / 設定）
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

        # New Chat 按鈕
        new_chat_btn = tk.Label(
            top_frame,
            text=f"  +  {self._tr('chat.new_chat_btn', default='New Chat')}",
            bg=_CHAT_ACCENT,
            fg="white",
            font=_FONT_MAIN,
            padx=16,
            pady=8,
            cursor="hand2",
        )
        new_chat_btn.pack(fill=tk.X, pady=(16, 0))
        new_chat_btn.bind("<Button-1>", self._on_new_chat)

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
        search_icon.bind("<Button-1>", self._on_search_click)

        # 對話列表容器（動態重建）
        self._conv_list_container = tk.Frame(sidebar, bg=_CHAT_PANEL)
        self._conv_list_container.pack(fill=tk.BOTH, expand=True, padx=12)
        self._refresh_conversation_list()

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
        settings_icon.bind("<Button-1>", self._on_settings_menu)

    def _build_conversation_item(self, parent, index, title, time_str, is_active):
        """建立單一對話項目，點擊可切換。"""
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

        def _select(_evt=None, i=index):
            self._select_conversation(i)

        item.bind("<Button-1>", _select)
        title_label.bind("<Button-1>", _select)
        time_label.bind("<Button-1>", _select)

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
        chevron.configure(cursor="hand2")
        chevron.bind("<Button-1>", self._on_model_menu)
        self._chevron_label = chevron

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
        self._header_info_label = info_label

        # 右側：更多按鈕
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
        more_btn.bind("<Button-1>", self._on_more_menu)

        # 底部邊框線
        border = tk.Frame(parent, bg=_CHAT_BORDER, height=1)
        border.grid(row=0, column=0, sticky="ews")

    # ============================================================
    # 聊天區
    # ============================================================
    def _build_chat_area(self, parent):
        history_wrap = tk.Frame(parent, bg=_CHAT_BG)
        history_wrap.grid(row=1, column=0, sticky="nsew", padx=24, pady=12)
        history_wrap.rowconfigure(0, weight=1)
        history_wrap.columnconfigure(0, weight=1)

        self._chat_canvas = tk.Canvas(
            history_wrap, bg=_CHAT_BG, highlightthickness=0, bd=0,
        )
        history_scroll = ttk.Scrollbar(
            history_wrap,
            command=self._chat_canvas.yview,
            style="Dark.Vertical.TScrollbar",
        )
        self._chat_canvas.configure(yscrollcommand=history_scroll.set)
        self._chat_canvas.grid(row=0, column=0, sticky="nsew")
        history_scroll.grid(row=0, column=1, sticky="ns")

        # 所有訊息卡片都放入 container，隨 Canvas 捲動
        self._msg_container = tk.Frame(self._chat_canvas, bg=_CHAT_BG)
        self._msg_window = self._chat_canvas.create_window(
            (0, 0), window=self._msg_container, anchor="nw",
        )
        self._msg_container.bind("<Configure>", self._on_msg_container_configure)
        self._chat_canvas.bind("<Configure>", self._on_chat_canvas_configure)

        self._bubbles = []
        self._current_bubble = None     # 串流中的 assistant 卡片
        self._thinking_widget = None
        self._stick_bottom = True       # 使用者停留在底部時自動跟隨捲動
        self._resize_job = None
        self._stream_render_job = None
        self._bind_wheel(self._chat_canvas)

    # ------------------------------------------------------------
    # 捲動 / 縮放管理
    # ------------------------------------------------------------
    def _on_msg_container_configure(self, _event=None):
        try:
            self._chat_canvas.configure(scrollregion=self._chat_canvas.bbox("all"))
        except tk.TclError:
            return
        if self._stick_bottom:
            self._chat_canvas.yview_moveto(1.0)

    def _on_chat_canvas_configure(self, event):
        self._chat_canvas.itemconfigure(self._msg_window, width=event.width)
        if self._resize_job is not None:
            try:
                self.after_cancel(self._resize_job)
            except tk.TclError:
                pass
        self._resize_job = self.after(150, self._relayout_bubbles)

    def _relayout_bubbles(self):
        """視窗寬度改變後重算所有卡片高度。"""
        self._resize_job = None
        for bubble in list(self._bubbles):
            bubble._fix_height()
        try:
            self._chat_canvas.configure(scrollregion=self._chat_canvas.bbox("all"))
            if self._stick_bottom:
                self._chat_canvas.yview_moveto(1.0)
        except tk.TclError:
            pass

    def _scroll_to_bottom(self):
        try:
            self._chat_canvas.yview_moveto(1.0)
        except tk.TclError:
            pass

    def _update_stick_bottom(self):
        try:
            self._stick_bottom = self._chat_canvas.yview()[1] >= 0.98
        except tk.TclError:
            pass

    def _on_chat_wheel(self, event):
        try:
            self._chat_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except tk.TclError:
            pass
        self.after_idle(self._update_stick_bottom)
        return "break"

    def _on_chat_wheel_linux(self, event):
        try:
            delta = -1 if event.num == 5 else 1
            self._chat_canvas.yview_scroll(delta, "units")
        except tk.TclError:
            pass
        self.after_idle(self._update_stick_bottom)
        return "break"

    def _bind_wheel(self, widget):
        """遞迴綁定滾輪事件，讓游標在卡片上也能捲動聊天區。"""
        widget.bind("<MouseWheel>", self._on_chat_wheel)
        widget.bind("<Button-4>", self._on_chat_wheel_linux)
        widget.bind("<Button-5>", self._on_chat_wheel_linux)
        for child in widget.winfo_children():
            self._bind_wheel(child)

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

        # 左側 + 按鈕
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
        plus_btn.bind("<Button-1>", self._on_plus_menu)

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

        # 首則訊息作為對話標題
        conv = self._active_conversation()
        if len(conv["messages"]) == 1:
            conv["title"] = raw if len(raw) <= 20 else raw[:20] + "…"
            self._refresh_conversation_list()

        self._start_generation(raw)

    def _on_close(self):
        self.destroy()

    # ============================================================
    # 對話列表管理（New Chat / 切換 / 搜尋）
    # ============================================================
    def _make_conversation(self):
        return {
            "title": self._tr("chat.new_chat", default="新對話"),
            "created": time.time(),
            "messages": [],
        }

    def _active_conversation(self):
        return self._conversations[self._active_conv_index]

    def _format_relative_time(self, ts):
        elapsed = max(0, int(time.time() - ts))
        if elapsed < 60:
            return self._tr("chat.time_now", default="Now")
        if elapsed < 3600:
            return f"{elapsed // 60}m"
        if elapsed < 86400:
            return f"{elapsed // 3600}h"
        return f"{elapsed // 86400}d"

    def _refresh_conversation_list(self):
        container = getattr(self, "_conv_list_container", None)
        if container is None:
            return
        for child in container.winfo_children():
            child.destroy()
        query = (self._search_query or "").strip().lower()
        for idx, conv in enumerate(self._conversations):
            if query:
                haystack = (conv["title"] + " " + " ".join(
                    m["content"] for m in conv["messages"]
                )).lower()
                if query not in haystack:
                    continue
            self._build_conversation_item(
                container,
                idx,
                conv["title"],
                self._format_relative_time(conv["created"]),
                idx == self._active_conv_index,
            )

    def _render_history(self):
        for child in self._msg_container.winfo_children():
            child.destroy()
        self._bubbles = []
        self._current_bubble = None
        self._thinking_widget = None
        for msg in self._conversation:
            role = msg.get("role", "assistant")
            if role not in ("user", "assistant"):
                role = "assistant"
            self._add_message(role, msg.get("content", ""))
        self._stick_bottom = True
        self.after_idle(self._scroll_to_bottom)

    def _select_conversation(self, index):
        if self._busy:
            self.bell()
            return
        if index == self._active_conv_index:
            return
        self._active_conv_index = index
        self._conversation = self._conversations[index]["messages"]
        self._render_history()
        self._refresh_conversation_list()

    def _on_new_chat(self, event=None):
        if self._busy:
            self.bell()
            return
        current = self._active_conversation()
        if not current["messages"]:
            # 目前已是空白對話，不重複新增
            return
        self._conversations.insert(0, self._make_conversation())
        self._active_conv_index = 0
        self._conversation = self._conversations[0]["messages"]
        self._render_history()
        self._refresh_conversation_list()

    def _on_search_click(self, event=None):
        win = getattr(self, "_search_window", None)
        if win is not None and win.winfo_exists():
            win.lift()
            return
        win = tk.Toplevel(self)
        self._search_window = win
        win.title(self._tr("chat.search_title", default="搜尋對話"))
        win.configure(bg=_CHAT_PANEL)
        win.geometry("320x48")
        win.transient(self)

        entry = tk.Entry(
            win, bg=_CHAT_BG, fg=_CHAT_TEXT,
            insertbackground=_CHAT_TEXT, font=_FONT_MAIN, relief="flat",
        )
        entry.pack(fill=tk.X, padx=10, pady=10)
        entry.insert(0, self._search_query)
        entry.focus_set()

        def on_change(_evt=None):
            self._search_query = entry.get()
            self._refresh_conversation_list()

        def on_close():
            self._search_query = ""
            self._refresh_conversation_list()
            win.destroy()

        entry.bind("<KeyRelease>", on_change)
        win.protocol("WM_DELETE_WINDOW", on_close)

    # ============================================================
    # Header 選單（模型切換 / 更多 / 設定）
    # ============================================================
    def _make_menu(self):
        return tk.Menu(
            self, tearoff=0,
            bg=_CHAT_PANEL, fg=_CHAT_TEXT,
            activebackground=_CHAT_ACCENT, activeforeground="white",
            font=_FONT_MAIN,
        )

    def _popup_menu(self, menu, widget):
        menu.tk_popup(widget.winfo_rootx(), widget.winfo_rooty() + widget.winfo_height())

    def _on_model_menu(self, event=None):
        menu = self._make_menu()
        get_models = getattr(self.provider, "get_available_models", None)
        models = []
        if callable(get_models):
            try:
                models = list(get_models() or [])
            except Exception:
                models = []
        current = getattr(self.provider, "model_name", None)
        for name in models:
            mark = "● " if name == current else "   "
            menu.add_command(label=f"{mark}{name}",
                             command=lambda n=name: self._switch_model(n))
        if not models:
            menu.add_command(
                label=self._tr("chat.no_models", default="無可用模型"),
                state="disabled",
            )
        widget = event.widget if event is not None else getattr(self, "_chevron_label", self)
        self._popup_menu(menu, widget)

    def _switch_model(self, model_name):
        set_model = getattr(self.provider, "set_model", None)
        if callable(set_model):
            try:
                set_model(model_name)
            except Exception as exc:
                messagebox.showerror(
                    self._tr("chat.title", default="LLM Chat Sandbox"),
                    str(exc), parent=self,
                )
                return
        self.model_display_name = model_name
        self.title(f"{self._tr('chat.title', default='LLM Chat Sandbox')} - {model_name}")
        if getattr(self, "_header_info_label", None) is not None:
            self._header_info_label.config(
                text=f"  ·  {model_name}  ·  {self.provider_display_name}"
            )

    def _on_settings_menu(self, event):
        menu = self._make_menu()
        menu.add_command(
            label=self._tr("chat.export_all", default="匯出所有對話…"),
            command=self._export_all_conversations,
        )
        menu.add_separator()
        menu.add_command(
            label=self._tr("chat.clear_all", default="清除所有對話"),
            command=self._clear_all_conversations,
        )
        self._popup_menu(menu, event.widget)

    def _on_more_menu(self, event):
        menu = self._make_menu()
        menu.add_command(
            label=self._tr("chat.export_current", default="匯出目前對話…"),
            command=self._export_current_conversation,
        )
        menu.add_command(
            label=self._tr("chat.clear_current", default="清空目前對話"),
            command=self._clear_current_conversation,
        )
        self._popup_menu(menu, event.widget)

    def _on_plus_menu(self, event):
        menu = self._make_menu()
        menu.add_command(
            label=self._tr("chat.paste_clipboard", default="貼上剪貼簿內容"),
            command=self._paste_clipboard,
        )
        menu.add_command(
            label=self._tr("chat.clear_input", default="清除輸入框"),
            command=self._clear_input,
        )
        menu.add_separator()
        menu.add_command(
            label=self._tr("chat.insert_sample", default="插入範例提示詞"),
            command=self._insert_sample_prompt,
        )
        self._popup_menu(menu, event.widget)

    def _paste_clipboard(self):
        try:
            text = self.clipboard_get()
        except tk.TclError:
            self.bell()
            return
        self._ensure_input_not_placeholder()
        self._input_text.insert("insert", text)
        self._input_text.focus_set()

    def _clear_input(self):
        self._input_text.delete("1.0", "end")
        self._input_text.focus_set()

    def _insert_sample_prompt(self):
        sample = self._tr(
            "chat.sample_prompt",
            default="請用初學者聽得懂的方式，解釋圍棋中「厚勢」與「實地」的差別。",
        )
        self._ensure_input_not_placeholder()
        self._input_text.insert("end", sample)
        self._input_text.focus_set()

    def _ensure_input_not_placeholder(self):
        current = self._input_text.get("1.0", "end-1c")
        if current == self._placeholder_text:
            self._input_text.delete("1.0", "end")
            self._input_text.config(fg=_CHAT_TEXT)

    # ============================================================
    # 對話清除 / 匯出
    # ============================================================
    def _clear_current_conversation(self):
        if self._busy:
            self.bell()
            return
        conv = self._active_conversation()
        conv["messages"].clear()
        conv["title"] = self._tr("chat.new_chat", default="新對話")
        conv["created"] = time.time()
        self._render_history()
        self._refresh_conversation_list()

    def _clear_all_conversations(self):
        if self._busy:
            self.bell()
            return
        self._conversations = [self._make_conversation()]
        self._active_conv_index = 0
        self._conversation = self._conversations[0]["messages"]
        self._search_query = ""
        self._render_history()
        self._refresh_conversation_list()

    def _export_conversations(self, targets, default_name):
        if not any(conv["messages"] for conv in targets):
            self.bell()
            return
        path = filedialog.asksaveasfilename(
            parent=self,
            defaultextension=".txt",
            initialfile=default_name,
            filetypes=[("Text Files", "*.txt")],
        )
        if not path:
            return
        lines = []
        for conv in targets:
            stamp = time.strftime("%Y-%m-%d %H:%M", time.localtime(conv["created"]))
            lines.append(f"# {conv['title']}  ({stamp})")
            for msg in conv["messages"]:
                role = (
                    self._tr("chat.role_user", default="User")
                    if msg.get("role") == "user"
                    else self._tr("chat.role_assistant", default="Assistant")
                )
                lines.append(f"[{role}] {msg.get('content', '').strip()}")
                lines.append("")
            lines.append("=" * 60)
            lines.append("")
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
        except OSError as exc:
            messagebox.showerror(
                self._tr("chat.title", default="LLM Chat Sandbox"),
                str(exc), parent=self,
            )

    def _export_current_conversation(self):
        conv = self._active_conversation()
        self._export_conversations([conv], f"{conv['title']}.txt")

    def _export_all_conversations(self):
        self._export_conversations(list(self._conversations), "llm_chat_history.txt")

    def _schedule(self, callback):
        try:
            if self.winfo_exists():
                self.after(0, callback)
        except tk.TclError:
            pass

    def _add_message(self, role, content, is_error=False):
        bubble = MessageBubble(self._msg_container, self, role, is_error=is_error)
        bubble.pack(fill=tk.X)
        self._bubbles.append(bubble)
        bubble.set_content(content)
        if self._stick_bottom:
            self.after_idle(self._scroll_to_bottom)
        return bubble

    def _show_thinking(self):
        if self._thinking_widget is not None:
            return
        widget = tk.Label(
            self._msg_container,
            text=f"\U0001F4AC {self._thinking_text}",
            bg=_CHAT_BG,
            fg=_CHAT_MUTED,
            font=_FONT_ITALIC,
            anchor="w",
        )
        widget.pack(fill=tk.X, padx=6, pady=8)
        self._thinking_widget = widget
        self._bind_wheel(widget)
        self._scroll_to_bottom()

    def _hide_thinking(self):
        widget = self._thinking_widget
        self._thinking_widget = None
        if widget is not None and widget.winfo_exists():
            widget.destroy()

    def _append_assistant_delta(self, chunk_text):
        if not chunk_text or chunk_text == self._thinking_text:
            return

        if self._stream_text and chunk_text.startswith(self._stream_text):
            delta = chunk_text[len(self._stream_text):]
        else:
            delta = chunk_text
        if not delta:
            return

        self._stream_text = chunk_text
        if self._current_bubble is None:
            self._hide_thinking()
            self._current_bubble = self._add_message("assistant", "")
        self._current_bubble.raw_content = self._stream_text
        # 串流期間 debounce 重繪（120ms），避免每個 chunk 都閃爍
        if self._stream_render_job is None:
            self._stream_render_job = self.after(120, self._render_stream_bubble)

    def _render_stream_bubble(self):
        self._stream_render_job = None
        if self._current_bubble is not None and self._current_bubble.winfo_exists():
            self._current_bubble.set_content(self._stream_text)
            if self._stick_bottom:
                self._scroll_to_bottom()

    def _finish_generation(self):
        if self._stream_render_job is not None:
            try:
                self.after_cancel(self._stream_render_job)
            except tk.TclError:
                pass
            self._stream_render_job = None

        if self._stream_text.strip():
            if self._current_bubble is not None and self._current_bubble.winfo_exists():
                self._current_bubble.set_content(self._stream_text)
            self._remember("assistant", self._stream_text)

        self._busy = False
        self._hide_thinking()
        self._current_bubble = None
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

    def _remember(self, role, content):
        """加入聊天記憶"""

        self._conversation.append({
            "role": role,
            "content": content,
        })

        # 超過限制時，只保留最新 N 則
        if len(self._conversation) > self._max_messages:
            self._conversation = self._conversation[-self._max_messages:]
