from rubicon.objc import objc_method, CGSize, NSObject, SEL
from travertino.size import at_least

from toga_iOS.libs import NSTextAlignment, UITextField, UITextBorderStyle, UIControlEventEditingChanged

from .base import Widget


class TogaTextField(UITextField):
    @objc_method
    def textFieldDidChange_(self, notification) -> None:
        if self.interface.on_change:
            self.interface.on_change(self.interface)


class TextInput(Widget):
    def create(self):
        self.native = TogaTextField.new()
        self.native.interface = self.interface

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
        return self.native.text

    def set_value(self, value):
        self.native.text = value

    def set_alignment(self, value):
        if value:
            self.native.textAlignment = NSTextAlignment(value)

    def set_font(self, value):
        if value:
            self.native.font = value._impl.native

    def rehint(self):
        # Height of a text input is known.
        fitting_size = self.native.systemLayoutSizeFittingSize(CGSize(0, 0))
        self.interface.intrinsic.width = at_least(fitting_size.width)
        self.interface.intrinsic.height = fitting_size.height

    def set_on_change(self, handler):
        # No special handling required
        pass
