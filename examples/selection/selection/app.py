import toga
from toga.constants import COLUMN, ROW
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
        self.main_window = toga.MainWindow(size=(640, 400))

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
                        toga.Selection(
                            style=Pack(width=200, padding=24),
                            items=["Curium", "Titanium", "Copernicium"],
                        ),
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


def main():
    # App name and namespace
    return SelectionApp("Selection", "org.beeware.selection")


if __name__ == "__main__":
    app = main()
    app.main_loop()
