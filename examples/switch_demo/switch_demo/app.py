import toga
from toga.colors import REBECCAPURPLE
from toga.constants import COLUMN, SwitchRole


class SwitchApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(size=(350, 300))

        # Add the content on the main window
        self.main_window.content = toga.Box(
            children=[
                toga.Box(
                    children=[
                        toga.Label(f"role={role}"),
                        # Simple switch with label and callback function called toggled
                        toga.Switch(
                            "Change Label", role=role, on_change=self.callback_label
                        ),
                        # Switch with initial state
                        toga.Switch("Initial state", role=role, value=True),
                        # Switch with label and enable option
                        toga.Switch("Disabled", role=role, enabled=False),
                        # Switch with a big font
                        toga.Switch(
                            "Big and colorful",
                            font_family="serif",
                            font_size=20,
                            font_weight="bold",
                            color=REBECCAPURPLE,
                            role=role,
                        ),
                    ],
                    direction=COLUMN,
                    gap=8,
                )
                for role in (SwitchRole.AUTOMATIC, SwitchRole.MAJOR, SwitchRole.MINOR)
            ],
            direction=COLUMN,
            margin=24,
            gap=20,
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
