from rubicon.objc import objc_method, SEL
from travertino.size import at_least

from toga_cocoa.libs import (
    NSButton,
    NSOnState,
    NSOffState,
    NSRoundedBezelStyle,
    NSSwitchButton,
)

from .base import Widget


class TogaSwitch(NSButton):
    @objc_method
    def onPress_(self, obj) -> None:
        if self.interface.on_toggle:
            self.interface.on_toggle(self.interface)


class Switch(Widget):
    def create(self):
        self.native = TogaSwitch.alloc().init()
        self.native.interface = self.interface

        self.native.bezelStyle = NSRoundedBezelStyle
        self.native.setButtonType(NSSwitchButton)
        self.native.target = self.native
        self.native.action = SEL('onPress:')

        # Add the layout constraints
        self.add_constraints()

    def set_label(self, label):
        self.native.title = self.interface.label

    def set_font(self, value):
        if value:
            self.native.font = value._impl.native

    def set_is_on(self, value):
        if value is True:
            self.native.state = NSOnState
        elif value is False:
            self.native.state = NSOffState

    def get_is_on(self):
        is_on = self.native.state
        if is_on == 1:
            return True
        elif is_on == 0:
            return False
        else:
            raise Exception('Undefined value for is_on of {}'.format(__class__))

    def rehint(self):
        content_size = self.native.intrinsicContentSize()
        self.interface.intrinsic.height = content_size.height
        self.interface.intrinsic.width = at_least(content_size.width)

    def set_on_toggle(self, handler):
        pass
