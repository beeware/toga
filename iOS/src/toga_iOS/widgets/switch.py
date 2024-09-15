from rubicon.objc import SEL, CGSize, objc_method, objc_property
from travertino.size import at_least

from toga_iOS.colors import native_color
from toga_iOS.libs import (
    UIControlEventValueChanged,
    UILabel,
    UILayoutConstraintAxis,
    UIStackView,
    UIStackViewAlignment,
    UISwitch,
)
from toga_iOS.widgets.base import Widget


class TogaStackView(UIStackView):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)


class TogaSwitch(UISwitch):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def onPress_(self, obj) -> None:
        self.interface.on_change()


class Switch(Widget):
    SPACING = 10

    def create(self):
        self.native = TogaStackView.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self
        self.native.axis = UILayoutConstraintAxis.Horizontal
        self.native.alignment = UIStackViewAlignment.Center
        self.native.spacing = self.SPACING

        self.native_label = UILabel.alloc().init()

        self.native_switch = TogaSwitch.alloc().init()
        self.native_switch.interface = self.interface
        self.native_switch.addTarget(
            self.native_switch,
            action=SEL("onPress:"),
            forControlEvents=UIControlEventValueChanged,
        )

        # Add switch and label to UIStackView
        self.native.addArrangedSubview(self.native_label)
        self.native.addArrangedSubview(self.native_switch)

        # Add the layout constraints
        self.add_constraints()

    def get_text(self):
        return str(self.native_label.text)

    def set_text(self, text):
        self.native_label.text = text

    def get_value(self):
        return self.native_switch.isOn()

    def set_value(self, value):
        old_value = self.native_switch.isOn()
        self.native_switch.setOn(value, animated=True)
        if value != old_value:
            self.interface.on_change()

    def get_enabled(self):
        return self.native_switch.isEnabled()

    def set_enabled(self, value):
        self.native_label.enabled = value
        self.native_switch.enabled = value

    def set_font(self, font):
        self.native_label.font = font._impl.native

    def set_color(self, value):
        self.native_label.textColor = native_color(value)

    def rehint(self):
        label_size = self.native_label.systemLayoutSizeFittingSize(CGSize(0, 0))
        switch_size = self.native_switch.systemLayoutSizeFittingSize(CGSize(0, 0))
        self.interface.intrinsic.width = at_least(
            label_size.width + self.SPACING + switch_size.width
        )
        self.interface.intrinsic.height = max(label_size.height, switch_size.height)
