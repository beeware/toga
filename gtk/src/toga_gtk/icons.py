import sys
from pathlib import Path

import toga

from .libs import GdkPixbuf, GLib


class Icon:
    EXTENSIONS = [".png", ".ico", ".icns"]
    SIZES = [512, 256, 128, 72, 64, 32, 16]

    def __init__(self, interface, path):
        self.interface = interface
        self._native = {}

        if path is None:
            # Use the executable location to find the share folder; look for icons
            # matching the app bundle in that location.
            usr = Path(sys.executable).parent.parent
            path = {
                size: (
                    usr
                    / f"share/icons/hicolor/{size}x{size}/apps/{toga.App.app.app_id}.png"
                )
                for size in self.SIZES
                if (
                    usr
                    / f"share/icons/hicolor/{size}x{size}/apps/{toga.App.app.app_id}.png"
                ).is_file()
            }

        self.paths = path

        if not path:
            raise FileNotFoundError("No icon variants found")

        # Preload all the required icon sizes
        try:
            for size, path in self.paths.items():
                native = GdkPixbuf.Pixbuf.new_from_file(str(path)).scale_simple(
                    size, size, GdkPixbuf.InterpType.BILINEAR
                )
                self._native[size] = native
        except GLib.GError:
            raise ValueError(f"Unable to load icon from {path}")

    def native(self, size):
        try:
            return self._native[size]
        except KeyError:
            for src_size in self._native:
                native = self._native[src_size].scale_simple(
                    size, size, GdkPixbuf.InterpType.BILINEAR
                )
                self._native[size] = native
                return native
