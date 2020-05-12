class Icon:
    EXTENSIONS = [".png", "-32.png"]
    SIZES = None

    def __init__(self, interface, path):
        self.interface = interface
        self.interface._impl = self
        self.path = path
        interface.factory.not_implemented("Icon")
