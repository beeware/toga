from pytest import xfail

from toga_cocoa.libs import NSButton

from .base import SimpleProbe


class SwitchProbe(SimpleProbe):
    native_class = NSButton

    @property
    def text(self):
        return str(self.native.title)

    @property
    def color(self):
        xfail("Can't get/set the text color of a button on macOS")
