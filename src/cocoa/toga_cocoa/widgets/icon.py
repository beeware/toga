from ..libs import NSImage


class Icon():
    EXTENSION = '.icns'

    def __init__(self, creator):
        self.creator = creator

    def create(self, filename):
        self._impl = NSImage.alloc().initWithContentsOfFile_(filename)

# TIBERIUS_ICON = Icon('tiberius', system=True)
