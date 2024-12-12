import toga
from toga.constants import COLUMN, ROW
from toga.style import Pack


class DividerApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(size=(300, 150))

        style = Pack(margin_top=24)
        substyle = Pack(margin_right=12, margin_left=12, flex=1)

        # Add the content on the main window
        self.main_window.content = toga.Box(
            children=[
                toga.Label("Section 1"),
                toga.Divider(style=style),
                toga.Label("Section 2", style=style),
                toga.Divider(style=style),
                toga.Label("Section 3", style=style),
                toga.Box(
                    children=[
                        toga.TextInput(placeholder="First textbox"),
                        toga.Divider(direction=toga.Divider.VERTICAL, style=substyle),
                        toga.TextInput(placeholder="Second textbox"),
                    ],
                    style=Pack(direction=ROW, margin=24, flex=1),
                ),
            ],
            style=Pack(direction=COLUMN, margin=24),
        )

        # Show the main window
        self.main_window.show()


def main():
    # Application class
    #   App name and namespace
    app = DividerApp("Dividers", "org.beeware.toga.examples.divider")
    return app


if __name__ == "__main__":
    app = main()
    app.main_loop()
