import asyncio
from datetime import datetime

import toga
from toga.constants import COLUMN
from toga.style import Pack


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

    def do_app_full_screen(self, widget, **kwargs):
        if self.is_full_screen:
            self.exit_full_screen()
        else:
            self.set_full_screen(self.main_window)

    def do_window_full_screen(self, widget, **kwargs):
        self.main_window.full_screen = not self.main_window.full_screen

    def do_title(self, widget, **kwargs):
        self.main_window.title = f"Time is {datetime.now()}"

    def do_new_windows(self, widget, **kwargs):
        non_resize_window = toga.Window(
            "Non-resizable Window",
            position=(200, 200),
            size=(300, 300),
            resizable=False,
            on_close=self.close_handler,
        )
        non_resize_window.content = toga.Box(
            children=[toga.Label("This window is not resizable")]
        )
        non_resize_window.show()

        non_close_window = toga.Window(
            "Non-closeable Window",
            position=(300, 300),
            size=(300, 300),
            closable=False,
        )
        non_close_window.content = toga.Box(
            children=[toga.Label("This window is not closable")]
        )
        non_close_window.show()

        no_close_handler_window = toga.Window(
            "No close handler",
            position=(400, 400),
            size=(300, 300),
        )
        no_close_handler_window.content = toga.Box(
            children=[toga.Label("This window has no close handler")]
        )
        no_close_handler_window.show()

    async def do_current_window_cycling(self, widget, **kwargs):
        for window in self.windows:
            self.current_window = window
            self.label.text = f"Current window is {self.current_window.id}"
            await asyncio.sleep(1)

    async def do_hide_cursor(self, widget, **kwargs):
        self.hide_cursor()
        self.label.text = "Momentarily hiding cursor..."

        await asyncio.sleep(2)

        self.show_cursor()
        self.label.text = "Cursor should be back!"

    def do_report(self, widget, **kwargs):
        self.label.text = (
            f"Window {self.main_window.title!r} "
            f"has size {self.main_window.size!r} "
            f"at {self.main_window.position!r}"
        )

    def do_next_content(self, widget):
        self.main_window.content = self.next_box

    def do_prev_content(self, widget):
        self.main_window.content = self.main_scroller

    def do_hide(self, widget):
        self.main_window.visible = False
        for i in range(5, 0, -1):
            print(f"Back in {i}...")
            yield 1
        self.main_window.visible = True
        self.main_window.info_dialog("Here we go again", "I'm back!")

    def do_beep(self, widget):
        self.app.beep()

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
        self.label = toga.Label("Ready.")

        # Buttons
        btn_style = Pack(flex=1, padding=5)
        btn_do_origin = toga.Button(
            "Go to origin", on_press=self.do_origin, style=btn_style
        )
        btn_do_left = toga.Button("Go left", on_press=self.do_left, style=btn_style)
        btn_do_right = toga.Button("Go right", on_press=self.do_right, style=btn_style)
        btn_do_small = toga.Button(
            "Become small", on_press=self.do_small, style=btn_style
        )
        btn_do_large = toga.Button(
            "Become large", on_press=self.do_large, style=btn_style
        )
        btn_do_app_full_screen = toga.Button(
            "Make app full screen", on_press=self.do_app_full_screen, style=btn_style
        )
        btn_do_window_full_screen = toga.Button(
            "Make window full screen",
            on_press=self.do_window_full_screen,
            style=btn_style,
        )
        btn_do_title = toga.Button(
            "Change title", on_press=self.do_title, style=btn_style
        )
        btn_do_new_windows = toga.Button(
            "Create Window", on_press=self.do_new_windows, style=btn_style
        )
        btn_do_current_window_cycling = toga.Button(
            "Cycle between windows",
            on_press=self.do_current_window_cycling,
            style=btn_style,
        )
        btn_do_hide_cursor = toga.Button(
            "Hide cursor",
            on_press=self.do_hide_cursor,
            style=btn_style,
        )
        btn_do_report = toga.Button("Report", on_press=self.do_report, style=btn_style)
        btn_change_content = toga.Button(
            "Change content", on_press=self.do_next_content, style=btn_style
        )
        btn_hide = toga.Button("Hide", on_press=self.do_hide, style=btn_style)
        btn_beep = toga.Button("Beep", on_press=self.do_beep, style=btn_style)

        self.inner_box = toga.Box(
            children=[
                self.label,
                btn_do_origin,
                btn_do_left,
                btn_do_right,
                btn_do_small,
                btn_do_large,
                btn_do_app_full_screen,
                btn_do_window_full_screen,
                btn_do_title,
                btn_do_new_windows,
                btn_do_current_window_cycling,
                btn_do_hide_cursor,
                btn_do_report,
                btn_change_content,
                btn_hide,
                btn_beep,
            ],
            style=Pack(direction=COLUMN),
        )
        self.main_scroller = toga.ScrollContainer(
            horizontal=False,
            vertical=True,
            style=Pack(flex=1),
        )
        self.main_scroller.content = self.inner_box

        btn_change_back = toga.Button(
            "Go back", on_press=self.do_prev_content, style=btn_style
        )
        self.next_box = toga.Box(
            children=[btn_change_back], style=Pack(direction=COLUMN)
        )

        restore_command = toga.Command(
            self.do_prev_content,
            text="Restore content",
            tooltip="Restore main window content",
        )

        self.commands.add(restore_command)
        self.main_window.toolbar.add(restore_command)

        # Add the content on the main window
        self.main_window.content = self.main_scroller

        # Show the main window
        self.main_window.show()


def main():
    return WindowDemoApp("Window Demo", "org.beeware.widgets.window")


if __name__ == "__main__":
    app = main()
    app.main_loop()
