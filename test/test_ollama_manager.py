import sys
import threading
import unittest
from pathlib import Path
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.ollama_manager import OllamaManager  # noqa: E402


class FakeResponse:
    def __init__(self, status_code=200, payload=None, lines=None, text=""):
        self.status_code = status_code
        self.payload = payload
        self.lines = lines or []
        self.text = text

    def json(self):
        return self.payload

    def iter_lines(self):
        return iter(self.lines)


class OllamaManagerTests(unittest.TestCase):
    def test_tags_classify_local_and_cloud_from_metadata(self):
        response = FakeResponse(
            payload={
                "models": [
                    {
                        "name": "gemma4:12b",
                        "model": "gemma4:12b",
                        "size": 7556508396,
                        "details": {"parameter_size": "11.9B", "quantization_level": "Q4_K_M"},
                        "capabilities": ["completion", "vision"],
                    },
                    {
                        "name": "minimax-m3:cloud",
                        "model": "minimax-m3:cloud",
                        "remote_model": "minimax-m3",
                        "remote_host": "https://ollama.com:443",
                        "capabilities": ["completion", "tools"],
                    },
                ]
            }
        )
        manager = OllamaManager("http://ollama-test")
        with patch("requests.get", return_value=response) as request:
            models, error = manager.refresh_model_catalog(force=True)

        self.assertIsNone(error)
        self.assertEqual({model.name for model in models}, {"gemma4:12b", "minimax-m3:cloud"})
        self.assertEqual(manager.get_local_models(), {"gemma4:12b"})
        self.assertEqual(manager.get_cloud_models(), {"minimax-m3:cloud"})
        self.assertTrue(manager.get_model("minimax-m3:cloud").is_cloud)
        self.assertEqual(request.call_args.args[0], "http://ollama-test/api/tags")

    def test_successful_catalog_is_cached_until_forced(self):
        response = FakeResponse(payload={"models": [{"name": "local:test"}]})
        manager = OllamaManager()
        with patch("requests.get", return_value=response) as request:
            manager.refresh_model_catalog(force=True)
            manager.refresh_model_catalog()
        self.assertEqual(request.call_count, 1)

    def test_failed_refresh_retains_last_successful_catalog(self):
        good = FakeResponse(payload={"models": [{"name": "local:test"}]})
        failed = FakeResponse(status_code=503, text="service unavailable")
        manager = OllamaManager()
        with patch("requests.get", side_effect=[good, failed]):
            manager.refresh_model_catalog(force=True)
            models, error = manager.refresh_model_catalog(force=True)

        self.assertEqual([model.name for model in models], ["local:test"])
        self.assertEqual(error, "HTTP 503")

    def test_cloud_model_cannot_be_pulled(self):
        response = FakeResponse(
            payload={
                "models": [
                    {"name": "cloud:test", "remote_model": "cloud-test", "remote_host": "https://ollama.com"}
                ]
            }
        )
        manager = OllamaManager()
        with patch("requests.get", return_value=response), patch("requests.post") as post:
            manager.refresh_model_catalog(force=True)
            completed = []
            started = manager.pull_model_async("cloud:test", complete_callback=lambda ok, msg: completed.append((ok, msg)))

        self.assertFalse(started)
        self.assertEqual(completed[0][0], False)
        post.assert_not_called()

    def test_pull_stream_reports_progress_and_refreshes_catalog(self):
        tags_response = FakeResponse(payload={"models": []})
        pull_response = FakeResponse(
            lines=[
                b'{"status":"pulling manifest"}',
                b'{"status":"downloading","completed":50,"total":100}',
            ]
        )
        manager = OllamaManager()
        progress = []
        completed = []
        finished = threading.Event()

        def on_complete(ok, message):
            completed.append((ok, message))
            finished.set()

        with patch("requests.get", return_value=tags_response), patch("requests.post", return_value=pull_response) as post:
            self.assertTrue(manager.pull_model_async("local:test", progress.append, on_complete))
            self.assertTrue(finished.wait(2))

        self.assertTrue(completed[0][0])
        self.assertTrue(any("50/100" in item for item in progress))
        self.assertEqual(post.call_args.args[0], "http://localhost:11434/api/pull")


if __name__ == "__main__":
    unittest.main()
