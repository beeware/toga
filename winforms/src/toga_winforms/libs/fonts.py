from ctypes.wintypes import HDC, HFONT

import System.Windows.Forms as WinForms
from System.Drawing import ContentAlignment

from toga.constants import CENTER, JUSTIFY, LEFT, RIGHT

from .gdi32 import DeleteObject, SelectObject


def TextAlignment(value):
    return {
        LEFT: ContentAlignment.TopLeft,
        RIGHT: ContentAlignment.TopRight,
        CENTER: ContentAlignment.TopCenter,
        JUSTIFY: ContentAlignment.TopLeft,
    }[value]


# Justify simply sets Left alignment. Is this the best option?
def HorizontalTextAlignment(value):
    return {
        LEFT: WinForms.HorizontalAlignment.Left,
        RIGHT: WinForms.HorizontalAlignment.Right,
        CENTER: WinForms.HorizontalAlignment.Center,
        JUSTIFY: WinForms.HorizontalAlignment.Left,
    }[value]


class FontDeviceContext:
    """A context manager for drawing with a given font in a given device context."""

    def __init__(
        self,
        handle_device_context: HDC,
        handle_font: HFONT,
    ):
        self._hdc = handle_device_context
        self._hfont = handle_font

    def __enter__(self):
        self._hfont_old = SelectObject(self._hdc, self._hfont)

    def __exit__(self, exc_type, exc_value, traceback):
        SelectObject(self._hdc, self._hfont_old)

    def __del__(self):
        DeleteObject(self._hfont)
