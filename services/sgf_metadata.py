"""Helpers for editable SGF game-information properties."""

from datetime import datetime


GAME_INFO_FIELDS = (
    ("GN",),
    ("PB", "PW"),
    ("BR", "WR"),
    ("RE",),
    ("DT",),
)


def validate_game_date(value: str) -> str:
    """Return a normalized date or raise ValueError for a non-SGF date."""
    value = (value or "").strip()
    if not value:
        return ""
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("date must use YYYY-MM-DD") from exc
    return value


def get_game_info(metadata: dict) -> dict[str, str]:
    """Read the editable game-info fields without exposing the metadata dict."""
    return {
        key: str(metadata.get(key, ""))
        for key in ("GN", "PB", "PW", "BR", "WR", "RE", "DT")
    }


def update_game_info(metadata: dict, values: dict[str, str]) -> dict:
    """Update editable fields in place while preserving every other property."""
    date_value = validate_game_date(values.get("DT", ""))
    for key in ("GN", "PB", "PW", "BR", "WR", "RE", "DT"):
        value = date_value if key == "DT" else str(values.get(key, "")).strip()
        if value:
            metadata[key] = value
        else:
            metadata.pop(key, None)
    return metadata