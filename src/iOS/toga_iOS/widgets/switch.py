from rubicon.objc import objc_method, CGSize
from .base import Widget
from ..libs import *


class TogaSwitch(UISwitch):
    @objc_method
    def onPress_(self, obj) -> None:
        if self.interface.on_toggle:
            self.interface.on_toggle(self.interface)


class Switch(Widget):
    def create(self):
        # Hack! Because UISwitch has no label, we place it in a UITableViewCell to get a label
        self.native = UITableViewCell.alloc().initWithStyle_reuseIdentifier_(UITableViewCellStyleDefault, 'row')
        self.native.interface = self.interface

        self.native_switch = TogaSwitch.alloc().init()
        self.native_switch.interface = self.interface
        self.native_switch.addTarget_action_forControlEvents_(self.native_switch, get_selector('onPress:'),
                                                              UIControlEventValueChanged)
        # Add Switch to UITableViewCell
        self.native.accessoryView = self.native_switch

        # Add the layout constraints
        self.add_constraints()

        fitting_size = self.native.systemLayoutSizeFittingSize_(CGSize(0, 0))
        self.interface.style.hint(
            min_height=fitting_size.height,
            min_width=fitting_size.width,
        )

    def set_label(self, label):
        self.native.textLabel.text = str(label)
        self.rehint()

    def set_is_on(self, value):
        self.native_switch.setOn_animated_(value, True)

    def get_is_on(self):
        return self.native_switch.isOn()

    def set_enabled(self, value):
        if value is True:
            self.native.textLabel.enabled = True
            self.native.accessoryView.enabled = True
        elif value is False:
            self.native.textLabel.enabled = False
            self.native.accessoryView.enabled = False

    def get_enabled(self):
        enabled = self.native.accessoryView.isEnabled()
        if enabled == 1:
            return True
        elif enabled == 0:
            return False
        else:
            raise Exception('Undefined value for enabled of {}'.format(__class__))

    def rehint(self):
        fitting_size = self.native.systemLayoutSizeFittingSize_(CGSize(0, 0))
        self.interface.style.hint(
            height=fitting_size.height,
            min_width=fitting_size.width,
        )
