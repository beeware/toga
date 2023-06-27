from .libs import GdkPixbuf


class Icon:
    EXTENSIONS = [".png", ".ico", ".icns"]
    SIZES = [16, 32, 72]

    def __init__(self, interface, path):
        self.interface = interface
        self.paths = path

        # Preload all the required icon sizes
        for size, path in self.paths.items():
            native = GdkPixbuf.Pixbuf.new_from_file(str(path)).scale_simple(
                size, size, GdkPixbuf.InterpType.BILINEAR
            )
            setattr(self, f"native_{size}", native)
