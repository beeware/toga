from pytest import xfail

from toga.colors import TRANSPARENT
from toga_cocoa.libs import NSButton, NSColor

from .base import SimpleProbe
from .properties import toga_color


class SwitchProbe(SimpleProbe):
    native_class = NSButton

    @property
    def text(self):
        return str(self.native.title)

    @property
    def color(self):
        xfail("Can't get/set the text color of a button on macOS")

    @property
    def background_color(self):
        if self.native.drawsBackground and self.native.backgroundColor:
            if self.native.backgroundColor != NSColor.controlBackgroundColor:
                return toga_color(self.native.backgroundColor)
        elif not self.native.drawsBackground:
            return TRANSPARENT
        return None
