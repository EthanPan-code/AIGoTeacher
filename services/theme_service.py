"""Application color themes and Windows system-theme resolution."""

from __future__ import annotations

try:
    import winreg
except ImportError:  # pragma: no cover - non-Windows development
    winreg = None


THEME_NAMES = ("system", "dark", "light")

# The light palette intentionally matches the original main_v3.py constants.
PALETTES = {
    "light": {
        "UI_BG": "#f5f0e8", "PANEL_BG": "#fffaf2", "PANEL_BORDER": "#d7c8ad",
        "TEACHER_TEXT_BG": "#fff6e8", "BOARD_BG": "#d9a95f", "BOARD_LINE": "#5b4228",
        "TEXT_MAIN": "#2f271f", "TEXT_MUTED": "#786858", "ACCENT": "#1f6f78",
        "ACCENT_DARK": "#15565d", "STONE_BLACK": "#171717", "STONE_WHITE": "#f7f3eb",
        "BEST_MOVE_BLUE": "#1967d2", "INPUT_BG": "#ffffff", "INPUT_FG": "#2f271f",
        "STATUS_BG": "#e8dfd2", "MENU_BG": "#fffaf2", "MENU_ACTIVE": "#ead7b8",
        "ERROR": "#c62828", "WARNING": "#b26a00", "SUCCESS": "#1f6f78",
        "INFO": "#1976a3", "SELECTION_BG": "#ead7b8", "SELECTION_FG": "#2f271f",
        "LOG_BG": "#1e1e1e", "LOG_FG": "#d4d4d4",
    },
    "dark": {
        "UI_BG": "#202124", "PANEL_BG": "#2b2d31", "PANEL_BORDER": "#4b5058",
        "TEACHER_TEXT_BG": "#25272b", "BOARD_BG": "#d9a95f", "BOARD_LINE": "#5b4228",
        "TEXT_MAIN": "#f1f3f4", "TEXT_MUTED": "#b7bdc8", "ACCENT": "#68c7d0",
        "ACCENT_DARK": "#3e9da8", "STONE_BLACK": "#171717", "STONE_WHITE": "#f7f3eb",
        "BEST_MOVE_BLUE": "#66a3ff", "INPUT_BG": "#35383f", "INPUT_FG": "#f1f3f4",
        "STATUS_BG": "#35383f", "MENU_BG": "#2b2d31", "MENU_ACTIVE": "#444a53",
        "ERROR": "#ff8a80", "WARNING": "#ffca70", "SUCCESS": "#72d6a0",
        "INFO": "#7dcfff", "SELECTION_BG": "#506070", "SELECTION_FG": "#ffffff",
        "LOG_BG": "#17181a", "LOG_FG": "#e5e7eb",
    },
}


def normalize_theme(value: str | None) -> str:
    return value if value in THEME_NAMES else "system"


def detect_system_theme() -> str:
    """Return the Windows theme at process startup; safely fall back to light."""
    if winreg is None:
        return "light"
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
        ) as key:
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return "light" if int(value) else "dark"
    except (OSError, ValueError, TypeError):
        return "light"


def resolve_theme(value: str | None) -> tuple[str, dict[str, str]]:
    configured = normalize_theme(value)
    effective = detect_system_theme() if configured == "system" else configured
    return configured, dict(PALETTES[effective])

