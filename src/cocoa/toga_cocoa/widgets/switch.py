from rubicon.objc import objc_method, get_selector

from toga.interface import Switch as SwitchInterface

from .base import WidgetMixin
from ..libs import *
from ..utils import process_callback


class TogaSwitch(NSButton):
    @objc_method
    def onPress_(self, obj) -> None:
        if self._interface.on_press:
            process_callback(self._interface.on_press(self._interface))


class Switch(SwitchInterface, WidgetMixin):
    def __init__(self, label, id=None, style=None, on_press=None, state=False):
        super().__init__(label, id=id, style=style, on_press=on_press, state=state)
        self._create()

    def create(self):
        self._impl = TogaSwitch.alloc().init()
        self._impl._interface = self

        self._impl.setBezelStyle_(NSRoundedBezelStyle)
        self._impl.setButtonType_(NSSwitchButton)
        self._impl.setTarget_(self._impl)
        self._impl.setAction_(get_selector('onPress:'))

        # Add the layout constraints
        self._add_constraints()

    def _set_label(self, label):
        self._impl.setTitle_(self.label)
        self.rehint()

    def _set_state(self, value):
        if value is True:
            self._impl.state = NSOnState
        elif value is False:
            self._impl.state = NSOffState

    def _get_state(self):
        state = self._impl.state
        if state == 1:
            return True
        elif state == 0:
            return False
        else:
            raise Exception('Undefined state of {}'.format(__class__))

    def rehint(self):
        fitting_size = self._impl.fittingSize()
        self.style.hint(
            height=fitting_size.height,
            min_width=fitting_size.width,
        )
