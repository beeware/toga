import toga
from toga.constants import COLUMN, ROW
from toga.style import Pack


class ExampleNumberInputApp(toga.App):
    # Button callback functions
    def do_stuff(self, widget, **kwargs):
        self.label.text = (
            f"Current values are {self.input1.value} and {self.input2.value}"
        )

    def do_clear(self, widget, **kwargs):
        self.input1.value = None
        self.input2.value = None
        self.label.text = "Ready."

    def on_change(self, widget):
        self.label.text = f"You entered the value: {widget.value}"

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow()

        # Label to show responses.
        self.label = toga.Label("Ready.")
        label1 = toga.Label("Enter value from -12 to 72:")
        self.input1 = toga.NumberInput(
            min=-12,
            max=72,
            step=2,
            value=37,
            on_change=self.on_change,
        )
        label2 = toga.Label("Enter value from 1.2 to 7.2:")
        self.input2 = toga.NumberInput(
            min=1.2,
            max=7.2,
            step=0.1,
            value=3.7,
            on_change=self.on_change,
        )
        box1 = toga.Box(
            children=[label1, self.input1],
            style=Pack(direction=ROW, padding=5),
        )
        box2 = toga.Box(
            children=[label2, self.input2],
            style=Pack(direction=ROW, padding=5),
        )
        # Buttons
        btn_style = Pack(flex=1)
        btn_do_stuff = toga.Button("Get value", on_press=self.do_stuff, style=btn_style)
        btn_clear = toga.Button("Clear", on_press=self.do_clear, style=btn_style)
        btn_box = toga.Box(
            children=[btn_do_stuff, btn_clear], style=Pack(direction=ROW)
        )

        # Outermost box
        outer_box = toga.Box(
            children=[btn_box, box1, box2, self.label],
            style=Pack(flex=1, direction=COLUMN, padding=10),
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    return ExampleNumberInputApp("Demo NumberInput", "org.beeware.widgets.numberinput")


if __name__ == "__main__":
    app = main()
    app.main_loop()
