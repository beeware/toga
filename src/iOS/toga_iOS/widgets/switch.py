from rubicon.objc import objc_method, CGSize, SEL
from toga_iOS.libs import(
    UIControlEventValueChanged,
    UILabel,
    UILayoutConstraintAxis,
    UIStackView,
    UISwitch,
)
from travertino.size import at_least

from .base import Widget


class TogaSwitch(UISwitch):
    @objc_method
    def onPress_(self, obj) -> None:
        if self.interface.on_toggle:
            self.interface.on_toggle(self.interface)


class Switch(Widget):
    def create(self):
        self.native = UIStackView.alloc().init()
        self.native.interface = self.interface
        self.native.axis = UILayoutConstraintAxis.Horizontal

        self.native_label = UILabel.alloc().init()

        self.native_switch = TogaSwitch.alloc().init()
        self.native_switch.interface = self.interface
        self.native_switch.addTarget_action_forControlEvents_(self.native_switch, SEL('onPress:'),
                                                              UIControlEventValueChanged)
        # Add switch and label to UIStackView
        self.native.addArrangedSubview_(self.native_label)
        self.native.addArrangedSubview_(self.native_switch)
        
        # Add the layout constraints
        self.add_constraints()

    def set_label(self, label):
        self.native_label.text = str(self.interface.label)
        self.rehint()

    def set_is_on(self, value):
        self.native_switch.setOn_animated_(value, True)

    def get_is_on(self):
        return self.native_switch.isOn()

    def set_on_toggle(self, handler):
        # No special handling required
        pass

    def get_enabled(self):
        value = self.native_switch.isEnabled()
        if value == 1:
            return True
        elif value == 0:
            return False
        else:
            raise RuntimeError('Undefined value for enabled: {} in {}'.format(value, __class__))

    def set_enabled(self, value):
        if value:
            self.native_label.enabled = True
            self.native_switch.enabled = True
        else:
            self.native_label.enabled = False
            self.native_switch.enabled = False

    def rehint(self):
        fitting_size = self.native.systemLayoutSizeFittingSize_(CGSize(0, 0))
        self.interface.intrinsic.width = at_least(fitting_size.width)
        self.interface.intrinsic.height = fitting_size.height
