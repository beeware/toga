from .libs import Gdk, GdkPixbuf, GLib, Gtk


class Icon:
    EXTENSIONS = [".png", ".ico", ".icns"]
    SIZES = [16, 32, 72]

    def __init__(self, interface, path):
        self.interface = interface
        self.paths = path

        # Preload all the required icon sizes
        try:
            for size, path in self.paths.items():
                native = Gtk.Image.new_from_paintable(
                    Gdk.Texture.new_for_pixbuf(
                        GdkPixbuf.Pixbuf.new_from_file(str(path)).scale_simple(
                            size, size, GdkPixbuf.InterpType.BILINEAR
                        )
                    )
                )
                setattr(self, f"native_{size}", native)
        except GLib.GError:
            raise ValueError(f"Unable to load icon from {path}")
