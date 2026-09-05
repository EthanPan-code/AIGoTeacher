"""尋找功能（Ctrl+F）的核心搜尋邏輯。

依設計規劃：
- 純函式模組，不含任何 UI 依賴，方便單元測試。
- 支援以「手數（數字）」或「座標（GTP 格式，如 Q16 / pd）」搜尋 GameNode 變化樹。
- 因為樹可能包含分支與打結，同一手數 / 座標可能出現多筆結果。
- 每筆結果都帶「路徑索引」（root→child[i]→child[j]...），沿用分頁快照同款慣例，
  不使用 id()，避免樹被複製後 id 重用造成誤判。
"""

from dataclasses import dataclass, field

# 單次搜尋結果上限（避免大型棋譜導致 UI 卡頓）
FIND_RESULT_LIMIT = 200

# 圍棋座標慣例：跳過字母 I
_COORD_LETTERS = "ABCDEFGHJKLMNOPQRSTUVWXYZ"


@dataclass
class FindResult:
    """單筆搜尋結果。"""
    node: object            # GameNode
    path_index: list        # 從 root 出發的 child 索引路徑，如 [0, 2, 1]（root 本身為 []）
    move_number: int        # 該手在自身分支內的手數（root = 0）
    branch_label: str       # 展示用文字，例：主線 / 變化 [0]→[2]
    coord: str              # GTP 座標（如 Q16），Pass 則為 "Pass"
    color: str              # "B" / "W"


def parse_coordinate(text: str, board_size: int = 19):
    """解析 GTP 座標輸入（如 'Q16'、'pd'、'q4'）。

    回傳 (x, y)，其中 x 欄 0 起、y 由上往下 0 起；無法解析回傳 None。
    """
    text = text.strip()
    if len(text) < 2:
        return None
    # 拆成字母前綴 + 數字後綴
    idx = 0
    while idx < len(text) and text[idx].isalpha():
        idx += 1
    letters, digits = text[:idx], text[idx:]
    if not letters or not digits or not digits.isdigit():
        return None
    letter = letters[0].upper()
    if len(letters) != 1 or letter not in _COORD_LETTERS[:board_size]:
        return None
    row = int(digits)
    if not (1 <= row <= board_size):
        return None
    x = _COORD_LETTERS.index(letter)
    y = board_size - row
    return (x, y)


def to_gtp_coord(x: int, y: int, board_size: int = 19) -> str:
    """(x, y) → GTP 座標字串（與 GoBoard.to_gtp_coord 相同慣例）。"""
    if x is None or y is None:
        return "Pass"
    col = _COORD_LETTERS[x] if x < len(_COORD_LETTERS) else "?"
    return f"{col}{board_size - y}"


def _iter_all_paths(node, path=None, depth=0):
    """DFS 走訪整棵樹，yield (node, path_index, depth)。

    depth 即從 root（深度 0）到該節點的步數，等於該分支內的手數。
    """
    if path is None:
        path = []
    yield node, path, depth
    for i, child in enumerate(node.children):
        yield from _iter_all_paths(child, path + [i], depth + 1)


def _branch_label(path, main_label, variation_label):
    if not path or all(i == 0 for i in path):
        return main_label
    return variation_label + " " + "→".join(str(i) for i in path)


def find(root, query: str, board_size: int = 19,
         main_label: str = "Main", variation_label: str = "Var",
         limit: int = FIND_RESULT_LIMIT):
    """在 GameNode 樹中搜尋。

    - query 為純數字 → 收集所有分支中 move_number == N 的節點
    - query 為座標   → 收集所有落在該座標的節點（不分手數）
    回傳 (results, truncated, query_kind)。query_kind 為 "move" / "coord" / None。
    """
    if root is None:
        return [], False, None
    query = (query or "").strip()
    if not query:
        return [], False, None

    move_target = None
    coord_target = None
    pass_target = False
    if query.isdigit():
        move_target = int(query)
        query_kind = "move"
    elif query.lower() in {"pass", "tt"}:
        pass_target = True
        query_kind = "coord"
    else:
        coord_target = parse_coordinate(query, board_size)
        if coord_target is None:
            return [], False, None
        query_kind = "coord"

    results = []
    truncated = False
    for node, path, depth in _iter_all_paths(root):
        move = getattr(node, "move", None)
        if move is None:
            continue  # root 本身無 move
        if move_target is not None:
            if depth != move_target:
                continue
        elif pass_target:
            if move[0] is not None or move[1] is not None:
                continue
        else:
            if tuple(move[:2]) != coord_target:
                continue
        results.append(FindResult(
            node=node,
            path_index=list(path),
            move_number=depth,
            branch_label=_branch_label(path, main_label, variation_label),
            coord=to_gtp_coord(move[0], move[1], board_size),
            color="B" if move[2] == "black" else "W",
        ))
        if len(results) >= limit:
            truncated = True
            break
    return results, truncated, query_kind


def resolve_path(root, path_index):
    """依路徑索引從 root 取回節點；路徑失效（樹已變動）時回傳 None。"""
    node = root
    for idx in path_index:
        if not (0 <= idx < len(node.children)):
            return None
        node = node.children[idx]
    return node
