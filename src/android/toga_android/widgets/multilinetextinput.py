from travertino.size import at_least

from toga.constants import CENTER, JUSTIFY, LEFT, RIGHT

from ..libs.android_widgets import (
    EditText,
    Gravity,
    InputType,
)
from .base import Widget


class MultilineTextInput(Widget):
    def create(self):
        self.native = EditText(self._native_activity)
        self.native.setInputType(
            InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_FLAG_MULTI_LINE
        )
        # Place the cursor at the top of the box.
        self.native.setGravity(Gravity.TOP)

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
        self.interface.factory.not_implemented("MutlineTextInput.set_font()")

    def set_value(self, value):
        self.native.setText(value)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface.MIN_HEIGHT)
