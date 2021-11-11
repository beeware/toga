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
REGISTERED_FONTS = {}


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

    @staticmethod
    def register(font_name, path):
        """
        Registers a file-based font under a nice family name

        Platforms that support dynamic font loading will load the font from the supplied path when a style references
        the font's family name, e.g.

        Font.register('awesome-free-solid', 'resources/Font Awesome 5 Free-Solid-900.otf')

        :param font_name: An arbitrary family name for the font
        :param path: The path to the font file, relative to the application's module directory.
        """
        REGISTERED_FONTS[font_name] = path
