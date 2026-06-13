import subprocess

subprocess.run(
    [
        "py",
        "-3.13",
        "-m",
        "PyInstaller",
        "GoTeacher.spec"
    ],
    check=True
)