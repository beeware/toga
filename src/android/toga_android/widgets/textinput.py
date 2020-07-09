from travertino.size import at_least

from toga.constants import CENTER, JUSTIFY, LEFT, RIGHT

from ..libs.android_widgets import (
    EditText,
    Gravity,
    TextWatcher,
    View__MeasureSpec
)
from .base import Widget


class TogaTextWatcher(TextWatcher):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl
        self.interface = impl.interface

    def beforeTextChanged(self, _charSequence, _start, _count, _after):
        pass

    def afterTextChanged(self, _editable):
        if self.interface.on_change:
            self.interface.on_change(widget=self.interface)

    def onTextChanged(self, _charSequence, _start, _before, _count):
        pass


class TextInput(Widget):
    def create(self):
        self.native = EditText(self._native_activity)
        self.native.addTextChangedListener(TogaTextWatcher(self))

    def get_value(self):
        return self.native.getText().toString()

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
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.native.measure(
            View__MeasureSpec.UNSPECIFIED, View__MeasureSpec.UNSPECIFIED
        )
        self.interface.intrinsic.height = self.native.getMeasuredHeight()
