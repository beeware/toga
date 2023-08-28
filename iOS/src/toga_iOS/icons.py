from toga_iOS.libs import UIImage


class Icon:
    EXTENSIONS = [".icns", ".png", ".bmp", ".ico"]
    SIZES = None

    def __init__(self, interface, path):
        self.interface = interface
        self.path = path
        self.native = UIImage.imageWithContentsOfFile(str(path))
        if self.native is None:
            raise ValueError(f"Unable to load icon from {path}")

        # Multiple icon interface instances can end up referencing the same native
        # instance, so make sure we retain a reference count at the impl level.
        self.native.retain()

    def __del__(self):
        if self.native:
            self.native.release()
