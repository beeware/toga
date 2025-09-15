import toga
from toga.constants import BLUE, CENTER, COLUMN, GREEN, RED, ROW, WHITE, YELLOW


class BoxApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(
            size=(800, 500), resizable=False, minimizable=False
        )
        self.yellow_button = toga.Button(
            text="Set yellow color",
            on_press=self.set_yellow_color,
            background_color=YELLOW,
        )
        self.inner_box = toga.Box(
            direction=ROW,
            children=[
                toga.Button(
                    text="Set red color",
                    on_press=self.set_red_color,
                    background_color=RED,
                ),
                self.yellow_button,
                toga.Button(
                    text="Set blue color",
                    on_press=self.set_blue_color,
                    background_color=BLUE,
                ),
                toga.Button(
                    text="Set green color",
                    on_press=self.set_green_color,
                    background_color=GREEN,
                ),
                toga.Button(
                    text="Reset color",
                    on_press=self.reset_color,
                    background_color=WHITE,
                ),
            ],
        )
        #  Create the outer box with 2 rows
        self.outer_box = toga.Box(
            direction=COLUMN,
            flex=1,
            children=[
                self.inner_box,
                toga.Label(text="Hello to my world!", text_align=CENTER),
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
        del self.outer_box.style.background_color

    def toggle_yellow_button(self, widget):
        if widget.value:
            self.inner_box.insert(1, self.yellow_button)
        else:
            self.inner_box.remove(self.yellow_button)


def main():
    return BoxApp("Box", "org.beeware.toga.examples.boxes")


if __name__ == "__main__":
    main().main_loop()
