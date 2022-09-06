from rubicon.objc import SEL, CGSize, objc_method, objc_property
from travertino.size import at_least

from toga_iOS.libs import (
    NSTextAlignment,
    UIControlEventEditingChanged,
    UITextBorderStyle,
    UITextField
)
from toga_iOS.widgets.base import Widget


class TogaTextField(UITextField):

    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def textFieldDidChange_(self, notification) -> None:
        if self.interface.on_change:
            self.interface.on_change(self.interface)


class TextInput(Widget):
    def create(self):
        self.native = TogaTextField.new()
        self.native.interface = self.interface
        self.native.impl = self

        self.native.borderStyle = UITextBorderStyle.RoundedRect

        self.native.addTarget(
            self.native,
            action=SEL('textFieldDidChange:'),
            forControlEvents=UIControlEventEditingChanged
        )

        # Add the layout constraints
        self.add_constraints()

    def set_readonly(self, value):
        self.native.enabled = not value

    def set_placeholder(self, value):
        self.native.placeholder = value

    def get_value(self):
        return str(self.native.text)

    def set_value(self, value):
        self.native.text = value

    def set_alignment(self, value):
        if value:
            self.native.textAlignment = NSTextAlignment(value)

    def set_font(self, font):
        if font:
            self.native.font = font.bind(self.interface.factory).native

    def rehint(self):
        # Height of a text input is known.
        fitting_size = self.native.systemLayoutSizeFittingSize(CGSize(0, 0))
        self.interface.intrinsic.width = at_least(fitting_size.width)
        self.interface.intrinsic.height = fitting_size.height

    def set_on_change(self, handler):
        # No special handling required
        pass

    def set_on_gain_focus(self, handler):
        self.interface.factory.not_implemented("TextInput.set_on_gain_focus()")

    def set_on_lose_focus(self, handler):
        self.interface.factory.not_implemented("TextInput.set_on_lose_focus()")

    def set_error(self, error_message):
        self.interface.factory.not_implemented("TextInput.set_error()")

    def clear_error(self):
        self.interface.factory.not_implemented("TextInput.clear_error()")

    def is_valid(self):
        self.interface.factory.not_implemented("TextInput.is_valid()")
