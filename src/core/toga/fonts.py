# Use the Travertino font definitions as-is
from travertino.fonts import font, Font as BaseFont
from travertino.constants import (
    NORMAL,
    SYSTEM, MESSAGE,
    SERIF, SANS_SERIF, CURSIVE, FANTASY, MONOSPACE,
    ITALIC, OBLIQUE,
    SMALL_CAPS,
    BOLD,
)


SYSTEM_DEFAULT_FONT_SIZE = -1


class Font(BaseFont):
    def __init__(self, family, size, style=NORMAL, variant=NORMAL, weight=NORMAL):
        super().__init__(family, size, style, variant, weight)
        self.factory = None
        self._impl = None

    def bind(self, factory):
        self.factory = factory
        self._impl = factory.Font(self)
        return self._impl

    def measure(self, text, dpi, tight=False):
        return self._impl.measure(text, dpi=dpi, tight=tight)
