from .utils import not_required_on
from .window import Window


class MainWindow(Window):
    @not_required_on('iOS', 'gtk')
    def on_close(self):
        pass


class App:
    def __init__(self, interface):
        pass

    def create(self):
        pass

    def open_document(self, fileURL):
        pass

    @not_required_on('mobile')
    def create_menus(self):
        pass

    def main_loop(self):
        pass

    @not_required_on('mobile')
    def exit(self):
        pass
