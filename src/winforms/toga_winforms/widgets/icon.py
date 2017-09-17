# from ..libs import NSImage


class Icon:
    def __init__(self, interface):
        self.interface = interface
        interface._impl = self
        # self.native = NSImage.alloc().initWithContentsOfFile(interface.filename)
