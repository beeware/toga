import toga
from toga.style import Pack
from toga.constants import COLUMN, ROW


class ExampleNumberInputApp(toga.App):
    ni1 = None

    # Button callback functions
    def do_stuff(self, widget, **kwargs):
        if self.ni1:
            self.label.text = "You entered following value: " + str(self.ni1.value)

    def do_clear(self, widget, **kwargs):
        self.label.text = "Ready."

    def handle_numberinput(self, widget):
        if self.ni1:
            self.label.text = "You entered following value: " + str(self.ni1.value)

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        # Label to show responses.
        self.label = toga.Label("Ready.")
        label1 = toga.Label("Enter value from 12 to 72:")
        self.ni1 = toga.NumberInput(
            min_value=12,
            max_value=72,
            value=12,
            on_change=self.handle_numberinput,
        )
        box1 = toga.Box(
            children=[label1, self.ni1],
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
            children=[btn_box, box1, self.label],
            style=Pack(flex=1, direction=COLUMN, padding=10, width=500, height=300),
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
