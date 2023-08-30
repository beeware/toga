from android.graphics import BitmapFactory


class Icon:
    EXTENSIONS = [".png"]
    SIZES = None

    def __init__(self, interface, path):
        self.interface = interface
        self.interface._impl = self
        self.path = path

        self.native = BitmapFactory.decodeFile(str(path))
        if self.native is None:
            raise ValueError(f"Unable to load icon from {path}")
