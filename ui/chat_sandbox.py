"""
LLM Chat Sandbox

Standalone Toplevel chat window for testing the currently selected LLM provider.
It uses a cloned provider instance so the main teacher UI is not touched.
"""

from __future__ import annotations

import copy
import threading
import traceback
import tkinter as tk
from tkinter import ttk


_CHAT_BG = "#f5f0e8"
_CHAT_PANEL = "#fffaf2"
_CHAT_BORDER = "#d7c8ad"
_CHAT_TEXT = "#2f271f"
_CHAT_MUTED = "#786858"
_CHAT_ACCENT = "#1f6f78"
_CHAT_ACCENT_D = "#15565d"

_USER_BUBBLE_BG = "#d4edf0"
_ASSISTANT_BUBBLE = "#ffffff"
_ERROR_BUBBLE = "#fce8e8"

_FONT_MAIN = ("Microsoft JhengHei", 11)
_FONT_BOLD = ("Microsoft JhengHei", 11, "bold")
_FONT_SMALL = ("Microsoft JhengHei", 9)


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

        self.title(f"{self._tr('chat.title', default='LLM Chat Sandbox')} - {self.model_display_name}")
        self.geometry("840x560")
        self.minsize(480, 380)
        self.configure(bg=_CHAT_BG)

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
        outer = tk.Frame(self, bg=_CHAT_BG)
        outer.pack(fill="both", expand=True)

        header = tk.Frame(outer, bg=_CHAT_BG)
        header.pack(fill="x", padx=12, pady=(12, 6))

        top_row = tk.Frame(header, bg=_CHAT_BG)
        top_row.pack(fill="x")

        title_label = tk.Label(
            top_row,
            text=self._tr("chat.title", default="LLM Chat Sandbox"),
            font=("Microsoft JhengHei", 15, "bold"),
            fg=_CHAT_TEXT,
            bg=_CHAT_BG,
            anchor="w",
        )
        title_label.pack(side="left", anchor="w")

        model_label = tk.Label(
            top_row,
            text=f"{self._tr('chat.model_label', default='Model')}: {self.model_display_name}",
            font=_FONT_SMALL,
            fg=_CHAT_MUTED,
            bg=_CHAT_BG,
            anchor="e",
        )
        model_label.pack(side="right", anchor="e")

        provider_label = tk.Label(
            header,
            text=f"{self._tr('chat.provider_label', default='Provider')}: {self.provider_display_name}",
            font=_FONT_SMALL,
            fg=_CHAT_MUTED,
            bg=_CHAT_BG,
            anchor="w",
        )
        provider_label.pack(fill="x", pady=(2, 0))

        history_wrap = tk.Frame(outer, bg=_CHAT_BG)
        history_wrap.pack(fill="both", expand=True, padx=12, pady=(0, 6))

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
            padx=4,
            pady=4,
            state="disabled",
        )
        history_scroll = ttk.Scrollbar(history_wrap, command=self._history_text.yview)
        self._history_text.configure(yscrollcommand=history_scroll.set)
        self._history_text.pack(side="left", fill="both", expand=True)
        history_scroll.pack(side="right", fill="y")

        self._history_text.tag_configure("assistant_role", foreground=_CHAT_ACCENT, font=_FONT_BOLD, spacing1=8, spacing3=2, justify="left")
        self._history_text.tag_configure("assistant_body", foreground=_CHAT_TEXT, background=_ASSISTANT_BUBBLE, spacing3=10, justify="left")
        self._history_text.tag_configure("user_role", foreground=_CHAT_ACCENT_D, font=_FONT_BOLD, spacing1=8, spacing3=2, justify="right")
        self._history_text.tag_configure("user_body", foreground=_CHAT_TEXT, background=_USER_BUBBLE_BG, spacing3=10, justify="left")
        self._history_text.tag_configure("error_role", foreground="#c0392b", font=_FONT_BOLD, spacing1=8, spacing3=2, justify="left")
        self._history_text.tag_configure("error_body", foreground="#b03a2e", background=_ERROR_BUBBLE, spacing3=10, justify="left")
        self._history_text.tag_configure("thinking", foreground=_CHAT_MUTED, font=("Microsoft JhengHei", 10, "italic"), spacing1=6, spacing3=6)

        self._history_text.bind("<MouseWheel>", self._on_mousewheel)
        self._history_text.bind("<Button-4>", self._on_mousewheel_linux)
        self._history_text.bind("<Button-5>", self._on_mousewheel_linux)

        input_wrap = tk.Frame(outer, bg=_CHAT_BG)
        input_wrap.pack(side="bottom", fill="x", padx=20, pady=(0, 12))

        self._input_text = tk.Text(
            input_wrap,
            height=3,
            wrap="word",
            font=_FONT_MAIN,
            bg=_CHAT_PANEL,
            fg=_CHAT_TEXT,
            insertbackground=_CHAT_ACCENT,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground=_CHAT_BORDER,
            highlightcolor=_CHAT_ACCENT,
            padx=8,
            pady=6,
        )
        self._input_text.pack(side="left", fill="x", expand=True)
        self._input_text.bind("<Return>", self._on_enter)
        self._input_text.bind("<Shift-Return>", self._on_shift_enter)

        send_btn = ttk.Button(input_wrap, text=self._tr("chat.send", default="Send"), command=self._on_send, width=10)
        send_btn.pack(side="right", padx=(8, 0))

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
        self._add_message("user", raw)
        self._start_generation(raw)

    def _on_close(self):
        self.destroy()

    def _append_history(self, role_text, content, tag):
        self._history_text.configure(state="normal")
        self._history_text.insert("end", f"{role_text}\n", f"{tag}_role")
        self._history_text.insert("end", f"{content}\n\n", f"{tag}_body")
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
        self._history_text.insert("end", f"{self._thinking_text}\n\n", "thinking")
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
        self._history_text.insert("end", delta, "assistant_body")
        self._history_text.configure(state="disabled")
        self._stream_text = chunk_text
        self._history_text.see("end")

    def _finish_generation(self):
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
                provider.chat_stream(user_text)
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