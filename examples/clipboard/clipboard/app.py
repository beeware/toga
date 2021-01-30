import toga
from toga.style import Pack
from toga.constants import COLUMN, ROW
from toga.util.clipboard import Clipboard


class ExampleClipboardApp(toga.App):
    # Button callback functions
    def do_clear(self, widget, **kwargs):
        self.clipboard.clear()
        self.label.text = "Clipboard cleared"

    def do_copy(self, widget, **kwargs):
        self.clipboard.set_text(self.input.value)
        self.label.text = "Text copied to clipboard"

    def do_paste(self, widget, **kwargs):
        txt = self.clipboard.get_text()
        if txt is None:
            self.label.text = "No text data available in clipboard"
        else:
            self.input.value = txt
            self.label.text = "Text pasted from clipboard"

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        # Label to show responses.
        self.label = toga.Label('Ready.')

        self.input = toga.MultilineTextInput(style=Pack(flex=1))
        self.clipboard = Clipboard()

        # Buttons
        btn_style = Pack(flex=1)
        btn_copy = toga.Button('Copy', on_press=self.do_copy, style=btn_style)
        btn_paste = toga.Button('Paste', on_press=self.do_paste, style=btn_style)
        btn_clear = toga.Button('Clear', on_press=self.do_clear, style=btn_style)
        btn_box = toga.Box(
            children=[
                btn_copy,
                btn_paste,
                btn_clear
            ],
            style=Pack(direction=ROW)
        )

        # Outermost box
        outer_box = toga.Box(
            children=[self.input, btn_box, self.label],
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
