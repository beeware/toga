from android.graphics import Color
from android.os import Build
from android.text import Layout
from android.view import Gravity
from java import jint

from toga.colors import TRANSPARENT, rgba
from toga.constants import BOTTOM, CENTER, JUSTIFY, LEFT, RIGHT, TOP


def toga_color(color_int):
    # Select the `int` overloads rather than the `long` ones.
    color_int = jint(color_int)
    if color_int == 0:
        return TRANSPARENT
    else:
        return rgba(
            Color.red(color_int),
            Color.green(color_int),
            Color.blue(color_int),
            Color.alpha(color_int) / 255,
        )


def toga_alignment(gravity, justification_mode=None):
    horizontal_gravity = gravity & Gravity.HORIZONTAL_GRAVITY_MASK
    if (Build.VERSION.SDK_INT < 26) or (
        justification_mode in (None, Layout.JUSTIFICATION_MODE_NONE)
    ):
        return {
            Gravity.LEFT: LEFT,
            Gravity.RIGHT: RIGHT,
            Gravity.CENTER_HORIZONTAL: CENTER,
        }[horizontal_gravity]
    elif (
        justification_mode == Layout.JUSTIFICATION_MODE_INTER_WORD
        and horizontal_gravity == Gravity.LEFT
    ):
        return JUSTIFY
    else:
        raise ValueError(f"unknown combination: {gravity=}, {justification_mode=}")


def toga_vertical_alignment(gravity):
    vertical_gravity = gravity & Gravity.VERTICAL_GRAVITY_MASK
    return {
        Gravity.TOP: TOP,
        Gravity.BOTTOM: BOTTOM,
        Gravity.CENTER_VERTICAL: CENTER,
    }[vertical_gravity]
