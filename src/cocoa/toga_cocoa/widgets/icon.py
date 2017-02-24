
from toga.interface import Button as ButtonInterface

from ..libs import NSImage


class Icon(IconInterface):
    def create(self, filename):
        self._impl = NSImage.alloc().initWithContentsOfFile_(filename)


TIBERIUS_ICON = Icon('tiberius.icns', system=True)
