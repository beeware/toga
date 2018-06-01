import toga
from toga.style import Pack
from toga.constants import COLUMN, ROW

class ComboBoxApp(toga.App):

    def startup(self):
        # Main window of the application with title and size
        self.main_window = toga.MainWindow(title=self.name, size=(640, 400))

        # set up common styles
        label_style = Pack(flex=1, padding_right=24)
        box_style = Pack(direction=ROW, padding=10)

        # Add the content on the main window
        self.main_window.content = toga.Box(
            children=[
                toga.Box(style=box_style, children=[
                    toga.Label("Select an element",
                        style=label_style),

                    toga.ComboBox(items=["Carbon", "Ytterbium", "Thulium"])
                ]),

                toga.Box(style=box_style, children=[
                    toga.Label("use the 'on_change' callback to respond to changes",
                        style=label_style),

                    toga.ComboBox(
                      on_change=self.my_on_change,
                      items=["Dubnium", "Holmium", "Zirconium"])

                ]),

                toga.Box(style=box_style, children=[
                    toga.Label("Long lists of items should scroll",
                        style=label_style),

                    toga.ComboBox(items=dir(toga)),
                ]),

                toga.Box(style=box_style, children=[
                    toga.Label("use some style!", style=label_style),

                    toga.ComboBox(
                        style=Pack(width=200, padding=24),
                        items=["Curium", "Titanium", "Copernicium"])
                ]),
            ],
            style=Pack(direction=COLUMN, padding=24)
        )

        self.main_window.show()

    def my_on_change(self, combobox):
        # get the current value of the slider with `combobox.value`
        print("The combobox widget changed to {0}".format(combobox.value))


def main():
    # App name and namespace
    return ComboBoxApp('ComboBox', 'org.pybee.combobox')
