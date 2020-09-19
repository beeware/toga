import toga
from toga.colors import BLUE, RED
from toga.constants import CENTER, COLUMN, GREEN, ROW, WHITE, YELLOW
from toga.style import Pack


class ExampleFocusApp(toga.App):
    a_button: toga.Button
    b_button: toga.Button
    c_button: toga.Button

    def startup(self):
        # Window class
        #   Main window of the application with title and size
        #   Also make the window non-resizable and non-minimizable.
        self.main_window = toga.MainWindow(
            title=self.name, size=(800, 500),
            resizeable=False, minimizable=False
        )

        self.a_button = toga.Button("A", on_press=self.on_button_press)
        self.b_button = toga.Button("B", on_press=self.on_button_press)
        self.c_button = toga.Button("C", on_press=self.on_button_press)
        # Add the content on the main window
        self.main_window.content = toga.Box(
            children=[self.a_button, self.b_button, self.c_button]
        )

        BUTTONS_GROUP = toga.Group("Buttons", order=2)
        self.commands.add(
            toga.Command(
                lambda widget: self.focus_on(self.a_button),
                label="Focus on A",
                shortcut=toga.Key.MOD_1 + "a",
                group=BUTTONS_GROUP
            ),
            toga.Command(
                lambda widget: self.focus_on(self.b_button),
                label="Focus on B",
                shortcut=toga.Key.MOD_1 + "b",
                group=BUTTONS_GROUP
            ),
            toga.Command(
                lambda widget: self.focus_on(self.c_button),
                label="Focus on C",
                shortcut=toga.Key.MOD_1 + "c",
                group=BUTTONS_GROUP
            )
        )
        # Show the main window
        self.main_window.show()

    @classmethod
    def on_button_press(cls, widget: toga.Button):
        print(widget.label, "was pressed.")

    @classmethod
    def focus_on(cls, button: toga.Button):
        button.focus()


def main():
    # Application class
    #   App name and namespace
    app = ExampleFocusApp('Focus', 'org.beeware.widgets.focus')
    return app
