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
        # Hack! Because UISwitch has no label, we place it in a UITableViewCell to get a label
        self._impl = UITableViewCell.alloc().initWithStyle_reuseIdentifier_(UITableViewCellStyleDefault, 'row')
        self._impl._interface = self

        self._impl_switch = TogaSwitch.alloc().init()
        self._impl_switch._interface = self
        self._impl_switch.addTarget_action_forControlEvents_(self._impl_switch, SEL('onPress:'),
                                                             UIControlEventValueChanged)
        # Add Switch to UITableViewCell
        self._impl.accessoryView = self._impl_switch

        # Add the layout constraints
        self._add_constraints()

    def _set_label(self, value):
        self._impl.textLabel.text = str(value)

    def _set_is_on(self, value):
        self._impl_switch.setOn_animated_(value, True)

    def _get_is_on(self):
        return self._impl_switch.isOn()

    def _set_enabled(self, value):
        if value is True:
            self._impl.textLabel.enabled = True
            self._impl.accessoryView.enabled = True
        elif value is False:
            self._impl.textLabel.enabled = False
            self._impl.accessoryView.enabled = False

    def _get_enabled(self):
        enabled = self._impl.accessoryView.isEnabled()
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
