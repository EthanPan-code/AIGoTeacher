import unittest
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.config_service import ConfigService
from services.provider_factory import ProviderFactory


class FakeSettingsBackend:
    def __init__(self, settings):
        self.settings = settings
        self.save_count = 0

    def save_settings(self):
        self.save_count += 1


class ProviderRemovalTests(unittest.TestCase):
    def test_only_supported_providers_are_registered(self):
        self.assertEqual(ProviderFactory.get_available_providers(), ("ollama", "nvidia", "openrouter"))

    def test_legacy_github_selection_migrates_to_ollama(self):
        backend = FakeSettingsBackend({"llm_provider": "github", "github_model": "openai/gpt-4o-mini"})
        config = ConfigService(backend)

        migrated = config.migrate_removed_github_provider("qwen2.5:3b")

        self.assertTrue(migrated)
        self.assertEqual(backend.settings["llm_provider"], "ollama")
        self.assertEqual(backend.settings["ollama_model"], "qwen2.5:3b")
        self.assertNotIn("github_model", backend.settings)
        self.assertEqual(backend.save_count, 1)

    def test_legacy_github_model_is_removed_without_changing_nvidia(self):
        backend = FakeSettingsBackend(
            {
                "llm_provider": "nvidia",
                "nvidia_model": "meta/llama-3.1-8b-instruct",
                "github_model": "openai/gpt-4o-mini",
            }
        )
        config = ConfigService(backend)

        config.migrate_removed_github_provider("qwen2.5:3b")

        self.assertEqual(backend.settings["llm_provider"], "nvidia")
        self.assertEqual(backend.settings["nvidia_model"], "meta/llama-3.1-8b-instruct")
        self.assertNotIn("github_model", backend.settings)

    def test_unknown_provider_falls_back_to_ollama(self):
        provider = ProviderFactory.create_provider(
            "github",
            ui_callback=lambda _message: None,
        )
        self.assertEqual(provider.__class__.__name__, "OllamaProvider")


if __name__ == "__main__":
    unittest.main()
