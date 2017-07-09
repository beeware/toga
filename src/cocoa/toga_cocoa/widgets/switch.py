from rubicon.objc import objc_method, get_selector

from .base import Widget
from ..libs import *
from ..utils import process_callback


class TogaSwitch(NSButton):
    @objc_method
    def onPress_(self, obj) -> None:
        if self.interface.on_toggle:
            process_callback(self.interface.on_toggle(self.interface))


class Switch(Widget):

    def create(self):
        self.native = TogaSwitch.alloc().init()
        self.native.interface = self.interface

        self.native.setBezelStyle_(NSRoundedBezelStyle)
        self.native.setButtonType_(NSSwitchButton)
        self.native.setTarget_(self.native)
        self.native.setAction_(get_selector('onPress:'))

        # Add the layout constraints
        self.add_constraints()

    def set_label(self, label):
        self.native.setTitle_(label)
        self.rehint()

    def set_is_on(self, value):
        if value is True:
            self.native.state = NSOnState
        elif value is False:
            self.native.state = NSOffState

    def get_is_on(self):
        is_on = self.native.state
        if is_on == 1:
            return True
        elif is_on == 0:
            return False
        else:
            raise Exception('Undefined value for is_on of {}'.format(__class__))

    def set_enabled(self, value):
        if value is True:
            self.native.enabled = True
        elif value is False:
            self.native.enabled = False

    def get_enabled(self):
        enabled = self.native.isEnabled()
        if enabled == 1:
            return True
        elif enabled == 0:
            return False
        else:
            raise Exception('Undefined value for enabled of {}'.format(__class__))

    def rehint(self):
        fitting_size = self.native.fittingSize()
        self.interface.style.hint(
            height=fitting_size.height,
            min_width=fitting_size.width,
        )
