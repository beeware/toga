from travertino.size import at_least

from .base import Widget


class TogaButton(extends=android.widget.Button):
    @super({context: android.content.Context})
    def __init__(self, context, interface):
        self._interface = interface


class TogaButtonListener(implements=android.view.View[OnClickListener]):
    @super({})
    def __init__(self, interface):
        self._interface = interface

    def onClick(self, v: android.view.View) -> None:
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
