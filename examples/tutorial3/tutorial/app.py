import toga
from toga.style.pack import *


class Graze(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(self.name)

        self.webview = toga.WebView(style=Pack(flex=1))
        self.url_input = toga.TextInput(
            initial='https://github.com/',
            style=Pack(flex=1, padding=5)
        )

        box = toga.Box(
            children=[
                toga.Box(
                    children=[
                        self.url_input,
                        toga.Button('Go', on_press=self.load_page, style=Pack(width=50, padding_right=5)),
                    ],
                    style=Pack(
                        direction=ROW
                    )
                ),
                self.webview,
            ],
            style=Pack(
                direction=COLUMN
            )
        )

        self.main_window.content = box
        self.webview.url = self.url_input.value

        # Show the main window
        self.main_window.show()

    def load_page(self, widget):
        self.webview.url = self.url_input.value


def main():
    return Graze('Graze', 'org.pybee.graze')


if __name__ == '__main__':
    main().main_loop()
