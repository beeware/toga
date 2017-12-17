import gi

gi.require_version("Pango", "1.0")
from gi.repository import Pango


CACHE = {}


def font(f):
    try:
        font = CACHE[f]
    except KeyError:
        font = Pango.FontDescription.from_string('{font.family} {font.size}'.format(font=f))

    return font
