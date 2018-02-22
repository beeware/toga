from rubicon.objc import objc_method, CGSize, SEL
from travertino.size import at_least

from toga_iOS.libs import (
    UIButton,
    UIColor,
    UIControlEventTouchDown,
    UIControlStateDisabled,
    UIControlStateNormal
)

from .base import Widget


class TogaButton(UIButton):
    @objc_method
    def onPress_(self, obj) -> None:
        if self.interface.on_press:
            self.interface.on_press(self.interface)


class Button(Widget):
    def create(self):
        self.native = TogaButton.alloc().init()
        self.native.interface = self.interface

        self.native.setTitleColor(self.native.tintColor, forState=UIControlStateNormal)
        self.native.setTitleColor(UIColor.grayColor, forState=UIControlStateDisabled)
        self.native.addTarget(self.native, action=SEL('onPress:'), forControlEvents=UIControlEventTouchDown)

        # Add the layout constraints
        self.add_constraints()

    def set_label(self, label):
        self.native.setTitle(self.interface.label, forState=UIControlStateNormal)

    def set_on_press(self, handler):
        # No special handling required.
        pass

    def rehint(self):
        fitting_size = self.native.systemLayoutSizeFittingSize(CGSize(0, 0))
        self.interface.intrinsic.width = at_least(fitting_size.width)
        self.interface.intrinsic.height = fitting_size.height
