from rubicon.objc import objc_method, CGSize, SEL
from toga_iOS.libs import(
    UIControlEventValueChanged,
    UISwitch,
    UITableViewCell,
    UITableViewCellStyleDefault
)

from .base import Widget


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
        self.native_switch.addTarget_action_forControlEvents_(self.native_switch, SEL('onPress:'),
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

    def set_on_toggle(self, handler):
        # No special handling required
        pass

    @property
    def enabled(self):
        value = self.native.accessoryView.isEnabled()
        if value == 1:
            return True
        elif value == 0:
            return False
        else:
            raise RuntimeError('Undefined value for enabled: {} in {}'.format(value, __class__))

    @enabled.setter
    def enabled(self, value):
        if value:
            self.native.textLabel.enabled = True
            self.native.accessoryView.enabled = True
        else:
            self.native.textLabel.enabled = False
            self.native.accessoryView.enabled = False

    def rehint(self):
        fitting_size = self.native.systemLayoutSizeFittingSize_(CGSize(0, 0))
        self.interface.style.hint(
            height=fitting_size.height,
            min_width=fitting_size.width,
        )
