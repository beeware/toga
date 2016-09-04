from rubicon.objc import objc_method

from .base import Widget
from ..libs import *
# from ..utils import process_callback


class TogaButton(UIButton):
    @objc_method
    def onPress_(self, obj) -> None:
        if self._interface.on_press:
            # process_callback(self._interface.on_press(self._interface))
            self._interface.on_press(self._interface)


class Button(Widget):
    def __init__(self, label, on_press=None, style=None):
        super(Button, self).__init__(style=style)
        self.label = label
        self.on_press = on_press

        self.startup()

    def startup(self):
        self._impl = TogaButton.alloc().init()
        self._impl._interface = self

        self._impl.setTitle_forState_(self.label, UIControlStateNormal)
        # self._impl.setTitleColor_forState_(UIColor.blackColor(), UIControlStateNormal)
        self._impl.setTitleColor_forState_(self._impl.tintColor, UIControlStateNormal)
        self._impl.addTarget_action_forControlEvents_(self._impl, get_selector('onPress:'), UIControlEventTouchDown)

        # Disable all autolayout functionality
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self._impl.setAutoresizesSubviews_(False)

        # Height of a button is known. Set the minimum width
        # of a button to be a square
        fitting_size = self._impl.systemLayoutSizeFittingSize_(CGSize(0, 0))
        self.style.hint(
            height=fitting_size.height,
            width=(fitting_size.width, None)
        )

        # Add the layout constraints
        self._add_constraints()
