from rubicon.objc import objc_method

from .base import Widget
from ..libs import *
# from ..utils import process_callback


class TogaButton(UIButton):
    @objc_method
    def onPress_(self, obj) -> None:
        if self.interface.on_press:
            # process_callback(self.interface.on_press(self.interface))
            self.interface.on_press(self.interface)


class Button(Widget):
    def __init__(self, label, on_press=None, **style):
        default_style = {
            'margin': 8
        }
        default_style.update(style)
        super(Button, self).__init__(**default_style)
        self.label = label
        self.on_press = on_press

        self.startup()

    def startup(self):
        self._impl = TogaButton.alloc().init()
        self._impl.interface = self

        self._impl.setTitle_forState_(self.label, UIControlStateNormal)
        # self._impl.setTitleColor_forState_(UIColor.blackColor(), UIControlStateNormal)
        self._impl.setTitleColor_forState_(self._impl.tintColor, UIControlStateNormal)
        self._impl.addTarget_action_forControlEvents_(self._impl, get_selector('onPress:'), UIControlEventTouchDown)

        # Disable all autolayout functionality
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self._impl.setAutoresizesSubviews_(False)

        # Height of a button is known.
        if self.height is None:
            self.height = self._impl.systemLayoutSizeFittingSize_(CGSize(0, 0)).height
        # Set the minimum width of a button to be a square
        if self.min_width is None:
            self.min_width = self._impl.systemLayoutSizeFittingSize_(CGSize(0, 0)).width
