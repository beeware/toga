import pytest

from toga.colors import TRANSPARENT, rgba
from toga.style.pack import BOTTOM, CENTER, JUSTIFY, LEFT, RIGHT, TOP
from toga_gtk.libs import Gtk


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


def toga_xalignment(xalign, justify=None):
    try:
        return {
            0.0: JUSTIFY if justify == Gtk.Justification.FILL else LEFT,
            1.0: RIGHT,
            0.5: CENTER,
        }[xalign]
    except KeyError:
        pytest.fail(f"Can't interpret GTK x alignment {xalign} with justify {justify}")


def toga_yalignment(yalign):
    try:
        return {
            0.0: TOP,
            0.5: CENTER,
            1.0: BOTTOM,
        }[yalign]
    except KeyError:
        pytest.fail(f"Can't interpret GTK y alignment {yalign}")


def toga_alignment_from_justification(justify):
    return {
        Gtk.Justification.LEFT: LEFT,
        Gtk.Justification.RIGHT: RIGHT,
        Gtk.Justification.CENTER: CENTER,
        Gtk.Justification.FILL: JUSTIFY,
    }[justify]
