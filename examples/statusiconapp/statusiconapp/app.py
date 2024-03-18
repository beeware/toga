import toga


class ExampleStatusIconApp(toga.App):
    def startup(self):
        # Set app to be a background app
        self.main_window = toga.App.BACKGROUND

        # This app has no user interface at present. It exists to demonstrate how you
        # can build an app that persists in the background with no main window.
        #
        # Support for defining status icons is coming soon (See #97)


def main():
    return ExampleStatusIconApp(
        "Status Icon App", "org.beeware.toga.examples.statusiconapp"
    )


if __name__ == "__main__":
    app = main()
    app.main_loop()
