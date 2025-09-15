import toga
from toga.colors import REBECCAPURPLE
from toga.constants import COLUMN


class SwitchApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(size=(350, 300))

        # Add the content on the main window
        self.main_window.content = toga.Box(
            children=[
                # Simple switch with label and callback function called toggled
                toga.Switch("Change Label", on_change=self.callback_label),
                # Switch with initial state
                toga.Switch("Initial state", value=True, margin_top=24),
                # Switch with label and enable option
                toga.Switch("Disabled", enabled=False, margin_top=24),
                # Switch with a big font
                toga.Switch(
                    "Big and colorful",
                    margin_top=24,
                    font_family="serif",
                    font_size=20,
                    font_weight="bold",
                    color=REBECCAPURPLE,
                ),
            ],
            direction=COLUMN,
            margin=24,
        )

        # Show the main window
        self.main_window.show()

    @staticmethod
    def callback_label(switch):
        # The label will change when you toggle the switch
        switch.text = f"Switch is {'on' if switch.value else 'off'}"


def main():
    return SwitchApp("Switches", "org.beeware.toga.examples.switch_demo")


if __name__ == "__main__":
    main().main_loop()
