from .libs.activity import IPythonApp, MainActivity
from .window import Window


# `MainWindow` is defined here in `app.py`, not `window.py`, to mollify the test suite.
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

    def onPause(self):
        print("Toga app: onPause")

    def onStop(self):
        print("Toga app: onStop")

    def onDestroy(self):
        print("Toga app: onDestroy")

    def onRestart(self):
        print("Toga app: onRestart")

    @property
    def native(self):
        # We access `MainActivity.singletonThis` freshly each time, rather than
        # storing a reference in `__init__()`, because it's not safe to use the
        # same reference over time because `rubicon-java` creates a JNI local
        # reference.
        return MainActivity.singletonThis


class App:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self._listener = None

    @property
    def native(self):
        return self._listener.native if self._listener else None

    def create(self):
        # The `_listener` listens for activity event callbacks. For simplicity,
        # the app's `.native` is the listener's native Java class.
        self._listener = TogaApp(self)
        # Call user code to populate the main window
        self.interface.startup()

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
