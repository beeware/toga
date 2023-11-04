from decimal import ROUND_UP

from android.os import Build
from android.text import Layout
from android.util import TypedValue
from android.view import Gravity, View
from android.widget import TextView
from travertino.size import at_least

from toga.constants import JUSTIFY
from toga_android.colors import native_color

from .base import Widget, align


def set_textview_font(tv, font, default_typeface, default_size):
    tv.setTypeface(font.typeface(default=default_typeface))
    tv.setTextSize(TypedValue.COMPLEX_UNIT_PX, font.size(default=default_size))


class TextViewWidget(Widget):
    def cache_textview_defaults(self):
        self._default_text_color = self.native.getCurrentTextColor()
        self._default_text_size = self.native.getTextSize()
        self._default_typeface = self.native.getTypeface()

    def set_font(self, font):
        set_textview_font(
            self.native, font._impl, self._default_typeface, self._default_text_size
        )

    def set_background_color(self, value):
        # In the case of EditText, this causes any custom color to hide the bottom border
        # line, but it's better than set_background_filter, which affects *only* the
        # bottom border line.
        self.set_background_simple(value)

    def set_color(self, value):
        if value is None:
            self.native.setTextColor(self._default_text_color)
        else:
            self.native.setTextColor(native_color(value))

    def set_textview_alignment(self, value, vertical_gravity):
        # Justified text wasn't added until API level 26.
        # We only run the test suite on API 31, so we need to disable branch coverage.
        if Build.VERSION.SDK_INT >= 26:  # pragma: no branch
            self.native.setJustificationMode(
                Layout.JUSTIFICATION_MODE_INTER_WORD
                if value == JUSTIFY
                else Layout.JUSTIFICATION_MODE_NONE
            )

        self.native.setGravity(vertical_gravity | align(value))


class Label(TextViewWidget):
    def create(self):
        self.native = TextView(self._native_activity)
        self.cache_textview_defaults()

    def get_text(self):
        return self.native.getText()

    def set_text(self, value):
        self.native.setText(value)

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

    def set_alignment(self, value):
        self.set_textview_alignment(value, Gravity.TOP)
