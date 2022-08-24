from typing import Callable

from travertino.constants import COLUMN

import toga
from toga.style import Pack


class MainBox(toga.Box):
    """The actual application box"""

    def __init__(self, on_back: Callable[[], None]):
        super().__init__(style=Pack(direction=COLUMN))
        self.add(
            toga.Button("Back", on_press=lambda _: on_back()),
            toga.Label("This box is the actual application!"),
            toga.Button("Press me to do something", on_press=self.show_hello_dialog)
        )

    def show_hello_dialog(self, widget):
        self.window.info_dialog("This is a title", "Hello there!")
