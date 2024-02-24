class Document:
    def __init__(self, interface):
        self.interface = interface

    def open(self):
        self.interface.read()
