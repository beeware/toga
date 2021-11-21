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
    SYSTEM,
)
from travertino.fonts import Font as BaseFont  # noqa: F401
from travertino.fonts import font  # noqa: F401
from travertino import constants  # noqa: F401


SYSTEM_DEFAULT_FONT_SIZE = -1
_REGISTERED_FONT_CACHE = {}


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
    def register(family, path, weight=NORMAL, style=NORMAL, variant=NORMAL):
        """
        Registers a file-based font with it's family name, style, variant and weight.
        When invalid values for style, variant or weight are passed, NORMAL will be used instead.

        Platforms that support dynamic font loading will load the font from the supplied path when a toga style
        references the registered font. When a font file includes multiple font weight/style/variant, you will
        need to register them separately

        Font.register("Font Awesome 5 Free Solid", "resources/Font Awesome 5 Free-Solid-900.otf")\n
        Font.register("Roboto", "resources/Roboto-Regular.ttf"\n
        Font.register("Roboto", "resources/Roboto-Bold.ttf", weight=Font.BOLD)\n
        Font.register("Bahnschrift", "resources/Bahnschrift.ttf"\n
        Font.register("Bahnschrift", "resources/Bahnschrift.ttf", weight=Font.BOLD)


        Args:
            family (str):  The font family name
            path (str):    The path to the font file, relative to the application's module directory.
            weight (str):  The font weight: Font.NORMAL (default) or a value from Font.FONT_WEIGHTS
            style (str):   The font style: Font.NORMAL (default) or a value from Font.FONT_STYLES
            variant (str): The font variant: Font.NORMAL (default) or a value from Font.FONT_VARIANTS
        """
        font_key = Font.make_registered_font_key(
            family, weight=weight, style=style, variant=variant
        )
        _REGISTERED_FONT_CACHE[font_key] = path

    @staticmethod
    def make_registered_font_key(family, weight, style, variant):
        """
        Creates a key for storing a registered font in the font cache.\n
        If weight, style or variant contain an invalid value, Font.NORMAL is used instead

        Args:
            family (str):  The font family name
            weight (str):  The font weight: Font.NORMAL (default) or a value from Font.FONT_WEIGHTS
            style (str):   The font style: Font.NORMAL (default) or a value from Font.FONT_STYLES
            variant (str): The font variant: Font.NORMAL (default) or a value from Font.FONT_VARIANTS

        Returns:
            The font key (str)
        """
        if weight not in constants.FONT_WEIGHTS:
            weight = NORMAL
        if style not in constants.FONT_STYLES:
            style = NORMAL
        if variant not in constants.FONT_VARIANTS:
            variant = NORMAL
        return "<registered_font_key: family={} weight={} style={} variant={}>".format(
            family, weight, style, variant
        )
