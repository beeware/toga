from travertino.size import at_least
from rubicon.objc import objc_method, SEL

from toga_cocoa.libs import NSButton, NSRoundedBezelStyle, NSMomentaryPushInButton

from .base import Widget


class TogaButton(NSButton):
    @objc_method
    def onPress_(self, obj) -> None:
        if self.interface.on_press:
            self.interface.on_press(self.interface)


class Button(Widget):
    def create(self):
        self.native = TogaButton.alloc().init()
        self.native.interface = self.interface

        self.native.bezelStyle = NSRoundedBezelStyle
        self.native.buttonType = NSMomentaryPushInButton
        self.native.target = self.native
        self.native.action = SEL('onPress:')

        # Add the layout constraints
        self.add_constraints()

    def set_font(self, font):
        if font:
            self.native.font = font._impl.native

    def set_label(self, label):
        self.native.title = self.interface.label

    def set_on_press(self, handler):
        # No special handling required
        pass

    def rehint(self):
        content_size = self.native.intrinsicContentSize()
        self.interface.intrinsic.width = at_least(content_size.width)
        self.interface.intrinsic.height = content_size.height
