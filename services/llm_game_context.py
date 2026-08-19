"""Compact, factual Go-game context for LLM teaching prompts.

This module deliberately contains no UI or KataGo process code so live and
full-game commentary serialize positions in exactly the same way.
"""

PROMPT_FORMAT_VERSION = "go-context-v2"


def _gtp(x, y, size=19):
    col = chr(ord("A") + int(x))
    if col >= "I":
        col = chr(ord(col) + 1)
    return f"{col}{size - int(y)}"


def _move_text(index, move, size=19):
    if not move:
        return f"{index}. Pass"
    x, y, color = move
    return f"{index}. {'B' if color == 'black' else 'W'} {_gtp(x, y, size)}"


def serialize_mainline(stones, size=19):
    return " ".join(_move_text(i, move, size) for i, move in enumerate(stones, 1)) or "(empty)"


def serialize_board(stones, size=19):
    board = [["." for _ in range(size)] for _ in range(size)]
    for x, y, color in stones:
        if 0 <= x < size and 0 <= y < size:
            board[y][x] = "X" if color == "black" else "O"
    cols = " ".join(chr(ord("A") + i + (1 if i >= 8 else 0)) for i in range(size))
    rows = []
    for y, row in enumerate(board):
        rows.append(f"{size-y:2d} " + " ".join(row))
    return "座標: " + cols + "\n" + "\n".join(rows) + "\n圖例: X=Black, O=White, .=empty"


def _analysis_lines(label, analysis):
    if not analysis:
        return f"{label}: unavailable (no cached KataGo result)"
    root = analysis.get("rootInfo", {})
    lines = [
        f"{label}: black_winrate={root.get('winrate', 'unknown')}",
        f"{label}: black_score_lead={root.get('scoreLead', 'unknown')}",
    ]
    moves = []
    for item in (analysis.get("moveInfos") or [])[:3]:
        moves.append(f"{item.get('move', 'unknown')} wr={item.get('winrate', 'unknown')} score={item.get('scoreLead', 'unknown')}")
    lines.append(f"{label}: top_moves=" + ("; ".join(moves) if moves else "unavailable"))
    return "\n".join(lines)


def serialize_game_context(stones, *, current_stones=None, before_stones=None,
                           after_stones=None, mistake=None, full_game=None,
                           before_analysis=None, after_analysis=None):
    """Serialize only the selected mainline and explicitly named snapshots."""
    current_stones = stones if current_stones is None else current_stones
    parts = [
        f"=== LLM Go Context ({PROMPT_FORMAT_VERSION}) ===",
        "CURRENT MAINLINE (only this variation is in scope):",
        serialize_mainline(current_stones),
        "CURRENT BOARD:",
        serialize_board(current_stones),
    ]
    if mistake:
        parts.extend([
            "MISTAKE FACTS:",
            f"mistake_move={mistake.get('mistake_move', 'unknown')}",
            f"mistake_player={mistake.get('mistake_player', 'unknown')}",
            f"winrate_before={mistake.get('winrate_before', 'unknown')}",
            f"winrate_after={mistake.get('winrate_after', 'unknown')}",
            f"score_lead_before={mistake.get('score_lead_before', 'unknown')}",
            f"score_lead_after={mistake.get('score_lead_after', 'unknown')}",
        ])
        if before_stones is not None:
            parts.extend(["POSITION BEFORE MISTAKE:", serialize_board(before_stones)])
        if after_stones is not None:
            parts.extend(["POSITION AFTER MISTAKE:", serialize_board(after_stones)])
        parts.append(_analysis_lines("PRE-MOVE ANALYSIS (mistake player's alternatives)", before_analysis))
        parts.append(_analysis_lines("POST-MISTAKE ANALYSIS (opponent's responses)", after_analysis))
        if "pre_move_best_moves" in mistake:
            parts.append(f"pre_move_best_moves={mistake['pre_move_best_moves'] or 'unavailable'}")
        if "post_mistake_opponent_best_moves" in mistake:
            parts.append(f"post_mistake_opponent_best_moves={mistake['post_mistake_opponent_best_moves'] or 'unavailable'}")
    if full_game:
        parts.extend(["FULL-GAME KEY MOMENTS:", str(full_game)])
    return "\n".join(parts)
