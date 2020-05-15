from toga.constants import LEFT, RIGHT, CENTER, JUSTIFY
from travertino.size import at_least

from ..libs.android_widgets import (
    EditText,
    Gravity,
    View__MeasureSpec,
    TextWatcher,
)
from .base import Widget


class TogaTextWatcher(TextWatcher):
    def __init__(self, text_input_interface):
        super().__init__()
        self.interface = text_input_interface

    def beforeTextChanged(self, _charSequence, _i, _i1, _i2):
        pass

    def afterTextChanged(self, _editable):
        if self.interface.on_change:
            self.interface.on_change(widget=self.interface)

    def onTextChanged(self, _charSequence, _i, _i1, _i2):
        pass


class TextInput(Widget):
    def create(self):
        self.native = EditText(self._native_activity)
        self.native.addTextChangedListener(TogaTextWatcher(self.interface))

    def get_value(self):
        return self.interface._impl.native.getText().toString()

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
        self.interface.factory.not_implemented("TextInput.set_font()")

    def set_value(self, value):
        self.native.setText(value)

    def set_on_change(self, handler):
        # No special handling required.
        pass

    def rehint(self):
        self.native.measure(
            View__MeasureSpec.UNSPECIFIED, View__MeasureSpec.UNSPECIFIED
        )
        self.interface.intrinsic.width = at_least(self.native.getMeasuredWidth())
        self.interface.intrinsic.height = self.native.getMeasuredHeight()
