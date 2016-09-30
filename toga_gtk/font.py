from toga.interface import Font as FontInterface

import gi
gi.require_version("Pango", "1.0")
from gi.repository import Pango


class Font(FontInterface):

    def create(self):
        self._impl = Pango.FontDescription.from_string(
            self.family + " " + str(self.size))
