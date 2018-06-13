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
from toga.platform import get_platform_factory


class Font(BaseFont):
    def __init__(self, family, size, style=NORMAL, variant=NORMAL, weight=NORMAL):
        super().__init__(family, size, style, variant, weight)
        self.__impl = None

    @property
    def _impl(self):
        if self.__impl is None:
            self.bind(None)
        return self.__impl

    def bind(self, factory):
        factory = get_platform_factory(factory)
        self.__impl = factory.Font(self)
        return self.__impl

    def measure(self, text, tight=False):
        return self._impl.measure(text, tight=tight)
