from rubicon.objc import objc_method

from toga.interface import Button as ButtonInterface

from .base import WidgetMixin
from ..libs import *
# from ..utils import process_callback


class TogaButton(UIButton):
    @objc_method
    def onPress_(self, obj) -> None:
        if self._interface.on_press:
            # process_callback(self._interface.on_press(self._interface))
            self._interface.on_press(self._interface)


class Button(ButtonInterface, WidgetMixin):
    def __init__(self, label, id=None, on_press=None, style=None):
        super().__init__(label, id=id, style=style, on_press=on_press)
        self._create()

    def create(self):
        self._impl = TogaButton.alloc().init()
        self._impl._interface = self

        self._impl.setTitleColor_forState_(self._impl.tintColor, UIControlStateNormal)
        self._impl.addTarget_action_forControlEvents_(self._impl, get_selector('onPress:'), UIControlEventTouchDown)

        # Add the layout constraints
        self._add_constraints()

    def _set_label(self, value):
        self._impl.setTitle_forState_(value, UIControlStateNormal)

    def rehint(self):
        fitting_size = self._impl.systemLayoutSizeFittingSize_(CGSize(0, 0))
        self.style.hint(
            height=fitting_size.height,
            min_width=fitting_size.width,
        )
