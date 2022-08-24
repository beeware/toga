"""The first box that opens when opening the application."""
from pathlib import Path
from tkinter.constants import CENTER
from typing import Callable

import toga
from toga.style import Pack
from travertino.constants import COLUMN, ROW


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
