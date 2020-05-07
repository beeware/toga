from travertino.size import at_least

from .base import Widget
from ..libs.android_widgets import (
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
        self.native.measure(
            View__MeasureSpec.UNSPECIFIED, View__MeasureSpec.UNSPECIFIED
        )
        self.interface.intrinsic.width = at_least(self.native.getMeasuredWidth())
        self.interface.intrinsic.height = self.native.getMeasuredHeight()

    def set_alignment(self, value):
        return super().set_alignment(value)
