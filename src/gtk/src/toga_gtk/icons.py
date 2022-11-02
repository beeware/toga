from .libs import GdkPixbuf, Gtk


class Icon:
    EXTENSIONS = [".png", ".ico", ".icns"]
    SIZES = [32, 72]

    def __init__(self, interface, path):
        self.interface = interface
        self.paths = path

        # Preload all the required icon sizes
        for size, path in self.paths.items():
            native = Gtk.Image.new_from_pixbuf(
                GdkPixbuf.Pixbuf.new_from_file(str(path)).scale_simple(
                    size, size, GdkPixbuf.InterpType.BILINEAR
                )
            )
            setattr(self, f"native_{size}", native)
