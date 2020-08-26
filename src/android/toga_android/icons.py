class Icon:
    EXTENSIONS = [".png"]
    SIZES = None

    def __init__(self, interface, path):
        self.interface = interface
        self.interface._impl = self
        self.path = path
