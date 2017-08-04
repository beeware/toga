from rubicon.objc import objc_method
from .base import Widget
from ..libs import *


# from ..utils import process_callback


class TogaButton(UIButton):
    @objc_method
    def onPress_(self, obj) -> None:
        if self.interface.on_press:
            self.interface.on_press(self.interface)


class Button(Widget):
    def create(self):
        self.native = TogaButton.alloc().init()
        self.native.interface = self.interface

        self.native.setTitleColor_forState_(self.native.tintColor, UIControlStateNormal)
        self.native.setTitleColor_forState_(UIColor.grayColor, UIControlStateDisabled)
        self.native.addTarget_action_forControlEvents_(self.native, SEL('onPress:'), UIControlEventTouchDown)

        # Add the layout constraints
        self.add_constraints()

    def set_label(self, label):
        self.native.setTitle_forState_(label, UIControlStateNormal)

    def rehint(self):
        fitting_size = self.native.systemLayoutSizeFittingSize_(CGSize(0, 0))
        self.interface.style.hint(
            height=fitting_size.height,
            min_width=fitting_size.width,
        )
