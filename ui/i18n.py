import json
import sys
import os
from pathlib import Path


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)

    # ✅ exe 模式（onedir）
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), relative_path)

    # 開發模式
    return os.path.join(os.path.abspath('.'), relative_path)

class I18n:
    def __init__(self, base_dir, settings_path, default_language='zh_TW'):

        # ✅ 只在這裡轉一次，並轉成 Path
        self.base_dir = Path(resource_path(base_dir))
        self.settings_path = Path(settings_path)  # ⚠️ 不要 resource_path（會寫入）

        self.default_language = default_language
        self.language = default_language
        self.translations = {}

        self.available_languages = ('zh_TW', 'en')
        self.settings = {}

        self._load_settings()
        self.load_language(self._read_saved_language())

    def _load_settings(self):
        try:
            with self.settings_path.open('r', encoding='utf-8') as f:
                self.settings = json.load(f)
        except (OSError, json.JSONDecodeError):
            self.settings = {}
            print("No settings found, using defaults.")

    def save_settings(self):
        self.settings_path.parent.mkdir(parents=True, exist_ok=True)
        with self.settings_path.open('w', encoding='utf-8') as f:
            json.dump(self.settings, f, indent=2, ensure_ascii=False)

    def _read_saved_language(self):
        try:
            with self.settings_path.open('r', encoding='utf-8') as f:
                language = json.load(f).get('language', self.default_language)
                if language in self.available_languages:
                    return language
        except (OSError, json.JSONDecodeError):
            pass
        return self.default_language

    def save_language(self):
        self.settings['language'] = self.language
        self.save_settings()

    def load_language(self, language):
        if language not in self.available_languages:
            language = self.default_language

        self.language = language
        self.translations = self._load_file(language)

    def set_language(self, language):
        self.load_language(language)
        self.save_language()

    def _load_file(self, language):
        # ✅ 不要再 resource_path（已經處理過 base_dir）
        path = self.base_dir / f'{language}.json'
        try:
            with path.open('r', encoding='utf-8') as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            print("[I18N LOAD FAIL]", path)
            print("ERROR:", repr(e))
            return {}

    def t(self, key, **kwargs):
        value = self.translations.get(key, key)

        if kwargs:
            try:
                return value.format(**kwargs)
            except (KeyError, ValueError):
                return key

        return value