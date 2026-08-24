from pytest import xfail

from toga.constants import SwitchRole
from toga_cocoa.libs import NSButton, NSView

from .base import SimpleProbe


class _CheckboxProbe(SimpleProbe):
    native_class = NSButton

    @property
    def text(self):
        return str(self.native.title)

    @property
    def color(self):
        xfail("Can't get/set the text color of a switch on macOS")


class _SwitchProbe(_CheckboxProbe):
    native_class = NSView

    async def press(self):
        self.impl.switch_native.performClick(None)

    @property
    def text(self):
        return str(self.impl.label_native.stringValue)

    @property
    def enabled(self):
        return self.impl.switch_native.isEnabled

    @property
    def font(self):
        return self.impl.label_native.font


# noinspection PyPep8Naming
def SwitchProbe(widget):
    if widget.role in {SwitchRole.SWITCH, SwitchRole.MAJOR}:
        return _SwitchProbe(widget)
    return _CheckboxProbe(widget)
