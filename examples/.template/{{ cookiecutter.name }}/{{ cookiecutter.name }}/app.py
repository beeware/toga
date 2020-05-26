import toga
from toga.style import Pack
from toga.constants import COLUMN, ROW


class Example{{ cookiecutter.widget_name }}App(toga.App):
    # Button callback functions
    def do_stuff(self, widget, **kwargs):
        self.label.text = "Do stuff."

    def do_clear(self, widget, **kwargs):
        self.label.text = "Ready."

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        # Label to show responses.
        self.label = toga.Label('Ready.')

        widget = toga.{{ cookiecutter.widget_name }}()

        # Buttons
        btn_style = Pack(flex=1)
        btn_do_stuff = toga.Button('Do stuff', on_press=self.do_stuff, style=btn_style)
        btn_clear = toga.Button('Clear', on_press=self.do_clear, style=btn_style)
        btn_box = toga.Box(
            children=[
                btn_do_stuff,
                btn_clear
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
    return Example{{ cookiecutter.widget_name }}App('{{ cookiecutter.formal_name }}', 'org.beeware.widgets.{{ cookiecutter.name }}')


if __name__ == '__main__':
    app = main()
    app.main_loop()
