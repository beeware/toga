import toga
from toga.constants import COLUMN


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
        self.width_button, self.height_button = (
            SizeButton(text, value=1, max=6, on_press=self.on_press)
            for text in ["W", "H"]
        )
        self.flex_button = SizeButton("F", value=0, max=3, on_press=self.on_press)
        super().__init__(
            direction=COLUMN,
            align_items="center",
            children=[
                toga.Label(title.upper(), font_weight="bold"),
                toga.Row(
                    children=[self.width_button, self.height_button, self.flex_button],
                ),
            ],
        )
        self.on_press(None)

    def on_press(self, button):
        self.on_change(
            self,
            self.width_button.value,
            self.height_button.value,
            self.flex_button.value,
        )


class Resize(toga.App):
    def startup(self):
        self.text_label, self.style_label = (
            toga.Label("", background_color="cyan") for i in range(2)
        )
        main_box = toga.Column(
            children=[
                toga.Row(
                    children=[
                        SizePanel("Text", on_change=self.on_change_text),
                        toga.Box(flex=1),
                        SizePanel("Style", on_change=self.on_change_style),
                    ],
                ),
                toga.Row(
                    children=[
                        self.text_label,
                        toga.Label(
                            "Left",
                            text_align="left",
                            background_color="pink",
                            height=50,
                            flex=1,
                        ),
                        toga.Label(
                            "Center",
                            text_align="center",
                            background_color="yellow",
                            height=50,
                            flex=1,
                        ),
                        self.style_label,
                    ],
                ),
                toga.Box(background_color="pink", flex=1),
                toga.Box(background_color="yellow", flex=1),
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
        # Increment should be large enough that the minimum window width can be
        # determined by either the buttons or the labels, depending on the labels' size.
        INCREMENT = 70
        setattr_if_changed(self.style_label, "width", width * INCREMENT)
        setattr_if_changed(self.style_label, "height", height * INCREMENT)
        setattr_if_changed(self.style_label, "flex", flex)


def setattr_if_changed(obj, name, value):
    """Ensure that each button click only changes one thing."""

    old_value = getattr(obj, name)
    if old_value != value:
        setattr(obj, name, value)


def main():
    return Resize("Resize", "org.beeware.toga.examples.resize")
