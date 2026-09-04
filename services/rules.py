"""Supported KataGo rules and per-game analysis setting helpers."""

from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class RulePreset:
    rule_id: str
    display_name: str
    default_komi: float
    katago_rules: str
    sgf_rule_name: str
    score_unit: str
    katago_komi: float


RULE_PRESETS = {
    "japanese": RulePreset("japanese", "比目法", 6.5, "japanese", "Japanese", "目", 6.5),
    "ing": RulePreset("ing", "應氏規則", 7.5, "japanese", "Ing", "點", 7.5),
    "area": RulePreset("area", "數子法", 3.75, "chinese", "Chinese", "子", 7.5),
    "custom": RulePreset("custom", "自訂貼目", 6.5, "japanese", "Japanese", "目", 6.5),
}
DEFAULT_RULE_ID = "japanese"
DEFAULT_KOMI = RULE_PRESETS[DEFAULT_RULE_ID].default_komi
MIN_KOMI = -100.0
MAX_KOMI = 100.0


def get_rule_preset(rule_id: str | None) -> RulePreset:
    return RULE_PRESETS.get(rule_id, RULE_PRESETS[DEFAULT_RULE_ID])


def normalize_rule_id(rule_id: str | None) -> str:
    return get_rule_preset(rule_id).rule_id


def validate_komi(value) -> float:
    try:
        komi = float(value)
    except (TypeError, ValueError):
        raise ValueError("komi must be a finite number")
    if not math.isfinite(komi) or not MIN_KOMI <= komi <= MAX_KOMI:
        raise ValueError("komi must be between -100 and 100")
    return komi


def get_katago_komi(rule_id, komi):
    """Convert the displayed score unit to KataGo's half-point komi unit."""
    preset = get_rule_preset(rule_id)
    value = preset.katago_komi if rule_id == "area" else validate_komi(komi)
    if not math.isclose(value * 2, round(value * 2), abs_tol=1e-9):
        raise ValueError("KataGo komi must use half-point increments")
    return value


def calculate_area_score(black_stones, white_stones, black_territory, white_territory, dead_black, dead_white):
    """Calculate area scores with dead stones awarded to the opponent."""
    black_total = black_stones - dead_black + black_territory + dead_white
    white_total = white_stones - dead_white + white_territory + dead_black
    return black_total, white_total


def normalize_analysis_settings(rule_id=None, komi=None) -> tuple[str, float]:
    normalized_rule = normalize_rule_id(rule_id)
    preset = get_rule_preset(normalized_rule)
    normalized_komi = preset.default_komi if komi is None else validate_komi(komi)
    return normalized_rule, normalized_komi