from travertino.size import at_least

from toga_cocoa.libs import (
    SEL,
    NSBezelStyle,
    NSButton,
    NSOffState,
    NSOnState,
    NSSwitchButton,
    objc_method
)

from .base import Widget
from ..libs import objc_property


class TogaSwitch(NSButton):

    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def onPress_(self, obj) -> None:
        if self.interface.on_change:
            self.interface.on_change(self.interface)


class Switch(Widget):
    def create(self):
        self.native = TogaSwitch.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self

        self.native.bezelStyle = NSBezelStyle.Rounded
        self.native.setButtonType(NSSwitchButton)
        self.native.target = self.native
        self.native.action = SEL('onPress:')

        # Add the layout constraints
        self.add_constraints()

    def set_text(self, text):
        self.native.title = self.interface.text

    def set_font(self, font):
        if font:
            self.native.font = font.bind(self.interface.factory).native

    def set_value(self, value):
        if value is True:
            self.native.state = NSOnState
        elif value is False:
            self.native.state = NSOffState

    def get_value(self):
        value = self.native.state
        if value == 1:
            return True
        elif value == 0:
            return False
        else:
            raise Exception('Undefined value for value of {}'.format(__class__))

    def rehint(self):
        content_size = self.native.intrinsicContentSize()
        self.interface.intrinsic.height = content_size.height
        self.interface.intrinsic.width = at_least(content_size.width)

    def set_on_change(self, handler):
        pass
