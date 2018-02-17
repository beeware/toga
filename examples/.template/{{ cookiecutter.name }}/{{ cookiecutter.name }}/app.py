import toga
from colosseum import CSS


class Example{{ cookiecutter.widget_name }}App(toga.App):
    # Button callback functions
    def do_stuff(self, widget, **kwargs):
        self.label.text = "Do stuff."

    def do_clear(self, widget, **kwargs):
        self.label.text = "Ready."

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(self.name)

        # Label to show responses.
        label = toga.Label('Ready.')

        widget = toga.{{ cookiecutter.widget_name }}()

        # Buttons
        btn_style = CSS(flex=1)
        btn_do_stuff = toga.Button('Do stuff', on_press=self.do_stuff, style=btn_style)
        btn_clear = toga.Button('Clear', on_press=do_clear, style=btn_style)
        btn_box = toga.Box(
            children=[
                btn_do_stuff,
                btn_clear
            ],
            style=CSS(flex_direction='row')
        )

        # Outermost box
        outer_box = toga.Box(
            children=[btn_box, widget, label],
            style=CSS(
                flex=1,
                flex_direction='column',
                padding=10,
                min_width=500,
                min_height=300
            )
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    return Example{{ cookiecutter.widget_name }}App('{{ cookiecutter.formal_name }}', 'org.pybee.widgets.{{ cookiecutter.name }}')


if __name__ == '__main__':
    app = main()
    app.main_loop()
