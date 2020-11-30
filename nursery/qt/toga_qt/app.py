import signal
from .libs.QtWidgets import QApplication, QMessageBox
from .window import Window


# TODO: MainWindow
class MainWindow(Window):
    pass


class App:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        self.create()

    def create(self):
        # Stimulate the build of the app
        self.native = QApplication.instance() or QApplication([])

    def create_menus(self):
        self.interface.factory.not_implemented('App.create_menus()')

    def main_loop(self):
        # Modify signal handlers to make sure Ctrl-C is caught and handled.
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        # self.native.exec_() # main loop
        # Qt works without running main loop (tested on PyQt5)
        # TODO: run fake main loop

    def set_main_window(self, window):
        self.native.setActiveWindow(window._impl.native)  # not sure

    def show_about_dialog(self):
        about = QMessageBox()
        # TODO: icon
        msg = ''
        title = ''
        if self.interface.name is not None:
            msg += self.interface.name + " "
            title = self.interface.name

        if self.interface.version is not None:
            msg += 'v' + self.interface.version

        if self.interface.author is not None:
            msg += '\nAuthor: ' + self.interface.author

        if self.interface.description is not None:
            msg += '\n\n' + self.interface.description

        if self.interface.home_page is not None:
            msg += '\nHome Page: ' + self.interface.home_page

        # TODO: set title
        about.setText("About " + title)
        about.setInformativeText(msg)
        about.exec_()

    def exit(self):
        self.native.quit()

    def set_on_exit(self, value):
        pass

    def current_window(self):
        return self.native.activeWindow()._impl

    def enter_full_screen(self, windows):
        for window in windows:
            window._impl.set_full_screen(True)

    def exit_full_screen(self, windows):
        for window in windows:
            window._impl.set_full_screen(False)

    def show_cursor(self):
        self.interface.factory.not_implemented('App.show_cursor()')

    def hide_cursor(self):
        self.interface.factory.not_implemented('App.hide_cursor()')

    def add_background_task(self, handler):
        self.interface.factory.not_implemented('App.add_background_task()')


# TODO: DocumentApp
class DocumentApp(App):
    pass
