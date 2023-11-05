import toga
from toga.constants import COLUMN
from toga.style import Pack


# This is a SimpleApp, so the MainWindow won't have a menubar.
class ExampleSimpleApp(toga.SimpleApp):
    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow()

        # Label to show responses.
        self.label = toga.Label("Ready.")

        # Outermost box
        outer_box = toga.Box(
            children=[self.label],
            style=Pack(flex=1, direction=COLUMN, padding=10, width=500, height=300),
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    return ExampleSimpleApp("Simple App", "org.beeware.simpleapp")


if __name__ == "__main__":
    app = main()
    app.main_loop()
