from rubicon.objc import objc_method, get_selector
from .base import Widget
from ..libs import *
from ..utils import process_callback


class TogaButton(NSButton):
    @objc_method
    def onPress_(self, obj) -> None:
        if self.interface.on_press:
            process_callback(self.interface.on_press(self.interface))


class Button(Widget):
    def __init__(self, creator):
        self._creator = creator
        self._create()

    def _create(self):
        self._native = TogaButton.alloc().init()
        self._native.interface = self._creator

        self._native.setBezelStyle_(NSRoundedBezelStyle)
        self._native.setButtonType_(NSMomentaryPushInButton)
        self._native.setTarget_(self._native)
        self._native.setAction_(get_selector('onPress:'))

        # Add the layout constraints
        self._add_constraints()

    def set_label(self, label):
        self._native.setTitle_(label)
        self.rehint()

    def rehint(self):
        fitting_size = self._native.fittingSize()
        self._creator.style.hint(
            height=fitting_size.height,
            min_width=fitting_size.width,
        )



