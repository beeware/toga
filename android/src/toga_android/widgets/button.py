from travertino.size import at_least

from ..libs.android.view import OnClickListener, View__MeasureSpec
from ..libs.android.widget import Button as A_Button
from .label import TextViewWidget


class TogaOnClickListener(OnClickListener):
    def __init__(self, button_impl):
        super().__init__()
        self.button_impl = button_impl

    def onClick(self, _view):
        self.button_impl.interface.on_press(None)


class Button(TextViewWidget):
    focusable = False

    def create(self):
        self.native = A_Button(self._native_activity)
        self.native.setOnClickListener(TogaOnClickListener(button_impl=self))
        self.cache_textview_defaults()

    def get_text(self):
        return str(self.native.getText())

    def set_text(self, text):
        self.native.setText(text)

    def set_enabled(self, value):
        self.native.setEnabled(value)

    def set_background_color(self, value):
        self.set_background_filter(value)

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
