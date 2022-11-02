class Icon:
    EXTENSIONS = [".png", ".bmp", ".ico"]
    SIZES = None

    def __init__(self, interface, path):
        self.interface = interface
        self.path = path
