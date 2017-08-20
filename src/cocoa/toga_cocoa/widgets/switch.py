from rubicon.objc import objc_method, SEL

from toga.interface import Switch as SwitchInterface

from .base import WidgetMixin
from ..libs import *
from ..utils import process_callback


class TogaSwitch(NSButton):
    @objc_method
    def onPress_(self, obj) -> None:
        if self._interface.on_toggle:
            process_callback(self._interface.on_toggle(self._interface))


class Switch(SwitchInterface, WidgetMixin):
    def __init__(self, label, id=None, style=None, on_toggle=None, is_on=False):
        super().__init__(label, id=id, style=style, on_toggle=on_toggle, is_on=is_on)
        self._create()

    def create(self):
        self._impl = TogaSwitch.alloc().init()
        self._impl._interface = self

        self._impl.setBezelStyle_(NSRoundedBezelStyle)
        self._impl.setButtonType_(NSSwitchButton)
        self._impl.setTarget_(self._impl)
        self._impl.setAction_(SEL('onPress:'))

        # Add the layout constraints
        self._add_constraints()

    def _set_label(self, label):
        self._impl.setTitle_(self.label)
        self.rehint()

    def _set_is_on(self, value):
        if value is True:
            self._impl.state = NSOnState
        elif value is False:
            self._impl.state = NSOffState

    def _get_is_on(self):
        is_on = self._impl.state
        if is_on == 1:
            return True
        elif is_on == 0:
            return False
        else:
            raise Exception('Undefined value for is_on of {}'.format(__class__))

    def _set_enabled(self, value):
        if value is True:
            self._impl.enabled = True
        elif value is False:
            self._impl.enabled = False

    def _get_enabled(self):
        enabled = self._impl.isEnabled()
        if enabled == 1:
            return True
        elif enabled == 0:
            return False
        else:
            raise Exception('Undefined value for enabled of {}'.format(__class__))

    def rehint(self):
        fitting_size = self._impl.fittingSize()
        self.style.hint(
            height=fitting_size.height,
            min_width=fitting_size.width,
        )
