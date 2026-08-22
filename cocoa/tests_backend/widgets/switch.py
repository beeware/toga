from pytest import xfail

from toga_cocoa.libs import NSButton, NSView

from .base import SimpleProbe


class CheckboxSwitchProbe(SimpleProbe):
    native_class = NSButton

    @property
    def text(self):
        return str(self.native.title)

    @property
    def color(self):
        xfail("Can't get/set the text color of a switch on macOS")


class SwitchSwitchProbe(CheckboxSwitchProbe):
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
    if not isinstance(widget._impl.native, NSButton):
        return SwitchSwitchProbe(widget)
    return CheckboxSwitchProbe(widget)
