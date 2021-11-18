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
from travertino import constants  # noqa: F401


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
    def register(family, path, weight=NORMAL, style=NORMAL, variant=NORMAL):
        """
        Registers a file-based font with it's family name, style, variant and weight.
        When invalid values for style, variant or weight are passed, NORMAL will be used instead.

        Platforms that support dynamic font loading will load the font from the supplied path when a toga style
        references the registered font, e.g.

        Font.register("Font Awesome 5 Free Solid", "resources/Font Awesome 5 Free-Solid-900.otf")

        Font.register("Roboto", "resources/Roboto-Bold.ttf", weight=Font.BOLD)

        Args:
            family (str):  The font family name
            path (str):    The path to the font file, relative to the application's module directory.
            weight (str):  The font weight: Font.NORMAL (default) or a value from Font.FONT_WEIGHTS
            style (str):   The font style: Font.NORMAL (default) or a value from Font.FONT_STYLES
            variant (str): The font variant: Font.NORMAL (default) or a value from Font.FONT_VARIANTS
        """
        registered_font = RegisteredFont(family, path, weight=weight, style=style, variant=variant)
        REGISTERED_FONTS[registered_font.key()] = registered_font

    @staticmethod
    def find_registered_font(family, weight=NORMAL, style=NORMAL, variant=NORMAL):
        """
        Returns the RegisteredFont which has been registered with Font.register()
        When the exact family/weight/style/variant combination has not been registered, the method tries
        to return the RegisteredFont for the registered family only, e.g.

        registered_font = Font.find_registered_font("Roboto", weight=Font.BOLD)

        Args:
            family (str):  The font family name
            weight (str):  The font weight: Font.NORMAL (default) or a value from Font.FONT_WEIGHTS
            style (str):   The font style: Font.NORMAL (default) or a value from Font.FONT_STYLES
            variant (str): The font variant: Font.NORMAL (default) or a value from Font.FONT_VARIANTS
        Returns:
            The RegisteredFont or None
        """
        font_key = RegisteredFont.get_key(family, weight, style, variant)
        try:
            return REGISTERED_FONTS[font_key]
        except KeyError:
            try:
                if weight != NORMAL or style != NORMAL or variant != NORMAL:
                    font_key_family = RegisteredFont.get_key(family, NORMAL, NORMAL, NORMAL)
                    print("Registered font " + font_key + " not found. Using " + font_key_family + " instead.")
                    return REGISTERED_FONTS[font_key_family]
                else:
                    return None
            except KeyError:
                print("Registered font " + font_key_family + " not found.")
                return None


class RegisteredFont():
    def __init__(self, family, path, weight=NORMAL, style=NORMAL, variant=NORMAL):
        self.family = family
        self.path = path
        self.weight = weight if weight in constants.FONT_WEIGHTS else NORMAL
        self.style = style if style in constants.FONT_STYLES else NORMAL
        self.variant = variant if variant in constants.FONT_VARIANTS else NORMAL

    def key(self):
        return "<RegisteredFont family={} weight={} style={} variant={}>".format(
            self.family,
            self.weight,
            self.style,
            self.variant
        )

    @staticmethod
    def get_key(family, weight, style, variant):
        if weight not in constants.FONT_WEIGHTS:
            weight = NORMAL
        if style not in constants.FONT_STYLES:
            style = NORMAL
        if variant not in constants.FONT_VARIANTS:
            variant = NORMAL
        return "<RegisteredFont family={} weight={} style={} variant={}>".format(
            family,
            weight,
            style,
            variant
        )
