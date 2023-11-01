from ctypes import c_int
from decimal import InvalidOperation

from rubicon.objc import SEL, CGSize, NSRange, objc_method, objc_property, send_message
from travertino.size import at_least

from toga.widgets.numberinput import _clean_decimal
from toga_iOS.colors import native_color
from toga_iOS.libs import (
    NSTextAlignment,
    UIControlEventEditingChanged,
    UIKeyboardType,
    UITextBorderStyle,
    UITextField,
)
from toga_iOS.widgets.base import Widget


class TogaNumericTextField(UITextField):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def textFieldDidChange_(self, notification) -> None:
        self.interface.on_change()

    @objc_method
    def textField_shouldChangeCharactersInRange_replacementString_(
        self,
        textField,
        textRange: NSRange,
        chars,
    ) -> bool:
        # chars will be zero length in the case of a deletion
        # otherwise, accept any number, or '.' (as long as this is the first one)
        # or `-` if it is the first character
        if (
            len(chars) == 0
            or chars.isdigit()
            or (chars == "." and "." not in self.text)
            or (chars == "-" and textRange.location == 0)
        ):
            return True
        return False

    @objc_method
    def textFieldDidEndEditing_(self, textField) -> None:
        self.impl.set_value(self.interface.value)


class NumberInput(Widget):
    def create(self):
        self.native = TogaNumericTextField.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self
        self.native.delegate = self.native
        self.native.borderStyle = UITextBorderStyle.RoundedRect
        # FIXME: See Rubicon #96
        # self.native.keyboardType = UIKeyboardType.DecimalPad
        send_message(
            self.native,
            "setKeyboardType:",
            UIKeyboardType.DecimalPad.value,
            restype=None,
            argtypes=[c_int],
        )

        # Make the text field respond to any content change.
        self.native.addTarget(
            self.native,
            action=SEL("textFieldDidChange:"),
            forControlEvents=UIControlEventEditingChanged,
        )

        # Add the layout constraints
        self.add_constraints()

    def get_readonly(self):
        return not self.native.isEnabled()

    def set_readonly(self, value):
        self.native.enabled = not value

    def set_step(self, step):
        # Step functionality isn't implemented on iOS
        pass

    def set_min_value(self, value):
        # No special handling required. Min clipping is performed
        # by the `value` getter.
        pass

    def set_max_value(self, value):
        # No special handling required. Max clipping is performed
        # by the `value` getter.
        pass

    def get_value(self):
        try:
            return _clean_decimal(str(self.native.text), self.interface.step)
        except InvalidOperation:
            return None

    def set_value(self, value):
        if value is None:
            self.native.text = ""
        else:
            self.native.text = str(value)
        self.interface.on_change()

    def set_alignment(self, value):
        self.native.textAlignment = NSTextAlignment(value)

    def set_font(self, font):
        self.native.font = font._impl.native

    def set_color(self, color):
        self.native.textColor = native_color(color)

    def set_background_color(self, color):
        self.set_background_color_simple(color)

    def rehint(self):
        # Height of a text input is known.
        fitting_size = self.native.systemLayoutSizeFittingSize(CGSize(0, 0))
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = fitting_size.height
