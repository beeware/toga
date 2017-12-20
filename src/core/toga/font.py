# Use the Travertino font definitions as-is
from travertino.fonts import font, Font
from travertino.constants import (
    NORMAL,
    SYSTEM, MESSAGE,
    SERIF, SANS_SERIF, CURSIVE, FANTASY, MONOSPACE,
    ITALIC, OBLIQUE,
    SMALL_CAPS,
    BOLD,
)
from toga.platform import get_platform_factory


def measure_text(font, text, tight=False, factory=None):
    return get_platform_factory(factory).measure_text(font, text, tight=tight)
