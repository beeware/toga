import toga
from toga.style.flow import *


class Graze(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(self.name)
        self.main_window.app = self

        self.webview = toga.WebView(style=Flow(flex=1))
        self.url_input = toga.TextInput(
            initial='https://github.com/',
            style=Flow(flex=1, padding=5)
        )

        box = toga.Box(
            children=[
                toga.Box(
                    children=[
                        self.url_input,
                        toga.Button('Go', on_press=self.load_page, style=Flow(width=50, padding_right=5)),
                    ],
                    style=Flow(
                        direction=ROW
                    )
                ),
                self.webview,
            ],
            style=Flow(
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
