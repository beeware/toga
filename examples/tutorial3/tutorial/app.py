import toga
from toga.style.pack import CENTER, COLUMN, ROW, Pack


class Graze(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.name)

        self.webview = toga.WebView(style=Pack(flex=1))
        self.url_input = toga.TextInput(
            initial='https://github.com/',
            style=Pack(flex=1)
        )

        box = toga.Box(
            children=[
                toga.Box(
                    children=[
                        self.url_input,
                        toga.Button('Go', on_press=self.load_page, style=Pack(width=50, padding_left=5)),
                    ],
                    style=Pack(
                        direction=ROW,
                        alignment=CENTER,
                        padding=5,
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
    return Graze('Graze', 'org.beeware.graze')


if __name__ == '__main__':
    main().main_loop()
