import subprocess

subprocess.run(
    [
        "py",
        "-3.13",
        "-m",
        "PyInstaller",
        "--clean",
        "GoTeacher.spec"
    ],
    check=True
)