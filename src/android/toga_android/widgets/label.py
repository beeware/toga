from travertino.size import at_least

from ..libs.android_widgets import Gravity, TextView, TypedValue, View__MeasureSpec
from .base import Widget, align


class Label(Widget):
    def create(self):
        self.native = TextView(self._native_activity)
        self.native.setSingleLine()

    def set_text(self, value):
        self.native.setText(value)

    def set_font(self, font):
        if font:
            font_impl = font.bind(self.interface.factory)
            self.native.setTextSize(TypedValue.COMPLEX_UNIT_SP, font_impl.get_size())
            self.native.setTypeface(font_impl.get_typeface(), font_impl.get_style())

    def rehint(self):
        # Refuse to rehint an Android TextView if it has no LayoutParams yet.
        # Calling measure() on an Android TextView w/o LayoutParams raises NullPointerException.
        if self.native.getLayoutParams() is None:
            return
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
        # Refuse to set alignment if create() has not been called.
        if self.native is None:
            return
        # Refuse to set alignment if widget has no container.
        # On Android, calling setGravity() when the widget has no LayoutParams
        # results in a NullPointerException.
        if self.native.getLayoutParams() is None:
            return
        self.native.setGravity(Gravity.CENTER_VERTICAL | align(value))
