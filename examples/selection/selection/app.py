import toga
from toga.constants import COLUMN, ROW
from toga.style import Pack


class SelectionApp(toga.App):
    CARBON = "Carbon"
    YTTERBIUM = "Ytterbium"
    THULIUM = "Thulium"
    OPTIONS = [CARBON, YTTERBIUM, THULIUM]

    def startup(self):
        # Main window of the application with title and size
        self.main_window = toga.MainWindow(title=self.name, size=(640, 400))

        # set up common styles
        label_style = Pack(flex=1, padding_right=24)
        box_style = Pack(direction=ROW, padding=10)

        # Add the content on the main window
        self.selection = toga.Selection(items=self.OPTIONS)

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
                        toga.Label(
                            "Selection value can be set by property setter",
                            style=label_style,
                        ),
                        toga.Button(label="Set Carbon", on_press=self.set_carbon),
                        toga.Button(label="Set Ytterbium", on_press=self.set_ytterbium),
                        toga.Button(label="Set THULIUM", on_press=self.set_thulium),
                    ],
                ),
                toga.Box(
                    style=box_style,
                    children=[
                        toga.Label(
                            "use the 'on_select' callback to respond to changes",
                            style=label_style,
                        ),
                        toga.Selection(
                            on_select=self.my_on_select,
                            items=["Dubnium", "Holmium", "Zirconium"],
                        ),
                    ],
                ),
                toga.Box(
                    style=box_style,
                    children=[
                        toga.Label(
                            "Long lists of items should scroll", style=label_style
                        ),
                        toga.Selection(items=dir(toga)),
                    ],
                ),
                toga.Box(
                    style=box_style,
                    children=[
                        toga.Label("use some style!", style=label_style),
                        toga.Selection(
                            style=Pack(width=200, padding=24),
                            items=["Curium", "Titanium", "Copernicium"],
                        ),
                    ],
                ),
                toga.Box(
                    style=box_style,
                    children=[
                        toga.Label(
                            "Selection widgets can be disabled", style=label_style
                        ),
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

    def my_on_select(self, selection):

        # get the current value of the slider with `selection.value`

        print("The selection widget changed to {0}".format(selection.value))


def main():
    # App name and namespace
    return SelectionApp("Selection", "org.beeware.selection")
