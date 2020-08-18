# Use the Travertino font definitions as-is
from travertino.constants import (  # noqa: F401
    BOLD,
    CURSIVE,
    FANTASY,
    ITALIC,
    MESSAGE,
    MONOSPACE,
    NORMAL,
    OBLIQUE,
    SANS_SERIF,
    SERIF,
    SMALL_CAPS,
    SYSTEM
)
from travertino.fonts import Font as BaseFont  # noqa: F401
from travertino.fonts import font  # noqa: F401


SYSTEM_DEFAULT_FONT_SIZE = -1


class Font(BaseFont):
    def __init__(self, family, size, style=NORMAL, variant=NORMAL, weight=NORMAL):
        super().__init__(family, size, style, variant, weight)
        self.factory = None
        self._impl = None

    def bind(self, factory):
        if self._impl is None:
            self.factory = factory
            self._impl = factory.Font(self)
        return self._impl

    def measure(self, text, dpi, tight=False):
        return self._impl.measure(text, dpi=dpi, tight=tight)
