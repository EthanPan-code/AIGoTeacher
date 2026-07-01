# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

project_root = os.path.abspath(".")

a = Analysis(
    ['ui\\main_v3.py'],
    pathex=[project_root],

    binaries=[
        ('katago.exe', '.'),
    ],

    datas=[
        # ===== 語言 =====
        ('i18n', 'i18n'),

        # ===== 圖片 =====
        ('image', 'image'),

        # ===== 模型 =====
        ('models', 'models'),

        # ===== 工具 =====
        ('tools', 'tools'),

        # ===== Providers / Services =====
        ('services', 'services'),
        ('providers', 'providers'),

        # ===== 設定檔 =====
        ('analysis_example.cfg', '.'),
        ('default_gtp.cfg', '.'),
        ('cacert.pem', '.'),

        # ===== Package data required by dynamic LLM imports =====
        *collect_data_files('certifi'),
        *collect_data_files('opencc'),
    ],

    hiddenimports=[
        *collect_submodules('tkinter'),
        *collect_submodules('requests'),
        'ollama',
        *collect_submodules('ollama'),
        *collect_submodules('httpx'),
        *collect_submodules('httpcore'),
        *collect_submodules('pydantic'),
        *collect_submodules('keyring.backends'),
        *collect_submodules('jaraco'),
        *collect_submodules('win32ctypes'),
        *collect_submodules('opencc'),
        *collect_submodules('PIL'),
        'certifi',
        'charset_normalizer',
        'idna',
        'urllib3',
    ],

    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],

    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)


exe = EXE(
    pyz,
    a.scripts,

    a.binaries,
    a.zipfiles,
    a.datas,

    [],
    name='AIGoTeacher',

    debug=False,
    bootloader_ignore_signals=False,

    strip=False,
    upx=False,

    console=False,

    disable_windowed_traceback=False,
    argv_emulation=False,

    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,

    icon='image/logo.ico',
    version='version_info.txt',
)
