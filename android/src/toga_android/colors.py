from android import R
from android.graphics import Color
from org.beeware.android import MainActivity
from travertino.colors import TRANSPARENT

typed_array = MainActivity.singletonThis.getTheme().obtainStyledAttributes(
    [R.attr.colorBackground]
)
DEFAULT_BACKGROUND_COLOR = typed_array.getColor(0, 0)
typed_array.recycle()

CACHE = {
    TRANSPARENT: Color.TRANSPARENT,
}


def native_color(c):
    try:
        color = CACHE[c]
    except KeyError:
        color = Color.argb(
            int(c.rgba.a * 255), int(c.rgba.r), int(c.rgba.g), int(c.rgba.b)
        )
        CACHE[c] = color

    return color
