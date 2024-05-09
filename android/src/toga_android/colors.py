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


def native_color_from_toga_color(toga_color):
    try:
        native_color = COLOR_CACHE[toga_color]
    except KeyError:
        native_color = Color.argb(
            int(toga_color.rgba.a * 255),
            int(toga_color.rgba.r),
            int(toga_color.rgba.g),
            int(toga_color.rgba.b),
        )
        COLOR_CACHE[toga_color] = native_color

    return native_color


def toga_color_from_native_color(native_color):
    # Select the `int` overloads rather than the `long` ones.
    color_int = jint(native_color)
    if color_int == 0:  # pragma: no cover
        return TRANSPARENT
    else:
        return rgba(
            Color.red(color_int),
            Color.green(color_int),
            Color.blue(color_int),
            Color.alpha(color_int) / 255,
        )
