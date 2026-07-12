import tkinter as tk
from tkinter import ttk  
from tkinter import filedialog
from tkinter import messagebox
import json, queue, threading, subprocess, time, os, copy, re, logging, itertools, sys, shutil, ctypes, platform  
import webbrowser
from collections import OrderedDict
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib as mpl
from dotenv import load_dotenv
from i18n import I18n
try:
    from PIL import Image, ImageOps, ImageTk
except ImportError:
    Image = None
    ImageOps = None
    ImageTk = None
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from version import APP_VERSION
mpl.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei', 'Arial'] 
mpl.rcParams['axes.unicode_minus'] = False 

BOARD_SIZE = 19
CELL_SIZE = 30
MARGIN = 40
COORD_MARGIN = 25  # 座標額外空間
BOARD_PIXEL = CELL_SIZE * (BOARD_SIZE - 1) + (MARGIN * 2)
CANVAS_SIZE = BOARD_PIXEL 
STONE_IMAGE_SIZE = 24
ANALYSIS_CACHE_LIMIT = 300
UI_POLL_INTERVAL_MS = 200
COMMENTARY_CACHE_LIMIT = 200  

UI_BG = "#f5f0e8"
PANEL_BG = "#fffaf2"
PANEL_BORDER = "#d7c8ad"
TEACHER_TEXT_BG = "#fff6e8"
BOARD_BG = "#d9a95f"
BOARD_LINE = "#5b4228"
TEXT_MAIN = "#2f271f"
TEXT_MUTED = "#786858"
ACCENT = "#1f6f78"
ACCENT_DARK = "#15565d"
STONE_BLACK = "#171717"
STONE_WHITE = "#f7f3eb"
BEST_MOVE_BLUE = "#1967d2"
RECOMMENDATION_LIMIT = 5
RECOMMENDATION_GREENS = ["#0b6b3a", "#198754", "#2ea66a", "#55bf7f"]
RECOMMENDATION_RADIUS = 15
VARIATION_HOVER_DELAY_MS = 1000
VARIATION_PREVIEW_LIMIT = 12
VARIATION_BLACK = "#222222"
VARIATION_WHITE = "#f4f0e8"
VARIATION_LABEL_BLACK = "#111111"
VARIATION_LABEL_WHITE = "#ffffff"
FEEDBACK_FORM_URL = "https://forms.gle/DkHPzEUCHx1NdKjE8"
DEFAULT_KATAGO_PATH = "katago.exe"
DEFAULT_MODEL_PATH = os.path.join("models", "kata.bin.gz")
MODEL_STANDARD_PATH = os.path.join("models", "kata.bin.gz")
MODEL_FAST_PATH = os.path.join("models", "kata-mini.txt.gz")
DEFAULT_CONFIG_PATH = "analysis_example.cfg"
APP_DATA_DIR_NAME = "AIGoTeacher"
RUNTIME_BUNDLE_DIR_NAME = "runtime"


