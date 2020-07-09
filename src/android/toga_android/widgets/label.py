from travertino.size import at_least

from toga.constants import CENTER, JUSTIFY, LEFT, RIGHT

from ..libs.android_widgets import Gravity, TextView, View__MeasureSpec
from .base import Widget


class Label(Widget):
    def create(self):
        self.native = TextView(self._native_activity)
        self.native.setSingleLine()

    def set_text(self, value):
        self.native.setText(value)

    def rehint(self):
        # Ask the Android TextView first for the height it would use in its
        # wildest dreams. This is the height of one line of text.
        self.native.measure(
            View__MeasureSpec.UNSPECIFIED, View__MeasureSpec.UNSPECIFIED
        )
        one_line_height = self.native.getMeasuredHeight()
        self.interface.intrinsic.height = one_line_height
        # Ask it how wide it would be if it had to be just one line tall.
        self.native.measure(
            View__MeasureSpec.UNSPECIFIED,
            View__MeasureSpec.makeMeasureSpec(
                one_line_height, View__MeasureSpec.AT_MOST
            ),
        )
        self.interface.intrinsic.width = at_least(self.native.getMeasuredWidth())

    def set_alignment(self, value):
        self.native.setGravity(
            {
                LEFT: Gravity.CENTER_VERTICAL | Gravity.LEFT,
                RIGHT: Gravity.CENTER_VERTICAL | Gravity.RIGHT,
                CENTER: Gravity.CENTER_VERTICAL | Gravity.CENTER_HORIZONTAL,
                JUSTIFY: Gravity.CENTER_VERTICAL | Gravity.CENTER_HORIZONTAL,
            }[value]
        )
