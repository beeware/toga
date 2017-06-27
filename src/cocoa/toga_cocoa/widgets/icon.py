from ..libs import NSImage


class Icon:
    EXTENSION = '.icns'

    def __init__(self, interface):
        self._interface = interface
        interface._impl = self

    def create(self, filename):
        self._native = NSImage.alloc().initWithContentsOfFile_(filename)
