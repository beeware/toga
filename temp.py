import toga
from toga.constants import ROW
from toga.style.pack import Pack
import toga.colors
import sys

IS_LINUX = sys.platform in ["linux", "linux2"]

class TestApp(toga.App):
    def startup(self):
        # Re-enable pydev debugging in this thread.
        try:
            import pydevd;
            pydevd.settrace()
        except ImportError:
            pass
        self.main_window = toga.MainWindow(size=(300, 150))

        style = Pack(padding_top=24)
        substyle = Pack(padding_right=12, padding_left=12, flex=1)

        # Add the content on the main window
        self.main_window.content = toga.Box(
                    children=[
                        toga.Button(text="Toggle"),
                        toga.Label(text="This is a very long line of text to test the wrapping feature in GTK.", style=Pack(flex=1,background_color=toga.colors.BLUE), wrap=1),
                        toga.TextInput(placeholder="Footer"),
                    ],
                    style=Pack(direction=ROW, padding=24),
                )

        # Show the main window
        self.main_window.show()

def main():
    # Application class
    #   App name and namespace
    app = TestApp("Test", "org.beeware.toga.examples.test")
    return app


if __name__ == "__main__":
    app = main()
    app.main_loop()
