from travertino.size import at_least

from .base import Widget
from ..libs import android_widgets


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
        self.interface.factory.not_implemented('Button.set_enabled()')

    def set_background_color(self, value):
        self.interface.factory.not_implemented('Button.set_background_color()')

    def set_on_press(self, handler):
        # No special handling required
        pass

    def rehint(self):
        if self.native.getMeasuredWidth():
            # print("REHINT button", self, self.native.getMeasuredWidth(), self.native.getMeasuredHeight())
            self.interface.intrinsic.width = at_least(self.native.getMeasuredWidth() / self.app._impl.device_scale)
            self.interface.intrinsic.height = self.native.getMeasuredHeight() / self.app._impl.device_scale
