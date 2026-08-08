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
        "UI_BG": "#141619",          # Deep obsidian slate
        "PANEL_BG": "#1c1e22",       # Layered elevated dark surface
        "PANEL_BORDER": "#2e323b",   # Muted border for subtle hierarchy
        "TEACHER_TEXT_BG": "#23262d",
        "BOARD_BG": "#c89b53",       # Warm natural Kaya wood tone (榧木色)
        "BOARD_LINE": "#3d2b10",      # Deep wood-ink line color
        "TEXT_MAIN": "#eceef0",      # Soft high-contrast off-white
        "TEXT_MUTED": "#786858",     # Balanced neutral muted text
        "ACCENT": "#51b3a1",         # Muted Jade / Emerald accent (溫潤翡翠)
        "ACCENT_DARK": "#368073",
        "STONE_BLACK": "#111214",
        "STONE_WHITE": "#f0ede6",
        "BEST_MOVE_BLUE": "#5b8def",
        "INPUT_BG": "#252830",
        "INPUT_FG": "#eceef0",
        "STATUS_BG": "#1c1e22",
        "MENU_BG": "#1c1e22",
        "MENU_ACTIVE": "#2d313b",
        "ERROR": "#e57373",
        "WARNING": "#ffb74d",
        "SUCCESS": "#81c784",
        "INFO": "#64b5f6",
        "SELECTION_BG": "#2e3b4e",
        "SELECTION_FG": "#ffffff",
        "LOG_BG": "#101114",
        "LOG_FG": "#d1d5db"
        }
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