def resource_path(relative_path):
    """取得打包後或開發環境的正確資源路徑"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def load_tk_image(file_path, size=None, fill_size=False):
    """Load an image as a Tk image, preferring Pillow for broad format support."""
    if Image and ImageTk:
        with Image.open(file_path) as img:
            img = ImageOps.exif_transpose(img)
            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGBA")

            if size:
                resample = Image.Resampling.LANCZOS
                if fill_size:
                    img = ImageOps.fit(img, size, method=resample)
                else:
                    img = img.copy()
                    img.thumbnail(size, resample)

            return ImageTk.PhotoImage(img)

    image = tk.PhotoImage(file=file_path)
    if size:
        target_w, target_h = size
        img_w, img_h = image.width(), image.height()
        if img_w > target_w or img_h > target_h:
            factor = max(1, min(img_w // target_w, img_h // target_h))
            image = image.subsample(factor, factor)
    return image




def is_frozen_app():
    return getattr(sys, "frozen", False)


def get_runtime_data_root():
    """Return the writable app data root.

    PyInstaller onefile extracts bundled files to a temporary _MEI directory, so
    writable runtime data must live elsewhere in packaged builds.
    """
    if is_frozen_app():
        local_app_data = os.getenv("LOCALAPPDATA")
        if local_app_data:
            return os.path.join(local_app_data, APP_DATA_DIR_NAME)
        return os.path.join(os.path.expanduser("~"), "AppData", "Local", APP_DATA_DIR_NAME)
    return PROJECT_ROOT


def ensure_runtime_dir(*parts):
    path = os.path.join(get_runtime_data_root(), *parts)
    os.makedirs(path, exist_ok=True)
    hide_path_on_windows(get_runtime_data_root())
    if parts:
        hide_path_on_windows(os.path.join(get_runtime_data_root(), parts[0]))
    return path


def hide_path_on_windows(path):
    if os.name != "nt" or not os.path.exists(path):
        return
    try:
        FILE_ATTRIBUTE_HIDDEN = 0x02
        attrs = ctypes.windll.kernel32.GetFileAttributesW(str(path))
        if attrs != -1 and not attrs & FILE_ATTRIBUTE_HIDDEN:
            ctypes.windll.kernel32.SetFileAttributesW(str(path), attrs | FILE_ATTRIBUTE_HIDDEN)
    except Exception:
        pass


def get_runtime_file_path(filename):
    if is_frozen_app():
        ensure_runtime_dir()
    return os.path.join(get_runtime_data_root(), filename)


def get_executable_dir():
    if is_frozen_app():
        return os.path.dirname(sys.executable)
    return PROJECT_ROOT


def iter_dotenv_paths():
    if is_frozen_app():
        yield os.path.join(get_executable_dir(), ".env")
        yield os.path.join(get_runtime_data_root(), ".env")
        yield os.path.join(os.getcwd(), ".env")
    else:
        yield os.path.join(PROJECT_ROOT, ".env")


def load_runtime_dotenv():
    loaded_paths = []
    seen = set()
    for path in iter_dotenv_paths():
        normalized = os.path.abspath(path)
        if normalized in seen:
            continue
        seen.add(normalized)
        if os.path.exists(normalized):
            load_dotenv(normalized)
            loaded_paths.append(normalized)
    return loaded_paths


def get_katago_runtime_overrides():
    if not is_frozen_app():
        return []

    home_data_dir = ensure_runtime_dir("KataGoData")
    analysis_log_dir = ensure_runtime_dir("logs", "analysis_logs")
    return [
        "-override-config",
        f"homeDataDir={home_data_dir},logDir={analysis_log_dir}",
    ]


def materialize_bundled_runtime_file(relative_path):
    """Copy bundled KataGo runtime files out of PyInstaller's _MEI directory.

    The onefile bootloader removes _MEI on exit. Running katago.exe or loading a
    large model directly from _MEI can keep file handles open long enough for
    cleanup to fail, so packaged builds execute from hidden LocalAppData storage.
    """
    if not is_frozen_app():
        return resource_path(relative_path)

    src = resource_path(relative_path)
    dest = os.path.join(ensure_runtime_dir(RUNTIME_BUNDLE_DIR_NAME), relative_path)
    os.makedirs(os.path.dirname(dest), exist_ok=True)

    needs_copy = True
    if os.path.exists(dest):
        try:
            needs_copy = os.path.getsize(src) != os.path.getsize(dest)
        except OSError:
            needs_copy = True

    if needs_copy:
        shutil.copy2(src, dest)
        hide_path_on_windows(dest)

    return dest


if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if is_frozen_app():
    bundled_cacert_path = resource_path("cacert.pem")
    if os.path.exists(bundled_cacert_path):
        os.environ.setdefault("SSL_CERT_FILE", bundled_cacert_path)
        os.environ.setdefault("REQUESTS_CA_BUNDLE", bundled_cacert_path)

LOADED_DOTENV_PATHS = load_runtime_dotenv()



from services.config_service import ConfigService
from services.keyring_service import (
    get_github_token,
    get_nvidia_api_key,
    normalize_api_key,
    set_github_token,
    set_nvidia_api_key,
)
from services.provider_factory import ProviderFactory
import threading  

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)
i18n = I18n(
    base_dir="i18n",
    settings_path=get_runtime_file_path("ui_settings.json")
)
config_service = ConfigService(i18n)


def t(key, **kwargs):
    return i18n.t(key, **kwargs)


def get_katago_path():
    if katago_path_mode_var.get() == "default":
        return materialize_bundled_runtime_file(DEFAULT_KATAGO_PATH)
    return katago_path_var.get().strip()


def get_model_path():
    mode = model_path_mode_var.get()
    if mode == "standard":
        return materialize_bundled_runtime_file(MODEL_STANDARD_PATH)
    if mode == "fast":
        return materialize_bundled_runtime_file(MODEL_FAST_PATH)
    return model_path_var.get().strip()


def get_config_path():
    if config_path_mode_var.get() == "default":
        return materialize_bundled_runtime_file(DEFAULT_CONFIG_PATH)
    return config_path_var.get().strip()


def get_model_display_name():
    mode = model_path_mode_var.get()
    if mode == "standard":
        return t("label.model_standard")
    if mode == "fast":
        return t("label.model_fast")
    return os.path.basename(model_path_var.get().strip()) or t("label.path_custom")


def get_config_display_name():
    if config_path_mode_var.get() == "default":
        return t("label.path_default")
    return os.path.basename(config_path_var.get().strip()) or t("label.path_custom")


winrate_display_state = {"key": "analysis.not_analyzed", "kwargs": {}}

# 【Phase 1】解說快取 — 儲存 LLM 生成的解說
# Key 格式: (turn, player_move_str) → Value: 解說文本
commentary_cache = {}  # {(turn, player_move): "解說文本", ...}
commentary_cache_lock = threading.Lock()  # 執行緒安全保護
full_game_commentary_cache = OrderedDict()
full_game_commentary_lock = threading.Lock()
FULL_GAME_COMMENTARY_CACHE_LIMIT = 50

def get_commentary_from_cache(turn, player_move):
    """從快取中取得該手數的解說 (執行緒安全)"""
    with commentary_cache_lock:
        key = (turn, str(player_move) if player_move else "Pass")
        return commentary_cache.get(key)

def add_to_commentary_cache(turn, player_move, text):
    """將解說文本新增到快取 (執行緒安全，儲存全部手數)"""
    with commentary_cache_lock:
        key = (turn, str(player_move) if player_move else "Pass")
        commentary_cache[key] = text
        logger.debug(f"已快取第 {turn} 手解說 (快取大小: {len(commentary_cache)})")

def get_full_game_commentary_from_cache(cache_key):
    with full_game_commentary_lock:
        cached = full_game_commentary_cache.get(cache_key)
        if cached:
            full_game_commentary_cache.move_to_end(cache_key)
        return cached

def add_full_game_commentary_to_cache(cache_key, text):
    if not text:
        return
    with full_game_commentary_lock:
        full_game_commentary_cache[cache_key] = text
        full_game_commentary_cache.move_to_end(cache_key)
        while len(full_game_commentary_cache) > FULL_GAME_COMMENTARY_CACHE_LIMIT:
            full_game_commentary_cache.popitem(last=False)

# 【Phase 1】全域狀態追蹤 — 追蹤當前正在生成的解說
current_critical_event = None  # 當前正在生成解說的 critical_event
current_generated_commentary = ""  # 累積生成的解說文本

# 【修復】回放模式旗標 — 當為 True 時，auto_analyze 不觸發新的 LLM 解說，
# 只更新勝率/AI 建議點；解說文字由 jump_to_specific_move 負責從快取顯示。
# play_move（正常落子）和 on_analyze_button_click 會設為 False。
is_playback_mode = False
score_analyzer = None
score_analyzer_initializing = False
score_analyzer_ready_callback = None
score_query_in_flight = False
score_estimate_pending_start = False
score_response_queue = queue.Queue()

def render_winrate_text(key, kwargs):
    render_kwargs = dict(kwargs)
    if "to_move_key" in render_kwargs:
        render_kwargs["to_move"] = t(render_kwargs.pop("to_move_key"))
    return t(key, **render_kwargs)


def set_winrate_text(key, **kwargs):
    winrate_display_state["key"] = key
    winrate_display_state["kwargs"] = kwargs
    winrate_label.config(text=render_winrate_text(key, kwargs))


def update_score_estimate_button_label():
    button = globals().get("btn_score_estimate")
    if button is None:
        return
    label_key = "button.close_score_estimate" if getattr(board, "score_estimate_active", False) else "button.score_estimate"
    button.config(text=t(label_key))

class KataGoAnalyzer:
    def __init__(self, katago_path, model_path, config_path, startup_callback=None):
        self.cmd = [
            katago_path,
            "analysis",
            "-model",
            model_path,
            "-config",
            config_path,
            *get_katago_runtime_overrides(),
        ]
        self.startup_callback = startup_callback
        self.ready_event = threading.Event()
        self.startup_lines = []
        self.startup_error = None
        self.startup_error_type = None  # "no_gpu" | "generic" | None
        self.closed = False
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        self.process = subprocess.Popen(
            self.cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
            encoding="utf-8",
            startupinfo=startupinfo,
        )
        self.response_queue = queue.Queue()
        self.analysis_cache = OrderedDict() # LRU：存儲已經分析過的局面
        self.pending_queries = {} # query_id -> {"board_hash": ..., "turn": ...}
        self.query_counter = itertools.count(1)
        self.cache_hits = 0
        self.cache_misses = 0
        
        # 【Phase 1】線程安全機制
        self.lock = threading.Lock()  # 保護 response_queue 和 analysis_cache
        self.full_analyze_event = threading.Event()  # 原子操作替代 is_full_analyzing 全局標誌
        
        # 啟動讀取執行緒，避免阻塞 UI
        self.reader_thread = threading.Thread(target=self._reader_thread, daemon=True)
        self.startup_log_thread = threading.Thread(target=self._startup_log_thread, daemon=True)
        self.reader_thread.start()
        self.startup_log_thread.start()

    def _notify_startup(self, key, **kwargs):
        if self.startup_callback:
            self.startup_callback(key, **kwargs)

    def _handle_startup_line(self, line):
        text = line.strip()
        if not text:
            return
        self.startup_lines.append(text)
        if len(self.startup_lines) > 80:
            self.startup_lines = self.startup_lines[-80:]

        # Check for OpenCL GPU not found errors first (before generic "Uncaught exception")
        if "CL_PLATFORM_NOT_FOUND_KHR" in text or "CL_DEVICE_NOT_FOUND" in text:
            self.startup_error = text
            self.startup_error_type = "no_gpu"
            logger.error("KataGo OpenCL 錯誤: %s", text)
            self._notify_startup("status.katago_no_gpu_found")
        elif "Performing autotuning" in text:
            self._notify_startup("status.katago_autotuning")
        elif "Done tuning" in text:
            self._notify_startup("status.katago_tuning_done")
        elif "Found OpenCL Device" in text or "Using OpenCL Device" in text:
            self._notify_startup("status.katago_gpu_ready")
        elif "Loaded model" in text:
            self._notify_startup("status.katago_loading_model")
        elif "Started, ready to begin handling requests" in text:
            self.ready_event.set()
            self._notify_startup("status.katago_ready")
        elif (
            "Uncaught exception" in text
        ):
            self.startup_error = text
            self.startup_error_type = "generic"
            self._notify_startup("status.katago_startup_failed")
            logger.info("KATAGO: %s", text)
            logger.error("TRIGGERED FAIL: %s", text)

    def _startup_log_thread(self):
        while True:
            if self.closed or not self.process.stderr:
                return
            try:
                line = self.process.stderr.readline()
            except (OSError, ValueError):
                return
            if not line:
                return
            self._handle_startup_line(line)

    def get_board_hash(self, stones):
        """將當前棋譜轉換成唯一的字串，作為快取的 Key"""
        moves = [["B" if c == "black" else "W", self.to_gtp(x, y)] for x, y, c in stones]
        return self.get_board_hash_from_moves(moves)

    def get_board_hash_from_moves(self, moves):
        """用一致的 KataGo moves 格式生成快取 key，避免 stones/list 格式不一致造成 miss。"""
        return json.dumps(moves, ensure_ascii=False, separators=(",", ":"))

    def _store_cache(self, board_hash, data):
        self.analysis_cache[board_hash] = data
        self.analysis_cache.move_to_end(board_hash)
        while len(self.analysis_cache) > ANALYSIS_CACHE_LIMIT:
            evicted_key, _ = self.analysis_cache.popitem(last=False)
            logger.debug("LRU 快取已移除最舊局面: key=%s cache_size=%s", evicted_key, len(self.analysis_cache))

    def send_query(
        self,
        stones,
        analyze_turns=None,
        response_queue=None,
        query_kind="live",
        use_cache=True,
        max_visits=None,
        include_ownership=False,
        include_ownership_stdev=False,
    ):
        if self.closed or self.process.poll() is not None:
            return None

        moves = [["B" if c == "black" else "W", self.to_gtp(x, y)] for x, y, c in stones]
        turn_num = len(stones)
        if analyze_turns is None:
            analyze_turns = [turn_num]
        analyze_turns = list(analyze_turns)
        target_queue = response_queue or self.response_queue
        board_hash = self.get_board_hash_from_moves(moves)
        
        # 【關鍵檢查】如果這個局面以前算過，直接把舊結果塞回 Queue，不用發請求給 KataGo
        # 【Phase 1】使用鎖保護快取讀取和 queue 操作
        if use_cache and len(analyze_turns) == 1 and analyze_turns[0] == turn_num:
            with self.lock:
                cached = self.analysis_cache.get(board_hash)
                if cached:
                    self.analysis_cache.move_to_end(board_hash)
                    self.cache_hits += 1
                    total = self.cache_hits + self.cache_misses
                    hit_rate = (self.cache_hits / total) * 100 if total else 0
                    print(f"DEBUG: 命中快取！直接讀取第 {len(stones)} 手分析結果")
                    logger.info("KataGo 快取命中: turn=%s hit_rate=%.1f%% (%s/%s)", len(stones), hit_rate, self.cache_hits, total)
                    target_queue.put(cached)
                    return None
                self.cache_misses += 1
        else:
            with self.lock:
                self.cache_misses += 1

        query_id = f"{query_kind}_{turn_num}_{int(time.time() * 1000)}_{next(self.query_counter)}"
        query = {
            "id": query_id,
            "moves": moves,
            "rules": "japanese",
            "komi": 6.5,
            "boardXSize": 19,
            "boardYSize": 19,
            "analyzeTurns": analyze_turns,
        }

        if max_visits is not None:
            query["maxVisits"] = max_visits
        if include_ownership:
            query["includeOwnership"] = True
        if include_ownership_stdev:
            query["includeOwnershipStdev"] = True

        with self.lock:
            self.pending_queries[query_id] = {
                "moves": moves,
                "pending_turns": set(analyze_turns),
                "response_queue": target_queue,
                "kind": query_kind,
            }

        try:
            self.process.stdin.write(json.dumps(query) + "\n")
            self.process.stdin.flush()
            return query_id
        except (BrokenPipeError, OSError) as e:
            with self.lock:
                self.pending_queries.pop(query_id, None)
            logger.error("KataGo 查詢送出失敗: id=%s turns=%s error=%s", query_id, analyze_turns, e)
            return None

    def _reader_thread(self):
        while True:
            if self.closed or not self.process.stdout:
                break
            try:
                line = self.process.stdout.readline()
            except (OSError, ValueError):
                break
            if not line: break
            if line.startswith("{"):
                try:
                    data = json.loads(line)
                    query_id = data["id"]
                    # 【Phase 1】使用鎖保護 queue 和快取的寫入
                    with self.lock:
                        pending = self.pending_queries.get(query_id)
                        if pending is None:
                            logger.warning("收到未知或已處理的 KataGo 回應，丟棄: id=%s", query_id)
                            continue

                        result_turn = data["turnNumber"]
                        if result_turn not in pending["pending_turns"]:
                            logger.warning(
                                "KataGo 回應手數與查詢不一致: id=%s expected_turns=%s result_turn=%s",
                                query_id, sorted(pending["pending_turns"]), result_turn
                            )
                            continue

                        pending["pending_turns"].remove(result_turn)
                        if not pending["pending_turns"]:
                            self.pending_queries.pop(query_id, None)

                        pending["response_queue"].put(data)
                        
                        # 只有完整的分析結果(含rootInfo)才存入快取
                        if "rootInfo" in data:
                            result_hash = self.get_board_hash_from_moves(pending["moves"][:result_turn])
                            self._store_cache(result_hash, data)
                except json.JSONDecodeError as e:
                    # 【改進異常處理】詳細記錄 JSON 解析錯誤
                    logger.warning("KataGo JSON 解析失敗: line=%r error=%s", line[:200], e)
                    continue
                except KeyError as e:
                    logger.warning("KataGo 回應缺少必要欄位: missing=%s data=%s", e, data)
                    continue
                except (TypeError, ValueError) as e:
                    logger.warning("KataGo 回應格式異常: error=%s data=%s", e, data)
                    continue
            else:
                self._handle_startup_line(line)

    def to_gtp(self, x, y):
        col = chr(ord('A') + x)
        if col >= 'I': col = chr(ord(col) + 1)
        return f"{col}{19 - y}"

    def get_result(self):
        try:
            # 【Phase 1】使用鎖保護 queue 的讀取
            with self.lock:
                return self.response_queue.get_nowait()
        except queue.Empty:
            return None

    def cancel_query(self, query_id):
        with self.lock:
            self.pending_queries.pop(query_id, None)

    def close(self, timeout=2):
        self.closed = True
        with self.lock:
            self.pending_queries.clear()

        if not self.process:
            return

        for stream_name in ("stdin",):
            stream = getattr(self.process, stream_name, None)
            if stream:
                try:
                    stream.close()
                except OSError:
                    pass

        if self.process.poll() is None:
            try:
                self.process.terminate()
                self.process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                logger.warning("KataGo process did not exit within %s seconds; killing it", timeout)
                self.process.kill()
                self.process.wait(timeout=3)

        for stream_name in ("stdout", "stderr"):
            stream = getattr(self.process, stream_name, None)
            if stream:
                try:
                    stream.close()
                except OSError:
                    pass

        for worker in (getattr(self, "reader_thread", None), getattr(self, "startup_log_thread", None)):
            if worker and worker.is_alive():
                worker.join(timeout=0.5)


class ScoreAnalyzer(KataGoAnalyzer):
    def __init__(self, startup_callback=None):
        super().__init__(
            get_katago_path(),
            materialize_bundled_runtime_file(MODEL_FAST_PATH),
            materialize_bundled_runtime_file(DEFAULT_CONFIG_PATH),
            startup_callback=startup_callback,
        )

    def send_query(self, stones, analyze_turns=None, response_queue=None, query_kind="score", use_cache=False):
        return super().send_query(
            stones,
            analyze_turns=analyze_turns,
            response_queue=response_queue,
            query_kind=query_kind,
            use_cache=False,
            max_visits=120,
            include_ownership=True,
            include_ownership_stdev=True,
        )

class GoDataFilter:
    def __init__(self, winrate_threshold=0.05, score_threshold=2.0):
        self.winrate_threshold = winrate_threshold
        self.score_threshold = score_threshold
        
        # 永遠紀錄黑棋視角的基準
        self.baseline_black_winrate = 0.5
        self.baseline_black_scoreLead = 0.0
        
        self.current_turn = 0
        self.latest_black_winrate = 0.5
        self.latest_black_scoreLead = 0.0
        self.has_triggered_this_turn = False
    
    def load_baseline_from_cache(self, turn, analyzer):
        """【改進】從快取中查詢上一手 (turn-1) 的分析結果，取出勝率和目數作為基準
        
        Args:
            turn: 當前手數
            analyzer: KataGoAnalyzer 實例，包含 analysis_cache
        
        Returns:
            (baseline_winrate, baseline_scoreLead) 或 None 如果快取中沒有上一手的結果
        """
        if turn <= 0:
            return None
        
        prev_turn = turn - 1
        # 取得棋局前 prev_turn 手的 hash（即上一手完成後的狀態）
        moves = board.stones[:prev_turn]
        moves_gtp = [["B" if c == "black" else "W", analyzer.to_gtp(x, y)] for x, y, c in moves]
        board_hash = analyzer.get_board_hash_from_moves(moves_gtp)
        
        # 從快取查詢
        cached_result = analyzer.analysis_cache.get(board_hash)
        if cached_result and "rootInfo" in cached_result:
            root_info = cached_result["rootInfo"]
            baseline_wr = root_info.get("winrate", None)
            baseline_sl = root_info.get("scoreLead", 0.0)
            logger.debug("【改進】從快取查詢到基準值: turn=%s prev_turn=%s winrate=%s scoreLead=%s", 
                        turn, prev_turn, baseline_wr, baseline_sl)
            return (baseline_wr, baseline_sl)
        
        logger.debug("【改進】快取中未找到上一手的分析: turn=%s prev_turn=%s hash=%s", 
                    turn, prev_turn, board_hash[:50])
        return None

    def process_analysis(self, current_turn, raw_result, last_move_gtp, *, is_playback=False):
        root_info = raw_result.get("rootInfo", {})
        
        # 1. 取得原始數據 (永遠是黑棋勝率/領先目數)
        current_black_winrate = root_info.get("winrate", 0.5)
        current_black_scoreLead = root_info.get("scoreLead", 0.0)

        # 2. 處理手數切換
        if current_turn > self.current_turn:
            # 前進：從快取查詢上一手的數據作為基準
            cache_result = self.load_baseline_from_cache(current_turn, analyzer)
            if cache_result:
                baseline_wr, baseline_sl = cache_result
                if baseline_wr is not None:
                    self.baseline_black_winrate = baseline_wr
                    self.baseline_black_scoreLead = baseline_sl
                    logger.info("基準值來自快取: turn=%s baseline_wr=%s baseline_sl=%s", 
                               current_turn, baseline_wr, baseline_sl)
                else:
                    self.baseline_black_winrate = self.latest_black_winrate
                    self.baseline_black_scoreLead = self.latest_black_scoreLead
                    logger.info("快取中無有效 winrate，使用內存備選: turn=%s", current_turn)
            else:
                self.baseline_black_winrate = self.latest_black_winrate
                self.baseline_black_scoreLead = self.latest_black_scoreLead
                logger.info("快取查詢失敗，使用內存備選: turn=%s baseline_wr=%s baseline_sl=%s", 
                           current_turn, self.latest_black_winrate, self.latest_black_scoreLead)
            
            self.current_turn = current_turn
            self.has_triggered_this_turn = False
        elif current_turn < self.current_turn:
            # 後退（Undo / 跳轉到過去）：重設基準為當前手數的觀測值，禁止觸發解說
            # 因為後退是在「回顧」而非「下棋」，不應該觸發失誤判定
            self.current_turn = current_turn
            self.baseline_black_winrate = current_black_winrate
            self.baseline_black_scoreLead = current_black_scoreLead
            self.latest_black_winrate = current_black_winrate
            self.latest_black_scoreLead = current_black_scoreLead
            self.has_triggered_this_turn = True  # 防止本次觸發
            logger.info("後退到手數 %s，重設基準並禁止觸發解說", current_turn)
            return None

        # 更新最新觀測值
        self.latest_black_winrate = current_black_winrate
        self.latest_black_scoreLead = current_black_scoreLead

        # 回放模式（跳轉到特定手數）不觸發新的 LLM 解說
        if is_playback:
            return None

        if self.has_triggered_this_turn or current_turn == 0:
            return None

        # 3. 計算勝率變動 (Baseline 是下棋前的狀態，Latest 是下棋後的狀態)
        # 如果剛才是「黑棋」下：黑棋勝率應該要升，若降了就是失誤
        # 如果剛才是「白棋」下：黑棋勝率應該要降，若升了就是白棋失誤
        
        player_just_moved = "Black" if current_turn % 2 != 0 else "White"
        
        if player_just_moved == "Black":
            # 黑棋下完，黑勝率跌了多少
            winrate_drop = self.baseline_black_winrate - current_black_winrate
            score_drop = self.baseline_black_scoreLead - current_black_scoreLead
        else:
            # 白棋下完，黑勝率反而漲了多少 (代表白棋虧了)
            winrate_drop = current_black_winrate - self.baseline_black_winrate
            score_drop = current_black_scoreLead - self.baseline_black_scoreLead

        # 4. 判定是否觸發
        if winrate_drop >= self.winrate_threshold or score_drop >= self.score_threshold:
            self.has_triggered_this_turn = True
            
            # 準備給 Ollama 的數據
            current_top_moves = []
            if "moveInfos" in raw_result:
                for info in raw_result["moveInfos"][:3]:
                    current_top_moves.append({"move": info["move"], "winrate": info["winrate"]})

            return {
                "turn": current_turn,
                "player": player_just_moved,
                "user_move": last_move_gtp,
                "winrate_drop": round(winrate_drop, 3),
                "current_best_moves": current_top_moves
            }

        return None

class GameNode:
    def __init__(self, move=None, parent=None):
        self.move = move  # 格式為 (x, y, color)，Root 為 None
        self.parent = parent
        self.children = []
        self.active_child_idx = 0  # 紀錄目前正在看哪一個變化圖分支

class BranchCanvas(tk.Canvas):
    def __init__(self, master, board_ref, **kwargs):
        super().__init__(master, **kwargs)
        self.board_ref = board_ref
        self.node_radius = 15
        self.bind("<Button-1>", self.on_click)

    def draw_branches(self):
        self.delete("all")
        curr = self.board_ref.current_node
        if not curr.parent:
            self.create_text(100, 42, text=t("branch.opening"), fill=TEXT_MUTED, font=("Microsoft JhengHei", 10))
            return

        parent = curr.parent
        branches = parent.children
        active_idx = parent.active_child_idx

        self.create_text(100, 15, text=t("branch.turn_branches", move_count=len(self.board_ref.stones)), font=("Microsoft JhengHei", 10), fill=TEXT_MAIN)

        # 橫向排列分支
        for i, node in enumerate(branches):
            x = 30 + i * 45
            y = 50
            color = STONE_WHITE if i == active_idx else "#d8d0c5"
            outline = ACCENT if i == active_idx else "#9d8f7f"
            width = 3 if i == active_idx else 1
            
            # 畫圓圈代表分支
            self.create_oval(x-self.node_radius, y-self.node_radius, 
                             x+self.node_radius, y+self.node_radius, 
                             fill=color, outline=outline, width=width, tags=f"branch_{i}")
            
            # 顯示座標縮寫 (如 R16)
            move = node.move
            txt = f"{self.board_ref.to_gtp_coord(move[0], move[1])}" if move else "Pass"
            self.create_text(x, y, text=txt, font=("Arial", 7, "bold"), fill=TEXT_MAIN, tags=f"branch_{i}")

    def on_click(self, event):
        item = self.find_closest(event.x, event.y)
        tags = self.gettags(item)
        for tag in tags:
            if tag.startswith("branch_"):
                idx = int(tag.split("_")[1])
                self.board_ref.jump_to_branch(idx)
                break

def auto_analyze():
    if not is_analyzer_ready():
        set_winrate_text("analysis.engine_not_ready")
        status_var.set(t("status.katago_initializing"))
        return

    # 如果正在整盤分析，直接跳過自動分析
    # 【Phase 1】用 analyzer.full_analyze_event.is_set() 代改 is_full_analyzing
    if analyzer.full_analyze_event.is_set():
        return
        
    board.clear_blue_point()
    set_winrate_text("analysis.thinking")
    analyzer.send_query(board.stones)



def run_full_game_analysis(progress_callback, cancel_state):
    """分析整盤棋並回傳每手的勝率列表 (複用全局 KataGo analyzer，支援取消與進度回報)"""
    if not is_analyzer_ready():
        return None, None

    stones_snapshot = copy.deepcopy(board.stones)
    total_moves = len(stones_snapshot)
    analyze_turns = list(range(total_moves + 1))
    full_response_queue = queue.Queue()

    winrates = {}
    scoreLeads = {}

    query_id = analyzer.send_query(
        stones_snapshot,
        analyze_turns=analyze_turns,
        response_queue=full_response_queue,
        query_kind="full",
        use_cache=False
    )
    if not query_id:
        return None, None

    while len(winrates) < len(analyze_turns):
        if cancel_state["cancel"]:  # 檢查是否按下取消
            analyzer.cancel_query(query_id)
            logger.info("全盤分析已被使用者取消: id=%s", query_id)
            break

        try:
            data = full_response_queue.get(timeout=0.2)
        except queue.Empty:
            continue

        try:
            turn = data["turnNumber"]
            root_info = data["rootInfo"]
            winrates[turn] = root_info["winrate"]
            scoreLeads[turn] = root_info.get("scoreLead", 0.0)
            # 呼叫回傳函數更新 UI 進度
            progress_callback(len(winrates), len(analyze_turns))
        except KeyError as e:
            logger.warning("全盤分析結果缺少欄位: missing=%s data=%s", e, data)
        except (TypeError, ValueError) as e:
            logger.warning("全盤分析結果格式異常: error=%s data=%s", e, data)

    if cancel_state["cancel"]:
        return None, None # 取消的話回傳 None
    
    sorted_turns = sorted(winrates.keys())
    wr_list = [winrates[i] for i in sorted_turns]
    sl_list = [scoreLeads[i] for i in sorted_turns]
    return wr_list, sl_list

def show_winrate_chart():
    if not is_analyzer_ready():
        show_analyzer_not_ready()
        return

    # 【Phase 1】用 analyzer.full_analyze_event 代改 is_full_analyzing
    if not board.stones or analyzer.full_analyze_event.is_set():
        return

    analyzer.full_analyze_event.set()  # 策設事件（原子操作） 
    btn_full_analysis.config(state="disabled")
    
    # ====== 1. 建立彈出進度視窗 ======
    progress_popup = tk.Toplevel(root)
    progress_popup.title(t("analysis.progress_title"))
    progress_popup.geometry("300x150")
    progress_popup.resizable(False, False)
    progress_popup.iconbitmap(resource_path("image/logo.ico"))
    progress_popup.transient(root) # 讓視窗保持在主視窗之上
    progress_popup.grab_set()      # 【關鍵】鎖定主視窗，無法點擊棋盤或其他按鈕
    
    # 置中顯示
    progress_popup.geometry("+%d+%d" % (root.winfo_rootx() + 50, root.winfo_rooty() + 50))

    lbl_status = tk.Label(progress_popup, text=t("analysis.start_engine"), font=("Microsoft JhengHei", 10))
    lbl_status.pack(pady=(20, 10))

    progress_bar = ttk.Progressbar(progress_popup, length=250, mode='determinate')
    progress_bar.pack(pady=5)

    cancel_state = {"cancel": False} # 用字典傳遞狀態，讓執行緒可以修改

    def on_cancel():
        cancel_state["cancel"] = True
        lbl_status.config(text=t("analysis.cancelling"))
        btn_cancel.config(state="disabled")

    btn_cancel = tk.Button(progress_popup, text=t("button.cancel_analysis"), command=on_cancel, width=10)
    btn_cancel.pack(pady=10)
    
    # 防止使用者按右上角 X 關閉視窗而沒有正確取消
    progress_popup.protocol("WM_DELETE_WINDOW", on_cancel)

    # ====== 2. UI 更新回呼函數 (從背景執行緒呼叫) ======
    def update_progress(current, total):
        percentage = int((current / total) * 100)
        # 確保透過 root.after 在主執行緒更新 UI
        root.after(0, lambda: lbl_status.config(text=t("analysis.progress", percentage=percentage, current=current, total=total)))
        root.after(0, lambda: progress_bar.config(value=percentage))

    # ====== 3. 背景執行分析任務 ======
    def task():
        try:
            wr_data, sl_data = run_full_game_analysis(update_progress, cancel_state)
            
            # 如果沒有取消，且有回傳資料，才畫圖
            if not cancel_state["cancel"] and wr_data and sl_data:
                root.after(0, lambda: plot_window(wr_data, sl_data))
                
        except Exception as e:
            print(f"分析失敗: {e}")
        finally:

            analyzer.full_analyze_event.clear()
            
            # 解除鎖定並銷毀進度視窗
            root.after(0, progress_popup.grab_release)
            root.after(0, progress_popup.destroy)
            
            # 恢復主介面按鈕
            root.after(0, lambda: btn_full_analysis.config(state="normal"))
            if cancel_state["cancel"]:
                root.after(0, lambda: set_winrate_text("analysis.cancelled"))
            else:
                root.after(0, lambda: set_winrate_text("analysis.completed"))

    threading.Thread(target=task, daemon=True).start()
    

def plot_window(winrates, scoreLeads):
    top = tk.Toplevel(root)
    top.title(t("analysis.chart_title_window"))
    top.geometry("1100x800")
    top.minsize(900, 680)
    top.iconbitmap(resource_path("image/logo.ico"))
    chart_window_state = {"closed": False}

    def on_chart_window_close():
        chart_window_state["closed"] = True
        top.destroy()

    def widget_exists(widget):
        try:
            return widget.winfo_exists()
        except tk.TclError:
            return False

    top.protocol("WM_DELETE_WINDOW", on_chart_window_close)

    controls_frame = ttk.Frame(top, padding=(10, 8, 10, 0))
    controls_frame.pack(fill=tk.X)
    ttk.Label(controls_frame, text=t("analysis.chart_mode_label")).pack(side=tk.LEFT, padx=(0, 8))

    chart_mode = tk.StringVar(value="black")
    mode_options = [
        (t("analysis.chart_mode_black"), "black"),
        (t("analysis.chart_mode_white"), "white"),
        (t("analysis.chart_mode_winrate"), "winrate"),
        (t("analysis.chart_mode_score"), "score"),
    ]
    for label, value in mode_options:
        ttk.Radiobutton(
            controls_frame,
            text=label,
            value=value,
            variable=chart_mode,
            command=lambda: apply_chart_mode(chart_mode.get()),
        ).pack(side=tk.LEFT, padx=(0, 10))
    
    fig = Figure(figsize=(10, 6), dpi=100)
    grid = fig.add_gridspec(2, 1, height_ratios=[3, 1], hspace=0.18)
    ax1 = fig.add_subplot(grid[0])
    
    chart_stones = list(board.stones)
    chart_board_hash = analyzer.get_board_hash(chart_stones)
    x_data = list(range(len(winrates)))
    black_winrates = [w * 100 for w in winrates]
    white_winrates = [(1.0 - w) * 100 for w in winrates]
    black_score_leads = [max(-15, min(15, sl)) for sl in scoreLeads]
    white_score_leads = [max(-15, min(15, -sl)) for sl in scoreLeads]
    move_losses = [0.0] * len(winrates)
    mistake_threshold = 30.0
    for move_idx in range(1, len(winrates)):
        move_color = chart_stones[move_idx - 1][2] if move_idx - 1 < len(chart_stones) else ("black" if move_idx % 2 == 1 else "white")
        black_delta = (winrates[move_idx - 1] - winrates[move_idx]) * 100
        loss = black_delta if move_color == "black" else -black_delta
        move_losses[move_idx] = max(0.0, loss)

    mistake_indices = [idx for idx, loss in enumerate(move_losses) if loss > mistake_threshold]
    blunder_idx = mistake_indices[-1] if mistake_indices else None
    
    # 在左側 Y 軸繪製勝率線
    line1, = ax1.plot(x_data, black_winrates, color='#2c3e50', picker=True, label=t("analysis.chart_winrate_label"), linewidth=2.5)
    
    # 建立右側 Y 軸用於目差
    ax2 = ax1.twinx()

    # 在右側 Y 軸繪製目差線
    line2, = ax2.plot(x_data, black_score_leads, color='#e74c3c', picker=True, label=t("analysis.chart_score_label"), linewidth=2.2, alpha=0.85)
    
    # 建立一條垂直的橘色指示線，代表當前手數
    current_line = ax1.axvline(x=len(board.stones), color='orange', alpha=0.8, linewidth=2)

    ax_diag = fig.add_subplot(grid[1], sharex=ax1)
    ax_diag.set_facecolor('#eeeeee')
    ax_diag.axhspan(0, mistake_threshold, color='#d9d9d9', alpha=0.7)
    mistake_losses = [move_losses[idx] for idx in mistake_indices]
    mistake_bars = ax_diag.bar(
        mistake_indices,
        mistake_losses,
        width=0.72,
        color='#f1c40f',
        edgecolor='#b7950b',
        linewidth=0.8,
        alpha=0.9,
        picker=True,
        label=t("analysis.chart_mistake_label"),
    )
    blunder_point = None
    if blunder_idx is not None:
        blunder_point = ax_diag.scatter(
            [blunder_idx],
            [move_losses[blunder_idx]],
            s=95,
            color='#d62728',
            edgecolor='white',
            linewidth=1.2,
            zorder=5,
            picker=True,
            label=t("analysis.chart_blunder_label"),
        )
    diag_current_line = ax_diag.axvline(x=len(board.stones), color='orange', alpha=0.8, linewidth=2)
    tooltip = ax_diag.annotate(
        "",
        xy=(0, 0),
        xytext=(10, 12),
        textcoords="offset points",
        bbox=dict(boxstyle="round,pad=0.35", fc="#fffaf2", ec="#9b8a70", alpha=0.95),
        arrowprops=dict(arrowstyle="->", color="#9b8a70"),
    )
    tooltip.set_visible(False)

    def set_current_move(move_idx):
        move_idx = max(0, min(move_idx, len(winrates) - 1))
        print(f"圖表觸發：跳轉至第 {move_idx} 手")
        board.jump_to_specific_move(move_idx)
        actual_move = len(board.stones)
        current_line.set_xdata([actual_move, actual_move])
        diag_current_line.set_xdata([actual_move, actual_move])
        canvas.draw_idle()

    # 點擊事件處理
    def on_click_chart(event):
        if event.inaxes not in [ax1, ax2, ax_diag] or event.xdata is None:
            return # 點在圖表外不處理
        
        move_idx = int(round(event.xdata))
        if event.inaxes == ax_diag and move_idx not in mistake_indices:
            return
        if 0 <= move_idx < len(winrates):
            set_current_move(move_idx)

    def on_key_chart(event):
        if event.key == "right":
            set_current_move(len(board.stones) + 1)
        elif event.key == "left":
            set_current_move(len(board.stones) - 1)

    def on_motion_chart(event):
        if event.inaxes != ax_diag:
            if tooltip.get_visible():
                tooltip.set_visible(False)
                canvas.draw_idle()
            return

        for move_idx in mistake_indices:
            if event.xdata is not None and abs(event.xdata - move_idx) <= 0.45:
                loss = move_losses[move_idx]
                if event.ydata is not None and -5 <= event.ydata <= loss + 8:
                    tooltip.xy = (move_idx, loss)
                    tooltip.set_text(t("analysis.chart_loss_tooltip", move=move_idx, loss=loss))
                    tooltip.set_visible(True)
                    canvas.draw_idle()
                    return

        if tooltip.get_visible():
            tooltip.set_visible(False)
            canvas.draw_idle()

    # 左側 Y 軸：勝率 (0-100%)
    winrate_midline = ax1.axhline(y=50, color='#95a5a6', linestyle='--', alpha=0.5, linewidth=1)  # 50% 中線
    ax1.set_ylim(-5, 105)
    ax1.set_ylabel(t("analysis.chart_y_winrate"), color='#2c3e50', fontsize=11)
    ax1.tick_params(axis='y', labelcolor='#2c3e50')
    
    # 右側 Y 軸：目差 (-15 ~ +15)
    # 設定右側坐標刻度：-15以下、-10、-5、±0、+5、+10、+15以上
    ax2.set_ylim(-20, 20)
    ax2.set_yticks([-15, -10, -5, 0, 5, 10, 15])
    score_labels = [t("analysis.score_below"), '-10', '-5', '0', '+5', '+10', t("analysis.score_above")]
    ax2.set_yticklabels(score_labels, fontsize=9)
    ax2.set_ylabel(t("analysis.chart_y_score"), color='#e74c3c', fontsize=11)
    ax2.tick_params(axis='y', labelcolor='#e74c3c')
    
    ax1.set_title(t("analysis.chart_title"), fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3, linestyle=':')
    ax1.tick_params(axis='x', labelbottom=False)

    ax_diag.axhline(y=mistake_threshold, color='#b7950b', linestyle='--', linewidth=1, alpha=0.7)
    diag_top = max([mistake_threshold + 10] + mistake_losses)
    ax_diag.set_ylim(0, min(100, diag_top + 8))
    ax_diag.set_ylabel(t("analysis.chart_y_loss"), color='#6f5f45', fontsize=10)
    ax_diag.set_xlabel(t("analysis.chart_x"))
    ax_diag.tick_params(axis='y', labelcolor='#6f5f45')
    ax_diag.grid(True, axis='y', alpha=0.25, linestyle=':')
    diag_lines = []
    diag_labels = []
    if mistake_indices:
        diag_lines.append(mistake_bars)
        diag_labels.append(t("analysis.chart_mistake_label"))
    if blunder_point is not None:
        diag_lines.append(blunder_point)
        diag_labels.append(t("analysis.chart_blunder_label"))
    if diag_lines:
        ax_diag.legend(diag_lines, diag_labels, loc='upper right', fontsize=9)

    canvas = FigureCanvasTkAgg(fig, master=top)
    chart_widget = canvas.get_tk_widget()
    chart_widget.configure(height=470)
    chart_widget.pack(fill=tk.BOTH, expand=False)

    teacher_panel = ttk.LabelFrame(top, text=t("analysis.teacher_panel_title"), padding=(10, 8))
    teacher_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
    teacher_controls = ttk.Frame(teacher_panel)
    teacher_controls.pack(fill=tk.X)
    summary_language = tk.StringVar(value=i18n.language if i18n.language in i18n.available_languages else "zh_TW")
    ttk.Label(teacher_controls, text=t("analysis.teacher_language_label")).pack(side=tk.LEFT, padx=(0, 6))
    language_combo = ttk.Combobox(
        teacher_controls,
        textvariable=summary_language,
        values=list(i18n.available_languages),
        state="readonly",
        width=8,
    )
    language_combo.pack(side=tk.LEFT, padx=(0, 8))
    btn_regenerate = ttk.Button(teacher_controls, text=t("button.regenerate"))
    btn_regenerate.pack(side=tk.LEFT, padx=(0, 8))
    btn_copy = ttk.Button(teacher_controls, text=t("button.copy_text"))
    btn_copy.pack(side=tk.LEFT)
    summary_status = ttk.Label(teacher_controls, text="", foreground=TEXT_MUTED)
    summary_status.pack(side=tk.RIGHT)
    summary_text = tk.Text(
        teacher_panel,
        height=7,
        font=("Microsoft JhengHei", 10),
        wrap="word",
        bg=TEACHER_TEXT_BG,
        fg=TEXT_MAIN,
        relief="solid",
        bd=1,
        padx=8,
        pady=8,
        state="disabled",
    )
    summary_scrollbar = ttk.Scrollbar(teacher_panel, orient=tk.VERTICAL, command=summary_text.yview)
    summary_text.configure(yscrollcommand=summary_scrollbar.set)
    summary_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=(8, 0))
    summary_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(8, 0))

    def set_summary_text(message):
        if threading.current_thread() is not threading.main_thread():
            root.after(0, set_summary_text, message)
            return
        if chart_window_state["closed"] or not widget_exists(summary_text):
            return
        summary_text.config(state="normal")
        summary_text.delete("1.0", tk.END)
        summary_text.insert(tk.END, message)
        summary_text.config(state="disabled")

    def set_summary_status(message):
        if threading.current_thread() is not threading.main_thread():
            root.after(0, set_summary_status, message)
            return
        if chart_window_state["closed"] or not widget_exists(summary_status):
            return
        summary_status.config(text=message)

    def get_turn_analysis(turn):
        moves = [["B" if c == "black" else "W", analyzer.to_gtp(x, y)] for x, y, c in chart_stones[:turn]]
        board_hash = analyzer.get_board_hash_from_moves(moves)
        with analyzer.lock:
            return analyzer.analysis_cache.get(board_hash)

    def format_move_summary(move_idx):
        if move_idx <= 0 or move_idx - 1 >= len(chart_stones):
            return t("teacher.best_unknown")
        x, y, color = chart_stones[move_idx - 1]
        return f"{move_idx}. {'B' if color == 'black' else 'W'} {board.to_gtp_coord(x, y)}"

    def collect_top_moves(turn):
        analysis = get_turn_analysis(turn)
        move_infos = (analysis or {}).get("moveInfos", [])
        top_moves = []
        for info in move_infos[:3]:
            move = info.get("move", t("teacher.best_unknown"))
            winrate = info.get("winrate")
            score = info.get("scoreLead")
            parts = [str(move)]
            if winrate is not None:
                parts.append(f"{winrate * 100:.1f}%")
            if score is not None:
                parts.append(f"{score:+.1f}")
            top_moves.append(" ".join(parts))
        return ", ".join(top_moves) if top_moves else t("teacher.best_unknown")

    def build_full_game_summary_data():
        opening_wr = black_winrates[0] if black_winrates else 50.0
        final_wr = black_winrates[-1] if black_winrates else 50.0
        peak_idx = max(range(len(black_winrates)), key=lambda idx: black_winrates[idx], default=0)
        low_idx = min(range(len(black_winrates)), key=lambda idx: black_winrates[idx], default=0)
        sharp_turns = []
        for idx in range(1, len(black_winrates)):
            delta = black_winrates[idx] - black_winrates[idx - 1]
            if abs(delta) >= 20:
                sharp_turns.append((idx, delta))

        mistakes = []
        for idx in mistake_indices:
            before = black_winrates[idx - 1] if idx > 0 else black_winrates[idx]
            after = black_winrates[idx]
            mistakes.append({
                "move": format_move_summary(idx),
                "loss": move_losses[idx],
                "before": before,
                "after": after,
                "suggestions": collect_top_moves(idx - 1),
            })

        blunder = None
        if blunder_idx is not None:
            blunder = {
                "move": format_move_summary(blunder_idx),
                "loss": move_losses[blunder_idx],
                "before": black_winrates[blunder_idx - 1] if blunder_idx > 0 else black_winrates[blunder_idx],
                "after": black_winrates[blunder_idx],
                "suggestions": collect_top_moves(blunder_idx - 1),
            }

        return {
            "opening_wr": opening_wr,
            "final_wr": final_wr,
            "peak": (peak_idx, black_winrates[peak_idx] if black_winrates else 50.0),
            "low": (low_idx, black_winrates[low_idx] if black_winrates else 50.0),
            "sharp_turns": sharp_turns[:5],
            "mistakes": mistakes,
            "blunder": blunder,
        }

    def build_summary_prompt(language):
        data = build_full_game_summary_data()
        
        # Helper: extract player (Black/White) from move string like "1. B R16" or "1. W R16"
        def get_player_from_move(move_str):
            """Extract player from move string format '1. B R16' or '1. W R16'"""
            if " B " in move_str:
                return "Black"
            elif " W " in move_str:
                return "White"
            return None
        
        # Helper: get localized player name
        def get_player_name(move_str):
            """Get localized player name (石頭.黑/石頭.白 or stone.black/stone.white)"""
            player = get_player_from_move(move_str)
            if player == "Black":
                return t("stone.black")
            elif player == "White":
                return t("stone.white")
            return ""
        
        mistake_lines = []
        for item in data["mistakes"]:
            player_name = get_player_name(item['move'])
            if language == "en":
                mistake_lines.append(
                    f"- Move {item['move'].split()[0][:-1]}: ({player_name}) loss {item['loss']:.1f}%, black winrate {item['before']:.1f}% -> {item['after']:.1f}%, KataGo: {item['suggestions']}"
                )
            else:
                mistake_lines.append(
                    f"- {item['move']}（{player_name}）: 失誤 {item['loss']:.1f}%，黑勝率 {item['before']:.1f}% → {item['after']:.1f}%，KataGo 推薦：{item['suggestions']}"
                )
        if not mistake_lines:
            if language == "en":
                mistake_lines.append("- No move exceeded the 30% mistake threshold.")
            else:
                mistake_lines.append("- 無超過 30% 的失誤。")

        sharp_lines = [
            f"- Move {idx}: black winrate changed {delta:+.1f}%"
            for idx, delta in data["sharp_turns"]
        ] or ["- No sharp winrate swing above 20% was detected."]

        blunder_text = "None"
        if data["blunder"]:
            b = data["blunder"]
            player_name = get_player_name(b['move'])
            if language == "en":
                blunder_text = (
                    f"Move {b['move'].split()[0][:-1]} ({player_name}): loss {b['loss']:.1f}%, black winrate {b['before']:.1f}% -> {b['after']:.1f}%, "
                    f"KataGo: {b['suggestions']}"
                )
            else:
                blunder_text = (
                    f"{b['move']}（{player_name}）：失誤 {b['loss']:.1f}%，黑勝率 {b['before']:.1f}% → {b['after']:.1f}%，"
                    f"KataGo 推薦：{b['suggestions']}"
                )

        if language == "en":
            system_prompt = "You are a calm, practical Go teacher. Give concise teaching feedback based on KataGo analysis. Each mistake is marked with the player who made it (Black or White)."
            user_prompt = (
                "Summarize this full Go game in 3-5 short teaching sentences.\n"
                "Focus on the overall trend, the decisive mistake, turning points, and one practical study suggestion.\n"
                "Explain mistakes from the perspective of the player who made them.\n\n"
                f"Overall trend: opening black winrate {data['opening_wr']:.1f}%, peak move {data['peak'][0]} at {data['peak'][1]:.1f}%, "
                f"low move {data['low'][0]} at {data['low'][1]:.1f}%, final black winrate {data['final_wr']:.1f}%.\n"
                f"Mistakes over 30%:\n{chr(10).join(mistake_lines)}\n"
                f"Worst mistake: {blunder_text}\n"
                f"Sharp turning points:\n{chr(10).join(sharp_lines)}"
            )
        else:
            system_prompt = """
            你是一位有經驗的圍棋老師。

            你看不到棋盤，只能根據 KataGo 的勝率變化與推薦著法進行教學回饋。

            請避免分析具體局部戰鬥、死活、定石或形狀，
            因為資料不足以支持這些判斷。

            請專注於：

            - 棋局整體走勢
            - 優勢建立與流失的時機
            - 關鍵失誤造成的影響
            - 可執行的學習建議

            每個失誤都會標明是黑棋或白棋的失誤，請以該方的角度說明失誤對局勢的影響。

            請用自然、人類化的語氣，
            不要逐條朗讀數據，
            不要重複大量百分比。
            """
            user_prompt = (
                "請以圍棋老師的角度，用 4~6 句話總結這盤棋。\n\n"

                "要求：\n"
                "- 不要逐條列出數據。\n"
                "- 不要重複大量勝率百分比。\n"
                "- 不要假裝看得到棋盤內容。\n"
                "- 可以根據勝率變化判斷局勢起伏。\n"
                "- 以失誤方的角度解說失誤如何影響局面。\n"
                "- 語氣自然，像老師下課後給學生的評語。\n\n"

                "請依序涵蓋：\n"
                "1. 棋局整體走勢\n"
                "2. 關鍵轉折點\n"
                "3. 最大失誤造成的影響\n"
                "4. 一項最值得優先練習的方向\n\n"

                f"開局黑勝率：{data['opening_wr']:.1f}%\n"
                f"最高點：第 {data['peak'][0]} 手（{data['peak'][1]:.1f}%）\n"
                f"最低點：第 {data['low'][0]} 手（{data['low'][1]:.1f}%）\n"
                f"終局黑勝率：{data['final_wr']:.1f}%\n\n"

                f"重大失誤：\n{chr(10).join(mistake_lines)}\n\n"

                f"最大失誤：\n{blunder_text}\n\n"

                f"主要轉折點：\n{chr(10).join(sharp_lines)}"
            )

        fallback_text = (
            t("analysis.teacher_fallback_none")
            if not data["mistakes"]
            else t(
                "analysis.teacher_fallback",
                final_wr=data["final_wr"],
                blunder=blunder_text,
            )
        )
        return system_prompt, user_prompt, fallback_text

    def get_summary_cache_key(language):
        provider_name = config_service.get_setting("llm_provider", "ollama")
        model_name = ProviderFactory.get_configured_model(config_service, provider_name)
        return chart_board_hash + f"|{language}|{provider_name}|{model_name}"

    def generate_teacher_summary(force=False):
        language = summary_language.get()
        cache_key = get_summary_cache_key(language)
        if not force:
            cached = get_full_game_commentary_from_cache(cache_key)
            if cached:
                set_summary_text(cached)
                set_summary_status(t("analysis.teacher_cached"))
                return

        provider_name = config_service.get_setting("llm_provider", "ollama")
        provider_display = ProviderFactory.get_display_name(provider_name)
        model_name = ProviderFactory.get_configured_model(config_service, provider_name)
        system_prompt, user_prompt, fallback_text = build_summary_prompt(language)
        generated = {"text": ""}
        thinking_text = t("analysis.teacher_generating", provider=provider_display)

        def on_summary_chunk(message):
            if threading.current_thread() is not threading.main_thread():
                root.after(0, on_summary_chunk, message)
                return
            if chart_window_state["closed"] or not widget_exists(summary_text):
                return
            if message != thinking_text:
                generated["text"] = message
            set_summary_text(message)

        def on_summary_complete():
            if threading.current_thread() is not threading.main_thread():
                root.after(0, on_summary_complete)
                return
            if chart_window_state["closed"] or not widget_exists(btn_regenerate):
                return
            text = generated["text"].strip()
            if text:
                add_full_game_commentary_to_cache(cache_key, text)
                set_summary_status(t("analysis.teacher_ready"))
            btn_regenerate.config(state="normal")

        summary_provider = ProviderFactory.create_provider(
            provider_name,
            ui_callback=on_summary_chunk,
            status_callback=update_status,
            model_name=model_name,
            translator=t,
            language_getter=lambda: language,
            on_complete_callback=on_summary_complete,
        )
        is_valid, error_message = summary_provider.validate_config()
        if not is_valid:
            set_summary_text(error_message or t("analysis.teacher_error"))
            set_summary_status(t("analysis.teacher_error"))
            return

        btn_regenerate.config(state="disabled")
        set_summary_status(t("analysis.teacher_generating", provider=provider_display))
        summary_provider.start_commentary({
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "thinking_text": thinking_text,
            "fallback_text": fallback_text,
        })

    def copy_summary_text():
        if chart_window_state["closed"] or not widget_exists(summary_text):
            return
        text = summary_text.get("1.0", tk.END).strip()
        if text:
            root.clipboard_clear()
            root.clipboard_append(text)
            set_summary_status(t("analysis.teacher_copied"))

    btn_regenerate.config(command=lambda: generate_teacher_summary(force=True))
    btn_copy.config(command=copy_summary_text)
    language_combo.bind("<<ComboboxSelected>>", lambda _event: generate_teacher_summary(force=False))

    def apply_chart_mode(mode):
        show_winrate = mode in ("black", "white", "winrate")
        show_score = mode in ("black", "white", "score")
        white_view = mode == "white"

        line1.set_ydata(white_winrates if white_view else black_winrates)
        line2.set_ydata(white_score_leads if white_view else black_score_leads)
        line1.set_visible(show_winrate)
        line2.set_visible(show_score)
        winrate_midline.set_visible(show_winrate)

        ax1.yaxis.set_visible(show_winrate)
        ax1.spines["left"].set_visible(show_winrate)
        ax2.yaxis.set_visible(show_score)
        ax2.spines["right"].set_visible(show_score)

        if white_view:
            line1.set_label(t("analysis.chart_white_winrate_label"))
            line2.set_label(t("analysis.chart_white_score_label"))
            ax1.set_ylabel(t("analysis.chart_y_white_winrate"), color='#2c3e50', fontsize=11)
            ax2.set_ylabel(t("analysis.chart_y_white_score"), color='#e74c3c', fontsize=11)
        else:
            line1.set_label(t("analysis.chart_winrate_label"))
            line2.set_label(t("analysis.chart_score_label"))
            ax1.set_ylabel(t("analysis.chart_y_winrate"), color='#2c3e50', fontsize=11)
            ax2.set_ylabel(t("analysis.chart_y_score"), color='#e74c3c', fontsize=11)

        visible_lines = [line for line in (line1, line2) if line.get_visible()]
        ax1.legend(visible_lines, [line.get_label() for line in visible_lines], loc='upper left', fontsize=10)
        fig.tight_layout()
        canvas.draw_idle()
        canvas.get_tk_widget().focus_set()
    
    apply_chart_mode(chart_mode.get())
    canvas.draw()
    canvas.get_tk_widget().focus_set()

    fig.canvas.mpl_connect('button_press_event', on_click_chart)
    fig.canvas.mpl_connect('key_press_event', on_key_chart)
    fig.canvas.mpl_connect('motion_notify_event', on_motion_chart)
    root.after(100, generate_teacher_summary)


def update_ui_with_data(result):
    """直接使用記憶體中的數據更新 UI，並將所有分析結果保存到快取以供後續比較使用"""
    try:
        current_turn = len(board.stones)
        result_turn = result["turnNumber"]
        
        # 檢查資料是否完整
        if "rootInfo" not in result:
            logger.debug("分析結果尚未包含 rootInfo，略過: id=%s turn=%s", result.get("id"), result_turn)
            return
        
        # 【改進】無論手數是否匹配，都將結果保存到快取
        # 這樣即使棋局推進，舊手數的分析結果仍可被查詢，用於判定失誤時的比較
        moves = result.get("moves", [])
        if moves:
            board_hash = analyzer.get_board_hash_from_moves(moves[:result_turn])
            analyzer._store_cache(board_hash, result)
            logger.debug("分析結果已快取: turn=%s cache_size=%s", result_turn, len(analyzer.analysis_cache))
        
        # 只有當是當前手數時，才更新 UI（藍圈、勝率標籤等）
        if result_turn != current_turn:
            logger.debug("結果已快取，但非當前手數，暫不更新 UI: result_turn=%s current_turn=%s", result_turn, current_turn)
            return

        raw_winrate = result["rootInfo"]["winrate"]
        is_black_turn = (current_turn % 2 == 0)
        black_wr = raw_winrate 
        white_wr = 1.0 - black_wr
        to_move_key = "stone.black" if is_black_turn else "stone.white"
        
        # 更新勝率標籤
        set_winrate_text("analysis.winrate_summary", to_move_key=to_move_key, black_wr=black_wr*100, white_wr=white_wr*100)

        # 繪製 AI 建議點：第一推薦藍點，其餘推薦綠點
        if "moveInfos" in result and len(result["moveInfos"]) > 0:
            board.draw_recommendation_points(result["moveInfos"], is_black_turn)
        else:
            board.clear_blue_point()

        # ====== 教學觸發邏輯 (原本的邏輯搬過來) ======
        last_move_gtp = "Pass"
        if board.stones:
            last_x, last_y, _ = board.stones[-1]
            last_move_gtp = board.to_gtp_coord(last_x, last_y)

        # 檢查是否需要叫老師出來說話
        critical_event = data_filter.process_analysis(
            current_turn, result, last_move_gtp, is_playback=is_playback_mode
        )
        if critical_event:
            # 【Phase 1】檢查是否已有快取的解說，若有則直接顯示，否則呼叫 LLM 生成新的
            cached_commentary = get_commentary_from_cache(critical_event["turn"], critical_event["user_move"])
            if cached_commentary:
                logger.debug(f"快取命中：第 {critical_event['turn']} 手 ({critical_event['user_move']}) 已有解說，直接顯示")
                update_teacher_ui(cached_commentary)
            else:
                logger.debug(f"快取未命中：第 {critical_event['turn']} 手 ({critical_event['user_move']})，呼叫 LLM 生成")
                # 【Phase 1】設置全域狀態，準備快取生成的解說
                global current_critical_event, current_generated_commentary
                current_critical_event = critical_event
                current_generated_commentary = ""
                # 呼叫 LLM 生成解說
                current_llm_worker.start_commentary(critical_event)
        else:
            # 【修復】沒有失誤時，清空舊解說（僅在非回放模式下）
            # 回放模式下解說由 jump_to_specific_move 負責，這裡不覆蓋
            if not is_playback_mode:
                update_teacher_ui("")

    except KeyError as e:
        logger.warning("UI 更新失敗，分析結果缺少必要欄位: missing=%s result=%s", e, result)
    except (TypeError, ValueError, IndexError) as e:
        logger.warning("UI 更新失敗，分析結果格式或座標異常: error=%s result=%s", e, result)

def on_analyze_button_click():
    if not is_analyzer_ready():
        show_analyzer_not_ready()
        return

    # 【修復】手動分析 → 非回放模式，允許觸發 LLM 解說
    global is_playback_mode
    is_playback_mode = False

    # 不再需要 threading.Thread(target=task)，因為發送請求是瞬間的
    board.clear_blue_point()
    set_winrate_text("analysis.ai_thinking")
    # 直接叫 analyzer 傳送當前棋局
    analyzer.send_query(board.stones)



# --- 棋盤邏輯 ---
class GoBoard(tk.Canvas):
    def __init__(self, master=None):
        super().__init__(
            master,
            width=CANVAS_SIZE,
            height=CANVAS_SIZE,
            bg=BOARD_BG,
            highlightthickness=1,
            highlightbackground=PANEL_BORDER
        )
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_color = "black"
        self.margin = MARGIN 
        self.preview_id = None
        self.blue_point_ids = []
        self.recommendation_points = {}
        self.score_estimate_active = False
        self.score_estimate_data = None
        self.variation_timer = None
        self.variation_hover_coord = None
        
        # --- 分支系統核心 ---
        self.root_node = GameNode()
        self.current_node = self.root_node
        self.analyze_timer = None

        # 自訂圖片
        self.board_bg_image = None
        self.board_frame_image = None
        self.board_frame_image_path = None  # 外框背景原始路徑（供 <Configure> 動態重縮放使用）
        self._frame_bg_resize_after_id = None  # <Configure> 節流用的 after id
        self.black_stone_image = None
        self.white_stone_image = None
        self.frame_bg_label = None  # 外框背景 Label（由 board_shell 注入）
        self._load_custom_images()

        self.draw_board()
        self.bind("<Button-1>", self.on_click)
        self.bind("<Motion>", self.preview)
        self.bind("<Leave>", self.on_leave)

    def _load_custom_images(self):
        """載入自訂圖片（如果有的話）"""
        self.board_bg_image = None
        self.board_frame_image = None
        self.board_frame_image_path = None
        self.black_stone_image = None
        self.white_stone_image = None

        bg_path = config_service.get_board_background()
        if bg_path and os.path.exists(bg_path):
            try:
                self.board_bg_image = load_tk_image(bg_path, (CANVAS_SIZE, CANVAS_SIZE), fill_size=True)
            except Exception as e:
                logger.warning(f"無法載入棋盤背景圖片 {bg_path}: {e}")

        frame_path = config_service.get_board_frame_background()
        if frame_path and os.path.exists(frame_path):
            self.board_frame_image_path = frame_path
            # 載入時 board_shell 尺寸可能尚未確定（winfo_width() 可能回傳 1），
            # 先用 CANVAS_SIZE 作為預設尺寸載入；待 board_shell 首次 <Configure> 觸發時
            # 再用實際尺寸重縮放（見 _resize_frame_background）。
            try:
                self.board_frame_image = load_tk_image(frame_path, (CANVAS_SIZE, CANVAS_SIZE), fill_size=True)
            except Exception as e:
                logger.warning(f"無法載入棋盤外框圖片 {frame_path}: {e}")
        self._apply_frame_background()

        black_path = config_service.get_black_stone_image()
        if black_path and os.path.exists(black_path):
            try:
                self.black_stone_image = load_tk_image(
                    black_path,
                    (STONE_IMAGE_SIZE, STONE_IMAGE_SIZE),
                    fill_size=True,
                )
            except Exception as e:
                logger.warning(f"無法載入黑棋圖片 {black_path}: {e}")

        white_path = config_service.get_white_stone_image()
        if white_path and os.path.exists(white_path):
            try:
                self.white_stone_image = load_tk_image(
                    white_path,
                    (STONE_IMAGE_SIZE, STONE_IMAGE_SIZE),
                    fill_size=True,
                )
            except Exception as e:
                logger.warning(f"無法載入白棋圖片 {white_path}: {e}")

    def _apply_frame_background(self):
        if self.frame_bg_label is None:
            return
        if self.board_frame_image:
            self.frame_bg_label.config(image=self.board_frame_image, text="")
            self.frame_bg_label.image = self.board_frame_image
        else:
            self.frame_bg_label.config(image="", text="")
        # 除錯輸出：確認背景 Label 與棋盤 Canvas 是兩個不同物件、尺寸不同
        try:
            print("BACKGROUND:", self.frame_bg_label.winfo_x(), self.frame_bg_label.winfo_y(),
                  self.frame_bg_label.winfo_width(), self.frame_bg_label.winfo_height())
            print("BOARD:", self.winfo_x(), self.winfo_y(),
                  self.winfo_width(), self.winfo_height())
        except Exception:
            pass

    def _resize_frame_background(self, size):
        """依 board_shell 實際尺寸重新縮放外框背景圖片（cover 模式：填滿裁切）。

        由 board_shell 的 <Configure> 事件回呼觸發，確保視窗縮放時背景圖片動態更新。
        棋盤 Canvas 本身保持固定 620×620，不會被縮放。
        """
        if not self.board_frame_image_path or not os.path.exists(self.board_frame_image_path):
            return
        if not self.frame_bg_label:
            return
        w, h = size
        # 尺寸無效時（例如初始化階段）退回 CANVAS_SIZE
        if w < 10 or h < 10:
            w, h = CANVAS_SIZE, CANVAS_SIZE
        try:
            new_img = load_tk_image(self.board_frame_image_path, (w, h), fill_size=True)
            self.board_frame_image = new_img
            self.frame_bg_label.config(image=new_img, text="")
            self.frame_bg_label.image = new_img
        except Exception as e:
            logger.warning(f"無法重縮放棋盤外框圖片 {self.board_frame_image_path}: {e}")

    @property
    def stones(self):
        """動態生成歷史落子紀錄，不會再因為提子而消失，確保 AI 判斷正確"""
        path = []
        curr = self.current_node
        while curr and curr.move is not None:
            path.append(curr.move)
            curr = curr.parent
        return path[::-1] # 反轉成從頭到尾的順序

    def _current_node_path(self):
        path = []
        curr = self.current_node
        while curr and curr.move is not None:
            path.append(curr)
            curr = curr.parent
        return path[::-1]

    def _branch_display_start_index(self):
        """Return 1-based move index where the current branch starts, or None on main line."""
        for idx, node in enumerate(self._current_node_path(), start=1):
            if node.parent and node.parent.children and node.parent.children[0] is not node:
                return idx
        return None

    def _build_live_move_numbers(self):
        history = self.stones
        branch_start = self._branch_display_start_index()
        board_state = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        move_numbers = {}

        for move_idx, (x, y, color) in enumerate(history, start=1):
            board_state[y][x] = color
            if branch_start is None:
                move_numbers[(x, y)] = move_idx
            elif move_idx >= branch_start:
                move_numbers[(x, y)] = move_idx - branch_start + 1
            else:
                move_numbers.pop((x, y), None)

            opponent = self._next_color(color)
            for nx, ny in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board_state[ny][nx] == opponent:
                    group, libs = self._get_group_and_liberties_on_board(board_state, nx, ny)
                    if not libs:
                        self._remove_group_on_board(board_state, group)
                        for gx, gy in group:
                            move_numbers.pop((gx, gy), None)

        return {
            (x, y): number
            for (x, y), number in move_numbers.items()
            if self.board[y][x] is not None
        }

    def _draw_move_numbers(self):
        self.delete("move_number")
        if not show_move_numbers_var.get():
            return

        margin = self.margin
        for (x, y), move_number in self._build_live_move_numbers().items():
            color = self.board[y][x]
            label_fill = "#ffffff" if color == "black" else "#111111"
            px, py = margin + x * CELL_SIZE, margin + y * CELL_SIZE
            self.create_text(
                px,
                py,
                text=str(move_number),
                fill=label_fill,
                font=("Arial", 8, "bold"),
                tags="move_number",
            )

    def _format_move_winrate(self, winrate, is_black_turn):
        if winrate is None:
            winrate = 0.5
        display_winrate = winrate if is_black_turn else 1.0 - winrate
        return f"{display_winrate * 100:.1f}%"

    def _draw_recommendation_point(self, x, y, winrate, is_black_turn, fill, text_fill):
        margin = self.margin
        px, py = margin + x * CELL_SIZE, margin + y * CELL_SIZE
        ov = self.create_oval(
            px - RECOMMENDATION_RADIUS,
            py - RECOMMENDATION_RADIUS,
            px + RECOMMENDATION_RADIUS,
            py + RECOMMENDATION_RADIUS,
            fill=fill,
            outline="#ffffff" if fill == BEST_MOVE_BLUE else "#174b2a",
            width=1,
            tags="blue_point",
        )
        label_text = self._format_move_winrate(winrate, is_black_turn)
        label = self.create_text(
            px,
            py,
            text=label_text,
            fill=text_fill,
            font=("Arial", 7, "bold"),
            tags="blue_point",
        )
        return [ov, label]

    def draw_recommendation_points(self, move_infos, is_black_turn):
        self.clear_blue_point()
        drawn_coords = set()
        drawn_count = 0
        self.recommendation_points = {}

        for move_info in move_infos:
            if drawn_count >= RECOMMENDATION_LIMIT:
                break

            gtp_coord = move_info.get("move", "")
            if not gtp_coord or gtp_coord.lower() == "pass":
                continue

            try:
                x, y = self.from_gtp_coord(gtp_coord)
            except (ValueError, IndexError):
                logger.debug("略過無法解析的 AI 推薦座標: %s", gtp_coord)
                continue

            if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
                continue
            if self.board[y][x] is not None or (x, y) in drawn_coords:
                continue

            if drawn_count == 0:
                fill = BEST_MOVE_BLUE
                text_fill = "#ffffff"
            else:
                fill = RECOMMENDATION_GREENS[min(drawn_count - 1, len(RECOMMENDATION_GREENS) - 1)]
                text_fill = "#000000"

            self.blue_point_ids.extend(
                self._draw_recommendation_point(
                    x,
                    y,
                    move_info.get("winrate", 0.5),
                    is_black_turn,
                    fill,
                    text_fill,
                )
            )
            self.recommendation_points[(x, y)] = {
                "move_info": move_info,
                "is_black_turn": is_black_turn,
            }
            drawn_coords.add((x, y))
            drawn_count += 1

    def draw_blue_point(self, x, y, winrate, is_black_turn):
        self.clear_blue_point()
        self.blue_point_ids.extend(
            self._draw_recommendation_point(x, y, winrate, is_black_turn, BEST_MOVE_BLUE, "#ffffff")
        )

    def clear_blue_point(self):
        self._cancel_variation_timer()
        self.clear_variation_preview()
        self.recommendation_points = {}
        self.delete("blue_point")

    def clear_score_estimate(self):
        self.score_estimate_active = False
        self.score_estimate_data = None
        self.delete("score_estimate")

    def _draw_score_estimate_overlay(self, ownership):
        self.delete("score_estimate")
        if not ownership:
            return

        margin = self.margin
        limit = min(len(ownership), BOARD_SIZE * BOARD_SIZE)

        for index in range(limit):
            value = ownership[index]
            if value is None:
                continue

            x = index % BOARD_SIZE
            y = index // BOARD_SIZE
            px, py = margin + x * CELL_SIZE, margin + y * CELL_SIZE
            stone = self.board[y][x]

            if stone is None:
                if value > 0.5:
                    self.create_rectangle(px - 9, py - 9, px + 9, py + 9, fill="#000000", outline="#000000", stipple="gray50", width=1, tags="score_estimate")
                elif value < -0.5:
                    self.create_rectangle(px - 9, py - 9, px + 9, py + 9, fill="#ffffff", outline="#ffffff", stipple="gray50", width=1, tags="score_estimate")
                continue

            if (stone == "black" and value < -0.5) or (stone == "white" and value > 0.5):
                marker_color = "#ffffff" if value < 0 else "#000000"
                self.create_line(px - 9, py - 9, px + 9, py + 9, fill=marker_color, width=3, tags="score_estimate")
                self.create_line(px - 9, py + 9, px + 9, py - 9, fill=marker_color, width=3, tags="score_estimate")

    def _cancel_variation_timer(self):
        if self.variation_timer:
            root.after_cancel(self.variation_timer)
            self.variation_timer = None
        self.variation_hover_coord = None

    def clear_variation_preview(self):
        self.delete("variation_preview")
        if show_move_numbers_var.get():
            self._draw_move_numbers()

    def _handle_recommendation_hover(self, coord):
        if coord not in self.recommendation_points:
            self._cancel_variation_timer()
            self.clear_variation_preview()
            return

        if coord == self.variation_hover_coord:
            return

        self._cancel_variation_timer()
        self.clear_variation_preview()
        self.variation_hover_coord = coord
        self.variation_timer = root.after(VARIATION_HOVER_DELAY_MS, lambda c=coord: self.show_variation_preview(c))

    def _next_color(self, color):
        return "white" if color == "black" else "black"

    def _remove_group_on_board(self, board_state, group):
        for gx, gy in group:
            board_state[gy][gx] = None

    def _get_group_and_liberties_on_board(self, board_state, x, y):
        color = board_state[y][x]
        visited, to_visit = set(), [(x, y)]
        group, liberties = [], set()
        while to_visit:
            cx, cy = to_visit.pop()
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))
            group.append((cx, cy))
            for nx, ny in [(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)]:
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                    if board_state[ny][nx] is None:
                        liberties.add((nx, ny))
                    elif board_state[ny][nx] == color:
                        to_visit.append((nx, ny))
        return group, liberties

    def _play_preview_move(self, board_state, x, y, color):
        if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE) or board_state[y][x] is not None:
            return False

        board_state[y][x] = color
        opponent = self._next_color(color)
        captured_any = False
        for nx, ny in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board_state[ny][nx] == opponent:
                group, libs = self._get_group_and_liberties_on_board(board_state, nx, ny)
                if not libs:
                    self._remove_group_on_board(board_state, group)
                    captured_any = True

        group, libs = self._get_group_and_liberties_on_board(board_state, x, y)
        if not libs and not captured_any:
            board_state[y][x] = None
            return False
        return True

    def _draw_variation_stone(self, x, y, color, move_number):
        margin = self.margin
        px, py = margin + x * CELL_SIZE, margin + y * CELL_SIZE
        fill = VARIATION_BLACK if color == "black" else VARIATION_WHITE
        outline = "#000000" if color == "black" else "#6f6252"
        label_fill = VARIATION_LABEL_WHITE if color == "black" else VARIATION_LABEL_BLACK
        self.create_oval(
            px - 12,
            py - 12,
            px + 12,
            py + 12,
            fill=fill,
            outline=outline,
            width=2,
            tags="variation_preview",
        )
        self.create_text(
            px,
            py,
            text=str(move_number),
            fill=label_fill,
            font=("Arial", 8, "bold"),
            tags="variation_preview",
        )

    def show_variation_preview(self, coord):
        self.variation_timer = None
        if coord != self.variation_hover_coord or coord not in self.recommendation_points:
            return

        point_data = self.recommendation_points[coord]
        move_info = point_data["move_info"]
        candidate_move = move_info.get("move", "")
        pv_moves = list(move_info.get("pv", []))
        if candidate_move and (not pv_moves or pv_moves[0].lower() != candidate_move.lower()):
            pv_moves.insert(0, candidate_move)

        self.clear_variation_preview()
        self.delete("move_number")
        board_state = copy.deepcopy(self.board)
        color = "black" if point_data["is_black_turn"] else "white"
        move_number = 1

        for gtp_coord in pv_moves[:VARIATION_PREVIEW_LIMIT]:
            if not gtp_coord or gtp_coord.lower() == "pass":
                color = self._next_color(color)
                continue

            try:
                x, y = self.from_gtp_coord(gtp_coord)
            except (ValueError, IndexError):
                logger.debug("略過無法解析的變化圖座標: %s", gtp_coord)
                color = self._next_color(color)
                continue

            if self._play_preview_move(board_state, x, y, color):
                self._draw_variation_stone(x, y, color, move_number)
                move_number += 1
            color = self._next_color(color)

    def save_state(self):
        """將當前狀態存入歷史堆疊"""
        state = (copy.deepcopy(self.stones), copy.deepcopy(self.board), self.current_color)
        self.history_stack.append(state)
        # 注意：正常落子時會清空 redo_stack，但在載入 SGF 或 Redo 操作時不應清空，
        # 這裡為了簡化，標準落子邏輯在 play_move 裡處理 redo_stack 的清空。
    def undo(self, event=None):
        if self.current_node.parent is not None:
            # 【修復】後退 → 回放模式，不觸發新的 LLM 解說
            global is_playback_mode
            is_playback_mode = True
            self.current_node = self.current_node.parent
            self.rebuild_board()
            self.on_state_change()
            self._show_playback_commentary()

    def redo(self, event=None):
        if self.current_node.children:
            # 【修復】前進到已存在的分支 → 回放模式，不觸發新的 LLM 解說
            global is_playback_mode
            is_playback_mode = True
            idx = self.current_node.active_child_idx
            self.current_node = self.current_node.children[idx]
            self.rebuild_board()
            self.on_state_change()
            self._show_playback_commentary()

    def switch_branch(self, direction):
        """切換同一手棋的不同變化圖 (direction: 1 或 -1)"""
        if self.current_node.parent and len(self.current_node.parent.children) > 1:
            # 【修復】切換分支 → 回放模式
            global is_playback_mode
            is_playback_mode = True
            parent = self.current_node.parent
            new_idx = (parent.active_child_idx + direction) % len(parent.children)
            parent.active_child_idx = new_idx
            self.current_node = parent.children[new_idx]
            self.rebuild_board()
            self.on_state_change()
            self._show_playback_commentary()

    def on_state_change(self):
        if self.score_estimate_active:
            self.clear_score_estimate()
            update_score_estimate_button_label()

        self.clear_blue_point()
        
        if not is_analyzer_ready():
            set_winrate_text("analysis.engine_not_ready")
            status_var.set(t("status.katago_initializing"))
            if hasattr(self, 'branch_ui'):
                self.branch_ui.draw_branches()
            return

        # 只有在非整盤分析狀態下才顯示「盤面更新中」
        # 【Phase 1】用 analyzer.full_analyze_event.is_set() 代改 is_full_analyzing
        if not analyzer.full_analyze_event.is_set():
            set_winrate_text("analysis.board_updating")
            
        if hasattr(self, 'branch_ui'):
            self.branch_ui.draw_branches()
                
        if self.analyze_timer:
            root.after_cancel(self.analyze_timer)
        
        # 檢查鎖定，避免排程任務在 500ms 後偷跑
        if not analyzer.full_analyze_event.is_set():
            self.analyze_timer = root.after(500, auto_analyze)

    def draw_board(self):
        margin = MARGIN

        # 如果有自訂背景圖片，繪製背景
        if self.board_bg_image:
            self.create_image(0, 0, image=self.board_bg_image, anchor="nw")
        else:
            # 使用預設背景色
            self.create_rectangle(0, 0, CANVAS_SIZE, CANVAS_SIZE, fill=BOARD_BG, outline="")

        # 畫線
        for i in range(BOARD_SIZE):
            x = margin + i * CELL_SIZE
            self.create_line(x, margin, x, margin + (BOARD_SIZE - 1) * CELL_SIZE, fill=BOARD_LINE)
            self.create_line(margin, x, margin + (BOARD_SIZE - 1) * CELL_SIZE, x, fill=BOARD_LINE)

        # 星位
        stars = [3, 9, 15]
        for r in stars:
            for c in stars:
                px, py = margin + r * CELL_SIZE, margin + c * CELL_SIZE
                self.create_oval(px-3, py-3, px+3, py+3, fill=BOARD_LINE, outline=BOARD_LINE)


        self.draw_coordinates(margin)

    def draw_coordinates(self, margin):
        font = ("Arial", 10)

        # 欄標 (A-T，不含 I)
        for i in range(BOARD_SIZE):
            col = chr(ord('A') + i)
            if col >= 'I':
                col = chr(ord(col) + 1)

            x = margin + i * CELL_SIZE

            # 上
            self.create_text(x, margin - 20, text=col, font=font, fill=TEXT_MUTED)
            # 下
            self.create_text(x, margin + (BOARD_SIZE - 1) * CELL_SIZE + 20, text=col, font=font, fill=TEXT_MUTED)

        # 列標 (1-19)
        for i in range(BOARD_SIZE):
            row = str(BOARD_SIZE - i)
            y = margin + i * CELL_SIZE

            # 左
            self.create_text(margin - 20, y, text=row, font=font, fill=TEXT_MUTED)
            # 右
            self.create_text(margin + (BOARD_SIZE - 1) * CELL_SIZE + 20, y, text=row, font=font, fill=TEXT_MUTED)

    def preview(self, event):
        if self.score_estimate_active:
            self._handle_recommendation_hover(None)
            return
        margin = self.margin
        x, y = round((event.x - margin) / CELL_SIZE), round((event.y - margin) / CELL_SIZE)
        if self.preview_id:
            self.delete(self.preview_id)
            self.preview_id = None
        if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and self.board[y][x] is None:
            px, py = margin + x * CELL_SIZE, margin + y * CELL_SIZE
            self.preview_id = self.create_oval(px-12, py-12, px+12, py+12, fill=ACCENT, outline="", stipple="gray50")
            if self.find_withtag("blue_point"):
                self.tag_lower(self.preview_id, "blue_point")
            self._handle_recommendation_hover((x, y))
        else:
            self._handle_recommendation_hover(None)

    def on_leave(self, event=None):
        if self.preview_id:
            self.delete(self.preview_id)
            self.preview_id = None
        self._handle_recommendation_hover(None)


    def play_move(self, x, y, forced_color=None):
        if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE) or self.board[y][x]:
            return False

        # 【修復】正常落子 → 非回放模式，允許觸發新的 LLM 解說
        global is_playback_mode
        is_playback_mode = False

        color = forced_color if forced_color else self.current_color
        
        # 1. 檢查是否已經有這個分支 (如果有，直接走進該變化圖)
        for idx, child in enumerate(self.current_node.children):
            if child.move == (x, y, color):
                self.current_node.parent.active_child_idx = idx if self.current_node.parent else 0
                self.current_node = child
                self.rebuild_board()
                self.on_state_change()
                return True

        # 2. 嘗試落子與提子判斷
        self.board[y][x] = color
        opponent = "white" if color == "black" else "black"
        captured_any = False
        for nx, ny in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
            if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and self.board[ny][nx] == opponent:
                group, libs = self.get_group_and_liberties(nx, ny)
                if not libs:
                    self.remove_group(group)
                    captured_any = True

        # 自殺檢查
        group, libs = self.get_group_and_liberties(x, y)
        if not libs and not captured_any:
            self.board[y][x] = None # 退回
            return False

        # 3. 合法，建立新節點並連接
        new_node = GameNode((x, y, color), self.current_node)
        self.current_node.children.append(new_node)
        self.current_node.active_child_idx = len(self.current_node.children) - 1
        self.current_node = new_node
        self.current_color = opponent
        self.refresh_display()
        self.on_state_change()
        return True

    def on_click(self, event):
        if self.score_estimate_active:
            return
        margin = self.margin
        x, y = round((event.x - margin) / CELL_SIZE), round((event.y - margin) / CELL_SIZE)
        self._handle_recommendation_hover(None)
        if self.play_move(x, y):
            self.refresh_display()

    def get_group_and_liberties(self, x, y):
        color = self.board[y][x]
        visited, to_visit = set(), [(x, y)]
        group, liberties = [], set()
        while to_visit:
            cx, cy = to_visit.pop()
            if (cx, cy) in visited: continue
            visited.add((cx, cy))
            group.append((cx, cy))
            for nx, ny in [(cx+1,cy), (cx-1,cy), (cx,cy+1), (cx,cy-1)]:
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                    if self.board[ny][nx] is None: liberties.add((nx, ny))
                    elif self.board[ny][nx] == color: to_visit.append((nx, ny))
        return group, liberties


    def remove_group(self, group):
        """修正：提子只清空視覺棋盤(board)，絕不能刪除歷史紀錄(stones)"""
        for (gx, gy) in group: 
            self.board[gy][gx] = None

    def rebuild_board(self):
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        history = self.stones  
        
        for x, y, color in history:
            # 落子
            self.board[y][x] = color
            
            # 執行提子邏輯 — 檢查相鄰所有對方棋子是否無氣
            opponent = "white" if color == "black" else "black"
            for nx, ny in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and self.board[ny][nx] == opponent:
                    group, libs = self.get_group_and_liberties(nx, ny)
                    if not libs:
                        # 該對方群組無氣，提掉它
                        self.remove_group(group)

        # 強制修正下一步顏色：如果歷史最後一手是黑，下一步必為白
        if history:
            last_color = history[-1][2]
            self.current_color = "white" if last_color == "black" else "black"
        else:
            self.current_color = "black"

        self.refresh_display()
        
    def refresh_display(self):
        self.delete("all")
        self.draw_board()
        margin = self.margin

        # 1. 繪製所有在棋盤上的棋子 (從 self.board 讀取，而非 history)
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                color = self.board[y][x]
                if color:
                    px, py = margin + x * CELL_SIZE, margin + y * CELL_SIZE
                    # 使用自訂棋子圖片（如果有的話）
                    if color == "black" and self.black_stone_image:
                        self.create_image(px, py, image=self.black_stone_image, anchor="center")
                    elif color == "white" and self.white_stone_image:
                        self.create_image(px, py, image=self.white_stone_image, anchor="center")
                    else:
                        # 預設圓形棋子
                        fill = STONE_BLACK if color == "black" else STONE_WHITE
                        outline = "#0f0f0f" if color == "black" else "#8e806f"
                        self.create_oval(px-12, py-12, px+12, py+12, fill=fill, outline=outline, width=1)

        # 2. 繪製最後一手標記 (紅色小方塊)
        if self.current_node and self.current_node.move:
            lx, ly, lcolor = self.current_node.move
            px, py = margin + lx * CELL_SIZE, margin + ly * CELL_SIZE
            # 標記在最後一手的中心
            self.create_rectangle(px-5, py-5, px+5, py+5, outline="red", width=2)

        self._draw_move_numbers()
        if self.score_estimate_data:
            self._draw_score_estimate_overlay(self.score_estimate_data.get("ownership", []))

        # 3. 顯示目前手數 (選擇性：顯示在標籤或標題)
        total_moves = len(self.stones)
        root.title(t("app.title_with_move", moves=total_moves))
    # --- 座標與檔案處理 ---
    def to_gtp_coord(self, x, y):
        col = chr(ord('A') + x)
        if col >= 'I': col = chr(ord(col) + 1)
        return f"{col}{BOARD_SIZE - y}"

    def from_gtp_coord(self, gtp):
        col_str = gtp[0].upper()
        row_str = gtp[1:]
        x = ord(col_str) - ord('A')
        if col_str > 'I': x -= 1
        y = BOARD_SIZE - int(row_str)
        return x, y

    def to_sgf_coord(self, x, y):
        return f"{chr(ord('a') + x)}{chr(ord('a') + y)}"
        
    def from_sgf_coord(self, sgf_c):
        if not sgf_c or len(sgf_c) < 2: return None # Handle Pass or Empty
        x = ord(sgf_c[0].lower()) - ord('a')
        y = ord(sgf_c[1].lower()) - ord('a')
        return x, y

    def export_as_json(self, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        # 現在 stones 是一個 property，直接呼叫即可
        current_path = self.stones 
        moves = [["B" if c == "black" else "W", self.to_gtp_coord(x, y)] for x, y, c in current_path]
        
        data = {
            "id": f"game_{int(time.time())}",
            "initialStones": [],
            "moves": moves,
            "rules": "japanese",
            "komi": 6.5,
            "boardXSize": 19,
            "boardYSize": 19,
            "analyzeTurns": [len(moves)]
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def export_as_sgf(self, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        # SGF 定義頭部
        sgf_content = "(;GM[1]FF[4]CA[UTF-8]AP[GoAI]KM[6.5]SZ[19]\n"
        
        # 【Phase 2】輔助函數：計算節點的轉換序號 (turn number)
        def get_node_turn_number(node):
            """計算節點在遊戲中的手數序號 (1-indexed)"""
            turns = 0
            current = node
            # 從該節點往回追溯到根節點
            while current.parent:
                current = current.parent
                turns += 1
            return turns + 1
        
        # 從根節點的子節點開始遞迴
        def write_node(node):
            content = ""
            if node.move:
                x, y, color = node.move
                bw = "B" if color == "black" else "W"
                gtp_move = self.to_gtp_coord(x, y)
                content += f";{bw}[{self.to_sgf_coord(x, y)}]"
                
                # 【Phase 2】新增註解：從快取中查詢該手數的解說
                turn_num = get_node_turn_number(node)
                cached_commentary = get_commentary_from_cache(turn_num, gtp_move)
                if cached_commentary:
                    # 轉義特殊字符，避免破壞 SGF 格式
                    escaped_commentary = cached_commentary.replace("\\", "\\\\").replace("]", "\\]")
                    content += f"C[{escaped_commentary}]"
                    logger.debug(f"【SGF 匯出】第 {turn_num} 手已新增註解: {len(escaped_commentary)} 字")
            
            if not node.children:
                return content
            
            if len(node.children) == 1:
                # 只有一個子節點，直接串下去
                return content + write_node(node.children[0])
            else:
                # 有多個分支，每個分支都要用 () 包起來
                for child in node.children:
                    content += "(" + write_node(child) + ")"
                return content

        sgf_content += write_node(self.root_node)
        sgf_content += ")"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(sgf_content)
        print(f"分支 SGF 已儲存至: {filename}")

    def load_sgf(self, filename):
        """讀取 SGF 並正確建立分支樹狀結構，同時恢復註解到快取【Phase 3】修正版本"""
        with open(filename, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # 1. 重置整棵樹
        self.root_node = GameNode()
        self.current_node = self.root_node
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_color = "black"

        # 【Phase 3】清空舊的快取，準備恢復註解
        global commentary_cache
        commentary_cache.clear()

        # 2. 遞迴解析 SGF 分支結構 (修正：支持正確的分支)
        def parse_sequence(content, pos, parent_node):
            """
            遞迴解析 SGF 序列（包括分支）
            content: 完整 SGF 文本
            pos: 當前解析位置
            parent_node: 該序列的父節點
            回傳：(最後的位置, 當前分支的最後節點)
            """
            turn_num = 0
            current = parent_node
            
            while pos < len(content):
                # 找下一個節點或分支標記
                if content[pos] == ';':
                    # 解析單個節點
                    pos += 1
                    match = re.match(r'([BW])\[([a-z]{0,2})\](?:C\[((?:[^\]]|\\\])*)\])?', content[pos:])
                    if match:
                        color_code = match.group(1)
                        sgf_pos = match.group(2)
                        comment = match.group(3)
                        pos += match.end()
                        
                        if sgf_pos and sgf_pos != "tt":
                            coords = self.from_sgf_coord(sgf_pos)
                            if coords:
                                x, y = coords
                                gtp_move = self.to_gtp_coord(x, y)
                                
                                # 建立新節點
                                color = "black" if color_code == "B" else "white"
                                new_node = GameNode((x, y, color), current)
                                current.children.append(new_node)
                                current = new_node
                                
                                # 恢復註解快取
                                turn_num += 1
                                if comment:
                                    unescaped_comment = comment.replace("\\]", "]").replace("\\\\", "\\")
                                    add_to_commentary_cache(turn_num, gtp_move, unescaped_comment)
                                    logger.debug(f"【SGF 載入】第 {turn_num} 手恢復註解: {len(unescaped_comment)} 字")
                elif content[pos] == '(':
                    # 開始分支，遞迴處理
                    pos += 1
                    pos, _ = parse_sequence(content, pos, current)
                elif content[pos] == ')':
                    # 分支結束
                    return pos + 1, current
                else:
                    pos += 1
            
            return pos, current
        
        # 3. 找到第一個 ; 開始解析
        start_pos = content.find('(;')
        if start_pos >= 0:
            parse_sequence(content, start_pos + 1, self.root_node)
            # 跳轉到主支的最後一手（最深的第一個子節點）
            node = self.root_node
            while node.children:
                node = node.children[0]
                self.current_node = node
        
        self.rebuild_board()
        # 【修復】載入棋譜 → 回放模式，不觸發新的 LLM 解說
        global is_playback_mode
        is_playback_mode = True
        logger.info(f"SGF 已載入並重建節點，恢復了 {len(commentary_cache)} 條註解")
        print("SGF 已載入並重建節點")

    def jump_to_specific_move(self, target_idx):
        """跳轉到當前分支的指定手數"""
        current_idx = len(self.stones)
        if target_idx == current_idx:
            return

        # 【修復】跳轉 → 回放模式，不觸發新的 LLM 解說
        global is_playback_mode
        is_playback_mode = True

        if target_idx < current_idx:
            # 目標在過去：不斷往回退 (Undo 邏輯)
            steps = current_idx - target_idx
            for _ in range(steps):
                if self.current_node.parent is not None:
                    self.current_node = self.current_node.parent
        else:
            # 目標在未來：不斷往前走 (Redo 邏輯)
            steps = target_idx - current_idx
            for _ in range(steps):
                if self.current_node.children:
                    # 預設走目前啟用的分支
                    idx = self.current_node.active_child_idx
                    self.current_node = self.current_node.children[idx]
                else:
                    break # 已經到底了

        # 重建盤面並觸發更新
        self.rebuild_board()
        self.on_state_change()
        # 顯示該手的快取解說（若有）
        self._show_playback_commentary()

    def jump_to_branch(self, idx):
        """點擊分支圖時跳轉"""
        if self.current_node.parent:
            # 【修復】切換分支 → 回放模式
            global is_playback_mode
            is_playback_mode = True
            parent = self.current_node.parent
            if 0 <= idx < len(parent.children):
                parent.active_child_idx = idx
                self.current_node = parent.children[idx]
                self.rebuild_board()
                self.on_state_change()
                self._show_playback_commentary()

    def _show_playback_commentary(self):
        """【修復】回放模式下，從快取顯示當前手數的解說；無快取則清空。
        
        此方法統一處理 undo / redo / switch_branch / jump_to_specific_move /
        jump_to_branch 的解說顯示，避免與 auto_analyze 觸發的 LLM 解說互相覆蓋。
        """
        turn = len(self.stones)
        if turn > 0 and self.current_node.move:
            x, y, _ = self.current_node.move
            last_move_gtp = self.to_gtp_coord(x, y)
            cached_commentary = get_commentary_from_cache(turn, last_move_gtp)
            if cached_commentary:
                update_teacher_ui(cached_commentary)
            else:
                update_teacher_ui("")
        else:
            # 空盤面，清空解說
            update_teacher_ui("")

# --- 主介面與事件綁定 ---
def save_game_as_json():
    filename = "gameinfo/game.json"
    board.export_as_json(filename)
    status_var.set(t("status.saved_json", path=filename))

def save_game_as_sgf():
    global current_sgf_path, loaded_sgf_overwrite_confirmed

    if not current_sgf_path:
        save_game_as_sgf_dialog()
        return

    if not loaded_sgf_overwrite_confirmed:
        should_overwrite = messagebox.askyesno(
            t("dialog.confirm_title"),
            t("dialog.confirm_overwrite_loaded_sgf", path=current_sgf_path),
        )
        if not should_overwrite:
            return
        loaded_sgf_overwrite_confirmed = True

    board.export_as_sgf(current_sgf_path)
    status_var.set(t("status.saved_sgf", path=current_sgf_path))

def save_game_as_json_dialog():
    filename = filedialog.asksaveasfilename(
        title=t("dialog.save_json_title"),
        defaultextension=".json",
        filetypes=[(t("filetype.json"), "*.json"), (t("filetype.all"), "*.*")]
    )
    if filename:
        board.export_as_json(filename)
        status_var.set(t("status.saved_json", path=filename))

def save_game_as_sgf_dialog():
    global current_sgf_path, loaded_sgf_overwrite_confirmed

    filename = filedialog.asksaveasfilename(
        title=t("dialog.save_sgf_title"),
        defaultextension=".sgf",
        filetypes=[(t("filetype.sgf"), "*.sgf"), (t("filetype.all"), "*.*")]
    )
    if filename:
        board.export_as_sgf(filename)
        current_sgf_path = filename
        loaded_sgf_overwrite_confirmed = True
        status_var.set(t("status.saved_sgf", path=filename))

def on_load_sgf_click():
    global current_sgf_path, loaded_sgf_overwrite_confirmed

    file_path = filedialog.askopenfilename(
        title=t("dialog.load_sgf_title"),
        filetypes=[(t("filetype.sgf"), "*.sgf"), (t("filetype.all"), "*.*")]
    )
    if file_path:
        board.load_sgf(file_path)
        current_sgf_path = file_path
        loaded_sgf_overwrite_confirmed = False
        status_var.set(t("status.loaded_sgf", path=file_path))

def new_game():
    global current_sgf_path, loaded_sgf_overwrite_confirmed, is_playback_mode

    if board.stones and not messagebox.askyesno(t("dialog.new_game_title"), t("dialog.new_game_message")):
        return
    current_sgf_path = None
    loaded_sgf_overwrite_confirmed = False
    # 【修復】新局開始 → 非回放模式
    is_playback_mode = False
    board.root_node = GameNode()
    board.current_node = board.root_node
    board.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    board.current_color = "black"
    board.clear_blue_point()
    board.refresh_display()
    board.on_state_change()
    update_teacher_ui(t("teacher.default_message"))
    status_var.set(t("status.new_game"))

def show_about():
    messagebox.showinfo(t("dialog.about_title"), t("dialog.about_message", version=APP_VERSION))


def summarize_score_estimate(ownership):
    black_territory = 0
    white_territory = 0
    dead_black = 0
    dead_white = 0

    for index, value in enumerate(ownership[: BOARD_SIZE * BOARD_SIZE]):
        if value is None:
            continue
        x = index % BOARD_SIZE
        y = index // BOARD_SIZE
        stone = board.board[y][x]

        if value > 0.5:
            if stone is None:
                black_territory += 1
            elif stone == "white":
                dead_white += 1
        elif value < -0.5:
            if stone is None:
                white_territory += 1
            elif stone == "black":
                dead_black += 1

    return {
        "black_territory": black_territory,
        "white_territory": white_territory,
        "dead_black": dead_black,
        "dead_white": dead_white,
    }


def start_score_analyzer_async(on_ready=None):
    global score_analyzer, score_analyzer_initializing, score_analyzer_ready_callback

    if score_analyzer and not getattr(score_analyzer, "closed", False) and getattr(score_analyzer, "ready_event", None) and score_analyzer.ready_event.is_set():
        if on_ready is not None:
            try:
                root.after(0, on_ready)
            except tk.TclError:
                pass
        return

    if score_analyzer_initializing:
        if on_ready is not None:
            score_analyzer_ready_callback = on_ready
        return

    score_analyzer_initializing = True
    score_analyzer_ready_callback = on_ready

    def finish_success(new_analyzer):
        global score_analyzer, score_analyzer_initializing, score_analyzer_ready_callback
        if is_shutting_down:
            new_analyzer.close(timeout=1)
            return
        score_analyzer = new_analyzer
        score_analyzer_initializing = False
        callback = score_analyzer_ready_callback
        score_analyzer_ready_callback = None
        if callback is not None:
            try:
                root.after(0, callback)
            except tk.TclError:
                pass

    def finish_failure(error):
        global score_analyzer_initializing, score_analyzer_ready_callback, score_query_in_flight, score_estimate_pending_start
        score_analyzer_initializing = False
        score_analyzer_ready_callback = None
        score_query_in_flight = False
        score_estimate_pending_start = False
        if not is_shutting_down:
            status_var.set(t("status.reinit_failed"))
            messagebox.showerror(t("dialog.error_title"), t("dialog.reinit_error", error=str(error)))

    def task():
        try:
            new_analyzer = ScoreAnalyzer()
            while not new_analyzer.ready_event.is_set():
                if is_shutting_down:
                    new_analyzer.close(timeout=1)
                    return
                if new_analyzer.process.poll() is not None:
                    error = new_analyzer.startup_error or t("error.katago_process_exited")
                    raise RuntimeError(error)
                time.sleep(0.1)

            if not is_shutting_down:
                try:
                    root.after(0, finish_success, new_analyzer)
                except tk.TclError:
                    new_analyzer.close(timeout=1)
        except (OSError, ValueError, RuntimeError) as e:
            if not is_shutting_down:
                try:
                    root.after(0, finish_failure, e)
                except tk.TclError:
                    pass

    threading.Thread(target=task, daemon=True).start()


def _handle_score_estimate_result(result):
    global score_query_in_flight, score_estimate_pending_start

    score_query_in_flight = False
    score_estimate_pending_start = False

    if is_shutting_down or not getattr(board, "score_estimate_active", False):
        return

    root_info = result.get("rootInfo", {})
    ownership = root_info.get("ownership") or result.get("ownership") or []
    if not ownership:
        board.clear_score_estimate()
        update_score_estimate_button_label()
        status_var.set(t("status.reinit_failed"))
        return

    score_lead = root_info.get("scoreLead", 0.0)
    summary = summarize_score_estimate(ownership)
    black_total = summary["black_territory"] + summary["dead_white"]
    white_total = summary["white_territory"] + summary["dead_black"]
    komi = 6.5
    net = black_total - white_total - komi
    if net >= 0:
        leader = t("stone.black")
        lead = net
    else:
        leader = t("stone.white")
        lead = -net
    board.score_estimate_data = {
        "ownership": ownership,
        "scoreLead": score_lead,
        "summary": summary,
        "black_total": black_total,
        "white_total": white_total,
        "komi": komi,
        "leader": leader,
        "lead": lead,
    }
    board.refresh_display()
    status_var.set(t("status.score_estimate_ready"))
    update_score_estimate_button_label()
    show_score_estimate_popup(summary, black_total, white_total, komi, leader, lead)


def show_score_estimate_popup(summary, black_total, white_total, komi, leader, lead):
    popup = tk.Toplevel(root)
    popup.title(t("dialog.score_estimate_title"))
    popup.iconbitmap(resource_path("image/logo.ico"))
    popup.resizable(False, False)
    popup.transient(root)

    def close_popup():
        popup.destroy()
        board.clear_score_estimate()
        update_score_estimate_button_label()
        status_var.set(t("status.score_estimate_cancelled"))

    popup.protocol("WM_DELETE_WINDOW", close_popup)

    frame = ttk.Frame(popup, padding=(20, 18, 20, 14))
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text=t("dialog.score_estimate_black",
                            black_total=black_total,
                            black_territory=summary["black_territory"],
                            dead_white=summary["dead_white"]),
              font=("Microsoft JhengHei", 11)).pack(anchor="w", pady=(0, 6))
    ttk.Label(frame, text=t("dialog.score_estimate_white",
                            white_total=white_total,
                            white_territory=summary["white_territory"],
                            dead_black=summary["dead_black"]),
              font=("Microsoft JhengHei", 11)).pack(anchor="w", pady=(0, 6))
    ttk.Label(frame, text=t("dialog.score_estimate_komi", komi=komi),
              font=("Microsoft JhengHei", 10), foreground=TEXT_MUTED).pack(anchor="w", pady=(0, 6))
    ttk.Label(frame, text=t("dialog.score_estimate_lead", leader=leader, lead=lead),
              font=("Microsoft JhengHei", 12, "bold")).pack(anchor="w", pady=(0, 6))
    ttk.Label(frame, text=t("dialog.score_estimate_dead",
                            dead_black=summary["dead_black"], dead_white=summary["dead_white"]),
              font=("Microsoft JhengHei", 10), foreground=TEXT_MUTED).pack(anchor="w", pady=(0, 14))

    ttk.Button(frame, text=t("dialog.score_estimate_ok"), command=close_popup).pack(anchor="center")

    popup.update_idletasks()
    w, h = popup.winfo_reqwidth(), popup.winfo_reqheight()
    x = root.winfo_rootx() + max(40, (root.winfo_width() - w) // 2)
    y = root.winfo_rooty() + max(40, (root.winfo_height() - h) // 2)
    popup.geometry(f"+{x}+{y}")
    popup.grab_set()
    popup.focus_set()


def _wait_for_score_estimate_response():
    try:
        result = score_response_queue.get()
    except Exception:
        result = None
    if result is None or is_shutting_down:
        return
    try:
        root.after(0, _handle_score_estimate_result, result)
    except tk.TclError:
        pass


def _start_score_estimate_query():
    global score_query_in_flight, score_estimate_pending_start

    if is_shutting_down or not score_estimate_pending_start:
        return
    if score_query_in_flight:
        return
    if score_analyzer is None or not getattr(score_analyzer, "ready_event", None) or not score_analyzer.ready_event.is_set():
        return

    score_query_in_flight = True
    board.score_estimate_active = True
    update_score_estimate_button_label()
    status_var.set(t("analysis.score_estimating"))

    query_id = score_analyzer.send_query(
        board.stones,
        analyze_turns=[len(board.stones)],
        response_queue=score_response_queue,
        query_kind="score",
        use_cache=False,
    )
    if query_id is None:
        score_query_in_flight = False
        score_estimate_pending_start = False
        board.clear_score_estimate()
        update_score_estimate_button_label()
        status_var.set(t("status.reinit_failed"))
        return

    threading.Thread(target=_wait_for_score_estimate_response, daemon=True).start()


def on_score_estimate_click():
    global score_estimate_pending_start

    if getattr(board, "score_estimate_active", False):
        on_close_score_estimate_click()
        return

    if score_query_in_flight:
        status_var.set(t("analysis.score_estimating"))
        return

    score_estimate_pending_start = True
    status_var.set(t("analysis.score_estimating"))
    start_score_analyzer_async(on_ready=_start_score_estimate_query)


def on_close_score_estimate_click():
    board.clear_score_estimate()
    update_score_estimate_button_label()
    status_var.set(t("status.score_estimate_cancelled"))

def open_feedback_form():
    try:
        webbrowser.open(FEEDBACK_FORM_URL, new=2)
        status_var.set(t("status.feedback_opened"))
    except Exception as e:
        logger.warning("無法開啟回饋表單: %s", e)
        messagebox.showerror(t("dialog.error_title"), t("dialog.feedback_open_error"))

def show_feedback():
    feedback_win = tk.Toplevel(root)
    feedback_win.title(t("dialog.feedback_title"))
    feedback_win.configure(bg=UI_BG)
    feedback_win.resizable(False, False)
    feedback_win.transient(root)
    feedback_win.iconbitmap(resource_path("image/logo.ico"))
    feedback_win.grab_set()

    outer = tk.Frame(feedback_win, bg=UI_BG, padx=18, pady=18)
    outer.pack(fill="both", expand=True)

    card = tk.Frame(
        outer,
        bg=PANEL_BG,
        highlightbackground=PANEL_BORDER,
        highlightthickness=1,
        padx=18,
        pady=16,
    )
    card.pack(fill="both", expand=True)

    tk.Label(
        card,
        text=t("dialog.feedback_heading"),
        bg=PANEL_BG,
        fg=TEXT_MAIN,
        font=("Microsoft JhengHei", 14, "bold"),
        anchor="w",
    ).pack(fill="x")
    tk.Label(
        card,
        text=t("dialog.feedback_message"),
        bg=PANEL_BG,
        fg=TEXT_MUTED,
        font=("Microsoft JhengHei", 10),
        justify="left",
        wraplength=360,
        anchor="w",
    ).pack(fill="x", pady=(8, 14))

    link_box = tk.Frame(card, bg=TEACHER_TEXT_BG, highlightbackground="#ead7b8", highlightthickness=1, padx=10, pady=8)
    link_box.pack(fill="x", pady=(0, 14))
    tk.Label(
        link_box,
        text=FEEDBACK_FORM_URL,
        bg=TEACHER_TEXT_BG,
        fg=ACCENT_DARK,
        font=("Consolas", 9),
        anchor="w",
    ).pack(fill="x")

    buttons = tk.Frame(card, bg=PANEL_BG)
    buttons.pack(fill="x")
    ttk.Button(
        buttons,
        text=t("button.open_feedback_form"),
        command=open_feedback_form,
        style="Primary.TButton",
    ).pack(side="left")
    ttk.Button(
        buttons,
        text=t("button.close"),
        command=feedback_win.destroy,
        style="Tool.TButton",
    ).pack(side="right")

    feedback_win.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() - feedback_win.winfo_width()) // 2
    y = root.winfo_y() + (root.winfo_height() - feedback_win.winfo_height()) // 2
    feedback_win.geometry(f"+{max(x, 0)}+{max(y, 0)}")

def change_katago_path():
    """選擇 KataGo 執行檔路徑"""
    file_path = filedialog.askopenfilename(
        title=t("dialog.katago_title"),
        filetypes=[(t("filetype.exe"), "*.exe"), (t("filetype.all"), "*.*")]
    )
    if file_path:
        katago_path_mode_var.set("custom")
        katago_path_var.set(file_path)
        reinitialize_analyzer()

def change_model_path():
    """選擇模型檔案路徑"""
    file_path = filedialog.askopenfilename(
        title=t("dialog.model_title"),
        filetypes=[(t("filetype.gz"), "*.gz"), (t("filetype.all"), "*.*")]
    )
    if file_path:
        model_path_mode_var.set("custom")
        model_path_var.set(file_path)
        reinitialize_analyzer()

def change_config_path():
    """選擇配置檔案路徑"""
    file_path = filedialog.askopenfilename(
        title=t("dialog.config_title"),
        filetypes=[(t("filetype.cfg"), "*.cfg"), (t("filetype.all"), "*.*")]
    )
    if file_path:
        config_path_mode_var.set("custom")
        config_path_var.set(file_path)
        reinitialize_analyzer()

def reinitialize_analyzer():
    """重新初始化分析器（關閉舊進程，建立新進程）"""
    for mode_var, path_var, label_key in [
        (katago_path_mode_var, katago_path_var, "label.katago_path"),
        (model_path_mode_var, model_path_var, "label.model_path"),
        (config_path_mode_var, config_path_var, "label.config_path"),
    ]:
        if mode_var.get() == "custom" and not path_var.get().strip():
            messagebox.showerror(
                t("dialog.error_title"),
                t("error.custom_path_required", field=t(label_key).rstrip(":")),
            )
            return False

    start_analyzer_async(show_success=True, replacing=True)
    return True


def update_llm_model_label(provider=None, model=None):
    provider = provider or config_service.get_setting("llm_provider", "ollama")
    if model is None:
        model = ProviderFactory.get_configured_model(config_service, provider)
    provider_name = ProviderFactory.get_display_name(provider)
    model_display = ProviderFactory.get_model_display_name(provider, model)
    llm_model_var.set(f"{model_display}")


# ============== Ollama 模型管理輔助函數 ==============
_ollama_icon_cache = {}


def _load_ollama_icon(icon_name, size=18):
    """直接加載 PNG 圖示（支援快取）"""
    cache_key = (icon_name, size)
    if cache_key in _ollama_icon_cache:
        return _ollama_icon_cache[cache_key]

    icon_path = resource_path(f"image/{icon_name}")
    if not os.path.exists(icon_path):
        _ollama_icon_cache[cache_key] = None
        return None

    try:
        from PIL import Image, ImageTk

        image = Image.open(icon_path)
        # 調整大小
        image = image.resize((size, size), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
    except Exception as e:
        logger.error(f"圖示載入失敗 ({icon_name}): {e}")
        photo = None

    _ollama_icon_cache[cache_key] = photo
    return photo


def detect_ollama_installed(timeout=2):
    """檢查系統是否能執行 `ollama --version`，回傳 (installed: bool, version_or_none)"""
    detection_json = resource_path("tools/ollama_detection.json")
    commands = []
    if os.path.exists(detection_json):
        try:
            with open(detection_json, "r", encoding="utf-8") as fh:
                data = json.load(fh)
                commands = data.get("commands", []) or []
        except Exception:
            commands = []

    # 嘗試使用 JSON 中的命令
    configured_path = config_service.get_setting("ollama_executable_path", None)
    for cmd_spec in commands:
        cmd = list(cmd_spec.get("cmd", []))
        if not cmd:
            continue
        # 若命令包含 {path}，但尚未設定 path，跳過
        cmd_str = " ".join(cmd)
        if "{path}" in cmd_str:
            if not configured_path:
                continue
            cmd = [p.replace("{path}", configured_path) for p in cmd]

        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            if proc.returncode == 0:
                out = (proc.stdout or proc.stderr or "").strip()
                first_line = out.splitlines()[0] if out else ""
                return True, first_line
        except Exception:
            continue

    # 若 JSON 未成功或不存在，再 fallback 嘗試 PATH 中的 ollama
    try:
        proc = subprocess.run(["ollama", "--version"], capture_output=True, text=True, timeout=timeout)
        if proc.returncode == 0:
            out = (proc.stdout or proc.stderr or "").strip()
            first_line = out.splitlines()[0] if out else ""
            return True, first_line
    except Exception:
        pass
    return False, None


def show_ollama_install_dialog(parent):
    """顯示簡單的 Ollama 安裝引導對話框（包含開啟下載頁與重新檢測）。"""
    win = tk.Toplevel(parent)
    win.title(t("dialog.ollama_install_title") if hasattr(t, '__call__') else "Ollama 安裝指南")
    win.geometry("540x420")
    win.iconbitmap(resource_path("image/logo.ico"))
    win.transient(parent)
    win.grab_set()
    frame = tk.Frame(win, bg=PANEL_BG)
    frame.pack(fill="both", expand=True, padx=12, pady=12)

    tk.Label(frame, text=t("dialog.ollama_install_intro") if hasattr(t, '__call__') else "未偵測到 Ollama，請依下列方式安裝：", bg=PANEL_BG, fg=TEXT_MAIN, font=("Microsoft JhengHei", 11, "bold")).pack(anchor="w")

    instructions = (
        "Windows:\n"
        "1) 前往官方下載： https://ollama.com/download\n"
        "2) 下載並執行安裝程式，完成後重新開啟終端或把安裝目錄加入 PATH\n\n"
        "macOS / Linux:\n"
        "請參考官方文件或使用 Docker 映像。\n\n"
        "安裝完成後請按「重新檢測」。"
    )

    txt = tk.Text(frame, height=12, wrap="word", bg="#f8f8f8", fg=TEXT_MAIN)
    txt.pack(fill="both", expand=True, pady=(8, 8))
    txt.insert("end", instructions)
    txt.config(state="disabled")

    btn_frame = tk.Frame(frame, bg=PANEL_BG)
    btn_frame.pack(fill="x", pady=(8, 0))

    def open_download():
        webbrowser.open("https://ollama.com/download")

    def recheck():
        installed, ver = detect_ollama_installed()
        if installed:
            messagebox.showinfo(t("dialog.success_title"), t("dialog.ollama_detected", version=ver) if hasattr(t, '__call__') else f"Ollama 已安裝：{ver}", parent=win)
            win.destroy()
        else:
            messagebox.showwarning(t("dialog.warning_title"), t("dialog.ollama_not_detected") if hasattr(t, '__call__') else "尚未偵測到 Ollama，請完成安裝後再重試。", parent=win)

    ttk.Button(btn_frame, text=t("button.open_download") if hasattr(t, '__call__') else "打開下載頁面", command=open_download).pack(side="left", padx=4)
    ttk.Button(btn_frame, text=t("button.recheck") if hasattr(t, '__call__') else "重新檢測", command=recheck).pack(side="left", padx=4)
    ttk.Button(btn_frame, text=t("button.close") if hasattr(t, '__call__') else "關閉", command=win.destroy).pack(side="right", padx=4)



def _create_ollama_model_row(parent, model_name, provider, model_status, selected_var, refresh_callback, download_success_callback=None):
    """
    為 Ollama 模型創建一個選擇行。
    - 已下載（available）：點擊直接選中
    - 雲端（cloud）：點擊直接選中，不顯示下載
    - 未下載（pending）：點擊彈出下載確認
    
    Args:
        parent: 父 Frame
        model_name: 模型名稱
        provider: OllamaProvider 實例
        model_status: 模型狀態 ('available' 或 'pending')
        selected_var: 選中模型的 StringVar
        refresh_callback: 刷新 UI 的回調函數
    """
    row_frame = tk.Frame(parent, bg=PANEL_BG, relief="flat", bd=0)
    row_frame.pack(fill="x", pady=3)
    is_cloud_model = provider.is_cloud_model(model_name)
    
    # 整行的點擊邏輯
    def on_row_click():
        if model_status in ("available", "cloud") or is_cloud_model:
            # 已下載或雲端模型：直接選中
            selected_var.set(model_name)
        else:
            # 未下載：彈出下載確認
            dialog_parent = parent.winfo_toplevel()
            _confirm_and_download_ollama_model(
                dialog_parent,
                model_name,
                provider,
                refresh_callback,
                on_success=download_success_callback,
            )
    
    # 模型名稱標籤
    model_label = tk.Label(
        row_frame,
        text=ProviderFactory.get_model_display_name("ollama", model_name),
        bg=PANEL_BG,
        fg=TEXT_MAIN,
        font=("Microsoft JhengHei", 10),
        cursor="hand2",
        padx=5,
        pady=5,
    )
    model_label.pack(side="left", fill="x", expand=True)
    model_label.bind("<Button-1>", lambda e: on_row_click())
    
    # 狀態圖示：直接使用 PNG 格式
    if model_status == "cloud" or is_cloud_model:
        icon_name = "cloud.png"
        fallback_text = "☁"
        status_color = "#2196F3"
    elif model_status == "available":
        icon_name = "available.png"
        fallback_text = "✓"
        status_color = "#4CAF50"
    else:
        icon_name = "download.png"
        fallback_text = "⬇"
        status_color = "#FF9800"

    status_icon = _load_ollama_icon(icon_name)
    status_text = "" if status_icon else fallback_text
    
    status_label = tk.Label(
        row_frame,
        text=status_text,
        image=status_icon,
        bg=PANEL_BG,
        fg=status_color,
        font=("Microsoft JhengHei", 12, "bold"),
        width=24,
        cursor="hand2"
    )
    status_label.image = status_icon
    status_label.pack(side="left", padx=(5, 5))
    status_label.bind("<Button-1>", lambda e: on_row_click())


def _download_ollama_model(parent, model_name, provider, refresh_callback, on_success=None):
    if provider.is_cloud_model(model_name):
        return

    model_size = provider.get_model_size(model_name)
    size_text = f" ({model_size})" if model_size else ""

    progress_win = tk.Toplevel(parent)
    progress_win.title(t("dialog.ollama_model_downloading"))
    progress_win.geometry("440x220")
    try:
        progress_win.iconbitmap(resource_path("image/logo.ico"))
    except Exception:
        pass
    progress_win.transient(parent)
    progress_win.configure(bg=PANEL_BG)

    frame = tk.Frame(progress_win, bg=PANEL_BG)
    frame.pack(fill="both", expand=True, padx=15, pady=15)

    tk.Label(
        frame,
        text=t("dialog.ollama_model_downloading_model", model=ProviderFactory.get_model_display_name("ollama", model_name), size=size_text),
        bg=PANEL_BG,
        fg=TEXT_MAIN,
        font=("Microsoft JhengHei", 11, "bold")
    ).pack(anchor="w", pady=(0, 10))

    progress_bar = ttk.Progressbar(frame, mode="indeterminate")
    progress_bar.pack(fill="x", pady=(0, 10))
    progress_bar.start(10)

    status_text = tk.Text(
        frame,
        height=5,
        width=54,
        bg="#f5f5f5",
        fg=TEXT_MAIN,
        font=("Courier New", 9),
        relief="solid",
        bd=1,
        padx=5,
        pady=5
    )
    status_text.pack(fill="both", expand=True, pady=(0, 10))
    status_text.config(state="disabled")

    ttk.Button(
        frame,
        text=t("button.close"),
        command=progress_win.destroy,
        width=12
    ).pack(anchor="e")

    def update_progress(message):
        if not progress_win.winfo_exists():
            return
        status_text.config(state="normal")
        status_text.insert("end", message + "\n")
        status_text.see("end")
        status_text.config(state="disabled")

    def on_download_complete(success, message):
        if not progress_win.winfo_exists():
            if success and on_success:
                on_success(model_name)
            return

        progress_bar.stop()
        update_progress("")
        update_progress(message)

        if success:
            messagebox.showinfo(
                t("dialog.success_title"),
                t("dialog.ollama_model_download_success", model=ProviderFactory.get_model_display_name("ollama", model_name)),
                parent=parent,
            )
            refresh_callback(model_name)
            if on_success:
                on_success(model_name)
            progress_win.destroy()
        else:
            messagebox.showerror(
                t("dialog.error_title"),
                t("dialog.ollama_model_download_failed", model=ProviderFactory.get_model_display_name("ollama", model_name), error=message),
                parent=parent,
            )

    def schedule_ui(callback, *args):
        try:
            if parent.winfo_exists():
                parent.after(0, callback, *args)
            elif root.winfo_exists():
                root.after(0, callback, *args)
        except tk.TclError:
            pass

    started = provider.start_model_download(
        model_name,
        progress_callback=lambda message: schedule_ui(update_progress, message),
        complete_callback=lambda success, message: schedule_ui(on_download_complete, success, message),
    )
    if not started:
        progress_bar.stop()
        update_progress(t("dialog.ollama_model_download_busy"))


def _confirm_and_download_ollama_model(parent, model_name, provider, refresh_callback, on_success=None):
    """
    顯示下載確認對話框並開始下載
    
    Args:
        parent: 父窗口
        model_name: 要下載的模型名稱
        provider: OllamaProvider 實例
        refresh_callback: 下載完成後的刷新回調
    """
    if provider.is_cloud_model(model_name):
        return

    model_size = provider.get_model_size(model_name)
    size_text = f" ({model_size})" if model_size else ""
    
    if not messagebox.askyesno(
        t("dialog.confirm_title"),
        t("dialog.ollama_model_confirm_download", model=model_name + size_text),
        parent=parent,
    ):
        return

    _download_ollama_model(parent, model_name, provider, refresh_callback, on_success=on_success)


# ============== LLM 選擇對話框 ==============
def _show_llm_selection_dialog(parent):
    """建立 LLM 提供商選擇對話框內容。"""
    dialog_win = tk.Toplevel(parent)
    dialog_win.title(t("dialog.llm_selection_title"))
    dialog_win.geometry("540x540")
    dialog_win.minsize(500, 480)
    dialog_win.iconbitmap(resource_path("image/logo.ico"))
    dialog_win.configure(bg=PANEL_BG)
    dialog_win.transient(parent)
    dialog_win.grab_set()
    
    # ===== 讀取當前配置 =====
    current_provider = config_service.get_setting("llm_provider", "ollama")
    current_ollama_model = config_service.get_setting("ollama_model", ProviderFactory.get_default_model("ollama"))
    current_nvidia_model = config_service.get_setting("nvidia_model", ProviderFactory.get_default_model("nvidia"))
    current_github_model = config_service.get_setting("github_model", ProviderFactory.get_default_model("github"))
    current_nvidia_api_key = get_nvidia_api_key()
    current_github_token = get_github_token()
    
    # ===== 狀態變數 =====
    provider_var = tk.StringVar(value=current_provider)
    ollama_model_var_local = tk.StringVar(value=current_ollama_model)
    nvidia_model_var_local = tk.StringVar(
        value=ProviderFactory.get_model_display_name("nvidia", current_nvidia_model)
    )
    github_model_var_local = tk.StringVar(
        value=ProviderFactory.get_model_display_name("github", current_github_model)
    )
    nvidia_api_key_var = tk.StringVar(value=current_nvidia_api_key)
    github_token_var = tk.StringVar(value=current_github_token)
    api_key_visible = tk.BooleanVar(value=False)
    github_token_visible = tk.BooleanVar(value=False)
    
    # ===== 主框架 =====
    main_frame = tk.Frame(dialog_win, bg=PANEL_BG)
    main_frame.pack(fill="both", expand=True, padx=15, pady=15)
    
    # ===== 標題 =====
    tk.Label(
        main_frame,
        text=t("dialog.provider_type"),
        bg=PANEL_BG,
        fg=TEXT_MAIN,
        font=("Microsoft JhengHei", 13, "bold"),
        bd=0,
        padx=0,
        pady=0
    ).pack(anchor="w", pady=(0, 10))
    
    # ===== 提供商選擇 =====
    provider_frame = tk.Frame(main_frame, bg=PANEL_BG)
    provider_frame.pack(fill="x", pady=(0, 20))
    
    radio_style = {
        "bg": PANEL_BG,
        "fg": TEXT_MAIN,
        "activebackground": PANEL_BG,
        "activeforeground": TEXT_MAIN,
        "selectcolor": PANEL_BG,
        "font": ("Microsoft JhengHei", 10),
        "bd": 0,
        "highlightthickness": 0,
    }
    tk.Radiobutton(provider_frame, text=t("dialog.provider_ollama"), variable=provider_var, value="ollama",
                   command=lambda: update_dialog_visibility(), **radio_style).pack(anchor="w")
    tk.Radiobutton(provider_frame, text=t("dialog.provider_nvidia"), variable=provider_var, value="nvidia",
                   command=lambda: update_dialog_visibility(), **radio_style).pack(anchor="w")
    tk.Radiobutton(provider_frame, text=t("dialog.provider_github"), variable=provider_var, value="github",
                   command=lambda: update_dialog_visibility(), **radio_style).pack(anchor="w")
    
    # ===== Ollama 配置區塊 =====
    ollama_frame = tk.LabelFrame(
        main_frame,
        text="Ollama",
        bg=PANEL_BG,
        fg=TEXT_MAIN,
        font=("Microsoft JhengHei", 10, "bold"),
        bd=1,
        relief="solid",
        padx=10,
        pady=10
    )
    ollama_frame.pack(fill="x", pady=(0, 10))
    
    tk.Label(
        ollama_frame,
        text=t("dialog.provider_ollama_model"),
        bg=PANEL_BG,
        fg=TEXT_MAIN,
        font=("Microsoft JhengHei", 10),
        bd=0,
        padx=0,
        pady=0
    ).pack(anchor="w", pady=(0, 8))

    # note: ollama executable path entry removed (use tools/ollama_detection.json or ui_settings.json)
    
    # Ollama 模型列表框（自定義 UI）
    ollama_provider = ProviderFactory.create_provider(
        "ollama",
        ui_callback=lambda x: None,
        translator=t,
        language_getter=lambda: i18n.language
    )
    
    available_models = [
        model
        for model in ProviderFactory.get_available_models("ollama")
        if not ollama_provider.is_paid_model(model)
    ]
    if ollama_provider.is_paid_model(current_ollama_model):
        current_ollama_model = ProviderFactory.get_default_model("ollama")
        ollama_model_var_local.set(current_ollama_model)
    
    # 創建固定高度、可捲動的模型列表，避免只顯示第一列。
    models_list_outer = tk.Frame(ollama_frame, bg=PANEL_BG, relief="solid", bd=1, height=190)
    models_list_outer.pack(fill="x", pady=(0, 8))
    models_list_outer.pack_propagate(False)

    models_canvas = tk.Canvas(
        models_list_outer,
        bg=PANEL_BG,
        bd=0,
        highlightthickness=0,
        height=188,
    )
    models_scrollbar = ttk.Scrollbar(models_list_outer, orient="vertical", command=models_canvas.yview)
    models_list_frame = tk.Frame(models_canvas, bg=PANEL_BG)
    models_window_id = models_canvas.create_window((0, 0), window=models_list_frame, anchor="nw")
    models_canvas.configure(yscrollcommand=models_scrollbar.set)
    models_canvas.pack(side="left", fill="both", expand=True)
    models_scrollbar.pack(side="right", fill="y")

    def update_models_scroll_region(event=None):
        models_canvas.configure(scrollregion=models_canvas.bbox("all"))
        models_canvas.itemconfigure(models_window_id, width=models_canvas.winfo_width())

    models_list_frame.bind("<Configure>", update_models_scroll_region)
    models_canvas.bind("<Configure>", update_models_scroll_region)
    
    def refresh_ollama_models(auto_select_model=None):
        """刷新 Ollama 模型列表"""
        # 清空舊的模型行
        for widget in models_list_frame.winfo_children():
            widget.destroy()
        
        # 重新創建模型行
        updated_status = ollama_provider.get_model_status()
        for model in available_models:
            if ollama_provider.is_paid_model(model):
                continue
            _create_ollama_model_row(
                models_list_frame,
                model,
                ollama_provider,
                updated_status.get(model, "pending"),
                ollama_model_var_local,
                refresh_ollama_models,
                download_success_callback=lambda downloaded_model: save_and_apply_settings("ollama", downloaded_model)
            )
        
        # 如果提供了自動選擇的模型，則選中它
        if auto_select_model:
            ollama_model_var_local.set(auto_select_model)
        update_models_scroll_region()
    
    # 初始創建模型行
    refresh_ollama_models()
    
    # 添加重新掃描按鈕
    rescan_frame = tk.Frame(ollama_frame, bg=PANEL_BG)
    rescan_frame.pack(fill="x", pady=(0, 0))
    
    ttk.Button(
        rescan_frame,
        text=t("button.rescan_models"),
        command=refresh_ollama_models,
        width=15
    ).pack(side="left", padx=(0, 5))

    # 模型選擇指示（顯示目前被選中的模型）
    try:
        selected_indicator = tk.Label(
            rescan_frame,
            text=t("status.ollama_model_selected", model=ProviderFactory.get_model_display_name("ollama", current_ollama_model)),
            bg=PANEL_BG,
            fg=TEXT_MUTED,
            font=("Microsoft JhengHei", 9)
        )

        def update_selected_indicator(*args):
            try:
                selected_indicator.config(
                    text=t(
                        "status.ollama_model_selected",
                        model=ProviderFactory.get_model_display_name("ollama", ollama_model_var_local.get()),
                    )
                )
            except Exception:
                pass

        ollama_model_var_local.trace("w", update_selected_indicator)
    except Exception:
        # 如果變數或元件不存在，忽略以避免啟動錯誤
        pass
    
    # Ollama 安裝狀態顯示與安裝指南按鈕
    try:
        ollama_install_status_label = tk.Label(
            rescan_frame,
            text="",
            bg=PANEL_BG,
            fg=TEXT_MUTED,
            font=("Microsoft JhengHei", 9)
        )

        def update_ollama_install_status_label():
            installed, ver = detect_ollama_installed()
            ver = ver.replace("ollama version is", "").strip() if ver else ""
            if installed:
                ollama_install_status_label.config(text=f"Ollama: {ver}", fg="#1f6f78")
            else:
                ollama_install_status_label.config(text=t("status.ollama_not_found") if hasattr(t, '__call__') else "Ollama: 未偵測", fg="#FF5722")

        # 把安裝按鈕放在左側，狀態標籤填滿剩餘空間
        ollama_install_button = ttk.Button(rescan_frame, text=t("button.install_guide") if hasattr(t, '__call__') else "安裝指南", width=12, command=lambda: show_ollama_install_dialog(rescan_frame))
        ollama_install_button.pack(side="left", padx=(6, 5))

        # 現在把先前建立但未 pack 的 selected_indicator 放到左側並擴展
        try:
            selected_indicator.pack(side="left", fill="x", expand=True)
        except Exception:
            pass

        ollama_install_status_label.pack(side="left", padx=(8, 0))

        # 立即檢測一次並更新狀態
        try:
            update_ollama_install_status_label()
        except Exception:
            pass
    except Exception:
        pass
    
    # ===== NVIDIA 配置區塊 =====
    nvidia_frame = tk.LabelFrame(
        main_frame,
        text="NVIDIA",
        bg=PANEL_BG,
        fg=TEXT_MAIN,
        font=("Microsoft JhengHei", 10, "bold"),
        bd=1,
        relief="solid",
        padx=10,
        pady=10
    )
    
    # API Key 部分
    tk.Label(
        nvidia_frame,
        text=t("dialog.provider_nvidia_api_key"),
        bg=PANEL_BG,
        fg=TEXT_MAIN,
        font=("Microsoft JhengHei", 10),
        bd=0,
        padx=0,
        pady=0
    ).pack(anchor="w", pady=(0, 5))
    api_key_frame = tk.Frame(nvidia_frame, bg=PANEL_BG)
    api_key_frame.pack(fill="x", pady=(0, 10))
    
    nvidia_api_key_entry = ttk.Entry(
        api_key_frame,
        textvariable=nvidia_api_key_var,
        show="●",
        width=35
    )
    nvidia_api_key_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
    
    def toggle_api_key_visibility():
        api_key_visible.set(not api_key_visible.get())
        if api_key_visible.get():
            nvidia_api_key_entry.config(show="")
            toggle_btn.config(text="◉")
        else:
            nvidia_api_key_entry.config(show="●")
            toggle_btn.config(text="◌")
    
    toggle_btn = ttk.Button(api_key_frame, text="◌", width=3, command=toggle_api_key_visibility)
    toggle_btn.pack(side="left")
    
    tk.Label(
        nvidia_frame,
        text=t("dialog.provider_api_key_env_hint"),
        bg=PANEL_BG,
        fg=TEXT_MUTED,
        font=("Microsoft JhengHei", 8),
        wraplength=400,
        justify="left",
        bd=0,
        padx=0,
        pady=0
    ).pack(anchor="w", pady=(0, 10))
    
    # 模型選擇部分
    tk.Label(
        nvidia_frame,
        text=t("dialog.provider_nvidia_model"),
        bg=PANEL_BG,
        fg=TEXT_MAIN,
        font=("Microsoft JhengHei", 10),
        bd=0,
        padx=0,
        pady=0
    ).pack(anchor="w", pady=(0, 5))
    nvidia_model_combo = ttk.Combobox(
        nvidia_frame,
        textvariable=nvidia_model_var_local,
        values=[name for name, _ in ProviderFactory.get_available_models_with_names("nvidia")],
        state="readonly",
        width=40
    )
    nvidia_model_combo.pack(fill="x", pady=(0, 10))

    # ===== GitHub Models 配置區塊 =====
    github_frame = tk.LabelFrame(
        main_frame,
        text="GitHub Models",
        bg=PANEL_BG,
        fg=TEXT_MAIN,
        font=("Microsoft JhengHei", 10, "bold"),
        bd=1,
        relief="solid",
        padx=10,
        pady=10
    )

    tk.Label(
        github_frame,
        text=t("dialog.provider_github_token"),
        bg=PANEL_BG,
        fg=TEXT_MAIN,
        font=("Microsoft JhengHei", 10),
        bd=0,
        padx=0,
        pady=0
    ).pack(anchor="w", pady=(0, 5))
    github_token_frame = tk.Frame(github_frame, bg=PANEL_BG)
    github_token_frame.pack(fill="x", pady=(0, 10))

    github_token_entry = ttk.Entry(
        github_token_frame,
        textvariable=github_token_var,
        show="●",
        width=35
    )
    github_token_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

    def toggle_github_token_visibility():
        github_token_visible.set(not github_token_visible.get())
        if github_token_visible.get():
            github_token_entry.config(show="")
            github_toggle_btn.config(text="◉")
        else:
            github_token_entry.config(show="●")
            github_toggle_btn.config(text="◌")

    github_toggle_btn = ttk.Button(github_token_frame, text="◌", width=3, command=toggle_github_token_visibility)
    github_toggle_btn.pack(side="left")

    tk.Label(
        github_frame,
        text=t("dialog.provider_github_token_env_hint"),
        bg=PANEL_BG,
        fg=TEXT_MUTED,
        font=("Microsoft JhengHei", 8),
        wraplength=420,
        justify="left",
        bd=0,
        padx=0,
        pady=0
    ).pack(anchor="w", pady=(0, 10))

    tk.Label(
        github_frame,
        text=t("dialog.provider_github_model"),
        bg=PANEL_BG,
        fg=TEXT_MAIN,
        font=("Microsoft JhengHei", 10),
        bd=0,
        padx=0,
        pady=0
    ).pack(anchor="w", pady=(0, 5))
    github_model_combo = ttk.Combobox(
        github_frame,
        textvariable=github_model_var_local,
        values=[name for name, _ in ProviderFactory.get_available_models_with_names("github")],
        state="readonly",
        width=40
    )
    github_model_combo.pack(fill="x", pady=(0, 10))
    
    # ===== 更新對話框可見性 =====
    def update_dialog_visibility():
        if provider_var.get() == "ollama":
            ollama_frame.pack(fill="x", pady=(0, 10))
            nvidia_frame.pack_forget()
            github_frame.pack_forget()
        elif provider_var.get() == "nvidia":
            ollama_frame.pack_forget()
            nvidia_frame.pack(fill="x", pady=(0, 10))
            github_frame.pack_forget()
        else:
            ollama_frame.pack_forget()
            nvidia_frame.pack_forget()
            github_frame.pack(fill="x", pady=(0, 10))
    
    update_dialog_visibility()
    
    # ===== 按鈕 =====
    button_frame = tk.Frame(main_frame, bg=PANEL_BG)
    button_frame.pack(fill="x", pady=(20, 0))
    
    def save_and_apply_settings(provider, selected_model, api_key=None, github_token=None):
        config_service.set_setting("llm_provider", provider)
        if provider == "ollama":
            config_service.set_setting("ollama_model", selected_model)
        elif provider == "nvidia":
            config_service.set_setting("nvidia_model", selected_model)
            try:
                set_nvidia_api_key(api_key)
            except Exception as e:
                logger.error("NVIDIA API Key 寫入 keyring 失敗: %s", e)
                messagebox.showerror(t("dialog.error_title"), str(e), parent=dialog_win)
                return False
        else:
            config_service.set_setting("github_model", selected_model)
            try:
                set_github_token(github_token)
            except Exception as e:
                logger.error("GitHub token 寫入 keyring 失敗: %s", e)
                messagebox.showerror(t("dialog.error_title"), str(e), parent=dialog_win)
                return False

        config_service.save()

        global current_llm_worker, ollama_worker
        current_llm_worker = ProviderFactory.create_provider(
            provider,
            ui_callback=update_teacher_ui,
            status_callback=update_status,
            model_name=selected_model,
            translator=t,
            language_getter=lambda: i18n.language,
            on_complete_callback=on_commentary_generation_complete,
            tone=config_service.get_llm_tone("friendly"),
            custom_prompt=config_service.get_custom_prompt(""),
        )
        provider_name = ProviderFactory.get_display_name(provider)
        model_display = ProviderFactory.get_model_display_name(provider, selected_model)
        status_var.set(t("status.llm_provider_switched", provider=provider_name, model=model_display))
        update_llm_model_label(provider, selected_model)
        ollama_worker = current_llm_worker
        update_teacher_ui(t("teacher.default_message"))
        return True

    def apply_settings():
        provider = provider_var.get()
        api_key = None
        github_token = None
        selected_model = None
        
        if provider == "nvidia":
            api_key = normalize_api_key(nvidia_api_key_var.get())
            if not api_key:
                messagebox.showerror(t("dialog.error_title"), t("error.nvidia_api_key_empty"), parent=dialog_win)
                return
            # Combobox shows display name — map back to model ID for validation/storage
            selected_display = nvidia_model_var_local.get()
            model_id = ProviderFactory.get_model_id_by_display_name("nvidia", selected_display) or selected_display
            validator = ProviderFactory.create_provider(
                "nvidia",
                ui_callback=update_teacher_ui,
                model_name=model_id,
                translator=t,
                language_getter=lambda: i18n.language,
                api_key=api_key
            )
            is_valid, error_message = validator.validate_config()
            if not is_valid:
                messagebox.showwarning(t("dialog.error_title"), error_message or t("error.nvidia_api_key_invalid"), parent=dialog_win)
                return
            selected_model = model_id
        elif provider == "github":
            github_token = normalize_api_key(github_token_var.get())
            if not github_token:
                messagebox.showerror(t("dialog.error_title"), t("error.github_token_empty"), parent=dialog_win)
                return
            # Combobox shows display name — map back to model ID for validation/storage
            selected_display = github_model_var_local.get()
            model_id = ProviderFactory.get_model_id_by_display_name("github", selected_display) or selected_display
            validator = ProviderFactory.create_provider(
                "github",
                ui_callback=update_teacher_ui,
                model_name=model_id,
                translator=t,
                language_getter=lambda: i18n.language,
                api_key=github_token
            )
            is_valid, error_message = validator.validate_config()
            if not is_valid:
                messagebox.showwarning(t("dialog.error_title"), error_message or t("error.github_token_invalid"), parent=dialog_win)
                return
            selected_model = model_id
        else:
            selected_model = ollama_model_var_local.get()
            if ollama_provider.is_paid_model(selected_model):
                selected_model = ProviderFactory.get_default_model("ollama")
                ollama_model_var_local.set(selected_model)
            if not ollama_provider.is_cloud_model(selected_model) and not ollama_provider.is_model_available(selected_model):
                choice = messagebox.askyesnocancel(
                    t("dialog.confirm_title"),
                    t("dialog.ollama_model_missing_prompt", model=ProviderFactory.get_model_display_name("ollama", selected_model)),
                    parent=dialog_win,
                )
                if choice is None:
                    return
                if choice:
                    _download_ollama_model(
                        dialog_win,
                        selected_model,
                        ollama_provider,
                        refresh_ollama_models,
                        on_success=lambda downloaded_model: (
                            save_and_apply_settings("ollama", downloaded_model) and dialog_win.destroy()
                        ),
                    )
                    return
                # If the user chooses No, keep the old behavior: save anyway.

        if save_and_apply_settings(provider, selected_model, api_key=api_key, github_token=github_token):
            dialog_win.destroy()
    
    ttk.Button(button_frame, text=t("button.apply"), command=apply_settings, width=12).pack(side="right", padx=(5, 0))
    ttk.Button(button_frame, text=t("button.cancel"), command=dialog_win.destroy, width=12).pack(side="right")


class LLMSelectionDialog:
    """通用 LLM 提供商與模型選擇對話框。"""
    def __init__(self, parent):
        self.parent = parent
        _show_llm_selection_dialog(parent)


def show_llm_selection_dialog():
    """顯示 LLM 提供商選擇對話框"""
    LLMSelectionDialog(root)


def set_llm_tone(tone: str):
    """設定 LLM 回應語氣"""
    from providers import tone_templates
    
    config_service.set_llm_tone(tone)
    config_service.save()
    
    tone_name = tone_templates.TONE_DISPLAY_NAMES.get(tone, tone)
    status_var.set(t("status.tone_changed", tone=tone_name))
    
    # 更新全局 provider 實例的語氣（如果存在）
    try:
        if hasattr(analyzer, 'provider') and analyzer.provider:
            analyzer.provider.set_tone(tone)
    except Exception as e:
        print(f"更新提供商語氣失敗: {e}")


def _format_bytes_as_gb(byte_count):
    """把位元組數轉成 GB 字串；輸入不可用時回傳 Unknown。"""
    try:
        value = float(byte_count)
        if value < 0:
            return "Unknown"
        return f"{value / (1024 ** 3):.1f} GB"
    except Exception:
        logger.exception("記憶體容量格式化失敗: %r", byte_count)
        return "Unknown"


def _run_powershell_json(command, timeout=5):
    """執行 PowerShell 並解析 JSON，失敗時回傳 None。

    這裡只用於診斷資訊的 best-effort 查詢，任何錯誤都不能影響主 UI。
    """
    try:
        creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-Command", command],
            capture_output=True,
            text=True,
            timeout=timeout,
            creationflags=creationflags,
        )
        if proc.returncode != 0:
            logger.warning("PowerShell 診斷查詢失敗: %s", (proc.stderr or proc.stdout or "").strip())
            return None
        output = (proc.stdout or "").strip()
        if not output:
            return None
        return json.loads(output)
    except Exception:
        logger.exception("PowerShell 診斷查詢例外")
        return None


def _get_windows_display_version(build_number):
    """根據 Windows build 推估 Windows 顯示版本。"""
    try:
        build_int = int(build_number)
        if build_int >= 22000:
            return "Windows 11"
        if build_int > 0:
            return "Windows 10"
    except Exception:
        logger.exception("Windows build 解析失敗: %r", build_number)
    return platform.platform() or "Unknown"


def _get_cpu_name():
    """取得 CPU 名稱；Windows 優先使用 CIM，失敗再回落到 platform。"""
    data = _run_powershell_json(
        "Get-CimInstance Win32_Processor | Select-Object -First 1 Name | ConvertTo-Json -Compress"
    )
    try:
        if isinstance(data, dict) and data.get("Name"):
            return str(data["Name"]).strip()
    except Exception:
        logger.exception("CPU 名稱解析失敗")

    try:
        return platform.processor() or os.environ.get("PROCESSOR_IDENTIFIER") or "Unknown"
    except Exception:
        logger.exception("CPU fallback 查詢失敗")
        return "Unknown"


def _get_physical_core_count():
    """取得實體核心數；CIM 失敗時以 Unknown 表示。"""
    data = _run_powershell_json(
        "Get-CimInstance Win32_Processor | Select-Object -First 1 NumberOfCores | ConvertTo-Json -Compress"
    )
    try:
        if isinstance(data, dict) and data.get("NumberOfCores") is not None:
            return str(data["NumberOfCores"])
    except Exception:
        logger.exception("CPU 核心數解析失敗")
    return "Unknown"


def _get_ram_info():
    """使用 Win32 GlobalMemoryStatusEx 取得 RAM 資訊。"""
    info = {"total": "Unknown", "available": "Unknown", "used": "Unknown"}

    try:
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        status = MEMORYSTATUSEX()
        status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
            logger.warning("GlobalMemoryStatusEx 回傳失敗")
            return info

        used = max(status.ullTotalPhys - status.ullAvailPhys, 0)
        info["total"] = _format_bytes_as_gb(status.ullTotalPhys)
        info["available"] = _format_bytes_as_gb(status.ullAvailPhys)
        info["used"] = _format_bytes_as_gb(used)
    except Exception:
        logger.exception("RAM 資訊取得失敗")

    return info


def _get_gpu_info():
    """取得第一張 GPU 的名稱與記憶體；不可用時回傳 Unknown。"""
    result = {"name": "Unknown", "memory": "Unknown"}
    data = _run_powershell_json(
        "Get-CimInstance Win32_VideoController | "
        "Select-Object -First 1 Name,AdapterRAM | ConvertTo-Json -Compress"
    )
    try:
        if isinstance(data, list) and data:
            data = data[0]
        if isinstance(data, dict):
            result["name"] = str(data.get("Name") or "Unknown").strip() or "Unknown"
            adapter_ram = data.get("AdapterRAM")
            if adapter_ram is not None:
                result["memory"] = _format_bytes_as_gb(adapter_ram)
    except Exception:
        logger.exception("GPU 資訊解析失敗")
    return result


def safe_get_system_info():
    """安全收集系統資訊，任何欄位失敗都不會讓 UI 崩潰。"""
    info = {
        "windows_version": "Unknown",
        "windows_build": "Unknown",
        "machine_type": "Unknown",
        "cpu_name": "Unknown",
        "cpu_core_count": "Unknown",
        "logical_processor_count": "Unknown",
        "total_ram": "Unknown",
        "available_ram": "Unknown",
        "used_ram": "Unknown",
        "gpu_name": "Unknown",
        "gpu_memory": "Unknown",
        "python": "Unknown",
    }

    try:
        version_parts = platform.version().split(".")
        build = version_parts[2] if len(version_parts) >= 3 else "Unknown"
        info["windows_version"] = _get_windows_display_version(build)
        info["windows_build"] = f"Build {build}" if build != "Unknown" else "Unknown"
    except Exception:
        logger.exception("Windows 版本資訊取得失敗")

    try:
        info["machine_type"] = platform.machine() or "Unknown"
    except Exception:
        logger.exception("Machine Type 取得失敗")

    info["cpu_name"] = _get_cpu_name()
    info["cpu_core_count"] = _get_physical_core_count()
    try:
        info["logical_processor_count"] = str(os.cpu_count() or "Unknown")
    except Exception:
        logger.exception("邏輯處理器數量取得失敗")

    ram_info = _get_ram_info()
    info["total_ram"] = ram_info["total"]
    info["available_ram"] = ram_info["available"]
    info["used_ram"] = ram_info["used"]

    gpu_info = _get_gpu_info()
    info["gpu_name"] = gpu_info["name"]
    info["gpu_memory"] = gpu_info["memory"]

    try:
        info["python"] = sys.version.replace("\n", " ")
    except Exception:
        logger.exception("Python 版本資訊取得失敗")

    return info


def safe_get_katago_info():
    """安全取得 KataGo 執行檔、設定檔、模型檔路徑與存在狀態。"""
    items = [
        ("executable", "KataGo Executable", get_katago_path, DEFAULT_KATAGO_PATH),
        ("config", "Config", get_config_path, DEFAULT_CONFIG_PATH),
        ("model", "Model", get_model_path, DEFAULT_MODEL_PATH),
    ]
    info = {}
    for key, label, getter, fallback in items:
        path = fallback
        exists = False
        try:
            path = getter() or fallback
            exists = os.path.exists(path)
        except Exception:
            logger.exception("%s 路徑檢查失敗", label)
        info[key] = {
            "label": label,
            "path": os.path.abspath(path) if path else "Unknown",
            "filename": os.path.basename(path) if path else fallback,
            "exists": bool(exists),
        }
    return info


def safe_get_ai_config():
    """安全取得目前 AI 提供商、模型與語言設定。"""
    config = {"provider": "Unknown", "model": "Unknown", "language": "Unknown"}
    try:
        provider_id = config_service.get_setting("llm_provider", "ollama")
        config["provider"] = ProviderFactory.get_display_name(provider_id)
        config["model"] = ProviderFactory.get_configured_model(config_service, provider_id)
    except Exception:
        logger.exception("AI Provider/Model 設定取得失敗")
    try:
        config["language"] = i18n.language
    except Exception:
        logger.exception("語言設定取得失敗")
    return config


def _create_labeled_row(parent, row, label, value, value_font=None):
    """建立診斷資訊視窗中的單列 label/value。"""
    ttk.Label(parent, text=label, style="Panel.TLabel").grid(row=row, column=0, sticky="nw", padx=(0, 16), pady=3)
    ttk.Label(
        parent,
        text=value,
        style="Panel.TLabel",
        font=value_font or ("Microsoft JhengHei", 10),
        wraplength=460,
        justify="left",
    ).grid(row=row, column=1, sticky="nw", pady=3)


def _create_info_section(parent, title, rows):
    """建立系統資訊視窗中的群組區塊。"""
    frame = ttk.LabelFrame(parent, text=title, padding=(12, 8, 12, 10))
    frame.pack(fill="x", padx=14, pady=(10, 0))
    frame.columnconfigure(1, weight=1)
    for index, (label, value) in enumerate(rows):
        _create_labeled_row(parent=frame, row=index, label=label, value=value)
    return frame








def setup_system_info_styles():
    style = ttk.Style()

    bg = style.lookup("TFrame", "background")

    style.configure(
        "InfoCard.TLabelframe",
        padding=10
    )

    style.configure(
        "InfoCard.TLabelframe.Label",
        font=("Segoe UI", 10, "bold")
    )

    style.configure(
        "InfoKey.TLabel",
        font=("Segoe UI", 9, "bold"),
        foreground="#555555"
    )

    style.configure(
        "InfoValue.TLabel",
        font=("Segoe UI", 9)
    )

    style.configure(
        "Success.TLabel",
        foreground="#0A9D4D",
        font=("Segoe UI", 9, "bold")
    )

    style.configure(
        "Error.TLabel",
        foreground="#D13438",
        font=("Segoe UI", 9, "bold")
    )

    style.configure(
        "HeaderTitle.TLabel",
        font=("Segoe UI", 16, "bold")
    )

    style.configure(
        "HeaderSub.TLabel",
        font=("Segoe UI", 9)
    )


def _create_info_section(parent, section_title, rows):

    frame = ttk.LabelFrame(
        parent,
        text=f" {section_title} ",
        style="InfoCard.TLabelframe"
    )

    frame.pack(
        fill="x",
        padx=8,
        pady=6
    )

    frame.columnconfigure(1, weight=1)

    for row_idx, (key, value) in enumerate(rows):

        ttk.Label(
            frame,
            text=key,
            style="InfoKey.TLabel"
        ).grid(
            row=row_idx,
            column=0,
            sticky="w",
            padx=(0, 25),
            pady=5
        )

        ttk.Label(
            frame,
            text=value,
            style="InfoValue.TLabel"
        ).grid(
            row=row_idx,
            column=1,
            sticky="ew",
            pady=5
        )


def _create_katago_section(parent, katago_info):

    frame = ttk.LabelFrame(
        parent,
        text=" KataGo 引擎狀態 ",
        style="InfoCard.TLabelframe"
    )

    frame.pack(
        fill="x",
        padx=8,
        pady=6
    )

    frame.columnconfigure(1, weight=1)

    for row, key in enumerate(("executable", "config", "model")):

        item = katago_info[key]

        ttk.Label(
            frame,
            text=item["label"],
            style="InfoKey.TLabel"
        ).grid(
            row=row,
            column=0,
            sticky="w",
            padx=(0, 25),
            pady=5
        )

        exists = item["exists"]

        ttk.Label(
            frame,
            text=f"{'✓' if exists else '✗'} {item['filename']}",
            style="Success.TLabel" if exists else "Error.TLabel"
        ).grid(
            row=row,
            column=1,
            sticky="w",
            pady=5
        )


def show_system_info_dialog():

    try:

        setup_system_info_styles()

        system_info = safe_get_system_info()
        katago_info = safe_get_katago_info()

        win = tk.Toplevel(root)

        win.title(t("dialog.system_info_title"))
        win.geometry("720x760")
        win.minsize(640, 600)

        win.iconbitmap(
            resource_path("image/logo.ico")
        )

        win.transient(root)
        win.grab_set()

        style = ttk.Style()

        bg = style.lookup("TFrame", "background")

        canvas = tk.Canvas(
            win,
            bg=bg,
            highlightthickness=0,
            borderwidth=0
        )

        scrollbar = ttk.Scrollbar(
            win,
            orient="vertical",
            command=canvas.yview
        )

        container = ttk.Frame(
            canvas,
            padding=20
        )

        container_id = canvas.create_window(
            (0, 0),
            window=container,
            anchor="nw"
        )

        def on_frame_configure(event):
            canvas.configure(
                scrollregion=canvas.bbox("all")
            )

        def on_canvas_configure(event):
            canvas.itemconfig(
                container_id,
                width=event.width
            )

        container.bind(
            "<Configure>",
            on_frame_configure
        )

        canvas.bind(
            "<Configure>",
            on_canvas_configure
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        def mousewheel(event):
            canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        canvas.bind_all(
            "<MouseWheel>",
            mousewheel
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        # =====================
        # Header
        # =====================

        ttk.Label(
            container,
            text="🖥 系統資訊與診斷",
            style="HeaderTitle.TLabel"
        ).pack(
            anchor="w"
        )

        ttk.Label(
            container,
            text="Developer Tools • 系統環境檢查 • KataGo 診斷",
            style="HeaderSub.TLabel"
        ).pack(
            anchor="w",
            pady=(0, 15)
        )

        ttk.Separator(
            container,
            orient="horizontal"
        ).pack(
            fill="x",
            pady=(0, 10)
        )

        _create_info_section(
            container,
            "作業系統",
            [
                ("Windows Version", system_info["windows_version"]),
                ("Windows Build", system_info["windows_build"]),
                ("Machine Type", system_info["machine_type"]),
            ]
        )

        _create_info_section(
            container,
            "中央處理器 (CPU)",
            [
                ("CPU Name", system_info["cpu_name"]),
                ("CPU Core Count", system_info["cpu_core_count"]),
                ("Logical Processor Count", system_info["logical_processor_count"]),
            ]
        )

        _create_info_section(
            container,
            "記憶體 (RAM)",
            [
                ("Total RAM", system_info["total_ram"]),
                ("Available RAM", system_info["available_ram"]),
                ("Used RAM", system_info["used_ram"]),
            ]
        )

        _create_info_section(
            container,
            "顯示卡 (GPU)",
            [
                ("GPU Name", system_info["gpu_name"]),
                ("GPU Memory", system_info["gpu_memory"]),
            ]
        )

        _create_katago_section(
            container,
            katago_info
        )

        separator = ttk.Separator(
            win,
            orient="horizontal"
        )

        separator.pack(
            side="bottom",
            fill="x"
        )

        button_frame = ttk.Frame(
            win,
            padding=(15, 10)
        )

        button_frame.pack(
            side="bottom",
            fill="x"
        )

        ttk.Button(
            button_frame,
            text=t("button.close"),
            width=12,
            command=win.destroy
        ).pack(
            side="right"
        )

    except Exception:
        logger.exception("系統資訊視窗建立失敗")
        messagebox.showerror(
            t("dialog.error_title"),
            t("dialog.system_info_error")
        )


def _iter_log_candidates():
    """依需求順序列出可附加到診斷報告的 log 目錄。"""
    yield os.path.join(get_runtime_data_root(), "logs")
    if is_frozen_app():
        yield os.path.join(get_runtime_data_root(), "logs", "analysis_logs")
    else:
        yield os.path.join(get_runtime_data_root(), "analysis_logs")


def _get_newest_log_file():
    """取得候選 log 目錄中最新的檔案。"""
    for directory in _iter_log_candidates():
        try:
            if not os.path.isdir(directory):
                continue
            files = [
                os.path.join(directory, name)
                for name in os.listdir(directory)
                if os.path.isfile(os.path.join(directory, name))
            ]
            if files:
                return max(files, key=os.path.getmtime)
        except Exception:
            logger.exception("讀取 log 目錄失敗: %s", directory)
    return None


def _read_recent_log_lines(max_lines=100):
    """讀取最新 log 的最後 max_lines 行；沒有 log 時回傳提示文字。"""
    log_path = _get_newest_log_file()
    if not log_path:
        return "No log file found"

    try:
        with open(log_path, "r", encoding="utf-8", errors="replace") as fh:
            lines = fh.readlines()
        tail = "".join(lines[-max_lines:]).rstrip()
        return f"Log File: {log_path}\n\n{tail}" if tail else f"Log File: {log_path}\n\n"
    except Exception:
        logger.exception("讀取最新 log 檔失敗: %s", log_path)
        return f"Failed to read log file: {log_path}"


def _build_diagnostic_report_text():
    """組合 diagnostic_report.txt 的完整內容。"""
    system_info = safe_get_system_info()
    katago_info = safe_get_katago_info()
    ai_config = safe_get_ai_config()
    build_time = time.strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        "Application",
        "===========",
        f"Version: {APP_VERSION}",
        f"Build Time: {build_time}",
        "",
        "System",
        "======",
        f"OS: {system_info['windows_version']} ({system_info['windows_build']}) {system_info['machine_type']}",
        f"Python: {system_info['python']}",
        f"CPU: {system_info['cpu_name']} / Cores: {system_info['cpu_core_count']} / Logical: {system_info['logical_processor_count']}",
        f"RAM: Total {system_info['total_ram']} / Available {system_info['available_ram']} / Used {system_info['used_ram']}",
        f"GPU: {system_info['gpu_name']} / Memory: {system_info['gpu_memory']}",
        "",
        "KataGo",
        "======",
        f"Executable Path: {katago_info['executable']['path']}",
        f"Exists: {katago_info['executable']['exists']}",
        f"Config Path: {katago_info['config']['path']}",
        f"Exists: {katago_info['config']['exists']}",
        f"Model Path: {katago_info['model']['path']}",
        f"Exists: {katago_info['model']['exists']}",
        "",
        "AI Configuration",
        "================",
        f"Provider: {ai_config['provider']}",
        f"Model: {ai_config['model']}",
        f"Language: {ai_config['language']}",
        "",
        "Recent Logs",
        "===========",
        _read_recent_log_lines(100),
        "",
    ]
    return "\n".join(lines)


def _open_folder(path):
    """開啟資料夾，失敗時記錄並顯示錯誤。"""
    try:
        if os.name == "nt" and hasattr(os, "startfile"):
            os.startfile(path)
        else:
            webbrowser.open(path)
    except Exception:
        logger.exception("開啟資料夾失敗: %s", path)
        messagebox.showerror(t("dialog.error_title"), t("dialog.open_folder_error"))


def _show_diagnostic_export_success(report_path, diagnostics_dir):
    """顯示診斷報告匯出完成訊息與開啟資料夾按鈕。"""
    win = tk.Toplevel(root)
    win.title(t("dialog.diagnostics_exported_title"))
    win.resizable(False, False)
    win.iconbitmap(resource_path("image/logo.ico"))
    win.transient(root)
    win.grab_set()

    frame = ttk.Frame(win, padding=(22, 18, 22, 18))
    frame.pack(fill="both", expand=True)

    ttk.Label(
        frame,
        text=t("dialog.diagnostics_exported_message"),
        font=("Microsoft JhengHei", 12, "bold"),
        justify="center",
    ).pack(fill="x")
    ttk.Label(
        frame,
        text="diagnostics/diagnostic_report.txt",
        font=("Consolas", 10),
        justify="center",
    ).pack(fill="x", pady=(8, 18))

    button_frame = ttk.Frame(frame)
    button_frame.pack(fill="x")
    ttk.Button(
        button_frame,
        text=t("button.open_folder"),
        command=lambda: _open_folder(diagnostics_dir),
        style="Primary.TButton",
    ).pack(side="left")
    ttk.Button(button_frame, text=t("button.close"), command=win.destroy).pack(side="right")

    win.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() - win.winfo_width()) // 2
    y = root.winfo_y() + (root.winfo_height() - win.winfo_height()) // 2
    win.geometry(f"+{max(x, 0)}+{max(y, 0)}")


def export_diagnostic_report():
    """匯出診斷報告到 diagnostics/diagnostic_report.txt。"""
    try:
        diagnostics_dir = os.path.join(get_runtime_data_root(), "diagnostics")
        try:
            os.makedirs(diagnostics_dir, exist_ok=True)
        except Exception:
            logger.exception("建立 diagnostics 資料夾失敗: %s", diagnostics_dir)
            messagebox.showerror(t("dialog.error_title"), t("dialog.diagnostics_export_error"))
            return

        report_path = os.path.join(diagnostics_dir, "diagnostic_report.txt")
        try:
            report_text = _build_diagnostic_report_text()
            with open(report_path, "w", encoding="utf-8") as fh:
                fh.write(report_text)
        except Exception:
            logger.exception("寫入診斷報告失敗: %s", report_path)
            messagebox.showerror(t("dialog.error_title"), t("dialog.diagnostics_export_error"))
            return

        logger.info("診斷報告已匯出: %s", report_path)
        _show_diagnostic_export_success(report_path, diagnostics_dir)
    except Exception:
        logger.exception("匯出診斷報告發生未預期錯誤")
        messagebox.showerror(t("dialog.error_title"), t("dialog.diagnostics_export_error"))


def show_chat_sandbox():
    """Open the LLM Chat Sandbox window for provider connectivity testing."""
    from ui.chat_sandbox import LLMChatWindow
    win = LLMChatWindow(
        root,
        current_llm_worker,
        provider_name=llm_provider,
        provider_display_name=ProviderFactory.get_display_name(llm_provider),
        model_display_name=ProviderFactory.get_model_display_name(
            llm_provider,
            getattr(current_llm_worker, "model_name", ""),
        ),
        translator=t,
        language_getter=lambda: i18n.language,
    )


def create_dev_menu(parent_menu):
    """建立 Dev 選單；初始建置與語言重建共用同一份項目。"""
    menu = tk.Menu(parent_menu, tearoff=0)
    menu.add_command(label=t("menu.system_info"), command=show_system_info_dialog)
    menu.add_command(label=t("menu.export_diagnostics"), command=export_diagnostic_report)
    menu.add_separator()
    menu.add_command(label=t("menu.check_log_title"), command=show_analysis_log_dialog)
    menu.add_separator()
    menu.add_command(label=t("menu.chat_sandbox"), command=show_chat_sandbox)
    return menu




def show_analysis_log_dialog():

    def open_analysis_log_path(path):
        text.config(state="normal")
        text.delete("1.0", tk.END)  
        
        if os.path.exists(path):
            with open(path, mode="r", encoding="utf-8") as file:
                content = file.read()
                text.insert(tk.END, content)
            
            # 載入文字後，執行語法高亮解析
            apply_highlighting()
        else:
            text.insert(tk.END, f"找不到日誌檔案：{path}\n")
            text.tag_add("ERROR", "1.0", "end")  # 將錯誤提示整段標紅
            
        text.config(state="disabled")

    def apply_highlighting():
        """解析文字並加上對應的顏色標籤"""
        # 定義不同層級的關鍵字與對應的 Tag 名稱
        rules = {
            "ERROR": r"\b(ERROR|CRITICAL|FAIL|FAILED|Exception|Traceback)\b",
            "WARN": r"\b(WARN|WARNING|DEBUG)\b",
            "INFO": r"\b(INFO|SUCCESS|OK)\b",
            "TIME": r"\b\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\+\d{4}\b"  
        }
        
        for tag_name, pattern in rules.items():
            # 清除舊的 tag 標記（避免重複疊加）
            text.tag_remove(tag_name, "1.0", tk.END)
            
            # 使用 re.finditer 尋找所有符合的關鍵字位置
            content = text.get("1.0", tk.END)
            for match in re.finditer(pattern, content, re.IGNORECASE):
                start_index = match.start()
                end_index = match.end()
                
                # 將字元索引轉換為 Tkinter Text 的 "行.列" 格式
                # Tkinter 的行從 1 開始，列從 0 開始
                start_pos = f"1.0 + {start_index} chars"
                end_pos = f"1.0 + {end_index} chars"
                
                text.tag_add(tag_name, start_pos, end_pos)

    # 選擇 log 視窗   
    analysis_log_win = tk.Toplevel(root)
    analysis_log_win.title(t("dialog.check_log_title"))
    analysis_log_win.geometry("750x600")
    analysis_log_win.iconbitmap(resource_path("image/logo.ico"))
    analysis_log_win.transient(root)
    analysis_log_win.grab_set()
    
    # 主面板佈局設定
    main_frame = ttk.Frame(analysis_log_win, padding=(16, 16, 16, 16))
    main_frame.pack(fill="both", expand=True)
    main_frame.columnconfigure(0, weight=1)
    main_frame.rowconfigure(2, weight=1)
    if is_frozen_app():
        analysis_log_path = os.path.join(get_runtime_data_root(), "logs", "analysis_logs")
    else:
        analysis_log_path = os.path.join(get_runtime_data_root(), "analysis_logs")

    file_names = os.listdir(analysis_log_path) if os.path.exists(analysis_log_path) else []
    file_names = file_names[::-1]

    # 1. 頂部路徑標示
    ttk.Label(main_frame, text=analysis_log_path, font=("Microsoft JhengHei", 10, "bold")).grid(row=0, column=0, sticky="nw", pady=(0, 6))

    # 2. 下拉選單
    combo = ttk.Combobox(main_frame, values=file_names, state="readonly")
    if file_names:
        combo.current(0)
    combo.grid(row=1, column=0, sticky="ew", pady=(0, 10))

    # 3. Log 顯示區塊（含滾動條）
    text_frame = ttk.Frame(main_frame)
    text_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
    text_frame.columnconfigure(0, weight=1)
    text_frame.rowconfigure(0, weight=1)

    v_scrollbar = ttk.Scrollbar(text_frame, orient="vertical")
    v_scrollbar.grid(row=0, column=1, sticky="ns")
    h_scrollbar = ttk.Scrollbar(text_frame, orient="horizontal")
    h_scrollbar.grid(row=1, column=0, sticky="ew")

    text = tk.Text(
        text_frame,
        wrap="none",
        font=("Consolas", 10),
        bg="#1e1e1e",
        fg="#d4d4d4",
        insertbackground="white",
        padx=10,
        pady=10,
        undo=False,
        yscrollcommand=v_scrollbar.set,
        xscrollcommand=h_scrollbar.set
    )
    text.grid(row=0, column=0, sticky="nsew")
    
    v_scrollbar.config(command=text.yview)
    h_scrollbar.config(command=text.xview)
    
    # --- 配置語法高亮的顏色樣式 ---
    text.tag_config("ERROR", foreground="#f44336", font=("Consolas", 10, "bold"))  # 明亮紅 + 粗體
    text.tag_config("WARN", foreground="#ff9800", font=("Consolas", 10, "bold"))   # 橘黃色 + 粗體
    text.tag_config("INFO", foreground="#4caf50")                                   # 溫和綠
    text.tag_config("TIME", foreground="#00bcd4")                                   # 青藍色
    # ----------------------------
    
    text.config(state="disabled")

    # 4. 按鈕區塊
    def on_confirm_click():
        if combo.get():
            current_path = os.path.join(analysis_log_path, combo.get())
            open_analysis_log_path(current_path)

    ttk.Button(
        main_frame, 
        text=t("dialog.confirm_title"), 
        command=on_confirm_click, 
        width=12
    ).grid(row=3, column=0, sticky="se")

def show_custom_prompt_dialog():
    """顯示自訂提示詞對話框"""
    from providers import tone_templates
    
    prompt_win = tk.Toplevel(root)
    prompt_win.title(t("dialog.custom_prompts_title"))
    prompt_win.geometry("700x520")
    prompt_win.iconbitmap(resource_path("image/logo.ico"))
    prompt_win.transient(root)
    prompt_win.grab_set()
    
    main_frame = ttk.Frame(prompt_win, padding=(16, 16, 16, 16))
    main_frame.pack(fill="both", expand=True)
    main_frame.columnconfigure(0, weight=1)
    main_frame.rowconfigure(1, weight=1)

    current_tone = config_service.get_llm_tone("friendly")

    ttk.Label(main_frame, text=t("dialog.prompt_label"), font=("Microsoft JhengHei", 10, "bold")).grid(row=0, column=0, sticky="nw", pady=(0, 6))

    prompt_text = tk.Text(main_frame, height=18, font=("Courier New", 10), wrap="word")
    prompt_text.grid(row=1, column=0, sticky="nsew", pady=(0, 12))

    prompt_scrollbar = ttk.Scrollbar(prompt_text, command=prompt_text.yview)
    prompt_scrollbar.pack(side="right", fill="y")
    prompt_text.config(yscrollcommand=prompt_scrollbar.set)

    custom_prompt = config_service.get_custom_prompt("")
    prompt_text.insert("1.0", custom_prompt or tone_templates.get_tone_prompt(current_tone))
    
    # 按鈕區塊
    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=2, column=0, sticky="ew", pady=(12, 0))
    button_frame.columnconfigure(1, weight=1)
    
    def save_prompts():
        prompt = prompt_text.get("1.0", "end-1c").strip()
        
        # 驗證提示詞
        if not prompt:
            messagebox.showerror(t("dialog.error_title"), t("error.prompt_empty"))
            return

        # 保存提示詞
        config_service.set_custom_prompt(prompt)
        config_service.save()
        
        # 更新 provider
        try:
            if hasattr(analyzer, 'provider') and analyzer.provider:
                analyzer.provider.set_custom_prompt(prompt)
            if current_llm_worker:
                current_llm_worker.set_custom_prompt(prompt)
        except Exception as e:
            print(f"更新提供商提示詞失敗: {e}")
        
        status_var.set(t("status.custom_prompts_saved"))
        prompt_win.destroy()
    
    def reset_prompts():
        if messagebox.askyesno(t("dialog.confirm_title"), "確定要重設為預設提示詞嗎？"):
            config_service.clear_custom_prompts()
            config_service.save()
            try:
                if hasattr(analyzer, 'provider') and analyzer.provider:
                    analyzer.provider.clear_custom_prompts()
                if current_llm_worker:
                    current_llm_worker.clear_custom_prompts()
            except Exception as e:
                print(f"重設提供商提示詞失敗: {e}")
            prompt_win.destroy()
    
    ttk.Button(button_frame, text=t("button.save_prompts"), command=save_prompts).pack(side="left", padx=(0, 8))
    ttk.Button(button_frame, text=t("button.reset_prompts"), command=reset_prompts).pack(side="left", padx=(0, 8))
    ttk.Button(button_frame, text=t("button.cancel"), command=prompt_win.destroy).pack(side="left")



def show_settings_dialog():
    """顯示設定對話框"""
    settings_win = tk.Toplevel(root)
    settings_win.title(t("dialog.settings_title"))
    settings_win.geometry("560x430")
    settings_win.iconbitmap(resource_path("image/logo.ico"))  # Set the icon for the settings window
    settings_win.transient(root)
    settings_win.grab_set()

    # 主框架
    main_frame = ttk.Frame(settings_win, padding=(16, 16, 16, 16))
    main_frame.pack(fill="both", expand=True)
    main_frame.columnconfigure(1, weight=1)

    def create_path_row(row, label_key, mode_var, path_var, browse_title_key, filetypes, placeholder, mode_options="2"):
        ttk.Label(main_frame, text=t(label_key), font=("Microsoft JhengHei", 10)).grid(
            row=row, column=0, sticky="nw", pady=(0, 10)
        )

        selector_frame = ttk.Frame(main_frame)
        selector_frame.grid(row=row, column=1, columnspan=2, sticky="ew", padx=(8, 0), pady=(0, 6))
        selector_frame.columnconfigure(2, weight=1)

        path_frame = ttk.Frame(main_frame)
        path_frame.grid(row=row + 1, column=1, columnspan=2, sticky="ew", padx=(8, 0), pady=(0, 12))
        path_frame.columnconfigure(0, weight=1)

        placeholder_state = {"active": False}
        custom_entry = tk.Entry(
            path_frame,
            font=("Microsoft JhengHei", 10),
            bg="white",
            fg=TEXT_MAIN,
            relief="solid",
            bd=1,
            insertbackground=TEXT_MAIN,
        )
        custom_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        def show_placeholder():
            if not custom_entry.get():
                placeholder_state["active"] = True
                custom_entry.config(fg="#888888")
                custom_entry.delete(0, "end")
                custom_entry.insert(0, placeholder)

        def hide_placeholder():
            if placeholder_state["active"]:
                placeholder_state["active"] = False
                custom_entry.config(fg=TEXT_MAIN)
                custom_entry.delete(0, "end")

        def sync_var():
            if not placeholder_state["active"]:
                path_var.set(custom_entry.get().strip())

        def set_entry_value(value):
            placeholder_state["active"] = False
            custom_entry.config(fg=TEXT_MAIN)
            custom_entry.delete(0, "end")
            custom_entry.insert(0, value)
            show_placeholder()

        def browse_path():
            file_path = filedialog.askopenfilename(
                title=t(browse_title_key),
                filetypes=filetypes,
                parent=settings_win,
            )
            if file_path:
                mode_var.set("custom")
                path_var.set(file_path)
                set_entry_value(file_path)
                update_mode()

        ttk.Button(path_frame, text=t("button.browse"), command=browse_path, width=10).grid(row=0, column=1)
        custom_entry.bind("<FocusIn>", lambda _event: hide_placeholder())
        custom_entry.bind("<FocusOut>", lambda _event: (sync_var(), show_placeholder()))

        if mode_options == "3":
            # 3 options: standard, fast, custom (for model path)
            ttk.Radiobutton(
                selector_frame,
                text=t("label.model_standard"),
                variable=mode_var,
                value="standard",
                command=lambda: (sync_var(), update_mode()),
            ).grid(row=0, column=0, sticky="w", padx=(0, 12))
            ttk.Radiobutton(
                selector_frame,
                text=t("label.model_fast"),
                variable=mode_var,
                value="fast",
                command=lambda: (sync_var(), update_mode()),
            ).grid(row=0, column=1, sticky="w", padx=(0, 12))
            ttk.Radiobutton(
                selector_frame,
                text=t("label.path_custom"),
                variable=mode_var,
                value="custom",
                command=lambda: (sync_var(), update_mode()),
            ).grid(row=0, column=2, sticky="w", padx=(0, 12))
            default_label = ttk.Label(selector_frame, text="", foreground="#666")
            default_label.grid(row=0, column=3, sticky="w")
        else:
            # 2 options: default, custom (for katago and config paths)
            ttk.Radiobutton(
                selector_frame,
                text=t("label.path_default"),
                variable=mode_var,
                value="default",
                command=lambda: (sync_var(), update_mode()),
            ).grid(row=0, column=0, sticky="w", padx=(0, 16))
            ttk.Radiobutton(
                selector_frame,
                text=t("label.path_custom"),
                variable=mode_var,
                value="custom",
                command=lambda: (sync_var(), update_mode()),
            ).grid(row=0, column=1, sticky="w", padx=(0, 16))
            default_label = ttk.Label(selector_frame, text=t("label.using_builtin_file"), foreground="#666")
            default_label.grid(row=0, column=2, sticky="w")

        def update_mode():
            mode = mode_var.get()
            if mode == "custom":
                default_label.grid_remove()
                path_frame.grid()
                if not custom_entry.get():
                    show_placeholder()
            else:
                if mode_options == "3":
                    # Show current model selection name
                    if mode == "standard":
                        default_label.config(text=t("label.model_standard"))
                    elif mode == "fast":
                        default_label.config(text=t("label.model_fast"))
                    default_label.grid()
                path_frame.grid_remove()

        set_entry_value(path_var.get().strip())
        update_mode()
        return sync_var

    sync_path_entries = [
        create_path_row(
            0,
            "label.katago_path",
            katago_path_mode_var,
            katago_path_var,
            "dialog.katago_title",
            [(t("filetype.exe"), "*.exe"), (t("filetype.all"), "*.*")],
            t("placeholder.katago_path"),
        ),
        create_path_row(
            2,
            "label.model_path",
            model_path_mode_var,
            model_path_var,
            "dialog.model_title",
            [(t("filetype.gz"), "*.gz"), (t("filetype.all"), "*.*")],
            t("placeholder.model_path"),
            "3",
        ),
        create_path_row(
            4,
            "label.config_path",
            config_path_mode_var,
            config_path_var,
            "dialog.config_title",
            [(t("filetype.cfg"), "*.cfg"), (t("filetype.all"), "*.*")],
            t("placeholder.config_path"),
        ),
    ]

    # 提示文字
    tip_frame = ttk.Frame(main_frame)
    tip_frame.grid(row=6, column=0, columnspan=3, sticky="ew", pady=(8, 0))
    ttk.Label(tip_frame, text=t("label.settings_tip"), 
              font=("Microsoft JhengHei", 9), foreground="#666").pack(anchor="w")

    # 按鈕框架
    btn_frame = ttk.Frame(main_frame)
    btn_frame.grid(row=7, column=0, columnspan=3, sticky="ew", pady=(24, 0))
    
    def apply_settings():
        for sync_path_entry in sync_path_entries:
            sync_path_entry()
        config_service.set_setting("katago_path_mode", katago_path_mode_var.get())
        config_service.set_setting("model_path_mode", model_path_mode_var.get())
        config_service.set_setting("config_path_mode", config_path_mode_var.get())
        config_service.save()
        if reinitialize_analyzer():
            settings_win.destroy()

    ttk.Button(btn_frame, text=t("button.apply"), command=apply_settings, width=12).pack(side="right", padx=(8, 0))
    ttk.Button(btn_frame, text=t("button.cancel"), command=settings_win.destroy, width=12).pack(side="right")


def show_appearance_settings_dialog():
    """顯示外觀設定對話框"""
    settings_win = tk.Toplevel(root)
    settings_win.title(t("settings.appearance_title"))
    settings_win.geometry("520x400")
    try:
        settings_win.iconbitmap(resource_path("image/logo.ico"))
    except Exception:
        pass
    settings_win.transient(root)
    settings_win.grab_set()

    main_frame = ttk.Frame(settings_win, padding=(16, 16, 16, 16))
    main_frame.pack(fill="both", expand=True)

    # 儲存當前值（用於取消時恢復）
    original_values = {
        "board_background": config_service.get_board_background(),
        "board_frame_background": config_service.get_board_frame_background(),
        "black_stone_image": config_service.get_black_stone_image(),
        "white_stone_image": config_service.get_white_stone_image(),
    }

    # 目前編輯中的值
    current_values = dict(original_values)

    # 圖片預覽標籤
    preview_labels = {}

    def create_image_row(parent, label_key, config_key, row):
        """建立一個圖片選擇行"""
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=(0, 12))
        frame.columnconfigure(1, weight=1)

        # 標籤
        ttk.Label(frame, text=t(label_key), font=("Microsoft JhengHei", 10)).grid(
            row=0, column=0, sticky="w", padx=(0, 12)
        )

        # 路徑顯示
        path_var = tk.StringVar(value=current_values[config_key] or t("settings.no_image_selected"))
        path_label = ttk.Label(frame, textvariable=path_var, foreground=TEXT_MUTED)
        path_label.grid(row=0, column=1, sticky="w", padx=(0, 8))

        # 預覽標籤
        preview_label = ttk.Label(frame, text="", background=PANEL_BG)
        preview_label.grid(row=0, column=2, padx=(0, 8))
        preview_labels[config_key] = preview_label

        def browse_image():
            file_path = filedialog.askopenfilename(
                title=t("settings.select_image"),
                filetypes=[
                    (
                        t("settings.image_files"),
                        "*.png *.jpg *.jpeg *.gif *.bmp *.webp *.tif *.tiff *.ico",
                    ),
                    (t("filetype.all"), "*.*")
                ],
                parent=settings_win,
            )
            if file_path:
                current_values[config_key] = file_path
                path_var.set(file_path)
                update_preview(config_key, file_path)

        def use_default():
            current_values[config_key] = ""
            path_var.set(t("settings.no_image_selected"))
            preview_labels[config_key].config(image="")

        ttk.Button(frame, text=t("button.browse"), command=browse_image, width=10).grid(
            row=0, column=3, padx=(0, 4)
        )
        ttk.Button(frame, text=t("settings.use_default"), command=use_default, width=10).grid(
            row=0, column=4, padx=(0, 0)
        )

        # 更新預覽
        if current_values[config_key]:
            update_preview(config_key, current_values[config_key])

        return path_var

    def update_preview(config_key, file_path):
        """更新圖片預覽"""
        try:
            if file_path and os.path.exists(file_path):
                img = load_tk_image(file_path, (60, 60))
                preview_labels[config_key].config(image=img, text="")
                preview_labels[config_key].image = img
            else:
                preview_labels[config_key].config(image="", text="")
        except Exception as e:
            logger.warning(f"無法載入圖片預覽 {file_path}: {e}")
            preview_labels[config_key].config(image="", text="")

    # 建立四個圖片選擇行
    create_image_row(main_frame, "settings.board_background", "board_background", 0)
    create_image_row(main_frame, "settings.board_frame", "board_frame_background", 1)
    create_image_row(main_frame, "settings.black_stone", "black_stone_image", 2)
    create_image_row(main_frame, "settings.white_stone", "white_stone_image", 3)

    # 按鈕框架
    btn_frame = ttk.Frame(main_frame)
    btn_frame.pack(fill="x", pady=(24, 0))

    def apply_changes():
        # 儲存設定
        config_service.set_board_background(current_values["board_background"])
        config_service.set_board_frame_background(current_values["board_frame_background"])
        config_service.set_black_stone_image(current_values["black_stone_image"])
        config_service.set_white_stone_image(current_values["white_stone_image"])
        config_service.save()

        # 重新載入棋盤圖片
        board._load_custom_images()
        board.refresh_display()

        settings_win.destroy()

    def cancel_changes():
        settings_win.destroy()

    ttk.Button(btn_frame, text=t("button.apply"), command=apply_changes, width=12).pack(side="right", padx=(8, 0))
    ttk.Button(btn_frame, text=t("button.cancel"), command=cancel_changes, width=12).pack(side="right")


# 滾輪事件處理
def on_mouse_wheel(event):
    # Windows: event.delta, Linux/Mac: event.num
    if event.delta > 0 or event.num == 4: # 滾輪向上 -> 上一步
        board.undo()
    elif event.delta < 0 or event.num == 5: # 滾輪向下 -> 下一步
        board.redo()

root = tk.Tk()
root.title(t("app.title"))
root.configure(bg=UI_BG)
root.minsize(930, 720)
root.iconbitmap(resource_path("image/logo.ico"))  

style = ttk.Style(root)
style.theme_use("clam")
style.configure(".", font=("Microsoft JhengHei", 10))
style.configure("TFrame", background=UI_BG)
style.configure("Panel.TFrame", background=PANEL_BG, relief="solid", borderwidth=1)
style.configure("TLabel", background=UI_BG, foreground=TEXT_MAIN)
style.configure("Panel.TLabel", background=PANEL_BG, foreground=TEXT_MAIN)
style.configure("Muted.TLabel", background=PANEL_BG, foreground=TEXT_MUTED)
style.configure("Title.TLabel", background=PANEL_BG, foreground=TEXT_MAIN, font=("Microsoft JhengHei", 13, "bold"))
style.configure("Primary.TButton", background=ACCENT, foreground="white", padding=(14, 8), borderwidth=0)
style.map("Primary.TButton", background=[("active", ACCENT_DARK), ("disabled", "#9eb9bd")])
style.configure("Tool.TButton", padding=(10, 7))
style.configure("Feedback.TButton", padding=(10, 7))

status_var = tk.StringVar(value=t("status.starting"))
llm_model_var = tk.StringVar(value="")
language_var = tk.StringVar(value=i18n.language)
analyzer = None
analyzer_initializing = False
is_shutting_down = False
current_sgf_path = None
loaded_sgf_overwrite_confirmed = False

# 模型和配置文件路徑設定
katago_path_mode_var = tk.StringVar(value=config_service.get_setting("katago_path_mode", "default"))
model_path_mode_var = tk.StringVar(value=config_service.get_setting("model_path_mode", "standard"))
config_path_mode_var = tk.StringVar(value=config_service.get_setting("config_path_mode", "default"))
katago_path_var = tk.StringVar(value="")
model_path_var = tk.StringVar(value="")
config_path_var = tk.StringVar(value="")

data_filter = GoDataFilter(winrate_threshold=0.05, score_threshold=2.0)


def on_closing():
    global is_shutting_down, analyzer_initializing
    if is_shutting_down:
        return
    is_shutting_down = True
    analyzer_initializing = False

    try:
        plt.close("all")
    except Exception:
        pass

    if analyzer and hasattr(analyzer, 'process'):
        try:
            analyzer.close(timeout=3)
        except subprocess.TimeoutExpired:
            logger.warning("KataGo process did not exit while closing")
        except OSError as e:
            logger.warning("Error closing KataGo process: %s", e)

    if score_analyzer and hasattr(score_analyzer, 'process'):
        try:
            score_analyzer.close(timeout=3)
        except subprocess.TimeoutExpired:
            logger.warning("Score KataGo process did not exit while closing")
        except OSError as e:
            logger.warning("Error closing Score KataGo process: %s", e)

    try:
        for child in root.winfo_children():
            if isinstance(child, tk.Toplevel):
                try:
                    child.destroy()
                except tk.TclError:
                    pass
        root.destroy()
    except tk.TclError:
        pass

root.protocol("WM_DELETE_WINDOW", on_closing)

from providers import tone_templates


def build_menu_bar():
    global menu_bar, file_menu, edit_menu, analysis_menu, settings_menu, language_menu
    global view_menu, help_menu, dev_menu, tone_menu, current_tone_var
    global show_teacher_var, show_branch_var, show_move_numbers_var, show_dev_var

    menu_bar = tk.Menu(root)

    def set_language(language):
        i18n.set_language(language)
        language_var.set(language)
        refresh_language()
        status_var.set(t("status.language_changed", language=t(f"language.{language}")))

    def toggle_teacher_panel():
        if show_teacher_var.get():
            teacher_section.grid()
        else:
            teacher_section.grid_remove()

    def toggle_branch_panel():
        if show_branch_var.get():
            branch_section.grid()
        else:
            branch_section.grid_remove()

    def toggle_move_numbers():
        board._handle_recommendation_hover(None)
        board._draw_move_numbers()

    def toggle_dev():
        config_service.set_setting("show_developer", show_dev_var.get())
        config_service.save()
        rebuild_menu_bar()

    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label=t("menu.new_game"), accelerator="Ctrl+N", command=new_game)
    file_menu.add_separator()
    file_menu.add_command(label=t("menu.load_sgf"), accelerator="Ctrl+O", command=on_load_sgf_click)
    file_menu.add_command(label=t("menu.save_json"), command=save_game_as_json)
    file_menu.add_command(label=t("menu.save_json_as"), command=save_game_as_json_dialog)
    file_menu.add_command(label=t("menu.save_sgf"), accelerator="Ctrl+S", command=save_game_as_sgf)
    file_menu.add_command(label=t("menu.save_sgf_as"), accelerator="Ctrl+Shift+S", command=save_game_as_sgf_dialog)
    file_menu.add_separator()
    file_menu.add_command(label=t("menu.exit"), accelerator="Alt+F4", command=on_closing)
    menu_bar.add_cascade(label=t("menu.file"), menu=file_menu)

    edit_menu = tk.Menu(menu_bar, tearoff=0)
    edit_menu.add_command(label=t("menu.undo"), accelerator="Ctrl+Z / ↑", command=lambda: board.undo())
    edit_menu.add_command(label=t("menu.redo"), accelerator="Ctrl+Y / ↓", command=lambda: board.redo())
    edit_menu.add_separator()
    edit_menu.add_command(label=t("menu.prev_branch"), accelerator="←", command=lambda: board.switch_branch(-1))
    edit_menu.add_command(label=t("menu.next_branch"), accelerator="→", command=lambda: board.switch_branch(1))
    menu_bar.add_cascade(label=t("menu.edit"), menu=edit_menu)

    analysis_menu = tk.Menu(menu_bar, tearoff=0)
    analysis_menu.add_command(label=t("menu.analyze_current"), accelerator="Ctrl+R", command=on_analyze_button_click)
    analysis_menu.add_command(label=t("menu.full_analysis"), accelerator="Ctrl+Shift+R", command=show_winrate_chart)
    menu_bar.add_cascade(label=t("menu.analysis"), menu=analysis_menu)

    settings_menu = tk.Menu(menu_bar, tearoff=0)
    settings_menu.add_command(label=t("menu.model_settings"), command=show_settings_dialog)
    settings_menu.add_command(label=t("settings.appearance"), command=show_appearance_settings_dialog)
    language_menu = tk.Menu(settings_menu, tearoff=0)
    for language in i18n.available_languages:
        language_menu.add_radiobutton(
            label=t(f"language.{language}"),
            value=language,
            variable=language_var,
            command=lambda lang=language: set_language(lang)
        )
    settings_menu.add_cascade(label=t("menu.language"), menu=language_menu)
    settings_menu.add_command(label=t("menu.llm_model"), command=show_llm_selection_dialog)
    tone_menu = tk.Menu(settings_menu, tearoff=0)
    current_tone_var = tk.StringVar(value=config_service.get_llm_tone("friendly"))
    for tone_id, tone_name in tone_templates.TONE_DISPLAY_NAMES.items():
        tone_menu.add_radiobutton(
            label=tone_name,
            value=tone_id,
            variable=current_tone_var,
            command=lambda tone=tone_id: set_llm_tone(tone)
        )
    settings_menu.add_cascade(label=t("menu.llm_tone"), menu=tone_menu)
    settings_menu.add_command(label=t("menu.custom_prompts"), command=show_custom_prompt_dialog)
    settings_menu.add_separator()
    settings_menu.add_command(label=t("menu.reinit_analyzer"), command=reinitialize_analyzer)
    menu_bar.add_cascade(label=t("menu.settings"), menu=settings_menu)

    view_menu = tk.Menu(menu_bar, tearoff=0)
    show_teacher_var = tk.BooleanVar(value=True)
    show_branch_var = tk.BooleanVar(value=True)
    show_move_numbers_var = tk.BooleanVar(value=False)
    show_dev_var = tk.BooleanVar(value=config_service.get_setting("show_developer", False))
    view_menu.add_checkbutton(label=t("menu.show_teacher"), variable=show_teacher_var, command=toggle_teacher_panel)
    view_menu.add_checkbutton(label=t("menu.show_branch"), variable=show_branch_var, command=toggle_branch_panel)
    view_menu.add_checkbutton(label=t("menu.show_move_numbers"), variable=show_move_numbers_var, command=toggle_move_numbers)
    view_menu.add_checkbutton(label=t("menu.dev_show"), variable=show_dev_var, command=toggle_dev)
    menu_bar.add_cascade(label=t("menu.view"), menu=view_menu)

    help_menu = tk.Menu(menu_bar, tearoff=0)
    help_menu.add_command(label=t("menu.shortcuts"), command=lambda: messagebox.showinfo(
        t("dialog.shortcuts_title"),
        t("dialog.shortcuts_message")
    ))
    help_menu.add_command(label=t("menu.about"), command=show_about)
    menu_bar.add_cascade(label=t("menu.help"), menu=help_menu)
    menu_bar.add_command(label=t("menu.feedback"), command=show_feedback)

    dev_menu = create_dev_menu(menu_bar)
    if show_dev_var.get():
        menu_bar.add_cascade(label=t("menu.dev"), menu=dev_menu)

    root.config(menu=menu_bar)
    return menu_bar


menu_bar = build_menu_bar()

# 綁定方向鍵
root.bind("<Up>", lambda e: board.undo())
root.bind("<Down>", lambda e: board.redo())
root.bind("<Left>", lambda e: board.switch_branch(-1))  # 上一個變化圖
root.bind("<Right>", lambda e: board.switch_branch(1))  # 下一個變化圖



# 綁定滑鼠滾輪
root.bind("<MouseWheel>", on_mouse_wheel)
root.bind("<Button-4>", on_mouse_wheel)
root.bind("<Button-5>", on_mouse_wheel)

# 綁定一般快捷鍵
root.bind("<Control-z>", lambda e: board.undo())
root.bind("<Control-y>", lambda e: board.redo())

root.bind("<Control-n>", lambda e: new_game())
root.bind("<Control-o>", lambda e: on_load_sgf_click())
root.bind("<Control-s>", lambda e: save_game_as_sgf())
root.bind("<Control-Shift-S>", lambda e: save_game_as_sgf_dialog())
root.bind("<Control-r>", lambda e: on_analyze_button_click())
root.bind("<Control-Shift-R>", lambda e: show_winrate_chart())

main_frame = ttk.Frame(root, padding=(16, 14, 16, 8))
main_frame.pack(fill="both", expand=True)
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=0)
main_frame.rowconfigure(0, weight=1)

board_shell = tk.Frame(main_frame, bg=PANEL_BG, highlightbackground=PANEL_BORDER, highlightthickness=1, padx=14, pady=14)
board_shell.grid(row=0, column=0, sticky="nsew", padx=(0, 14))

# 外框背景層：顯示在棋盤四周的留白區域（不包含棋盤本身）
board_frame_bg_label = tk.Label(board_shell, bd=0, highlightthickness=0)
board_frame_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

board = GoBoard(board_shell)
board.pack(anchor="center")
board.frame_bg_label = board_frame_bg_label
# board_frame_bg_label 在 board 之前建立，預設疊加順序已正確（Label在下、Canvas在上），
# 無需額外 lift/tkraise。tk.Canvas 覆寫了 lift/tkraise（用於 canvas items），
# 不接受無參數呼叫，故不可調用。

# <Configure> 動態重縮放：視窗縮放導致 board_shell 尺寸改變時，重新縮放外框背景圖片。
# 棋盤 Canvas 本身保持固定 620×620，不會被縮放。
def _on_board_shell_configure(event):
    # 節流：避免拖曳視窗時頻繁重算圖片，延遲 100ms 執行
    if board._frame_bg_resize_after_id is not None:
        board.after_cancel(board._frame_bg_resize_after_id)
    board._frame_bg_resize_after_id = board.after(
        100, lambda: board._resize_frame_background((event.width, event.height))
    )

board_shell.bind("<Configure>", _on_board_shell_configure)

info_frame = ttk.Frame(main_frame, style="Panel.TFrame", padding=(14, 14, 14, 14))
info_frame.grid(row=0, column=1, sticky="ns")
info_frame.columnconfigure(0, weight=1)
info_frame.columnconfigure(1, weight=1)
info_frame.rowconfigure(8, weight=1)

ai_analysis_label = ttk.Label(info_frame, text=t("label.ai_analysis"), style="Title.TLabel")
ai_analysis_label.grid(row=0, column=0, columnspan=2, sticky="w")
winrate_label = ttk.Label(info_frame, text=t("analysis.not_analyzed"), style="Panel.TLabel", justify="left", anchor="w")
winrate_label.grid(row=1, column=0, columnspan=2, pady=(8, 14), sticky="ew")

btn_analyze = ttk.Button(info_frame, text=t("button.analyze"), command=on_analyze_button_click, style="Primary.TButton")
btn_analyze.grid(row=2, column=0, columnspan=2, pady=(0, 8), sticky="ew")

btn_full_analysis = ttk.Button(info_frame, text=t("button.full_analysis"), command=show_winrate_chart, style="Tool.TButton")
btn_full_analysis.grid(row=3, column=0, columnspan=2, pady=(0, 12), sticky="ew")

btn_undo = ttk.Button(info_frame, text=t("button.undo"), command=board.undo, style="Tool.TButton")
btn_undo.grid(row=4, column=0, padx=(0, 4), pady=(0, 8), sticky="ew")
btn_redo = ttk.Button(info_frame, text=t("button.redo"), command=board.redo, style="Tool.TButton")
btn_redo.grid(row=4, column=1, padx=(4, 0), pady=(0, 8), sticky="ew")

btn_load_sgf = ttk.Button(info_frame, text=t("button.load_sgf"), command=on_load_sgf_click, style="Tool.TButton")
btn_load_sgf.grid(row=5, column=0, padx=(0, 4), pady=(0, 8), sticky="ew")
btn_save_sgf_as = ttk.Button(info_frame, text=t("button.save_sgf_as"), command=save_game_as_sgf_dialog, style="Tool.TButton")
btn_save_sgf_as.grid(row=5, column=1, padx=(4, 0), pady=(0, 8), sticky="ew")
btn_score_estimate = ttk.Button(info_frame, text=t("button.score_estimate"), command=on_score_estimate_click, style="Tool.TButton")
btn_score_estimate.grid(row=6, column=0, padx=(0, 4), pady=(0, 14), sticky="ew")

branch_section = tk.Frame(info_frame, bg=PANEL_BG)
branch_section.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(0, 14))
branch_title_label = tk.Label(
    branch_section,
    text=t("label.branch_switch"),
    bg=PANEL_BG,
    fg=TEXT_MAIN,
    font=("Microsoft JhengHei", 10, "bold"),
    bd=0,
    padx=0,
    pady=0
)
branch_title_label.pack(anchor="w")
branch_ui = BranchCanvas(branch_section, board_ref=board, width=220, height=96, bg=PANEL_BG, highlightbackground=PANEL_BORDER, highlightthickness=1)
branch_ui.pack(fill="x", pady=(6, 0))

board.branch_ui = branch_ui

teacher_section = tk.Frame(info_frame, bg=PANEL_BG)
teacher_section.grid(row=8, column=0, columnspan=2, sticky="nsew")
teacher_header = tk.Frame(teacher_section, bg=PANEL_BG)
teacher_header.pack(fill="x")
teacher_title_label = tk.Label(
    teacher_header,
    text=t("label.teacher"),
    bg=PANEL_BG,
    fg=TEXT_MAIN,
    font=("Microsoft JhengHei", 10, "bold"),
    bd=0,
    padx=0,
    pady=0
)
teacher_title_label.pack(side="left")
teacher_model_label = tk.Label(
    teacher_header,
    textvariable=llm_model_var,
    bg=PANEL_BG,
    fg=TEXT_MUTED,
    font=("Microsoft JhengHei", 10),
    bd=0,
    padx=0,
    pady=0
)
teacher_model_label.pack(side="right")
teacher_text = tk.Text(
    teacher_section,
    width=30,
    height=9,
    font=("Microsoft JhengHei", 10),
    wrap="word",
    bg=TEACHER_TEXT_BG,
    fg=TEXT_MAIN,
    insertbackground=TEXT_MAIN,
    selectbackground="#ead7b8",
    selectforeground=TEXT_MAIN,
    relief="solid",
    bd=1,
    padx=8,
    pady=8,
    state="disabled"
)
teacher_text.pack(fill="both", expand=True, pady=(6, 0))

status_bar = ttk.Label(root, textvariable=status_var, anchor="w", padding=(12, 5), background="#e8dfd2", foreground=TEXT_MUTED)
status_bar.pack(side="bottom", fill="x")

def update_status(message):
    if is_shutting_down:
        return
    if threading.current_thread() is threading.main_thread():
        status_var.set(message)
    else:
        try:
            root.after(0, status_var.set, message)
        except tk.TclError:
            pass


def is_analyzer_ready():
    return (
        not is_shutting_down
        and analyzer is not None
        and not getattr(analyzer, "closed", False)
        and getattr(analyzer, "ready_event", None)
        and analyzer.ready_event.is_set()
    )


def set_analysis_controls_state(enabled):
    state = "normal" if enabled else "disabled"
    for name in ("btn_analyze", "btn_full_analysis"):
        widget = globals().get(name)
        if widget is not None:
            widget.config(state=state)


def show_analyzer_not_ready():
    status_var.set(t("status.katago_initializing"))
    set_winrate_text("analysis.engine_not_ready")


def create_katago_startup_popup():
    popup = tk.Toplevel(root)
    popup.title(t("startup.title"))
    popup.geometry("420x170")
    popup.iconbitmap(resource_path("image/logo.ico"))
    popup.resizable(False, False)
    popup.transient(root)
    popup.protocol("WM_DELETE_WINDOW", lambda: None)

    x = root.winfo_rootx() + max(40, (root.winfo_width() - 420) // 2)
    y = root.winfo_rooty() + max(40, (root.winfo_height() - 170) // 2)
    popup.geometry(f"+{x}+{y}")

    frame = ttk.Frame(popup, padding=(18, 16, 18, 14))
    frame.pack(fill="both", expand=True)

    title_label = ttk.Label(frame, text=t("startup.heading"), font=("Microsoft JhengHei", 12, "bold"))
    title_label.pack(anchor="w")

    message_var = tk.StringVar(value=t("status.katago_initializing"))
    message_label = ttk.Label(frame, textvariable=message_var, wraplength=370, justify="left")
    message_label.pack(anchor="w", pady=(10, 8))

    detail_label = ttk.Label(frame, text=t("startup.first_run_hint"), foreground=TEXT_MUTED, wraplength=370, justify="left")
    detail_label.pack(anchor="w")

    progress_bar = ttk.Progressbar(frame, mode="indeterminate", length=360)
    progress_bar.pack(fill="x", pady=(14, 0))
    progress_bar.start(12)

    return {"window": popup, "message_var": message_var, "progress_bar": progress_bar}


def start_analyzer_async(show_success=False, replacing=False):
    global analyzer, analyzer_initializing

    if analyzer_initializing:
        status_var.set(t("status.katago_initializing"))
        return

    old_analyzer = analyzer
    analyzer = None
    analyzer_initializing = True
    set_analysis_controls_state(False)
    set_winrate_text("analysis.engine_not_ready")
    status_var.set(t("status.katago_initializing"))
    popup = create_katago_startup_popup()

    def update_startup_message(key, **kwargs):
        if is_shutting_down:
            return
        message = t(key, **kwargs)

        def apply_message():
            if is_shutting_down:
                return
            if popup["window"].winfo_exists():
                popup["message_var"].set(message)
            status_var.set(message)

        try:
            root.after(0, apply_message)
        except tk.TclError:
            pass

    def finish_success(new_analyzer):
        global analyzer, analyzer_initializing
        if is_shutting_down:
            new_analyzer.close(timeout=1)
            return
        analyzer = new_analyzer
        analyzer_initializing = False
        set_analysis_controls_state(True)
        status_var.set(t("status.ready"))
        set_winrate_text("analysis.not_analyzed")
        if popup["window"].winfo_exists():
            popup["progress_bar"].stop()
            popup["window"].destroy()
        if show_success:
            messagebox.showinfo(
                t("dialog.success_title"),
                t("dialog.reinit_success", model=get_model_display_name(), config=get_config_display_name())
            )
        if globals().get("board") is not None and board.stones:
            root.after(100, auto_analyze)

    def finish_failure(error, error_type=None):
        global analyzer_initializing
        if is_shutting_down:
            return
        analyzer_initializing = False
        set_analysis_controls_state(False)
        status_var.set(t("status.reinit_failed"))
        if popup["window"].winfo_exists():
            popup["progress_bar"].stop()
            popup["window"].destroy()
        logger.error("KataGo 初始化失敗: %s", error)
        if error_type == "no_gpu":
            messagebox.showerror(t("dialog.no_gpu_title"), t("dialog.no_gpu_message"))
        else:
            messagebox.showerror(t("dialog.error_title"), t("dialog.reinit_error", error=str(error)))

    def warn_if_slow():
        if is_shutting_down:
            return
        if analyzer_initializing and popup["window"].winfo_exists():
            message = t("status.katago_autotuning_slow")
            popup["message_var"].set(message)
            status_var.set(message)

    try:
        root.after(30000, warn_if_slow)
    except tk.TclError:
        pass

    def task():
        if is_shutting_down:
            return
        if old_analyzer is not None:
            try:
                old_analyzer.close(timeout=2)
            except subprocess.TimeoutExpired:
                logger.warning("舊 KataGo 進程未能在 2 秒內結束，將繼續重新初始化")
            except (AttributeError, OSError) as e:
                logger.warning("關閉舊 KataGo 進程時發生問題: %s", e)

        try:
            new_analyzer = KataGoAnalyzer(
                get_katago_path(),
                get_model_path(),
                get_config_path(),
                startup_callback=update_startup_message
            )

            while not new_analyzer.ready_event.is_set():
                if is_shutting_down:
                    new_analyzer.close(timeout=1)
                    return
                if new_analyzer.process.poll() is not None:
                    error = new_analyzer.startup_error or t("error.katago_process_exited")
                    error_type = getattr(new_analyzer, 'startup_error_type', None)
                    raise RuntimeError(f"{error_type}|{error}" if error_type else error)
                time.sleep(0.1)

            if not is_shutting_down:
                try:
                    root.after(0, finish_success, new_analyzer)
                except tk.TclError:
                    new_analyzer.close(timeout=1)
        except (OSError, ValueError, RuntimeError) as e:
            if not is_shutting_down:
                try:
                    error_msg = str(e)
                    error_type = None
                    if error_msg.startswith("no_gpu|"):
                        error_type = "no_gpu"
                        error_msg = error_msg[7:]  # Remove "no_gpu|" prefix
                    root.after(0, finish_failure, error_msg, error_type)
                except tk.TclError:
                    pass

    threading.Thread(target=task, daemon=True).start()

def update_teacher_ui(message):
    """給 LLM Provider 呼叫的回呼函數，用來更新文字框"""
    if is_shutting_down:
        return
    if threading.current_thread() is not threading.main_thread():
        try:
            root.after(0, update_teacher_ui, message)
        except tk.TclError:
            pass
        return
    
    global current_generated_commentary
    
    # 【Phase 1】累積生成的解說文本（用於快取存儲）
    if current_critical_event and message and not message.startswith(("思考", "thinking")):
        current_generated_commentary += message
    
    teacher_text.config(state="normal")
    teacher_text.delete("1.0", tk.END)
    teacher_text.insert(tk.END, message)
    teacher_text.config(state="disabled")


def on_commentary_generation_complete():
    """【Phase 1】LLM 生成完成後的回呼 — 將完整的解說存儲到快取"""
    global current_critical_event, current_generated_commentary
    if is_shutting_down:
        current_critical_event = None
        current_generated_commentary = ""
        return
    if current_critical_event and current_generated_commentary:
        try:
            add_to_commentary_cache(
                current_critical_event["turn"],
                current_critical_event["user_move"],
                current_generated_commentary
            )
            logger.info(f"已將第 {current_critical_event['turn']} 手的解說存儲到快取")
        except Exception as e:
            logger.warning(f"儲存解說到快取失敗: {e}")
        finally:
            current_critical_event = None
            current_generated_commentary = ""


def rebuild_menu_bar():
    return build_menu_bar()


def refresh_language():
    root.title(t("app.title_with_move", moves=len(board.stones)) if board.stones else t("app.title"))

    rebuild_menu_bar()

    ai_analysis_label.config(text=t("label.ai_analysis"))
    btn_analyze.config(text=t("button.analyze"))
    btn_full_analysis.config(text=t("button.full_analysis"))
    btn_undo.config(text=t("button.undo"))
    btn_redo.config(text=t("button.redo"))
    btn_load_sgf.config(text=t("button.load_sgf"))
    btn_save_sgf_as.config(text=t("button.save_sgf_as"))
    update_score_estimate_button_label()
    branch_title_label.config(text=t("label.branch_switch"))
    teacher_title_label.config(text=t("label.teacher"))
    update_llm_model_label()
    winrate_label.config(text=render_winrate_text(winrate_display_state["key"], winrate_display_state["kwargs"]))
    branch_ui.draw_branches()


# 初始化 LLM Provider - 根據配置選擇提供商
llm_provider = config_service.get_setting("llm_provider", "ollama")
current_llm_worker = ProviderFactory.create_from_config(
    config_service,
    ui_callback=update_teacher_ui,
    status_callback=update_status,
    translator=t,
    language_getter=lambda: i18n.language,
    on_complete_callback=on_commentary_generation_complete,  # 【Phase 1】傳入完成回呼
)

if llm_provider == "nvidia" and not get_nvidia_api_key():
    logger.warning("NVIDIA API Key 未設置，仍保留 NVIDIA 設定；請設定 NVIDIA_API_KEY、KATAGO_NVIDIA_API_KEY 或在 LLM 對話框設定")
    root.after(0, lambda: messagebox.showwarning(
        t("dialog.error_title"),
        t("error.nvidia_api_key_missing_env")
    ))
elif llm_provider == "github" and not get_github_token():
    logger.warning("GitHub token 未設置，仍保留 GitHub Models 設定；請設定 GITHUB_TOKEN、KATAGO_GITHUB_TOKEN 或在 LLM 對話框設定")
    root.after(0, lambda: messagebox.showwarning(
        t("dialog.error_title"),
        t("error.github_token_missing_env")
    ))

# 向後相容性：ollama_worker 指向 current_llm_worker
ollama_worker = current_llm_worker
update_llm_model_label(llm_provider)

update_teacher_ui(t("teacher.default_message"))
branch_ui.draw_branches()
start_analyzer_async()

def poll_ai():
    if is_shutting_down:
        return
    if not is_analyzer_ready():
        try:
            root.after(UI_POLL_INTERVAL_MS, poll_ai)
        except tk.TclError:
            pass
        return

    result = analyzer.get_result()
    # 【新增檢查】【Phase 1】如果正在整盤分析，就不要把結果畫到介面上
    if result and not analyzer.full_analyze_event.is_set():
        update_ui_with_data(result) 
    
    try:
        root.after(UI_POLL_INTERVAL_MS, poll_ai)
    except tk.TclError:
        pass


poll_ai()

root.mainloop()
