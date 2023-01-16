import toga
from toga.constants import BLUE, CENTER, COLUMN, GREEN, RED, ROW, WHITE, YELLOW
from toga.style import Pack


class ExampleBoxApp(toga.App):
    def startup(self):
        # Window class
        #   Main window of the application with title and size
        #   Also make the window non-resizable and non-minimizable.
        self.main_window = toga.MainWindow(
            title=self.name, size=(800, 500), resizeable=False, minimizable=False
        )
        self.yellow_button = toga.Button(
            text="Set yellow color",
            on_press=self.set_yellow_color,
            style=Pack(background_color=YELLOW),
        )
        self.inner_box = toga.Box(
            style=Pack(direction=ROW),
            children=[
                toga.Button(
                    text="Set red color",
                    on_press=self.set_red_color,
                    style=Pack(background_color=RED),
                ),
                self.yellow_button,
                toga.Button(
                    text="Set blue color",
                    on_press=self.set_blue_color,
                    style=Pack(background_color=BLUE),
                ),
                toga.Button(
                    text="Set green color",
                    on_press=self.set_green_color,
                    style=Pack(background_color=GREEN),
                ),
                toga.Button(
                    text="Reset color",
                    on_press=self.reset_color,
                    style=Pack(background_color=WHITE),
                ),
            ],
        )
        #  Create the outer box with 2 rows
        self.outer_box = toga.Box(
            style=Pack(direction=COLUMN, flex=1),
            children=[
                self.inner_box,
                toga.Label(text="Hello to my world!", style=Pack(text_align=CENTER)),
                toga.Switch(
                    "Enable yellow", value=True, on_change=self.toggle_yellow_button
                ),
            ],
        )

        # Add the content on the main window
        self.main_window.content = self.outer_box

        # Show the main window
        self.main_window.show()

    def set_red_color(self, widget):
        self.outer_box.style.background_color = RED

    def set_yellow_color(self, widget):
        self.outer_box.style.background_color = YELLOW

    def set_blue_color(self, widget):
        self.outer_box.style.background_color = BLUE

    def set_green_color(self, widget):
        self.outer_box.style.background_color = GREEN

    def reset_color(self, widget):
        self.outer_box.style.background_color = None

    def toggle_yellow_button(self, widget):
        if widget.value:
            self.inner_box.insert(1, self.yellow_button)
        else:
            self.inner_box.remove(self.yellow_button)


def main():
    # Application class
    #   App name and namespace
    app = ExampleBoxApp("Box", "org.beeware.widgets.boxes")
    return app


if __name__ == "__main__":
    app = main()
    app.main_loop()
