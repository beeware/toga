from .libs import IPythonApp, MainActivity
from .window import Window


class MainWindow(Window):
    pass


class TogaApp(IPythonApp):
    def __init__(self, app):
        super().__init__()
        self._interface = app
        MainActivity.setPythonApp(self)
        print('Python app launched & stored in Android Activity class')

    def onCreate(self):
        print("Toga app: onCreate")

    def onStart(self):
        print("Toga app: onStart")

    def onResume(self):
        print("Toga app: onResume")

    def onResume(self):
        print("Toga app: onResume")

    def onPause(self):
        print("Toga app: onPause")

    def onStop(self):
        print("Toga app: onStop")

    def onDestroy(self):
        print("Toga app: onDestroy")

    def onRestart(self):
        print("Toga app: onRestart")


class App:
    _MAIN_WINDOW_CLASS = MainWindow

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

    def create(self):
        self._listener = TogaApp(self)

    def open_document(self, fileURL):
        print("Can't open document %s (yet)" % fileURL)

    def main_loop(self):
        # Connect the Python code to the Java Activity.
        self.create()
        # The app loop is integrated with the main Android event loop,
        # so there is no further work to do.

    def set_main_window(self, window):
        pass

    def exit(self):
        pass

    def set_on_exit(self, value):
        pass

    def add_background_task(self, handler):
        self.interface.factory.not_implemented('App.add_background_task()')
