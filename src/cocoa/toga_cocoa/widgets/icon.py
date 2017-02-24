
from toga.interface import Icon as IconInterface

from ..libs import NSImage


class Icon(IconInterface):
    EXTENSION = '.icns'

    def create(self, filename):
        self._impl = NSImage.alloc().initWithContentsOfFile_(filename)


TIBERIUS_ICON = Icon('tiberius', system=True)
