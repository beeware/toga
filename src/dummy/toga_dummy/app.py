from toga import Command
from .utils import LoggedObject, not_required_on
from .window import Window


class MainWindow(Window):
    @not_required_on('mobile')
    def on_close(self):
        self.action('handle MainWindow on_close')


def dummy_command(app, name):
    app._set_value("{name} command".format(name=name), name)
    return Command(None, name)


class App(LoggedObject):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface

    def create(self):
        self._action('create')

    @not_required_on('mobile')
    def create_menus(self):
        self._action('create menus')

    def main_loop(self):
        self._action('main loop')

    def set_main_window(self, window):
        self._set_value('main_window', window)

    def exit(self):
        self._action('exit')

    def set_on_exit(self, value):
        self._set_value('on_exit', value)

    @not_required_on('mobile')
    def current_window(self):
        self._action('current_window')

    @not_required_on('mobile')
    def enter_full_screen(self, windows):
        self._action('enter_full_screen', windows=windows)

    @not_required_on('mobile')
    def exit_full_screen(self, windows):
        self._action('exit_full_screen', windows=windows)

    @not_required_on('mobile')
    def show_cursor(self):
        self._action('show_cursor')

    @not_required_on('mobile')
    def hide_cursor(self):
        self._action('hide_cursor')

    def add_background_task(self, handler):
        self._action('add_background_task', handler=handler)

    def about_command(self):
        return dummy_command(self, "about")

    def preferences_command(self):
        return dummy_command(self, "preferences")

    def home_page_command(self):
        return dummy_command(self, "homepage")

    def quit_command(self):
        return dummy_command(self, "quit")


@not_required_on('mobile', 'web')
class DocumentApp(App):
    pass
