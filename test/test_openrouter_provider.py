import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from providers.openrouter_provider import (  # noqa: E402
    OPENROUTER_CHAT_ENDPOINT,
    OPENROUTER_MODELS_ENDPOINT,
    OpenRouterProvider,
    discover_openrouter_models,
)
from services.keyring_service import get_openrouter_api_key  # noqa: E402


class FakeResponse:
    def __init__(self, status_code=200, payload=None, lines=None, text=""):
        self.status_code = status_code
        self._payload = payload
        self._lines = lines or []
        self.text = text

    def json(self):
        return self._payload

    def iter_lines(self):
        return iter(self._lines)


class OpenRouterProviderTests(unittest.TestCase):
    def test_model_discovery_parses_openai_compatible_response(self):
        response = FakeResponse(payload={"data": [{"id": "openai/gpt-4o-mini"}, {"id": "google/gemini-2.0-flash-001"}]})
        with patch("requests.get", return_value=response) as request:
            result = discover_openrouter_models("sk-or-test")

        self.assertEqual(result, (True, ["openai/gpt-4o-mini", "google/gemini-2.0-flash-001"]))
        self.assertEqual(request.call_args.args[0], OPENROUTER_MODELS_ENDPOINT)
        self.assertEqual(request.call_args.kwargs["headers"]["Authorization"], "Bearer sk-or-test")

    def test_streaming_request_uses_openrouter_headers_and_emits_text(self):
        response = FakeResponse(
            lines=[
                b'data: {"choices":[{"delta":{"content":"Hello"}}]}',
                b'data: {"choices":[{"delta":{"content":" world"}}]}',
                b"data: [DONE]",
            ]
        )
        output = []
        provider = OpenRouterProvider(
            ui_callback=output.append,
            api_key="sk-or-test",
            model_name="openai/gpt-4o-mini",
            translator=lambda key, **kwargs: key,
            language_getter=lambda: "en",
        )
        with patch("requests.post", return_value=response) as request:
            provider._generate_task({"full_prompt": "Say hello", "conversation": []})

        self.assertEqual(output, ["Hello", "Hello world"])
        self.assertEqual(request.call_args.args[0], OPENROUTER_CHAT_ENDPOINT)
        headers = request.call_args.kwargs["headers"]
        self.assertEqual(headers["Authorization"], "Bearer sk-or-test")
        self.assertEqual(headers["HTTP-Referer"], "https://github.com/EthanPan-code/AIGoTeacher")
        self.assertEqual(headers["X-OpenRouter-Title"], "AI Go Teacher")

    def test_mid_stream_error_uses_fallback(self):
        response = FakeResponse(lines=[b'data: {"error":{"message":"rate limited"}}'])
        output = []
        provider = OpenRouterProvider(
            ui_callback=output.append,
            api_key="sk-or-test",
            translator=lambda key, **kwargs: key,
            language_getter=lambda: "en",
        )
        with patch("requests.post", return_value=response):
            provider._generate_task({"fallback_text": "fallback"})

        self.assertEqual(output[-1], "fallback")

    def test_keyring_value_precedes_environment(self):
        with patch("services.keyring_service.keyring.get_password", return_value=" keyring-key "), patch.dict(
            os.environ, {"OPENROUTER_API_KEY": "environment-key"}
        ):
            self.assertEqual(get_openrouter_api_key(), "keyring-key")


if __name__ == "__main__":
    unittest.main()
