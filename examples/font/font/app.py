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

    def do_monospace_button(self, widget):
        self.textpanel.value += widget.label + '\n'

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        # Buttons
        btn_style = Pack(flex=1)
        btn_clear = toga.Button('Clear', on_press=self.do_clear, style=btn_style)
        btn1 = toga.Button('Normal', on_press=self.do_normal_button, style=btn_style)
        btn2 = toga.Button('Monospace', on_press=self.do_monospace_button, style=Pack(font_family='monospace'))
        # toga.Font.register('awesome-free-regular', 'resources/Font Awesome 5 Free-Regular-400.otf')
        toga.Font.register('awesome-free-regular', str(self.app.paths.app)+'\\resources\\Font Awesome 5 Free-Regular-400.otf')
        btn3 = toga.Button('\uf0c5', on_press=self.do_monospace_button, style=Pack(font_family='awesome-free-regular', font_size=16))
        btn_box = toga.Box(
            children=[
                btn_clear,
                btn1, btn2, btn3
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
