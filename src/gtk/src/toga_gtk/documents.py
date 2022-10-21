class Document:
    def __init__(self, interface):
        self.interface = interface
        self.interface.read()
