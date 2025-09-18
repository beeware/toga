import sys
from pathlib import Path

from PySide6.QtGui import QIcon

import toga

IMPL_DICT = {}


class Icon:
    EXTENSIONS = [".png", ".jpeg", ".jpg", ".gif", ".bmp", ".ico"]
    SIZES = None

    def __init__(self, interface, path):
        self.interface = interface

        if path is None:
            SIZES = [512, 256, 128, 72, 64, 32, 16]  # same as GTK for now.
            # Use the executable location to find the share folder; look for icons
            # matching the app bundle in that location.
            hicolor = Path(sys.executable).parent.parent / "share/icons/hicolor"
            sizes = {
                size: hicolor / f"{size}x{size}/apps/{toga.App.app.app_id}.png"
                for size in SIZES
                if (hicolor / f"{size}x{size}/apps/{toga.App.app.app_id}.png").is_file()
            }

            if not sizes:
                raise FileNotFoundError("No icon variants found")

            path = sizes[max(sizes)]

        self.native = QIcon(str(path))

        if self.native.isNull():
            raise ValueError(f"Unable to load icon from {path}")

        IMPL_DICT[self.native] = self

        self.path = path
