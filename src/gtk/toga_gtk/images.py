class Image:
    def __init__(self, interface):
        self.interface = interface
        self.interface.impl = self
        self.native = None

    def load_image(self, path):
        # Not needed in GTK
        pass
