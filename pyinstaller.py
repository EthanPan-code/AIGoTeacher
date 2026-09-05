import subprocess

subprocess.run(
    [
        "py",
        "-3.13",
        "-m",
        "PyInstaller",
        "--clean",
        "AIGoTeacher.spec"
    ],
    check=True
)