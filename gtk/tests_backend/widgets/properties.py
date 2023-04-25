import pytest
from travertino.fonts import Font

from toga.colors import TRANSPARENT, rgba
from toga.fonts import BOLD, ITALIC, NORMAL, OBLIQUE, SMALL_CAPS
from toga.style.pack import CENTER, JUSTIFY, LEFT, RIGHT
from toga_gtk.libs import Gtk, Pango


def toga_color(color):
    if color:
        c = rgba(
            int(color.red * 255),
            int(color.green * 255),
            int(color.blue * 255),
            color.alpha,
        )

        # Background color of rgba(0,0,0,0.0) is TRANSPARENT.
        if c.r == 0 and c.g == 0 and c.b == 0 and c.a == 0.0:
            return TRANSPARENT
        else:
            return c
    else:
        return None


_FONT_STYLE_REVERSE_MAP = {Pango.Style.ITALIC: ITALIC, Pango.Style.OBLIQUE: OBLIQUE}

_FONT_VARIANT_REVERSE_MAP = {Pango.Variant.SMALL_CAPS: SMALL_CAPS}

_FONT_WEIGHT_REVERSE_MAP = {Pango.Weight.BOLD: BOLD}


def toga_font(font):
    return Font(
        family=font.get_family(),
        size=int(font.get_size() / Pango.SCALE),
        style=_FONT_STYLE_REVERSE_MAP.get(font.get_style(), NORMAL),
        weight=_FONT_WEIGHT_REVERSE_MAP.get(font.get_weight(), NORMAL),
        variant=_FONT_VARIANT_REVERSE_MAP.get(font.get_variant(), NORMAL),
    )


def toga_alignment(xalign, yalign, justify):
    if yalign != 0.5:
        pytest.fail("Y-alignment should be 0.5")

    try:
        return {
            (0.0, Gtk.Justification.LEFT): LEFT,
            (1.0, Gtk.Justification.RIGHT): RIGHT,
            (0.5, Gtk.Justification.CENTER): CENTER,
            (0.0, Gtk.Justification.FILL): JUSTIFY,
        }[(xalign, justify)]
    except KeyError:
        pytest.fail(f"Can't interpret GTK x alignment {xalign} with justify {justify}")
