"""Application version helpers for AI Go Teacher.

Run this file to update every project file that stores the app version:

    py version.py 0.1.3-beta
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


APP_VERSION = "0.3.0-beta"

PROJECT_ROOT = Path(__file__).resolve().parent
VERSION_INFO_PATH = PROJECT_ROOT / "version_info.txt"
MAIN_V3_PATH = PROJECT_ROOT / "ui" / "main_v3.py"


def version_tuple(version: str) -> tuple[int, int, int, int]:
    """Return the numeric tuple used by PyInstaller's VSVersionInfo."""
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)", version)
    if not match:
        raise ValueError("Version must start with MAJOR.MINOR.PATCH, e.g. 0.1.2-beta")
    major, minor, patch = (int(part) for part in match.groups())
    return major, minor, patch, 0


def _replace_once(pattern: str, replacement: str, text: str, path: Path) -> str:
    new_text, count = re.subn(pattern, replacement, text, count=1, flags=re.MULTILINE)
    if count != 1:
        raise RuntimeError(f"Could not update expected version field in {path}")
    return new_text


def update_version_module(version: str) -> None:
    path = Path(__file__).resolve()
    text = path.read_text(encoding="utf-8")
    text = _replace_once(
        r'^(APP_VERSION\s*=\s*)["\'][^"\']+["\']',
        rf'\1"{version}"',
        text,
        path,
    )
    path.write_text(text, encoding="utf-8")


def update_version_info(version: str) -> None:
    filevers = version_tuple(version)
    tuple_text = f"({filevers[0]},{filevers[1]},{filevers[2]},{filevers[3]})"
    text = VERSION_INFO_PATH.read_text(encoding="utf-8")
    text = re.sub(r"filevers=\([^)]+\)", f"filevers={tuple_text}", text, count=1)
    text = re.sub(r"prodvers=\([^)]+\)", f"prodvers={tuple_text}", text, count=1)
    text = re.sub(
        r"StringStruct\('FileVersion', '[^']+'\)",
        f"StringStruct('FileVersion', '{version}')",
        text,
    )
    text = re.sub(
        r"StringStruct\('ProductVersion', '[^']+'\)",
        f"StringStruct('ProductVersion', '{version}')",
        text,
    )
    VERSION_INFO_PATH.write_text(text, encoding="utf-8")


def verify_main_v3_uses_version_module() -> None:
    text = MAIN_V3_PATH.read_text(encoding="utf-8")
    required = ("from version import APP_VERSION", "dialog.about_message\", version=APP_VERSION")
    missing = [item for item in required if item not in text]
    if missing:
        raise RuntimeError(
            "ui/main_v3.py is not wired to version.py. Missing: " + ", ".join(missing)
        )


def sync_version(version: str) -> None:
    version_tuple(version)
    verify_main_v3_uses_version_module()
    update_version_module(version)
    update_version_info(version)


def main() -> None:
    parser = argparse.ArgumentParser(description="Synchronize AI Go Teacher version files.")
    parser.add_argument("version", nargs="?", default=APP_VERSION, help="Version like 0.1.2-beta")
    args = parser.parse_args()
    sync_version(args.version)
    print(f"Synced version to {args.version}")


if __name__ == "__main__":
    main()
