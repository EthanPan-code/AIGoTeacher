"""Synchronize Windows IME composition fonts with focused Tk widgets.

Tk delegates the rendering of an unfinished composition string to the Windows
IME.  This module only changes the font in that IME context; it deliberately
does not alter Tk's global font defaults or widget bindings owned by callers.
"""

from __future__ import annotations

import ctypes
import logging
import os
from ctypes import wintypes

import tkinter.font as tkfont


logger = logging.getLogger(__name__)


class LOGFONTW(ctypes.Structure):
    _fields_ = [
        ("lfHeight", wintypes.LONG),
        ("lfWidth", wintypes.LONG),
        ("lfEscapement", wintypes.LONG),
        ("lfOrientation", wintypes.LONG),
        ("lfWeight", wintypes.LONG),
        ("lfItalic", wintypes.BYTE),
        ("lfUnderline", wintypes.BYTE),
        ("lfStrikeOut", wintypes.BYTE),
        ("lfCharSet", wintypes.BYTE),
        ("lfOutPrecision", wintypes.BYTE),
        ("lfClipPrecision", wintypes.BYTE),
        ("lfQuality", wintypes.BYTE),
        ("lfPitchAndFamily", wintypes.BYTE),
        ("lfFaceName", wintypes.WCHAR * 32),
    ]


def _font_height_from_tk_size(size: int | float, dpi: float) -> int:
    """Convert a Tk font size to a negative Windows LOGFONT height.

    Tk uses positive values for points and negative values for pixels.  A
    negative LOGFONT height requests the character height rather than the
    cell height, which is the least surprising match for Tk's rendered text.
    """
    size = int(round(float(size)))
    dpi = float(dpi) if dpi and dpi > 0 else 96.0
    if size >= 0:
        points = max(size, 1)
        return -max(1, int(round(points * dpi / 72.0)))
    return -max(1, abs(size))


class ImeFontManager:
    """Apply the focused Tk widget's font to the Windows IME context."""

    SUPPORTED_CLASSES = frozenset({"Entry", "Text", "TEntry", "TCombobox"})

    def __init__(self, root):
        self.root = root
        self._binding_id = None
        self._imm32 = None
        self._imm_get_context = None
        self._imm_set_composition_font = None
        self._imm_release_context = None
        self._load_imm32()

    def _load_imm32(self):
        if os.name != "nt":
            return
        try:
            imm32 = ctypes.WinDLL("imm32", use_last_error=True)
            get_context = imm32.ImmGetContext
            get_context.argtypes = [wintypes.HWND]
            get_context.restype = wintypes.HANDLE

            set_font = imm32.ImmSetCompositionFontW
            set_font.argtypes = [wintypes.HANDLE, ctypes.POINTER(LOGFONTW)]
            set_font.restype = wintypes.BOOL

            release_context = imm32.ImmReleaseContext
            release_context.argtypes = [wintypes.HWND, wintypes.HANDLE]
            release_context.restype = wintypes.BOOL
        except (AttributeError, OSError, TypeError):
            logger.debug("Windows IMM32 API is unavailable", exc_info=True)
            return

        self._imm32 = imm32
        self._imm_get_context = get_context
        self._imm_set_composition_font = set_font
        self._imm_release_context = release_context

    def install(self):
        """Install the manager's FocusIn binding once and return its id."""
        if self._binding_id is not None:
            return self._binding_id
        try:
            self._binding_id = self.root.bind_all(
                "<FocusIn>", self._on_focus_in, add="+"
            )
        except Exception:
            logger.debug("Unable to install IME FocusIn binding", exc_info=True)
            self._binding_id = None
        return self._binding_id

    def uninstall(self):
        """Remove only this manager's binding."""
        if self._binding_id is None:
            return
        try:
            self.root.unbind_all("<FocusIn>", self._binding_id)
        except Exception:
            logger.debug("Unable to remove IME FocusIn binding", exc_info=True)
        finally:
            self._binding_id = None

    def _on_focus_in(self, _event=None):
        try:
            self.refresh()
        except Exception:
            logger.debug("Unable to refresh IME composition font", exc_info=True)
        # Never return break: other focus handlers and Tk must continue.
        return None

    def _focused_widget(self):
        try:
            widget = self.root.focus_get()
        except Exception:
            return None
        if widget is None:
            return None
        try:
            widget_class = widget.winfo_class()
        except Exception:
            return None
        if widget_class in self.SUPPORTED_CLASSES:
            return widget
        return None

    def _make_logfont(self, widget) -> LOGFONTW | None:
        try:
            font_spec = widget.cget("font")
            font = tkfont.Font(widget, font=font_spec)
            actual = font.actual()
            dpi = widget.winfo_fpixels("1i")
            logfont = LOGFONTW()
            logfont.lfHeight = _font_height_from_tk_size(actual["size"], dpi)
            logfont.lfWeight = 700 if actual["weight"] == "bold" else 400
            logfont.lfItalic = 1 if actual["slant"] == "italic" else 0
            logfont.lfUnderline = 1 if actual["underline"] else 0
            logfont.lfStrikeOut = 1 if actual["overstrike"] else 0
            logfont.lfCharSet = 1  # DEFAULT_CHARSET; let Windows choose glyphs.
            logfont.lfFaceName = str(actual["family"])[:31]
            return logfont
        except Exception:
            logger.debug("Unable to convert Tk font to LOGFONTW", exc_info=True)
            return None

    def refresh(self):
        """Apply the current focused widget's font to its IME context."""
        if self._imm_get_context is None:
            return False
        widget = self._focused_widget()
        if widget is None:
            return False
        logfont = self._make_logfont(widget)
        if logfont is None:
            return False
        try:
            hwnd = wintypes.HWND(widget.winfo_id())
            context = self._imm_get_context(hwnd)
            if not context:
                return False
            try:
                self._imm_set_composition_font(context, ctypes.byref(logfont))
            except (OSError, ctypes.ArgumentError):
                logger.debug("ImmSetCompositionFontW failed", exc_info=True)
            finally:
                try:
                    self._imm_release_context(hwnd, context)
                except (OSError, ctypes.ArgumentError):
                    logger.debug("ImmReleaseContext failed", exc_info=True)
            return True
        except (OSError, ctypes.ArgumentError, TypeError, ValueError):
            logger.debug("Unable to update IME composition font", exc_info=True)
            return False


__all__ = ["ImeFontManager", "LOGFONTW", "_font_height_from_tk_size"]
