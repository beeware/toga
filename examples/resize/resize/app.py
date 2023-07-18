import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class SizeButton(toga.Button):
    def __init__(self, text, *, value, max, on_press):
        self.value = value
        self.max = max
        self.on_press_impl = on_press
        super().__init__(text, on_press=self.on_press_wrapper)

    def on_press_wrapper(self, button):
        self.value = (self.value + 1) % (self.max + 1)
        self.on_press_impl(button)


class SizePanel(toga.Box):
    def __init__(self, title, *, on_change):
        self.on_change = on_change
        self.width, self.height = (
            SizeButton(text, value=1, max=6, on_press=self.on_press)
            for text in ["W", "H"]
        )
        self.flex = SizeButton("F", value=0, max=3, on_press=self.on_press)
        super().__init__(
            style=Pack(direction=COLUMN, alignment="center"),
            children=[
                toga.Label(title.upper(), style=Pack(font_weight="bold")),
                toga.Box(
                    style=Pack(direction=ROW),
                    children=[self.width, self.height, self.flex],
                ),
            ],
        )
        self.on_press(None)

    def on_press(self, button):
        self.on_change(self, self.width.value, self.height.value, self.flex.value)


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
                        toga.Label(
                            "Left",
                            style=Pack(
                                text_align="left",
                                background_color="pink",
                                height=50,
                                flex=1,
                            ),
                        ),
                        toga.Label(
                            "Center",
                            style=Pack(
                                text_align="center",
                                background_color="yellow",
                                height=50,
                                flex=1,
                            ),
                        ),
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

    def on_change_text(self, panel, width, height, flex):
        text = "\n".join(" ".join("X" for i in range(width)) for j in range(height))
        setattr_if_changed(self.text_label, "text", text)
        setattr_if_changed(self.text_label.style, "flex", flex)

    def on_change_style(self, panel, width, height, flex):
        # Increment should be large enough that the minimum window width can be determined
        # by either the buttons or the labels, depending on the labels' size.
        INCREMENT = 70
        setattr_if_changed(self.style_label.style, "width", width * INCREMENT)
        setattr_if_changed(self.style_label.style, "height", height * INCREMENT)
        setattr_if_changed(self.style_label.style, "flex", flex)


def setattr_if_changed(obj, name, value):
    """Ensure that each button click only changes one thing."""

    old_value = getattr(obj, name)
    if old_value != value:
        setattr(obj, name, value)


def main():
    return Resize("Resize", "org.beeware.resize")
