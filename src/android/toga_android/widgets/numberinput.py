from decimal import Decimal

from travertino.size import at_least

from ..libs.android_widgets import (
    EditText,
    Gravity,
    InputType,
    TextWatcher,
    TypedValue,
    View__MeasureSpec
)
from .base import Widget, align


def decimal_from_string(s):
    """If s is the empty string, return `None`. Otherwise, convert to a `Decimal`,
    allowing any exceptions to bubble up."""
    if not s:
        return None
    return Decimal(s)


def string_from_decimal(d):
    '''Implement the inverse of `decimal_from_string()`. This way, Toga's
    `NumericInput` can pass us a `None` or `Decimal`, and we can always place
    a String in the Android `EditText`.'''
    if d is None:
        return ""
    return str(d)


class TogaNumberInputWatcher(TextWatcher):
    def __init__(self, impl):
        super().__init__()
        self.interface = impl.interface

    def beforeTextChanged(self, _charSequence, _start, _count, _after):
        pass

    def afterTextChanged(self, editable):
        # Toga `NumberInput` stores the value as a property on the `interface`.
        self.interface._value = decimal_from_string(editable.toString())
        # Call the user on_change callback, if it exists.
        if self.interface.on_change:
            self.interface.on_change(widget=self.interface)

    def onTextChanged(self, _charSequence, _start, _before, _count):
        pass


class NumberInput(Widget):
    def create(self):
        self.native = EditText(self._native_activity)
        self.native.addTextChangedListener(TogaNumberInputWatcher(self))

        # A `NumberInput` in Toga supports signed decimal numbers.
        self.native.setInputType(
            InputType.TYPE_CLASS_NUMBER
            | InputType.TYPE_NUMBER_FLAG_DECIMAL
            | InputType.TYPE_NUMBER_FLAG_SIGNED
        )

    def set_readonly(self, value):
        self.native.setFocusable(not value)

    def set_placeholder(self, value):
        # Android EditText's setHint() requires a Python string.
        self.native.setHint(value if value is not None else "")

    def set_alignment(self, value):
        self.native.setGravity(Gravity.CENTER_VERTICAL | align(value))

    def set_font(self, font):
        if font:
            font_impl = font.bind(self.interface.factory)
            self.native.setTextSize(TypedValue.COMPLEX_UNIT_SP, font_impl.get_size())
            self.native.setTypeface(font_impl.get_typeface(), font_impl.get_style())

    def set_value(self, value):
        # Store a string in the Android widget. The `afterTextChanged` method
        # will call the user on_change handler.
        self.native.setText(string_from_decimal(value))

    def set_step(self, step):
        self.interface.factory.not_implemented("NumberInput.set_step()")

    def set_max_value(self, value):
        self.interface.factory.not_implemented("NumberInput.set_max_value()")

    def set_min_value(self, value):
        self.interface.factory.not_implemented("NumberInput.set_min_value()")

    def set_on_change(self, handler):
        # No special handling required.
        pass

    def rehint(self):
        self.native.measure(
            View__MeasureSpec.UNSPECIFIED, View__MeasureSpec.UNSPECIFIED
        )
        self.interface.intrinsic.width = at_least(self.native.getMeasuredWidth())
        self.interface.intrinsic.height = self.native.getMeasuredHeight()
