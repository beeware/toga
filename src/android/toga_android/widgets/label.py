from toga.constants import LEFT, RIGHT, CENTER, JUSTIFY
from travertino.size import at_least

from .base import Widget
from ..libs.android_widgets import (
    Gravity,
    TextView,
    View__MeasureSpec,
)


class Label(Widget):
    def create(self):
        self.native = TextView(self._native_activity)
        self.native.setSingleLine()

    def set_text(self, value):
        self.native.setText(value)

    def rehint(self):
        # With the Android TextView, we use `measureText()` to compute the width
        # of the text -- calling `measure()` seems to ignore the text, perhaps
        # because the TextView is willing to truncate the text. We do use
        # height information from `measure()`, which seems fine.
        text = self.native.getText().toString()
        width = self.native.getPaint().measureText(text)
        self.interface.intrinsic.width = at_least(width)
        self.native.measure(
            View__MeasureSpec.UNSPECIFIED, View__MeasureSpec.UNSPECIFIED
        )
        self.interface.intrinsic.height = self.native.getMeasuredHeight()

    def set_alignment(self, value):
        self.native.setGravity(
            {
                LEFT: Gravity.CENTER_VERTICAL | Gravity.LEFT,
                RIGHT: Gravity.CENTER_VERTICAL | Gravity.RIGHT,
                CENTER: Gravity.CENTER_VERTICAL | Gravity.CENTER_HORIZONTAL,
                JUSTIFY: Gravity.CENTER_VERTICAL | Gravity.CENTER_HORIZONTAL,
            }[value]
        )
