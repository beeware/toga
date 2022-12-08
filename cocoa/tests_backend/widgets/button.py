from pytest import skip

from toga_cocoa.libs import NSButton

from .base import SimpleProbe


class ButtonProbe(SimpleProbe):
    native_class = NSButton

    @property
    def text(self):
        return self.native.title

    @property
    def color(self):
        skip("Can't get/set the color of a button")
