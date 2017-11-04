from .utils import not_required_on, LoggedObject
from .window import Window


class MainWindow(Window):
    @not_required_on('mobile')
    def on_close(self):
        self.action('handle MainWindow on_close')


class App(LoggedObject):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface

    def create(self):
        self._action('create')

    def open_document(self, fileURL):
        self._action('open document', fileURL=fileURL)

    @not_required_on('mobile')
    def create_menus(self):
        self._action('create menus')

    def main_loop(self):
        self._action('main loop')

    @not_required_on('mobile', 'web')
    def exit(self):
        self._action('exit')
