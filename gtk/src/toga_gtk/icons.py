import sys
from pathlib import Path

import toga

from .libs import GTK_VERSION, Gdk, GdkPixbuf, GLib, Gtk


class Icon:
    EXTENSIONS = [".png", ".ico", ".icns"]
    SIZES = [512, 256, 128, 72, 64, 32, 16]

    def __init__(self, interface, path, size=None):
        self.interface = interface
        self._native = {}
        self.size = size

        if path is None:
            # Use the executable location to find the share folder; look for icons
            # matching the app bundle in that location.
            hicolor = Path(sys.executable).parent.parent / "share/icons/hicolor"
            path = {
                size: hicolor / f"{size}x{size}/apps/{toga.App.app.app_id}.png"
                for size in self.SIZES
                if (hicolor / f"{size}x{size}/apps/{toga.App.app.app_id}.png").is_file()
            }

        self.paths = path

        if not path:
            raise FileNotFoundError("No icon variants found")

        # Preload all the required icon sizes
        try:
            for size, path in self.paths.items():
                if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
                    native = GdkPixbuf.Pixbuf.new_from_file(str(path)).scale_simple(
                        size, size, GdkPixbuf.InterpType.BILINEAR
                    )
                else:  # pragma: no-cover-if-gtk3
                    native = Gtk.Image.new_from_paintable(
                        Gdk.Texture.new_from_filename(str(path))
                    )
                self._native[size] = native
        except GLib.GError as exc:
            raise ValueError(f"Unable to load icon from {path}") from exc

    def native(self, size):
        pixel_size = self.size
        if pixel_size is None and GTK_VERSION < (4, 0, 0):
            pixel_size = size
        try:
            return self._native[pixel_size]
        except KeyError:
            native = self._native[next(iter(self._native))]
            if GTK_VERSION < (4, 0, 0):
                # pragma: no-cover-if-gtk4
                # self._native will have at least one entry, and it will have been
                # populated in reverse size order, so the first value returned will
                # be the largest size discovered.
                native = native.scale_simple(size, size, GdkPixbuf.InterpType.BILINEAR)
                self._native[size] = native
                return native
            else:  # pragma: no-cover-if-gtk3
                if pixel_size is not None:
                    native.set_pixel_size(self.size)
                    self._native[pixel_size] = native
                else:
                    native.set_icon_size(size)
                return native
