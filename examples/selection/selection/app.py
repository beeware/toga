import toga
from toga.constants import COLUMN, ROW
from toga.fonts import MONOSPACE
from toga.style import Pack


class SelectionApp(toga.App):
    CARBON = "Carbon"
    YTTERBIUM = "Ytterbium"
    THULIUM = "Thulium"
    OPTIONS = [CARBON, YTTERBIUM, THULIUM]
    DATA_OPTIONS = [
        {"name": CARBON, "number": 6, "weight": 12.011},
        {"name": YTTERBIUM, "number": 70, "weight": 173.04},
        {"name": THULIUM, "number": 69, "weight": 168.93},
    ]

    def startup(self):
        # Main window of the application with title and size
        self.main_window = toga.MainWindow(title=self.name, size=(640, 400))

        # set font toggle
        self.big_font = False

        # set up common styles
        label_style = Pack(flex=1, padding_right=24)
        box_style = Pack(direction=ROW, padding=10)

        # Add the content on the main window
        self.selection = toga.Selection(items=self.OPTIONS)
        self.empty_selection = toga.Selection()
        self.source_selection = toga.Selection(
            accessor="name",
            items=self.DATA_OPTIONS,
        )
        self.styled_selection = toga.Selection(
            style=Pack(
                width=200,
                padding=24,
                font_family="serif",
            ),
            items=["Curium", "Titanium", "Copernicium"],
        )

        self.main_window.content = toga.Box(
            children=[
                toga.Box(
                    style=box_style,
                    children=[
                        toga.Label("Select an element", style=label_style),
                        self.selection,
                    ],
                ),
                toga.Box(
                    style=box_style,
                    children=[
                        toga.Label("Empty selection", style=label_style),
                        self.empty_selection,
                    ],
                ),
                toga.Box(
                    style=box_style,
                    children=[
                        toga.Label("Selection from source", style=label_style),
                        self.source_selection,
                    ],
                ),
                toga.Box(
                    style=box_style,
                    children=[
                        toga.Button("Print", on_press=self.report_selection),
                        toga.Button("Carbon", on_press=self.set_carbon),
                        toga.Button("Ytterbium", on_press=self.set_ytterbium),
                        toga.Button("Thulium", on_press=self.set_thulium),
                    ],
                ),
                toga.Box(
                    style=box_style,
                    children=[
                        toga.Label(
                            "on_change callback",
                            style=label_style,
                        ),
                        toga.Selection(
                            on_change=self.my_on_change,
                            items=["Dubnium", "Holmium", "Zirconium"],
                        ),
                    ],
                ),
                toga.Box(
                    style=box_style,
                    children=[
                        toga.Label("Long lists should scroll", style=label_style),
                        toga.Selection(items=dir(toga)),
                    ],
                ),
                toga.Box(
                    style=box_style,
                    children=[
                        toga.Label("Use some style!", style=label_style),
                        self.styled_selection,
                    ],
                ),
                toga.Box(
                    style=box_style,
                    children=[
                        toga.Label("Disabled", style=label_style),
                        toga.Selection(
                            items=[
                                "Helium",
                                "Neon",
                                "Argon",
                                "Krypton",
                                "Xenon",
                                "Radon",
                                "Oganesson",
                            ],
                            enabled=False,
                        ),
                    ],
                ),
                toga.Box(
                    style=box_style,
                    children=[
                        toga.Button("Change font", on_press=self.change_font),
                    ],
                ),
            ],
            style=Pack(direction=COLUMN, padding=24),
        )

        self.main_window.show()

    def set_carbon(self, widget):
        self.selection.value = self.CARBON

    def set_ytterbium(self, widget):
        self.selection.value = self.YTTERBIUM

    def set_thulium(self, widget):
        self.selection.value = self.THULIUM

    def my_on_change(self, selection):
        # get the current value of the slider with `selection.value`

        print(f"The selection widget changed to {selection.value}")

    def report_selection(self, widget):
        print(
            f"Element: {self.selection.value!r}; "
            f"Empty: {self.empty_selection.value!r}; "
            f"Source: {self.source_selection.value.name} has weight {self.source_selection.value.weight}"
        )

    def change_font(self, widget):
        self.big_font = not self.big_font
        if self.big_font:
            self.styled_selection.style.font_family = MONOSPACE
            self.styled_selection.style.font_size = 30
            # self.styled_selection.style.font_style = ITALIC
        else:
            self.styled_selection.style.font_family = "serif"
            del self.styled_selection.style.font_size
            # del self.styled_selection.style.font_style


def main():
    # App name and namespace
    return SelectionApp("Selection", "org.beeware.selection")


if __name__ == "__main__":
    app = main()
    app.main_loop()
