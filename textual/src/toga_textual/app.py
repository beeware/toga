import asyncio

from textual.app import App as TextualApp

from .window import Window


class MainWindow(Window):
    def textual_close(self):
        self.interface.app.on_exit()


class TogaApp(TextualApp):
    def __init__(self, impl):
        super().__init__()
        self.interface = impl.interface
        self.impl = impl

    def on_mount(self) -> None:
        self.impl.create()


class App:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        self.loop = asyncio.new_event_loop()
        self.native = TogaApp(self)

    def create(self):
        self.interface._startup()
        self.set_current_window(self.interface.main_window._impl)

    def create_menus(self):
        pass

    def main_loop(self):
        self.native.run()

    def set_main_window(self, window):
        self.native.push_screen(self.interface.main_window.id)

    def show_about_dialog(self):
        pass

    def beep(self):
        self.native.bell()

    def exit(self):
        self.native.exit()

    def get_current_window(self):
        pass

    def set_current_window(self, window):
        self.native.switch_screen(window.native)
        self.native.title = window.get_title()

    def enter_full_screen(self, windows):
        pass

    def exit_full_screen(self, windows):
        pass

    def show_cursor(self):
        pass

    def hide_cursor(self):
        pass


class DocumentApp(App):
    pass
