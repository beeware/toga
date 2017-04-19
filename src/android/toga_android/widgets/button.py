from toga.interface import Button as ButtonInterface

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


class Button(ButtonInterface, WidgetMixin):
    def __init__(self, label, id=None, style=None, on_press=None):
        super().__init__(label, id=id, style=style, on_press=on_press)

    def create(self):
        self._impl = TogaButton(self.app._impl, self)

        self._listener = TogaButtonListener(self)

        self._impl.setOnClickListener(self._listener)

    def _set_label(self, label):
        self._impl.setText(self.label)

    def _set_enabled(self, value):
        pass

    def rehint(self):
        if self._impl.getMeasuredWidth():
            # print("REHINT button", self, self._impl.getMeasuredWidth(), self._impl.getMeasuredHeight())
            self.style.hint(
                min_width=self._impl.getMeasuredWidth() / self.app._impl.device_scale,
                height=self._impl.getMeasuredHeight() / self.app._impl.device_scale,
            )
