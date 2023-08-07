from textual.widgets import Button as TextualButton

from .base import Widget


class TogaButton(TextualButton):
    def __init__(self, impl):
        super().__init__()
        self.interface = impl.interface
        self.impl = impl

    def on_button_pressed(self, event: TextualButton.Pressed) -> None:
        self.interface.on_press(None)


class Button(Widget):
    def create(self):
        self.native = TogaButton(self)

    def get_text(self):
        return self.native.text

    def set_text(self, text):
        self.native.label = text
