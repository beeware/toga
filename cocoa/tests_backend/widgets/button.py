from pytest import fail, xfail

from toga.style.pack import NONE
from toga_cocoa.libs import NSBezelStyle, NSButton, NSFont

from .base import SimpleProbe
from .properties import toga_color


class ButtonProbe(SimpleProbe):
    native_class = NSButton

    @property
    def text(self):
        return str(self.native.title)

    def assert_no_icon(self):
        assert self.native.image is None

    def assert_icon_size(self):
        icon = self.native.image
        if icon:
            assert (icon.size.width, icon.size.height) == (32, 32)
        else:
            fail("Icon does not exist")

    @property
    def icon_size(self):
        if self.native.image:
            return (self.native.image.size.width, self.native.image.size.height)
        else:
            return None

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
            or self.native.image is not None
        ):
            assert self.native.bezelStyle == NSBezelStyle.RegularSquare
        else:
            assert self.native.bezelStyle == NSBezelStyle.Rounded

        return super().height
