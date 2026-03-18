from decimal import ROUND_UP

from android.view import Gravity, View
from android.widget import TextView
from travertino.size import at_least

from toga_android.widgets.label import TextViewWidget


class HelloWorld(TextViewWidget):
    def create(self):
        self.native = TextView(self._native_activity)
        self.cache_textview_defaults()
        self.native.setText("Hello World!")

    def rehint(self):
        # Ask the Android TextView first for its minimum possible height.
        # This is the height with word-wrapping disabled.
        self.native.measure(View.MeasureSpec.UNSPECIFIED, View.MeasureSpec.UNSPECIFIED)
        min_height = self.native.getMeasuredHeight()
        self.interface.intrinsic.height = self.scale_out(min_height, ROUND_UP)
        # Ask it how wide it would be if it had to be the minimum height.
        self.native.measure(
            View.MeasureSpec.UNSPECIFIED,
            View.MeasureSpec.makeMeasureSpec(min_height, View.MeasureSpec.AT_MOST),
        )
        self.interface.intrinsic.width = self.scale_out(
            at_least(self.native.getMeasuredWidth()), ROUND_UP
        )

    def set_text_align(self, value):
        self.set_textview_alignment(value, Gravity.TOP)
