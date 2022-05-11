from datetime import datetime

import toga
from toga.style import Pack
from toga.constants import COLUMN


class WindowDemoApp(toga.App):
    # Button callback functions
    def do_origin(self, widget, **kwargs):
        self.main_window.position = (0, 0)

    def do_left(self, widget, **kwargs):
        self.main_window.position = (-1000, 500)

    def do_right(self, widget, **kwargs):
        self.main_window.position = (2000, 500)

    def do_small(self, widget, **kwargs):
        self.main_window.size = (400, 300)

    def do_large(self, widget, **kwargs):
        self.main_window.size = (1500, 1000)

    def do_title(self, widget, **kwargs):
        self.main_window.title = f"Time is {datetime.now()}"

    def do_new_windows(self, widget, **kwargs):
        non_resize_window = toga.Window(
            "Non-resizable Window",
            position=(200, 200),
            size=(300, 300),
            resizeable=False,
            on_close=self.close_handler,
        )
        non_resize_window.content = toga.Box(
            children=[toga.Label("This window is not resizable")]
        )
        self.app.windows += non_resize_window
        non_resize_window.show()

        non_close_window = toga.Window(
            "Non-closeable Window",
            position=(300, 300),
            size=(300, 300),
            closeable=False,
        )
        non_close_window.content = toga.Box(
            children=[toga.Label("This window is not closeable")]
        )
        self.app.windows += non_close_window
        non_close_window.show()

        no_close_handler_window = toga.Window(
            "No close handler",
            position=(400, 400),
            size=(300, 300),
        )
        no_close_handler_window.content = toga.Box(
            children=[toga.Label("This window has no close handler")]
        )
        self.app.windows += no_close_handler_window
        no_close_handler_window.show()

    def do_report(self, widget, **kwargs):
        self.label.text = (
            f"Window {self.main_window.title!r} "
            f"has size {self.main_window.size!r} "
            f"at {self.main_window.position!r}"
        )

    def exit_handler(self, app, **kwargs):
        self.close_count += 1
        if self.close_count % 2 == 1:
            self.main_window.info_dialog("Can't close app", "Try that again")
            return False
        return True

    def close_handler(self, window, **kwargs):
        self.close_count += 1
        if self.close_count % 2 == 1:
            self.main_window.info_dialog("Can't close window", "Try that again")
            return False
        return True

    def startup(self):
        # Track in-app closes
        self.close_count = 0

        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)
        self.on_exit = self.exit_handler

        # Label to show responses.
        self.label = toga.Label('Ready.')

        # Buttons
        btn_style = Pack(flex=1, padding=5)
        btn_do_origin = toga.Button('Go to origin', on_press=self.do_origin, style=btn_style)
        btn_do_left = toga.Button('Go left', on_press=self.do_left, style=btn_style)
        btn_do_right = toga.Button('Go right', on_press=self.do_right, style=btn_style)
        btn_do_small = toga.Button('Become small', on_press=self.do_small, style=btn_style)
        btn_do_large = toga.Button('Become large', on_press=self.do_large, style=btn_style)
        btn_do_title = toga.Button('Change title', on_press=self.do_title, style=btn_style)
        btn_do_new_windows = toga.Button('Create Window', on_press=self.do_new_windows, style=btn_style)
        btn_do_report = toga.Button('Report', on_press=self.do_report, style=btn_style)
        btn_box = toga.Box(
            children=[
                self.label,
                btn_do_origin,
                btn_do_left,
                btn_do_right,
                btn_do_small,
                btn_do_large,
                btn_do_title,
                btn_do_new_windows,
                btn_do_report,
            ],
            style=Pack(direction=COLUMN)
        )

        # Add the content on the main window
        self.main_window.content = btn_box

        # Show the main window
        self.main_window.show()


def main():
    return WindowDemoApp('Window Demo', 'org.beeware.widgets.window')


if __name__ == '__main__':
    app = main()
    app.main_loop()
