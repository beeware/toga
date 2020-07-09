import toga
from toga.colors import BLUE, RED
from toga.constants import CENTER, COLUMN, GREEN, ROW, WHITE
from toga.style import Pack


class ExampleBoxApp(toga.App):
    def startup(self):
        # Window class
        #   Main window of the application with title and size
        #   Also make the window non-resizable and non-minimizable.
        self.main_window = toga.MainWindow(
            title=self.name, size=(800, 500),
            resizeable=False, minimizable=False
        )
        inner_box = toga.Box(
            style=Pack(direction=ROW),
            children=[
                toga.Button(
                    label="Set red color",
                    on_press=self.set_red_color,
                    style=Pack(background_color=RED)
                ),
                toga.Button(
                    label="Set blue color",
                    on_press=self.set_blue_color,
                    style=Pack(background_color=BLUE)
                ),
                toga.Button(
                    label="Set green color",
                    on_press=self.set_green_color,
                    style=Pack(background_color=GREEN)
                ),
                toga.Button(
                    label="Reset color",
                    on_press=self.reset_color,
                    style=Pack(background_color=WHITE)
                )
            ]
        )
        #  Create the outer box with 2 rows
        self.outer_box = toga.Box(
            style=Pack(direction=COLUMN, flex=1),
            children=[
                inner_box,
                toga.Label(text="Hello to my world!", style=Pack(text_align=CENTER))
            ]
        )

        # Add the content on the main window
        self.main_window.content = self.outer_box

        # Show the main window
        self.main_window.show()

    def set_red_color(self, widget):
        self.outer_box.style.background_color = RED

    def set_blue_color(self, widget):
        self.outer_box.style.background_color = BLUE

    def set_green_color(self, widget):
        self.outer_box.style.background_color = GREEN

    def reset_color(self, widget):
        self.outer_box.style.background_color = None


def main():
    # Application class
    #   App name and namespace
    app = ExampleBoxApp('Box', 'org.beeware.widgets.boxes')
    return app
