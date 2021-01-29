import toga
from toga.style import Pack
from toga.constants import COLUMN, ROW


class WindowDemoApp(toga.App):
    # Button callback functions
    def do_get_position(self, widget, **kwargs):
        self.label.text = "Current position: "+str(self.main_window.position)

    def do_set_position(self, widget, **kwargs):
        self.main_window.position = (int(self.X.value), int(self.Y.value))

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name, position=(200, 300))
        flex_style = Pack(flex=1)

        # Label to show responses.
        self.label = toga.Label('Ready.', style=flex_style)

        # Input fields for new position
        self.X = toga.TextInput(placeholder='new X position')
        self.Y = toga.TextInput(placeholder='new Y position')

        # Buttons
        btn_do_get = toga.Button('Get window position', on_press=self.do_get_position, style=flex_style)
        btn_do_set = toga.Button('Set window position', on_press=self.do_set_position, style=flex_style)
        label_box = toga.Box(
            children=[
                self.label
            ],
            style=Pack(direction=ROW)
        )
        input_box = toga.Box(
            children=[
                self.X, self.Y
            ],
            style=Pack(direction=ROW)
        )

        # Outermost box
        outer_box = toga.Box(
            children=[label_box, btn_do_get, input_box, btn_do_set],
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
    return WindowDemoApp('Window Demo', 'org.beeware.widgets.window_demo')


if __name__ == '__main__':
    app = main()
    app.main_loop()
