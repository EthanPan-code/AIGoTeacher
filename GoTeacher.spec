# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_submodules

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
    ],

    hiddenimports=[
        *collect_submodules('tkinter'),
    ],

    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],

    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

# =========================
# 🚀 ONEFILE 正確寫法
# =========================
exe = EXE(
    pyz,
    a.scripts,

    a.binaries,
    a.zipfiles,
    a.datas,

    [],
    name='KataGoUI',

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
)