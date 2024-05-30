from android import R
from android.graphics import Color
from java import jint
from org.beeware.android import MainActivity
from travertino.colors import TRANSPARENT

from toga.colors import rgba

typed_array = MainActivity.singletonThis.getTheme().obtainStyledAttributes(
    [R.attr.colorBackground]
)
DEFAULT_BACKGROUND_COLOR = typed_array.getColor(0, 0)
typed_array.recycle()

COLOR_CACHE = {
    TRANSPARENT: Color.TRANSPARENT,
}


def native_color(c):
    try:
        color = COLOR_CACHE[c]
    except KeyError:
        color = Color.argb(
            int(c.rgba.a * 255),
            int(c.rgba.r),
            int(c.rgba.g),
            int(c.rgba.b),
        )
        COLOR_CACHE[c] = color

    return native_color


def toga_color(c):  # pragma: no cover
    # Select the `int` overloads rather than the `long` ones.
    color_int = jint(c)
    if color_int == 0:
        return TRANSPARENT
    else:
        return rgba(
            Color.red(color_int),
            Color.green(color_int),
            Color.blue(color_int),
            Color.alpha(color_int) / 255,
        )
