import toga
from toga.constants import COLUMN, ROW


class DividerApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(size=(300, 150))

        # Add the content on the main window
        self.main_window.content = toga.Box(
            children=[
                toga.Label("Section 1"),
                toga.Divider(margin_top=24),
                toga.Label("Section 2", margin_top=24),
                toga.Divider(margin_top=24),
                toga.Label("Section 3", margin_top=24),
                toga.Box(
                    children=[
                        toga.TextInput(placeholder="First textbox"),
                        toga.Divider(
                            direction=toga.Divider.VERTICAL,
                            margin_right=12,
                            margin_left=12,
                            flex=1,
                        ),
                        toga.TextInput(placeholder="Second textbox"),
                    ],
                    direction=ROW,
                    margin=24,
                    flex=1,
                ),
            ],
            direction=COLUMN,
            margin=24,
        )

        # Show the main window
        self.main_window.show()


def main():
    return DividerApp("Dividers", "org.beeware.toga.examples.divider")


if __name__ == "__main__":
    main().main_loop()
