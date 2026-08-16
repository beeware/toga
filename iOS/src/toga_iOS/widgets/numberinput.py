from ctypes import c_int, c_void_p
from decimal import InvalidOperation

from rubicon.objc import (
    SEL,
    CGPoint,
    CGSize,
    NSRange,
    objc_method,
    objc_property,
    send_message,
    send_super,
)
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
    def pointInside_withEvent_(self, point: CGPoint, event) -> bool:  # pragma: no cover
        # To keep consistency with non-mobile platforms, we'll resign the
        # responder status when you tap somewhere outside this view. This can't
        # be emulated in CI because it requires an actual touch event; however,
        # it's entirely cosmetic, so we can live with the missing coverage.
        point_inside = send_super(
            __class__,
            self,
            "pointInside:withEvent:",
            point,
            event,
            argtypes=[CGPoint, c_void_p],
        )
        if not bool(point_inside):
            # The delay is required for proper animation of keyboard dismissal
            # for some reason.
            self.performSelector(
                SEL("resignFirstResponder"),
                withObject=None,
                afterDelay=0.0,
            )
        return point_inside

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
        return (
            len(chars) == 0
            or chars.isdigit()
            or (chars == "." and "." not in self.text)
            or (chars == "-" and textRange.location == 0)
        )

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

    def set_text_align(self, value):
        self.native.textAlignment = NSTextAlignment(value)

    def set_font(self, font):
        self.native.font = font._impl.native

    def set_color(self, color):
        self.native.textColor = native_color(color)

    def rehint(self):
        # Height of a number input is known.
        fitting_size = self.native.systemLayoutSizeFittingSize(CGSize(0, 0))
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = fitting_size.height
