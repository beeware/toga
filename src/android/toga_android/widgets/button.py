from travertino.size import at_least

from toga_android.colors import native_color

from ..libs.android.graphics import PorterDuff__Mode
from ..libs.android.util import TypedValue
from ..libs.android.view import OnClickListener, View__MeasureSpec
from ..libs.android.widget import Button as A_Button
from .base import Widget


class TogaOnClickListener(OnClickListener):
    def __init__(self, button_impl):
        super().__init__()
        self.button_impl = button_impl

    def onClick(self, _view):
        if self.button_impl.interface.on_press:
            self.button_impl.interface.on_press(widget=self.button_impl.interface)


class Button(Widget):
    def create(self):
        self.native = A_Button(self._native_activity)
        self.native.setOnClickListener(TogaOnClickListener(button_impl=self))

    def set_text(self, text):
        self.native.setText(self.interface.text)

    def set_enabled(self, value):
        self.native.setEnabled(value)

    def set_font(self, font):
        if font:
            font_impl = font.bind(self.interface.factory)
            self.native.setTextSize(TypedValue.COMPLEX_UNIT_SP, font_impl.get_size())
            self.native.setTypeface(font_impl.get_typeface(), font_impl.get_style())

    def set_on_press(self, handler):
        # No special handling required
        pass

    def set_color(self, value):
        if value:
            self.native.setTextColor(native_color(value))

    def set_background_color(self, value):
        if value:
            # do not use self.native.setBackgroundColor - this messes with the button style!
            self.native.getBackground().setColorFilter(native_color(value), PorterDuff__Mode.MULTIPLY)

    def rehint(self):
        # Like other text-viewing widgets, Android crashes when rendering
        # `Button` unless it has its layout params set. Guard for that case.
        if not self.native.getLayoutParams():
            return
        self.native.measure(
            View__MeasureSpec.UNSPECIFIED,
            View__MeasureSpec.UNSPECIFIED,
        )
        self.interface.intrinsic.width = at_least(self.native.getMeasuredWidth())
        self.interface.intrinsic.height = self.native.getMeasuredHeight()
