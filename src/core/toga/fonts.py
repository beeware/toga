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

from toga.platform import get_platform_factory

SYSTEM_DEFAULT_FONT_SIZE = -1


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

    def measure(self, text, dpi, tight=False):
        return self._impl.measure(text, dpi=dpi, tight=tight)
