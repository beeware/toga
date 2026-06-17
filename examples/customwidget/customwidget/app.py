from hello_world_widget.hello_world import HelloWorld

import toga


class CustomWidgetApp(toga.App):
    def startup(self):
        # Set up a minimalist main window
        self.main_window = toga.Window()

        # Label to show responses.
        self.hello_world = HelloWorld(
            font_family=["fantasy"],
            font_size=24,
            text_align="center",
            margin=5,
        )

        self.main_window.content = self.hello_world

        self.main_window.show()


def main():
    return CustomWidgetApp(
        "Custom Widget App",
        "org.beeware.toga.examples.customwidget",
    )


if __name__ == "__main__":
    main().main_loop()
