from travertino.size import at_least

from toga.fonts import SYSTEM_DEFAULT_FONT_SIZE

from toga_cocoa.libs import (
    SEL,
    NSBezelStyle,
    NSButton,
    NSMomentaryPushInButton,
    objc_method,
    objc_property,
)

from .base import Widget


class TogaButton(NSButton):

    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def onPress_(self, obj) -> None:
        if self.interface.on_press:
            self.interface.on_press(self.interface)


class Button(Widget):
    def create(self):
        self.native = TogaButton.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self

        self.native.bezelStyle = NSBezelStyle.Rounded
        self.native.buttonType = NSMomentaryPushInButton
        self.native.target = self.native
        self.native.action = SEL('onPress:')

        # Add the layout constraints
        self.add_constraints()

    def set_font(self, font):
        if font:
            self.native.font = font.bind(self.interface.factory).native

    def set_text(self, text):
        self.native.title = self.interface.text

    def set_on_press(self, handler):
        # No special handling required
        pass

    def rehint(self):
        # Normal Cocoa "rounded" buttons have a fixed height by definition.
        # If the user specifies any font size other than the default,
        # or specifies an explicit height for layout, switch to using a
        # RegularSquare button.
        if (
            self.interface.style.font_size != SYSTEM_DEFAULT_FONT_SIZE
            or self.interface.style.height
        ):
            self.native.bezelStyle = NSBezelStyle.RegularSquare
        else:
            self.native.bezelStyle = NSBezelStyle.Rounded

        content_size = self.native.intrinsicContentSize()
        self.interface.intrinsic.width = at_least(content_size.width)
        self.interface.intrinsic.height = content_size.height
