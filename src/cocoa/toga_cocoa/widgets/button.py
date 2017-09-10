from rubicon.objc import objc_method, SEL
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

        self.native.bezelStyle = NSRoundedBezelStyle
        self.native.buttonType = NSMomentaryPushInButton
        self.native.target = self.native
        self.native.action = SEL('onPress:')

        # Add the layout constraints
        self.add_constraints()

    def set_label(self, label):
        self.native.title = label
        self.rehint()

    def set_on_press(self, handler):
        pass

    def rehint(self):
        fitting_size = self.native.fittingSize()
        self.interface.style.hint(
            height=fitting_size.height,
            min_width=fitting_size.width,
        )



