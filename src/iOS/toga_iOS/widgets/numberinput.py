from ctypes import c_int
from rubicon.objc import objc_method, CGSize, NSObject, SEL, NSRange, send_message
from travertino.size import at_least

from toga_iOS.libs import NSTextAlignment, UIKeyboardType, UITextField, UITextBorderStyle, UIControlEventEditingChanged

from .base import Widget


class TogaNumericTextField(UITextField):
    @objc_method
    def textFieldDidChange_(self, notification) -> None:
        if self.interface.on_change:
            self.interface.on_change(self.interface)

    @objc_method
    def textField_shouldChangeCharactersInRange_replacementString_(self, textField, textRange: NSRange, chars) -> bool:
        # chars will be zero length in the case of a deletion
        # otherwise, accept any number, or '.' (as long as this is the first one)
        if (len(chars) == 0
                    or chars.isdigit()
                    or (chars == '.' and '.' not in self.interface.value)
                ):
            return True
        return False


class NumberInput(Widget):
    def create(self):
        self.native = TogaNumericTextField.alloc().init()
        self.native.interface = self.interface
        self.native.delegate = self.native
        self.native.borderStyle = UITextBorderStyle.RoundedRect
        # FIXME: See Rubicon #96
        # self.native.keyboardType = UIKeyboardType.DecimalPad
        send_message(
            self.native,
            'setKeyboardType:',
            UIKeyboardType.DecimalPad.value,
            restype=None,
            argtypes=[c_int]
        )

        # Make the text field respond to any content change.
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

    def set_step(self, step):
        # No implementation required.
        # Step functionality doesn't make sense on iOS
        pass

    def set_min_value(self, value):
        # No special handling required
        pass

    def set_max_value(self, value):
        # No special handling required
        pass

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
