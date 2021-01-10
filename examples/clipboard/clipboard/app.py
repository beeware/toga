import toga
from toga.style import Pack
from toga.constants import COLUMN, ROW


class ExampleClipboardApp(toga.App):
    # Button callback functions
    def do_copy(self, widget, **kwargs):
        self.label.text = "Do stuff."

    def do_paste(self, widget, **kwargs):
        self.label.text = "Ready."

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        # Label to show responses.
        self.label = toga.Label('Ready.')

        widget = toga.Clipboard()

        # Buttons
        btn_style = Pack(flex=1)
        btn_copy = toga.Button('copy', on_press=self.do_copy, style=btn_style)
        btn_paste = toga.Button('Paste', on_press=self.do_paste, style=btn_style)
        btn_box = toga.Box(
            children=[
                btn_copy,
                btn_paste
            ],
            style=Pack(direction=ROW)
        )

        # Outermost box
        outer_box = toga.Box(
            children=[btn_box, widget, self.label],
            style=Pack(
                flex=1,
                direction=COLUMN,
                padding=10,
                width=500,
                height=300
            )
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    return ExampleClipboardApp('Clipboard Demo', 'org.beeware.widgets.clipboard')


if __name__ == '__main__':
    app = main()
    app.main_loop()
