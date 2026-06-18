import subprocess
import shutil

path = ['build', 'dist']

for i in path:
    try:
        shutil.rmtree(i)
        print(f"{i}及其包含的所有檔案已成功刪除")
    except FileNotFoundError:
        print(f"找不到{i}")
    except PermissionError as e:
        print(f"沒有權限刪除{i}\n", e)

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