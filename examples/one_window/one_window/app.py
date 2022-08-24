import toga
from one_window.welcome_box import WelcomeBox
from one_window.main_box import MainBox


class ExampleOneWindow(toga.App):
    welcome_box: WelcomeBox
    main_box: MainBox

    def startup(self):
        # Set up main window
        self.main_window = toga.Window(title=self.name, size=(1000, 500))
        self.welcome_box = WelcomeBox(on_start=self.move_next)
        self.main_box = MainBox(on_back=self.move_back)
        self.main_window.content = self.welcome_box

        # Show the main window
        self.main_window.show()

    def move_next(self):
        self.main_window.content = self.main_box

    def move_back(self):
        self.main_window.content = self.welcome_box


def main():
    return ExampleOneWindow("Demo NumberInput", "org.beeware.widgets.numberinput")


if __name__ == "__main__":
    app = main()
    app.main_loop()
