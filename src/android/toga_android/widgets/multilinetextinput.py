from toga.constants import LEFT

from travertino.size import at_least

from ..libs.android_widgets import (
    EditText,
    Gravity,
    InputType,
)
from .base import Widget, align


class MultilineTextInput(Widget):
    def create(self):
        self.native = EditText(self._native_activity)
        self.native.setInputType(
            InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_FLAG_MULTI_LINE
        )
        # Set default alignment
        self.set_alignment(LEFT)

    def get_value(self):
        return self.native.getText().toString()

    def set_readonly(self, value):
        self.native.setFocusable(not value)

    def set_placeholder(self, value):
        # Android EditText's setHint() requires a Python string.
        self.native.setHint(value if value is not None else "")

    def set_alignment(self, value):
        self.native.setGravity(Gravity.TOP | align(value))

    def set_font(self, value):
        self.interface.factory.not_implemented("MutlineTextInput.set_font()")

    def set_value(self, value):
        self.native.setText(value)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface.MIN_HEIGHT)
