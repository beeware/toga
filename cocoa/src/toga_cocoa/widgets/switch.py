from travertino.size import at_least

from toga_cocoa.libs import (
    SEL,
    NSBezelStyle,
    NSButton,
    NSOffState,
    NSOnState,
    NSSwitchButton,
    objc_method,
    objc_property,
)

from .base import Widget


class TogaSwitch(NSButton):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def onPress_(self, obj) -> None:
        self.interface.on_change()


class Switch(Widget):
    def create(self):
        self.native = TogaSwitch.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self

        self.native.bezelStyle = NSBezelStyle.Rounded
        self.native.setButtonType(NSSwitchButton)
        self.native.target = self.native
        self.native.action = SEL("onPress:")

        # Add the layout constraints
        self.add_constraints()

    def get_text(self):
        return str(self.native.title)

    def set_text(self, text):
        self.native.title = text

    def set_font(self, font):
        self.native.font = font._impl.native

    def get_value(self):
        return self.native.state == NSOnState

    def set_value(self, value):
        old_value = self.native.state == NSOnState
        self.native.state = NSOnState if value else NSOffState
        if self.interface.on_change and value != old_value:
            self.interface.on_change()

    def rehint(self):
        content_size = self.native.intrinsicContentSize()
        self.interface.intrinsic.width = at_least(content_size.width)
        self.interface.intrinsic.height = content_size.height
