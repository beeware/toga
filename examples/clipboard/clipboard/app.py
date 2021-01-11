import toga
from toga.style import Pack
from toga.constants import COLUMN, ROW


class ExampleClipboardApp(toga.App):
    # Button callback functions
    def do_copy(self, widget, **kwargs):
        self.clipboard.set_clipdata(self.input.value)
        self.label.text = "Text copied to clipboard"

    def do_paste(self, widget, **kwargs):
        txt = self.clipboard.get_clipdata()
        self.input.value = txt
        self.label.text = "Text pasted from clipboard"

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        # Label to show responses.
        self.label = toga.Label('Ready.')
        
        self.input = Toga.TextInput(style=Pack(flex=1))
        self.clipboard = toga.Clipboard()

        # Buttons
        btn_style = Pack(flex=1)
        btn_copy = toga.Button('Copy', on_press=self.do_copy, style=btn_style)
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
