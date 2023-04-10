import warnings

# Use the Travertino font definitions as-is
from travertino import constants
from travertino.constants import ITALIC  # noqa: F401
from travertino.constants import (  # noqa: F401
    BOLD,
    CURSIVE,
    FANTASY,
    MESSAGE,
    MONOSPACE,
    NORMAL,
    OBLIQUE,
    SANS_SERIF,
    SERIF,
    SMALL_CAPS,
    SYSTEM,
)
from travertino.fonts import font  # noqa: F401
from travertino.fonts import Font as BaseFont

from toga.platform import get_platform_factory

SYSTEM_DEFAULT_FONT_SIZE = -1
_REGISTERED_FONT_CACHE = {}


class Font(BaseFont):
    def __init__(self, family, size, style=NORMAL, variant=NORMAL, weight=NORMAL):
        super().__init__(family, size, style, variant, weight)
        self.factory = get_platform_factory()
        self._impl = self.factory.Font(self)

    def bind(self, factory=None):
        warnings.warn(
            "Fonts no longer need to be explicitly bound.", DeprecationWarning
        )
        return self._impl

    def measure(self, text, dpi, tight=False):
        return self._impl.measure(text, dpi=dpi, tight=tight)

    @staticmethod
    def register(family, path, weight=NORMAL, style=NORMAL, variant=NORMAL):
        """Registers a file-based font with its family name, style, variant
        and weight. When invalid values for style, variant or weight are
        passed, ``NORMAL`` will be used.

        When a font file includes multiple font weight/style/etc., each variant
        must be registered separately::

            # Register a simple regular font
            Font.register("Font Awesome 5 Free Solid", "resources/Font Awesome 5 Free-Solid-900.otf")

            # Register a regular and bold font, contained in separate font files
            Font.register("Roboto", "resources/Roboto-Regular.ttf")
            Font.register("Roboto", "resources/Roboto-Bold.ttf", weight=Font.BOLD)

            # Register a single font file that contains both a regular and bold weight
            Font.register("Bahnschrift", "resources/Bahnschrift.ttf")
            Font.register("Bahnschrift", "resources/Bahnschrift.ttf", weight=Font.BOLD)

        :param family: The font family name. This is the name that can be
                referenced in style definitions.
        :param path: The path to the font file.
        :param weight: The font weight. Default value is ``NORMAL``.
        :param style: The font style. Default value is ``NORMAL``.
        :param variant: The font variant. Default value is ``NORMAL``.
        """
        font_key = Font.registered_font_key(
            family, weight=weight, style=style, variant=variant
        )
        _REGISTERED_FONT_CACHE[font_key] = path

    @staticmethod
    def registered_font_key(family, weight, style, variant):
        """Creates a key for storing a registered font in the font cache.

        If weight, style or variant contain an invalid value, ``NORMAL`` is
        used instead.

        :param family: The font family name. This is the name that can be
            referenced in style definitions.
        :param weight: The font weight. Default value is ``NORMAL``.
        :param style: The font style. Default value is ``NORMAL``.
        :param variant: The font variant. Default value is ``NORMAL``.
        :returns: The font key
        """
        if weight not in constants.FONT_WEIGHTS:
            weight = NORMAL
        if style not in constants.FONT_STYLES:
            style = NORMAL
        if variant not in constants.FONT_VARIANTS:
            variant = NORMAL

        return family, weight, style, variant
