class Icon:
    EXTENSIONS = [".png", ".bmp", ".ico"]
    SIZES = None

    def __init__(self, interface, path, size=None):
        self.interface = interface
        self.path = path
        self.size = size
