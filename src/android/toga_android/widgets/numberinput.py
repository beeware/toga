from decimal import Decimal

from toga.constants import LEFT, RIGHT, CENTER, JUSTIFY
from travertino.size import at_least

from ..libs.android_widgets import (
    EditText,
    Gravity,
    InputType,
    View__MeasureSpec,
    TextWatcher,
)
from .base import Widget


class TogaNumberInputWatcher(TextWatcher):
    def __init__(self, number_input_interface):
        super().__init__()
        self.interface = number_input_interface

    def beforeTextChanged(self, _charSequence, _i, _i1, _i2):
        pass

    def afterTextChanged(self, _editable):
        current_string = self.interface._impl.native.getText().toString()
        new_value = Decimal(current_string) if current_string else None
        old_value = self.interface.value

        # In case we get fired twice with the same value, succeed vacuously.
        if new_value == old_value:
            return

        # Toga `NumberInput` stores the value as a property on the `interface`.
        self.interface.value = new_value

        # Call user on_change function, if needed.
        if self.interface.on_change:
            self.interface.on_change(widget=self.interface)

    def onTextChanged(self, _charSequence, _i, _i1, _i2):
        pass


class NumberInput(Widget):
    def create(self):
        self.native = EditText(self._native_activity)
        self.native.addTextChangedListener(TogaNumberInputWatcher(self.interface))
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
        self.native.setGravity(
            {
                LEFT: Gravity.CENTER_VERTICAL | Gravity.LEFT,
                RIGHT: Gravity.CENTER_VERTICAL | Gravity.RIGHT,
                CENTER: Gravity.CENTER_VERTICAL | Gravity.CENTER_HORIZONTAL,
                JUSTIFY: Gravity.CENTER_VERTICAL | Gravity.CENTER_HORIZONTAL,
            }[value]
        )

    def set_font(self, value):
        self.interface.factory.not_implemented("NumberInput.set_font()")

    def set_value(self, value):
        # Toga's `value` is a `Decimal` or `None`, but Android needs a string.
        str_value = str(value) if value is not None else ""
        if str_value == self.native.getText().toString():
            return
        self.native.setText(str_value)

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
