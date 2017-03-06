from toga.interface import Button as ButtonInterface

from ..libs import *

from .base import WidgetMixin
# from ..utils import process_callback


class TogaButton(WinForms.Button):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.Click += self.on_click

    def on_click(self, sender, event):
        self.interface.on_press(self.interface)


class Button(ButtonInterface, WidgetMixin):
    def __init__(self, label, id=None, style=None, on_press=None):
        super().__init__(label, id=id, style=style, on_press=on_press)
        self._create()

    def create(self):
        self._impl = TogaButton(self)

        # Add the layout constraints
        self._add_constraints()

    def _set_label(self, label):
        self._impl.Text = self.label
        self.rehint()

    def rehint(self):
        # print(dir(self._impl))
        self._impl.Size = Size(0, 0)
        self.style.hint(
            height=self._impl.PreferredSize.Height,
            min_width=self._impl.PreferredSize.Width,
        )
