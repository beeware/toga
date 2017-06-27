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
    def create(self):
        self.native = TogaButton.alloc().init()
        self.native.interface = self.interface

        self.native.setBezelStyle_(NSRoundedBezelStyle)
        self.native.setButtonType_(NSMomentaryPushInButton)
        self.native.setTarget_(self.native)
        self.native.setAction_(get_selector('onPress:'))

        # Add the layout constraints
        self.add_constraints()

    def set_label(self, label):
        self.native.setTitle_(label)
        self.rehint()

    def rehint(self):
        fitting_size = self.native.fittingSize()
        self.interface.style.hint(
            height=fitting_size.height,
            min_width=fitting_size.width,
        )



