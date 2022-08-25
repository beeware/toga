from pathlib import Path
from typing import Callable

from travertino.constants import ROW, CENTER, COLUMN

import toga
from toga.style import Pack

LOGO_SIZE = 200


class WelcomeBox(toga.Box):
    """Box for welcoming users."""

    def __init__(self, on_start: Callable[[], None]):
        """Constructor."""
        super().__init__(style=Pack(direction=ROW, alignment=CENTER))
        left_side = self.build_left_side(on_start=on_start)
        right_side = self.build_right_side()
        self.add(left_side, right_side)

    @classmethod
    def build_left_side(cls, on_start: Callable[[], None]):
        return toga.Box(
            style=Pack(flex=1, direction=COLUMN),
            children=[
                toga.Box(style=Pack(flex=1)),
                toga.Box(
                    style=Pack(direction=ROW, alignment=CENTER),
                    children=[
                        toga.Box(style=Pack(flex=1)),
                        toga.Button("Click me to move to next box!", on_press=lambda _: on_start()),
                        toga.Box(style=Pack(flex=1)),
                    ]
                ),
                toga.Box(style=Pack(flex=1)),
            ]
        )

    @classmethod
    def build_right_side(cls):
        logo_path = Path(__file__).parent / "resources" / "toga.png"
        logo = toga.Image(str(logo_path))
        return toga.Box(
            style=Pack(direction=COLUMN, alignment=CENTER, flex=1),
            children=[
                toga.Box(style=Pack(flex=1)),
                toga.ImageView(
                    image=logo,
                    style=Pack(height=LOGO_SIZE, width=LOGO_SIZE, alignment=CENTER),
                ),
                toga.Box(
                    style=Pack(direction=ROW, alignment=CENTER),
                    children=[
                        toga.Label(
                            "Welcome to One Window Example!",
                            style=Pack(font_size=20)
                        ),
                    ],
                ),
                toga.Box(style=Pack(flex=1))
            ],
        )


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


class ExampleOneWindow(toga.App):
    welcome_box: WelcomeBox
    main_box: MainBox

    def startup(self):
        # Set up main window
        self.main_window = toga.Window(title=self.name, size=(1000, 500))
        self.welcome_box = WelcomeBox(on_start=self.move_next)
        self.main_box = MainBox(on_back=self.move_back)
        self.main_window.content = self.welcome_box

        # Show the main window
        self.main_window.show()

    def move_next(self):
        self.main_window.content = self.main_box

    def move_back(self):
        self.main_window.content = self.welcome_box


def main():
    return ExampleOneWindow("Demo NumberInput", "org.beeware.widgets.numberinput")


if __name__ == "__main__":
    app = main()
    app.main_loop()
