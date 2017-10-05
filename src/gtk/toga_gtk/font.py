
import gi
gi.require_version("Pango", "1.0")
from gi.repository import Pango


class Font:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.create()

    def create(self):
        self._impl = Pango.FontDescription.from_string(
            self.family + " " + str(self.size))
