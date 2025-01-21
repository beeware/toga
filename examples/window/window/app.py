import asyncio
from datetime import datetime
from functools import partial

import toga
from toga.constants import COLUMN, RIGHT, ROW, WindowState
from toga.style import Pack


class WindowDemoApp(toga.App):
    # Button callback functions
    def do_origin(self, widget, **kwargs):
        self.main_window.position = (0, 0)
        self.do_report()

    def do_up(self, widget, **kwargs):
        self.main_window.position = (
            self.main_window.position.x,
            self.main_window.position.y - 200,
        )
        self.do_report()

    def do_down(self, widget, **kwargs):
        self.main_window.position = (
            self.main_window.position.x,
            self.main_window.position.y + 200,
        )
        self.do_report()

    def do_left(self, widget, **kwargs):
        self.main_window.position = (
            self.main_window.position.x - 200,
            self.main_window.position.y,
        )
        self.do_report()

    def do_right(self, widget, **kwargs):
        self.main_window.position = (
            self.main_window.position.x + 200,
            self.main_window.position.y,
        )
        self.do_report()

    def do_screen_top(self, widget, **kwargs):
        self.main_window.screen_position = (
            self.main_window.screen_position.x,
            0,
        )
        self.do_report()

    def do_screen_bottom(self, widget, **kwargs):
        self.main_window.screen_position = (
            self.main_window.screen_position.x,
            self.main_window.screen.size.height - self.main_window.size.height,
        )
        self.do_report()

    def do_screen_left(self, widget, **kwargs):
        self.main_window.screen_position = (
            0,
            self.main_window.screen_position.y,
        )
        self.do_report()

    def do_screen_right(self, widget, **kwargs):
        self.main_window.screen_position = (
            self.main_window.screen.size.width - self.main_window.size.width,
            self.main_window.screen_position.y,
        )
        self.do_report()

    def do_small(self, widget, **kwargs):
        self.main_window.size = (400, 300)
        self.do_report()

    def do_large(self, widget, **kwargs):
        self.main_window.size = (1500, 1000)
        self.do_report()

    def do_current_window_state(self, widget, **kwargs):
        self.label.text = f"Current state: {self.main_window.state}"

    def do_window_state_normal(self, widget, **kwargs):
        self.main_window.state = WindowState.NORMAL

    def do_window_state_maximize(self, widget, **kwargs):
        self.main_window.state = WindowState.MAXIMIZED

    def do_window_state_minimize(self, widget, **kwargs):
        self.main_window.state = WindowState.MINIMIZED
        for i in range(5, 0, -1):
            print(f"Back in {i}...")
            yield 1
        self.main_window.state = WindowState.NORMAL

    def do_window_state_full_screen(self, widget, **kwargs):
        self.main_window.state = WindowState.FULLSCREEN

    def do_window_state_presentation(self, widget, **kwargs):
        self.main_window.state = WindowState.PRESENTATION

    def do_app_presentation_mode(self, widget, **kwargs):
        if self.in_presentation_mode:
            self.exit_presentation_mode()
        else:
            self.enter_presentation_mode([self.main_window])

    def do_title(self, widget, **kwargs):
        self.main_window.title = f"Time is {datetime.now()}"

    def do_new_windows(self, widget, **kwargs):
        non_resize_window = toga.Window(
            "Non-resizable Window",
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

        second_main_window = toga.MainWindow()
        extra_command = toga.Command(
            lambda cmd: print("A little extra"),
            text="Extra",
            icon=toga.Icon.APP_ICON,
        )
        second_main_window.toolbar.add(extra_command)
        second_main_window.show()

    def do_screen_change(self, screen, widget, **kwargs):
        self.current_window.screen = screen
        self.do_report()

    async def do_save_screenshot(self, screen, window, **kwargs):
        screenshot = screen.as_image()
        path = await self.main_window.save_file_dialog(
            "Save screenshot",
            suggested_filename=f"Screenshot_{screen.name}.png",
            file_types=["png"],
        )
        if path is None:
            return
        screenshot.save(path)

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

    def do_report(self, *args, **kwargs):
        window = self.main_window
        screen = window.screen
        self.label.text = (
            f"Window: size={tuple(window.size)}, position={tuple(window.position)}, "
            f"screen_position={tuple(window.screen_position)}\n"
            f"Screen: name={screen.name!r}, size={tuple(screen.size)}, "
            f"origin={tuple(screen.origin)}"
        )

    def do_next_content(self, widget):
        self.main_window.content = self.next_box

    def do_prev_content(self, widget):
        self.main_window.content = self.main_scroller

    async def do_hide(self, widget):
        self.main_window.visible = False
        for i in range(5, 0, -1):
            print(f"Back in {i}...")
            await asyncio.sleep(1)
        self.main_window.visible = True
        await self.main_window.dialog(toga.InfoDialog("Here we go again", "I'm back!"))

    def do_beep(self, widget):
        self.app.beep()

    async def on_exit(self):
        self.close_count += 1
        if self.close_count % 2 == 1:
            await self.main_window.dialog(
                toga.InfoDialog("Can't close app", "Try that again")
            )
            return False
        return True

    async def close_handler(self, window, **kwargs):
        self.close_count += 1
        if self.close_count % 2 == 1:
            await self.main_window.dialog(
                toga.InfoDialog("Can't close window", "Try that again")
            )
            return False
        return True

    def startup(self):
        # Track in-app closes
        self.close_count = 0

        # Set up main window
        self.main_window = toga.MainWindow()

        # Label to show responses.
        self.label = toga.Label("Ready.")

        # Buttons
        btn_style = Pack(flex=1, margin=5)

        row_move = toga.Box(
            style=Pack(direction=ROW),
            children=[
                toga.Label("Move: "),
                toga.Button("Origin", on_press=self.do_origin, style=btn_style),
                toga.Button("Up", on_press=self.do_up, style=btn_style),
                toga.Button("Down", on_press=self.do_down, style=btn_style),
                toga.Button("Left", on_press=self.do_left, style=btn_style),
                toga.Button("Right", on_press=self.do_right, style=btn_style),
            ],
        )

        row_screen_edge = toga.Box(
            style=Pack(direction=ROW),
            children=[
                toga.Label("Screen edge: "),
                toga.Button("Top", on_press=self.do_screen_top, style=btn_style),
                toga.Button("Bottom", on_press=self.do_screen_bottom, style=btn_style),
                toga.Button("Left", on_press=self.do_screen_left, style=btn_style),
                toga.Button("Right", on_press=self.do_screen_right, style=btn_style),
            ],
        )

        btn_do_small = toga.Button(
            "Become small", on_press=self.do_small, style=btn_style
        )
        btn_do_large = toga.Button(
            "Become large", on_press=self.do_large, style=btn_style
        )
        btn_do_current_window_state = toga.Button(
            "Get current window state",
            on_press=self.do_current_window_state,
            style=btn_style,
        )
        btn_do_window_state_normal = toga.Button(
            "Make window state normal",
            on_press=self.do_window_state_normal,
            style=btn_style,
        )
        btn_do_window_state_maximize = toga.Button(
            "Make window state maximized",
            on_press=self.do_window_state_maximize,
            style=btn_style,
        )
        btn_do_window_state_minimize = toga.Button(
            "Make window state minimized",
            on_press=self.do_window_state_minimize,
            style=btn_style,
        )
        btn_do_window_state_full_screen = toga.Button(
            "Make window state full screen",
            on_press=self.do_window_state_full_screen,
            style=btn_style,
        )
        btn_do_window_state_presentation = toga.Button(
            "Make window state presentation",
            on_press=self.do_window_state_presentation,
            style=btn_style,
        )
        btn_do_app_presentation_mode = toga.Button(
            "Toggle app presentation mode",
            on_press=self.do_app_presentation_mode,
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

        screen_change_btns_box = toga.Box(
            children=[
                toga.Label(
                    text="Move current window to:",
                    style=Pack(width=200, text_align=RIGHT),
                )
            ],
            style=Pack(margin=5),
        )
        for index, screen in sorted(enumerate(self.screens), key=lambda s: s[1].origin):
            screen_change_btns_box.add(
                toga.Button(
                    text=f"{index}: {screen.name}",
                    on_press=partial(self.do_screen_change, screen),
                    style=Pack(margin_left=5),
                )
            )
        screen_as_image_btns_box = toga.Box(
            children=[
                toga.Label(
                    text="Take screenshot of screen:",
                    style=Pack(width=200, text_align=RIGHT),
                )
            ],
            style=Pack(margin=5),
        )
        for index, screen in sorted(enumerate(self.screens), key=lambda s: s[1].origin):
            screen_as_image_btns_box.add(
                toga.Button(
                    text=f"{index}: {screen.name}",
                    on_press=partial(self.do_save_screenshot, screen),
                    style=Pack(margin_left=5),
                )
            )

        self.inner_box = toga.Box(
            children=[
                self.label,
                row_move,
                row_screen_edge,
                btn_do_report,
                btn_do_small,
                btn_do_large,
                btn_do_current_window_state,
                btn_do_window_state_normal,
                btn_do_window_state_maximize,
                btn_do_window_state_minimize,
                btn_do_window_state_full_screen,
                btn_do_window_state_presentation,
                btn_do_app_presentation_mode,
                btn_do_title,
                btn_do_new_windows,
                btn_do_current_window_cycling,
                btn_do_hide_cursor,
                btn_change_content,
                btn_hide,
                btn_beep,
                screen_change_btns_box,
                screen_as_image_btns_box,
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
            icon=toga.Icon.APP_ICON,
        )

        self.commands.add(restore_command)
        self.main_window.toolbar.add(restore_command)

        # Add the content on the main window
        self.main_window.content = self.main_scroller

        # Show the main window
        self.main_window.show()


def main():
    return WindowDemoApp("Window Demo", "org.beeware.toga.examples.window")


if __name__ == "__main__":
    app = main()
    app.main_loop()
