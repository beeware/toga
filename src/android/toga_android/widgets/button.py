from travertino.size import at_least

from .base import Widget


class TogaButton:
    # TODO: Extend `android.widget.Button`. Provide app as `context`.
    def __init__(self, context, interface):
        self._interface = interface


class TogaButtonListener:
    # TODO: Extend `android.view.View[OnClickListener]`.
    def __init__(self, interface):
        self._interface = interface

    def onClick(self, v) -> None:
        self._interface.on_press(self._interface)


class Button(Widget):
    def create(self):
        self.native = TogaButton(self.app._impl, self.interface)

        self._listener = TogaButtonListener(self)

        self.native.setOnClickListener(self._listener)

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
