import gi

try:
    gi.require_version("Pango", "1.0")
    from gi.repository import Pango
except ImportError:
    pango = None


class Font:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.create()

    def create(self):
        if pango is None:
            raise RuntimeError(
                "'from gi.repository import Pango' failed; may need to install gir1.2-pango-1.0."
            )

        self.native = Pango.FontDescription.from_string(
            self.interface.family + " " + str(self.interface.size))
