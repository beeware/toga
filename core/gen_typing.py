from pathlib import Path

from toga import toga_core_imports

typing_path = Path(__file__).parent / "src" / "toga" / "toga_typing.py"

with typing_path.open(mode="w") as f:
    f.write("# flake8: noqa\n")  # Ignore unused imports
    for object, module in toga_core_imports.items():
        f.write(f"from {module} import {object}\n")
