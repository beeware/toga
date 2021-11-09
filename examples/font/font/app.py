import toga
from toga.style import Pack
from toga.constants import COLUMN, ROW


class ExampleFontExampleApp(toga.App):
    textpanel = None

    # Button callback functions
    def do_clear(self, widget, **kwargs):
        self.textpanel.value = ""

    def do_normal_button(self, widget):
        self.textpanel.value += widget.label + '\n'

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        # Buttons
        btn_style = Pack(flex=1)
        btn_clear = toga.Button('Clear', on_press=self.do_clear, style=btn_style)
        btn1 = toga.Button('Normal button', on_press=self.do_normal_button, style=btn_style)
        btn_box = toga.Box(
            children=[
                btn_clear,
                btn1
            ],
            style=Pack(direction=ROW)
        )

        self.textpanel = toga.MultilineTextInput(readonly=False, style=Pack(flex=1), placeholder='Ready.')

        # Outermost box
        outer_box = toga.Box(
            children=[btn_box, self.textpanel],
            style=Pack(
                flex=1,
                direction=COLUMN,
                padding=10
            )
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    return ExampleFontExampleApp('Font Example', 'org.beeware.widgets.font')


if __name__ == '__main__':
    app = main()
    app.main_loop()
