from rubicon.objc import objc_method

from toga.interface import Switch as SwitchInterface

from .base import WidgetMixin
from ..libs import *


class TogaSwitch(UISwitch):
    @objc_method
    def onPress_(self, obj) -> None:
        if self._interface.on_toggle:
            self._interface.on_toggle(self._interface)


class Switch(SwitchInterface, WidgetMixin):
    def __init__(self, label, id=None, on_toggle=None, style=None, is_on=False):
        super().__init__(label, id=id, style=style, on_toggle=on_toggle, is_on=is_on)
        self._create()

    def create(self):
        self._impl = TogaSwitch.alloc().init()
        self._impl._interface = self

        self._impl.addTarget_action_forControlEvents_(self._impl, get_selector('onPress:'), UIControlEventValueChanged)

        # Add the layout constraints
        self._add_constraints()

    def _set_label(self, value):
        Warning('{} does not implement the label functionality at the moment.'.format(__class__))

    def _set_is_on(self, value):
        self._impl.setOn_animated_(value, True)

    def _get_is_on(self):
        return self._impl.isOn()

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
        fitting_size = self._impl.systemLayoutSizeFittingSize_(CGSize(0, 0))
        self.style.hint(
            height=fitting_size.height,
            min_width=fitting_size.width,
        )
