from rubicon.objc import objc_method
from .base import Widget
from ..libs import *
# from ..utils import process_callback


class TogaButton(UIButton):
    @objc_method
    def onPress_(self, obj) -> None:
        if self.interface._interface.on_press:
            self.interface._interface.on_press(self.interface)


class Button(Widget):
    def __init__(self, interface):
        self._interface = interface
        self._create()

    def _create(self):
        self._native = TogaButton.alloc().init()
        self._native.interface = self

        self._native.setTitleColor_forState_(self._native.tintColor, UIControlStateNormal)
        self._native.setTitleColor_forState_(UIColor.grayColor, UIControlStateDisabled)
        self._native.addTarget_action_forControlEvents_(self._native, get_selector('onPress:'), UIControlEventTouchDown)

        # Add the layout constraints
        self._add_constraints()

    def set_label(self, value):
        self._native.setTitle_forState_(value, UIControlStateNormal)

    def rehint(self):
        fitting_size = self._native.systemLayoutSizeFittingSize_(CGSize(0, 0))
        self._interface.style.hint(
            height=fitting_size.height,
            min_width=fitting_size.width,
        )
