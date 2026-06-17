from textual.containers import Horizontal
from textual.widgets import Label, Switch as TextualSwitch
from travertino.size import at_least

from toga_textual.widgets.base import Widget


class TogaSwitch(TextualSwitch):
    def __init__(self, impl):
        super().__init__()
        self.interface = impl.interface
        self.impl = impl

    def on_switch_changed(self, event: TextualSwitch.Changed) -> None:
        self.interface.on_change()


class Switch(Widget):
    def create(self):
        self.native_switch = TogaSwitch(self)
        self.native_label = Label()
        self.native = Horizontal(self.native_switch, self.native_label)

    def get_text(self):
        return str(self.native_label.renderable)

    def set_text(self, text):
        self.native_label.update(text)
        self.refresh()

    def get_value(self):
        return self.native_switch.value

    def set_value(self, value):
        self.native_switch.value = value

    def rehint(self):
        self.interface.intrinsic.width = at_least(len(self.get_text()) + 8)
        self.interface.intrinsic.height = 3
