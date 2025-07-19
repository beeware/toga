class Icon:
    EXTENSIONS = [".png"]
    SIZES = None

    def __init__(self, interface, path, size=None):
        super().__init__()
        self.interface = interface
        self.path = path
        self.size = size
