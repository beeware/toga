import sys
from pathlib import Path

from PySide6.QtGui import QIcon

import toga

from .libs import create_qapplication

IMPL_DICT = {}


class Icon:
    EXTENSIONS = [".png", ".jpeg", ".jpg", ".gif", ".bmp", ".ico"]
    SIZES = None

    def __init__(self, interface, path):
        # A QApplication must exist before pixmaps can be manipulated
        create_qapplication()
        self.interface = interface

        if path is None:
            # Briefcase's Linux application packaging still yields sized icons;
            # look for the highest size, since Qt icon sizing is handled by the
            # theme, and from Toga's perspective, they're unsized.
            SIZES = [512, 256, 128, 72, 64, 32, 16]
            hicolor = Path(sys.executable).parent.parent / "share/icons/hicolor"
            sizes = {
                size: hicolor / f"{size}x{size}/apps/{toga.App.app.app_id}.png"
                for size in SIZES
                if (hicolor / f"{size}x{size}/apps/{toga.App.app.app_id}.png").is_file()
            }

            if not sizes:  # pragma: no cover
                raise FileNotFoundError("No icon variants found")

            path = sizes[max(sizes)]

        self.native = QIcon(str(path))

        # A lot of Qt's APIs simply results in null when anything is wrong.
        if self.native.isNull():
            raise ValueError(f"Unable to load icon from {path}")

        IMPL_DICT[self.native.cacheKey()] = self

        self.path = path
