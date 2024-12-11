import toga
from toga.style import Pack


class ExampleSimpleApp(toga.App):
    def startup(self):
        # Set up a minimalist main window
        self.main_window = toga.Window()

        # Label to show responses.
        self.label = toga.Label("Ready.")

        # Outermost box
        outer_box = toga.Box(
            children=[self.label],
            style=Pack(margin=10),
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    return ExampleSimpleApp("Simple App", "org.beeware.toga.examples.simpleapp")


if __name__ == "__main__":
    app = main()
    app.main_loop()
