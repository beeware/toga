from rubicon.objc import objc_method, get_selector

from toga.interface import Button as ButtonInterface

from .base import WidgetMixin
from ..libs import *
from ..utils import process_callback


class TogaButton(NSButton):
    @objc_method
    def onPress_(self, obj) -> None:
        if self._interface.on_press:
            process_callback(self._interface.on_press(self._interface))


class Button(ButtonInterface, WidgetMixin):
    def __init__(self, label, id=None, style=None, on_press=None):
        super().__init__(label, id=id, style=style, on_press=on_press)
        self.startup()

        self.label = label

    def startup(self):
        self._impl = TogaButton.alloc().init()
        self._impl._interface = self

        self._impl.setBezelStyle_(NSRoundedBezelStyle)
        self._impl.setButtonType_(NSMomentaryPushInButton)
        self._impl.setTarget_(self._impl)
        self._impl.setAction_(get_selector('onPress:'))

        # Height of a button is known.
        fitting_size = self._impl.fittingSize()
        self.style.hint(
            height=fitting_size.height,
            width=(fitting_size.width, None)
        )

        # Add the layout constraints
        self._add_constraints()

    def _set_label(self, label):
        self._impl.setTitle_(self.label)
