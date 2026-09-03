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


RULE_PRESETS = {
    "japanese": RulePreset("japanese", "日本規則", 6.5, "japanese", "Japanese"),
    "ing": RulePreset("ing", "應氏規則", 7.5, "japanese", "Ing"),
    "custom": RulePreset("custom", "自訂貼目", 6.5, "japanese", "Japanese"),
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
    if not math.isclose(komi * 2, round(komi * 2), abs_tol=1e-9):
        raise ValueError("komi must use half-point increments")
    return komi


def normalize_analysis_settings(rule_id=None, komi=None) -> tuple[str, float]:
    normalized_rule = normalize_rule_id(rule_id)
    preset = get_rule_preset(normalized_rule)
    normalized_komi = preset.default_komi if komi is None else validate_komi(komi)
    return normalized_rule, normalized_komi