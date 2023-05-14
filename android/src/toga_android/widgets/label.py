from travertino.size import at_least

from toga.constants import JUSTIFY
from toga_android.colors import native_color

from ..libs.android.os import Build
from ..libs.android.text import Layout
from ..libs.android.view import Gravity, View__MeasureSpec
from ..libs.android.widget import TextView
from .base import Widget, align


class TextViewWidget(Widget):
    def cache_textview_defaults(self):
        self._default_text_color = self.native.getCurrentTextColor()
        self._default_text_size = self.native.getTextSize()
        self._default_typeface = self.native.getTypeface()

    def set_font(self, font):
        font._impl.apply(self.native, self._default_text_size, self._default_typeface)

    def set_color(self, value):
        if value is None:
            self.native.setTextColor(self._default_text_color)
        else:
            self.native.setTextColor(native_color(value))


class Label(TextViewWidget):
    def create(self):
        self.native = TextView(self._native_activity)
        self.cache_textview_defaults()

    def get_text(self):
        return self.native.getText()

    def set_text(self, value):
        self.native.setText(value)

    def set_background_color(self, value):
        self.set_background_color_simple(value)

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
            View__MeasureSpec.makeMeasureSpec(min_height, View__MeasureSpec.AT_MOST),
        )
        self.interface.intrinsic.width = at_least(self.native.getMeasuredWidth())

    def set_alignment(self, value):
        # Refuse to set alignment if widget has no container.
        # On Android, calling setGravity() when the widget has no LayoutParams
        # results in a NullPointerException.
        if not self.native.getLayoutParams():
            return

        # Justified text wasn't added until API level 26.
        # We only run the test suite on API 31, so we need to disable branch coverage.
        if Build.VERSION.SDK_INT >= 26:  # pragma: no branch
            self.native.setJustificationMode(
                Layout.JUSTIFICATION_MODE_INTER_WORD
                if value == JUSTIFY
                else Layout.JUSTIFICATION_MODE_NONE
            )

        self.native.setGravity(Gravity.CENTER_VERTICAL | align(value))
