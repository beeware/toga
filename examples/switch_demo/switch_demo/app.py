import toga
from toga.colors import REBECCAPURPLE
from toga.constants import COLUMN
from toga.style import Pack


class SwitchApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(size=(350, 300))

        # Add the content on the main window
        self.main_window.content = toga.Box(
            children=[
                # Simple switch with label and callback function called toggled
                toga.Switch("Change Label", on_change=self.callbackLabel),
                # Switch with initial state
                toga.Switch("Initial state", value=True, style=Pack(margin_top=24)),
                # Switch with label and enable option
                toga.Switch("Disabled", enabled=False, style=Pack(margin_top=24)),
                # Switch with a big font
                toga.Switch(
                    "Big and colorful",
                    style=Pack(
                        margin_top=24,
                        font_family="serif",
                        font_size=20,
                        font_weight="bold",
                        color=REBECCAPURPLE,
                    ),
                ),
            ],
            style=Pack(direction=COLUMN, margin=24),
        )

        # Show the main window
        self.main_window.show()

    def callbackLabel(self, switch):
        # Some action when you hit the switch
        #   In this case the label will change
        switch.text = f"switch is {'on' if switch.value else 'off'}"


def main():
    # Application class
    #   App name and namespace
    app = SwitchApp("Switches", "org.beeware.toga.examples.switch_demo")
    return app


if __name__ == "__main__":
    app = main()
    app.main_loop()
