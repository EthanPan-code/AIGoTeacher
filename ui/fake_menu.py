"""Themeable, Tk-only application menu bar.

This deliberately does not use native Tk menus.  Native menus are owned by the
Windows theme and cannot be made consistent with the application's palette.
"""

from __future__ import annotations

import tkinter as tk


class FakeMenuBar(tk.Frame):
    """A small menu system built from Frames and Buttons.

    Menu definitions are plain dictionaries so the application can keep its
    existing callbacks and translation keys in one place.  Supported item
    types are ``command``, ``separator``, ``submenu``, ``check`` and ``radio``.
    """

    def __init__(self, master, palette_getter, font=("Microsoft JhengHei", 10)):
        super().__init__(master, bd=0, highlightthickness=0)
        self._palette_getter = palette_getter
        self._font = font
        self._menus = []
        self._buttons = []
        self._popup = None
        self._child_popup = None
        self._active_menu = None
        self._active_submenu = None
        self.pack(fill="x", side="top")
        self.master.bind("<Escape>", self.close, add="+")
        self.master.bind("<Button-1>", self._on_root_click, add="+")

    def set_menus(self, menus):
        self.close()
        self._menus = menus
        for child in self.winfo_children():
            child.destroy()
        self._buttons.clear()
        self._apply_bar_palette()
        for index, menu in enumerate(menus):
            button = tk.Button(
                self,
                text=menu["label"],
                command=lambda i=index: self.toggle(i),
                font=self._font,
                bd=0,
                relief="flat",
                padx=12,
                pady=7,
                cursor="hand2",
                anchor="w",
            )
            button.pack(side="left")
            self._buttons.append(button)
        self.refresh_theme()

    def _palette(self):
        return self._palette_getter()

    def _apply_bar_palette(self):
        palette = self._palette()
        self.configure(bg=palette["PANEL_BG"])

    def refresh_theme(self):
        palette = self._palette()
        self._apply_bar_palette()
        for button in self._buttons:
            button.configure(
                bg=palette["PANEL_BG"],
                fg=palette["TEXT_MAIN"],
                activebackground=palette["MENU_ACTIVE"],
                activeforeground=palette["TEXT_MAIN"],
            )
        for popup in (self._popup, self._child_popup):
            if popup is not None and popup.winfo_exists():
                self._style_popup(popup)

    def refresh_labels(self, menus):
        self.set_menus(menus)

    def toggle(self, index):
        if self._active_menu == index and self._popup is not None:
            self.close()
            return
        self.close()
        self._active_menu = index
        self._popup = self._make_popup(self._menus[index]["items"])
        self.update_idletasks()
        button = self._buttons[index]
        x = self.winfo_x() + button.winfo_x()
        y = self.winfo_y() + self.winfo_height()
        self._popup.place(x=x, y=y)
        self._popup.lift()

    def _make_popup(self, items, child=False):
        palette = self._palette()
        popup = tk.Frame(self.master, bd=0, relief="flat", padx=4, pady=4)
        self._style_popup(popup)
        for item in items:
            item_type = item.get("type", "command")
            if item_type == "separator":
                tk.Frame(popup, height=1, bd=0, bg=self._palette()["PANEL_BORDER"]).pack(fill="x", pady=4)
                continue
            if item_type == "submenu":
                text = f"{item['label']}  ›"
                command = lambda data=item: self._open_submenu(data)
            else:
                marker = ""
                if item_type in ("check", "radio"):
                    marker = "✓ " if item.get("get_state", lambda: False)() else "   "
                text = marker + item["label"]
                accelerator = item.get("accelerator")
                if accelerator:
                    text += f"    {accelerator}"
                command = lambda data=item: self._run(data)
            button = tk.Button(
                popup,
                text=text,
                command=command,
                font=self._font,
                bd=0,
                borderwidth=0,
                highlightthickness=0,
                relief="flat",
                padx=9,
                pady=5,
                anchor="w",
                justify="left",
                cursor="hand2",
                bg=palette["MENU_BG"],
                fg=palette["TEXT_MAIN"],
                activebackground=palette["MENU_ACTIVE"],
                activeforeground=palette["TEXT_MAIN"],
            )
            button.pack(fill="x")
            button.bind("<Enter>", lambda event, b=button: self._hover(b, True))
            button.bind("<Leave>", lambda event, b=button: self._hover(b, False))
        return popup

    def _style_popup(self, popup):
        palette = self._palette()
        popup.configure(bg=palette["MENU_BG"], highlightbackground=palette["PANEL_BORDER"])
        for child in popup.winfo_children():
            if isinstance(child, tk.Button):
                child.configure(
                    bg=palette["MENU_BG"],
                    fg=palette["TEXT_MAIN"],
                    activebackground=palette["MENU_ACTIVE"],
                    activeforeground=palette["TEXT_MAIN"],
                )

    def _hover(self, button, active):
        palette = self._palette()
        button.configure(
            bg=palette["MENU_ACTIVE"] if active else palette["MENU_BG"],
            fg=palette["TEXT_MAIN"],
            activebackground=palette["MENU_ACTIVE"],
            activeforeground=palette["TEXT_MAIN"],
        )

    def _run(self, item):
        self.close()
        if item.get("type") == "radio" and item.get("variable") is not None:
            item["variable"].set(item["value"])
        elif item.get("type") == "check" and item.get("variable") is not None:
            item["variable"].set(not item["variable"].get())
        item["command"]()

    def _open_submenu(self, item):
        if self._child_popup is not None and self._child_popup.winfo_exists():
            self._child_popup.destroy()
        self._active_submenu = item
        self._child_popup = self._make_popup(item["items"], child=True)
        self.update_idletasks()
        source = self._popup
        x = source.winfo_x() + source.winfo_width()
        y = source.winfo_y()
        self._child_popup.place(x=x, y=y)
        self._child_popup.lift()

    def _on_root_click(self, event):
        widget = event.widget
        if any(self._is_descendant(widget, candidate) for candidate in self._buttons):
            return
        if self._popup is not None and self._is_descendant(widget, self._popup):
            return
        if self._child_popup is not None and self._is_descendant(widget, self._child_popup):
            return
        self.close()

    @staticmethod
    def _is_descendant(widget, ancestor):
        while widget is not None:
            if widget == ancestor:
                return True
            widget = getattr(widget, "master", None)
        return False

    def close(self, event=None):
        for popup in (self._child_popup, self._popup):
            if popup is not None:
                try:
                    popup.destroy()
                except tk.TclError:
                    pass
        self._child_popup = None
        self._popup = None
        self._active_menu = None
        self._active_submenu = None
        return "break" if event is not None else None
