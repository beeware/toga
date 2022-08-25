import toga
from toga.constants import COLUMN
from toga.style import Pack


class SwitchApp(toga.App):

    def startup(self):
        # Window class
        #   Main window of the application with title and size
        self.main_window = toga.MainWindow(title=self.name, size=(350, 300))

        # Add the content on the main window
        self.main_window.content = toga.Box(
            children=[
                # Simple switch with label and callback function called toggled
                toga.Switch('Change Label', on_change=self.callbackLabel),

                # Switch with initial state
                toga.Switch('Initial state', value=True, style=Pack(padding_top=24)),

                # Switch with label and enable option
                toga.Switch('Disabled', enabled=False, style=Pack(padding_top=24)),

                # Switch with a big font
                toga.Switch('Big font', style=Pack(padding_top=24, font_family='serif', font_size=20,
                                                   font_weight='bold'))
            ],
            style=Pack(direction=COLUMN, padding=24)
        )

        # Show the main window
        self.main_window.show()

    def callbackLabel(self, switch):
        # Some action when you hit the switch
        #   In this case the label will change
        switch.text = "switch is %s" % {0: "off", 1: "on"}[switch.value]


def main():
    # Application class
    #   App name and namespace
    app = SwitchApp('Switches', 'org.beeware.helloworld')
    return app


if __name__ == '__main__':
    app = main()
    app.main_loop()
