from pytest import xfail

from toga.style.pack import NONE
from toga_cocoa.libs import NSBezelStyle, NSButton, NSFont

from .base import SimpleProbe
from .properties import toga_color


class ButtonProbe(SimpleProbe):
    native_class = NSButton

    @property
    def text(self):
        return str(self.native.title)

    @property
    def color(self):
        xfail("Can't get/set the text color of a button on macOS")

    @property
    def background_color(self):
        if self.native.bezelColor:
            return toga_color(self.native.bezelColor)
        else:
            return None

    @property
    def height(self):
        # If the button has a manual height set, or has a non-default font size
        # it should have a different bezel style.
        if (
            self.widget.style.height != NONE
            or self.native.font.pointSize != NSFont.systemFontSize
        ):
            assert self.native.bezelStyle == NSBezelStyle.RegularSquare
        else:
            assert self.native.bezelStyle == NSBezelStyle.Rounded

        return super().height
