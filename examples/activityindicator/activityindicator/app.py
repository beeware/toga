import toga
from toga.style import Pack
from toga.constants import ROW, CENTER


class ExampleActivityIndicatorApp(toga.App):
    # Button callback functions
    def do_stuff(self, widget, **kwargs):

        if self._running:
            self.spinner.stop()
            self.button.label = 'Start'
            self._running = False
        else:
            self.spinner.start()
            self.button.label = 'Stop'
            self._running = True

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        self._running = False

        self.spinner = toga.ActivityIndicator(style=Pack(padding_left=10, height=16))
        self.button = toga.Button('Start', on_press=self.do_stuff, style=Pack(padding_right=10))

        box = toga.Box(
            children=[
                self.button,
                self.spinner
            ],
            style=Pack(direction=ROW, height=20, padding=20, alignment=CENTER, flex=1)
        )

        # Add the content on the main window
        self.main_window.content = box
        self.main_window.size = (200, 200)

        # Show the main window
        self.main_window.show()


def main():
    return ExampleActivityIndicatorApp('Activity Indicator', 'org.beeware.widgets.activityindicator')


if __name__ == '__main__':
    app = main()
    app.main_loop()
