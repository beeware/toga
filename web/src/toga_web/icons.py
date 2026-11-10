from typing import ClassVar


class Icon:
    EXTENSIONS: ClassVar[list[str]] = [".png", ".bmp", ".ico"]
    SIZES = None

    def __init__(self, interface, path):
        self.interface = interface
        self.path = path
