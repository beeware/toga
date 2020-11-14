import toga
from toga.constants import COLUMN, ROW
from toga.style import Pack


class ExampleMultilineTextInputApp(toga.App):
    # Button callback functions
    def enable_toggle_pressed(self, widget, **kwargs):
        self.multiline_input.enabled = not self.multiline_input.enabled

    def readonly_toggle_pressed(self, widget, **kwargs):
        self.multiline_input.readonly = not self.multiline_input.readonly

    def add_content_pressed(self, widget, **kwargs):
        self.multiline_input.value = "All work and no play makes Jack a dull boy... " * 100

    def clear_pressed(self, widget, **kwargs):
        self.multiline_input.clear()

    def set_label(self, widget):
        if self.multiline_input.value == "":
            self.label.text = "Nothing has been written yet"
            return
        number_of_lines = len(self.multiline_input.value.split("\n"))
        self.label.text = "{} lines has been written".format(number_of_lines)

    def startup(self):
        self.main_window = toga.MainWindow(title=self.name)

        self.multiline_input = toga.MultilineTextInput(
            placeholder='Enter text here...',
            initial='Initial value',
            style=Pack(flex=1),
            on_change=self.set_label
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
        button_add_content = toga.Button(
            'Add content',
            on_press=self.add_content_pressed,
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
                button_add_content,
                button_clear,
            ],
            style=Pack(
                direction=ROW,
                padding=10
            )
        )
        self.label = toga.Label("Nothing has been written yet")

        outer_box = toga.Box(
            children=[btn_box, self.multiline_input, self.label],
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
