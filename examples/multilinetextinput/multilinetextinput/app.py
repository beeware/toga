import toga
from toga.constants import COLUMN, ROW
from toga.style import Pack


class ExampleMultilineTextInputApp(toga.App):
    # Button callback functions
    def enable_toggle_pressed(self, widget, **kwargs):
        self.multiline_input.enabled = not self.multiline_input.enabled

    def readonly_toggle_pressed(self, widget, **kwargs):
        self.multiline_input.readonly = not self.multiline_input.readonly

    def clear_pressed(self, widget, **kwargs):
        self.multiline_input.clear()

    def startup(self):
        self.main_window = toga.MainWindow(title=self.name)

        self.multiline_input = toga.MultilineTextInput(
            placeholder='Enter text here...',
            initial='Initial value',
            style=Pack(flex=1)
        )

        button_toggle_enabled = toga.Button(
            'Toggle enabled',
            on_press=self.enable_toggle_pressed,
            style=Pack(flex=1)
        )
        button_toggle_readonly = toga.Button(
            'Toggle readonly',
            on_press=self.readonly_toggle_pressed,
            style=Pack(flex=1)
        )
        button_clear = toga.Button(
            'Clear',
            on_press=self.clear_pressed,
            style=Pack(flex=1)
        )
        btn_box = toga.Box(
            children=[
                button_toggle_enabled,
                button_toggle_readonly,
                button_clear
            ],
            style=Pack(
                direction=ROW,
                padding=10
            )
        )

        outer_box = toga.Box(
            children=[btn_box, self.multiline_input],
            style=Pack(
                direction=COLUMN,
                padding=10
            )
        )

        self.main_window.content = outer_box
        self.main_window.show()


def main():
    return ExampleMultilineTextInputApp('Multiline Text Input', 'org.beeware.widgets.multilinetextinput')


if __name__ == '__main__':
    app = main()
    app.main_loop()
