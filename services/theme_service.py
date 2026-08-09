"""Application color themes and Windows system-theme resolution."""

from __future__ import annotations

try:
    import winreg
except ImportError:  # pragma: no cover - non-Windows development
    winreg = None


THEME_NAMES = ("system", "dark", "light")


PALETTES = {
    "light": {

    "UI_BG": "#f5f0e8", "PANEL_BG": "#fffaf2", "PANEL_BORDER": "#d7c8ad",
    "HEADER_COLOR":"#fff6e8",
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

        # ========= Background =========

        "UI_BG": "#1B1D22",          # 主背景
        "PANEL_BG": "#23262D",       # Panel
        "PANEL_BORDER": "#343944",   # Border

        "STATUS_BG": "#20242A",
        "MENU_BG": "#23262D",
        "MENU_ACTIVE": "#303642",

        # ========= Board =========

        "BOARD_BG": "#CEA15C",       # Kaya 木頭
        "BOARD_LINE": "#4C3518",

        # ========= Typography =========

        "TEXT_MAIN": "#E6E8EB",
        "TEXT_MUTED": "#786858",

        # ========= Accent =========

        "ACCENT": "#3C8E3D",
        "ACCENT_DARK": "#255B26",

        # ========= Input =========

        "INPUT_BG": "#2A2F38",
        "INPUT_FG": "#ECEFF3",

        # ========= Teacher =========

        "TEACHER_TEXT_BG": "#252A33",

        # ========= Stones =========

        "STONE_BLACK": "#121417",
        "STONE_WHITE": "#F2EFE8",

        # ========= Analysis =========

        "BEST_MOVE_BLUE": "#5F8FFF",

        # ========= Selection =========

        "SELECTION_BG": "#38475C",
        "SELECTION_FG": "#FFFFFF",

        # ========= Status =========

        "SUCCESS": "#67C587",
        "WARNING": "#E8B44D",
        "ERROR": "#E57373",
        "INFO": "#64AFFF",

        # ========= Log =========

        "LOG_BG": "#191B20",
        "LOG_FG": "#D7DCE2"
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
