from travertino.size import at_least

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
        return self.native.label

    def set_text(self, text):
        self.native.label = text

    def rehint(self):
        self.interface.intrinsic.width = at_least(len(self.native.label) + 8)
        self.interface.intrinsic.height = 3
