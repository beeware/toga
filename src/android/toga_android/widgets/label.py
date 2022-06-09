from travertino.size import at_least

from toga_android.colors import native_color

from ..libs.android.util import TypedValue
from ..libs.android.view import Gravity, View__MeasureSpec
from ..libs.android.widget import TextView
from .base import Widget, align


class Label(Widget):
    def create(self):
        self.native = TextView(self._native_activity)

    def set_text(self, value):
        self.native.setText(value)

    def set_font(self, font):
        if font:
            font_impl = font.bind(self.interface.factory)
            self.native.setTextSize(TypedValue.COMPLEX_UNIT_SP, font_impl.get_size())
            self.native.setTypeface(font_impl.get_typeface(), font_impl.get_style())

    def set_color(self, color):
        if color:
            self.native.setTextColor(native_color(color))

    def rehint(self):
        # Refuse to rehint an Android TextView if it has no LayoutParams yet.
        # Calling measure() on an Android TextView w/o LayoutParams raises NullPointerException.
        if not self.native.getLayoutParams():
            return
        # Ask the Android TextView first for its minimum possible height.
        # This is the height with word-wrapping disabled.
        self.native.measure(
            View__MeasureSpec.UNSPECIFIED, View__MeasureSpec.UNSPECIFIED
        )
        min_height = self.native.getMeasuredHeight()
        self.interface.intrinsic.height = min_height
        # Ask it how wide it would be if it had to be the minimum height.
        self.native.measure(
            View__MeasureSpec.UNSPECIFIED,
            View__MeasureSpec.makeMeasureSpec(
                min_height, View__MeasureSpec.AT_MOST
            ),
        )
        self.interface.intrinsic.width = at_least(self.native.getMeasuredWidth())

    def set_alignment(self, value):
        # Refuse to set alignment if create() has not been called.
        if self.native is None:
            return
        # Refuse to set alignment if widget has no container.
        # On Android, calling setGravity() when the widget has no LayoutParams
        # results in a NullPointerException.
        if not self.native.getLayoutParams():
            return
        self.native.setGravity(Gravity.CENTER_VERTICAL | align(value))
