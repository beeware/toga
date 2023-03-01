import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class SizeButton(toga.Button):
    INITIAL_SIZE = 1
    MAX_SIZE = 6

    def __init__(self, text, *, on_press):
        self.value = self.INITIAL_SIZE
        self.on_press_impl = on_press
        super().__init__(text, on_press=self.on_press_wrapper)

    def on_press_wrapper(self, button):
        self.value = (self.value + 1) % (self.MAX_SIZE + 1)
        self.on_press_impl(button)


class SizePanel(toga.Box):
    def __init__(self, title, *, on_change):
        self.on_change = on_change
        self.width_button, self.height_button = (
            SizeButton(text, on_press=self.on_press) for text in ["Width", "Height"]
        )
        super().__init__(
            style=Pack(direction=COLUMN, alignment="center"),
            children=[
                toga.Label(title.upper(), style=Pack(font_weight="bold")),
                toga.Box(
                    style=Pack(direction=ROW),
                    children=[self.width_button, self.height_button],
                ),
            ],
        )
        self.on_press(None)

    def on_press(self, button):
        self.on_change(self, self.width_button.value, self.height_button.value)


class Resize(toga.App):
    def startup(self):
        self.text_label, self.style_label = (
            toga.Label("", style=Pack(background_color="cyan")) for i in range(2)
        )
        main_box = toga.Box(
            style=Pack(direction=COLUMN),
            children=[
                toga.Box(
                    style=Pack(direction=ROW),
                    children=[
                        SizePanel("Text", on_change=self.on_change_text),
                        toga.Box(style=Pack(flex=1)),
                        SizePanel("Style", on_change=self.on_change_style),
                    ],
                ),
                toga.Box(
                    style=Pack(direction=ROW),
                    children=[
                        self.text_label,
                        toga.Label("", style=Pack(background_color="pink", flex=1)),
                        toga.Label("", style=Pack(background_color="yellow", flex=1)),
                        self.style_label,
                    ],
                ),
                toga.Box(style=Pack(background_color="pink", flex=1)),
                toga.Box(style=Pack(background_color="yellow", flex=1)),
            ],
        )

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def on_change_text(self, panel, width, height):
        self.text_label.text = "\n".join(
            " ".join("X" for i in range(width)) for j in range(height)
        )

    def on_change_style(self, panel, width, height):
        INCREMENT = 50
        self.style_label.style.update(
            width=width * INCREMENT, height=height * INCREMENT
        )


def main():
    return Resize()
