from .base import WidgetMixin


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
    def __init__(self, label, id=None, style=None, on_press=None):
        super().__init__(label, id=id, style=style, on_press=on_press)

    def create(self):
        self.native = TogaButton(self.app._impl, self.interface)

        self._listener = TogaButtonListener(self)

        self.native.setOnClickListener(self._listener)

    def set_label(self, label):
        self.native.setText(self.label)

    def set_enabled(self, value):
        pass

    def set_background_color(self, value):
        pass

    def rehint(self):
        if self.native.getMeasuredWidth():
            # print("REHINT button", self, self.native.getMeasuredWidth(), self.native.getMeasuredHeight())
            self.interface.style.hint(
                min_width=self.native.getMeasuredWidth() / self.app._impl.device_scale,
                height=self.native.getMeasuredHeight() / self.app._impl.device_scale,
            )
