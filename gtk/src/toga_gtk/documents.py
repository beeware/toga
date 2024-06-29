class Document:
    def __init__(self, interface):
        self.interface = interface

    def open(self):
        if self.interface.path.exists():
            self.interface.read()
        else:
            raise FileNotFoundError()
