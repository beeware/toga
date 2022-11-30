from java import jint

from android.graphics import Color
from toga.colors import rgba


def toga_color(color_int):
    # Select the `int` overloads rather than the `long` ones.
    color_int = jint(color_int)
    return rgba(
        Color.red(color_int),
        Color.green(color_int),
        Color.blue(color_int),
        Color.alpha(color_int) / 255,
    )
