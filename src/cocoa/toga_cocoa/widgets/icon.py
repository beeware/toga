from toga_cocoa.libs import NSImage


class Icon:
    def __init__(self, interface):
        self.interface = interface
        interface.__impl = self
        self.native = NSImage.alloc().initWithContentsOfFile(interface.filename)
