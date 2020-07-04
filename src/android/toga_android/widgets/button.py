from travertino.size import at_least

from ..libs import android_widgets
from .base import Widget


class TogaOnClickListener(android_widgets.OnClickListener):
    def __init__(self, button_impl):
        super().__init__()
        self.button_impl = button_impl

    def onClick(self, _view):
        if self.button_impl.interface.on_press:
            self.button_impl.interface.on_press(widget=self.button_impl.interface)


class Button(Widget):
    def create(self):
        self.native = android_widgets.Button(self._native_activity)
        self.native.setOnClickListener(TogaOnClickListener(button_impl=self))

    def set_label(self, label):
        self.native.setText(self.interface.label)

    def set_enabled(self, value):
        self.native.setEnabled(value)

    def set_background_color(self, value):
        self.interface.factory.not_implemented("Button.set_background_color()")

    def set_on_press(self, handler):
        # No special handling required
        pass

    def rehint(self):
        self.native.measure(
            android_widgets.View__MeasureSpec.UNSPECIFIED,
            android_widgets.View__MeasureSpec.UNSPECIFIED,
        )
        self.interface.intrinsic.width = at_least(self.native.getMeasuredWidth())
        self.interface.intrinsic.height = self.native.getMeasuredHeight()
