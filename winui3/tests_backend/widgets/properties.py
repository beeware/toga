from win32more.Microsoft.UI.Xaml import TextAlignment
from win32more.Microsoft.UI.Xaml.Media import Brush, SolidColorBrush

from toga import rgba as TogaColor
from toga.constants import TRANSPARENT
from toga.style.pack import CENTER, JUSTIFY, LEFT, RIGHT


def brush_to_color(brush: Brush):
    if not brush:
        return

    color = SolidColorBrush(value=brush.value).Color
    color_tuple = (color.R, color.G, color.B, color.A / 255)

    if color_tuple == (0, 0, 0, 0):
        return TRANSPARENT

    return TogaColor(*color_tuple)


def toga_x_text_align(alignment):
    return {
        TextAlignment.Left: LEFT,
        TextAlignment.Right: RIGHT,
        TextAlignment.Center: CENTER,
        TextAlignment.Justify: JUSTIFY,
    }[alignment]
