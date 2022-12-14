from pytest import xfail

from toga_cocoa.libs import NSButton

from .base import SimpleProbe
from .properties import toga_color, toga_font


class ButtonProbe(SimpleProbe):
    native_class = NSButton

    @property
    def text(self):
        return self.native.title

    @property
    def color(self):
        xfail("Can't get/set the text color of a button on macOS")

    @property
    def font(self):
        return toga_font(self.native.font)

    @property
    def background_color(self):
        if self.native.bezelColor:
            return toga_color(self.native.bezelColor)
        else:
            return None
