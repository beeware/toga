from android import PythonActivity

from toga.interface.app import App as AppInterface

from .window import Window


class MainWindow(Window):
    pass


class TogaApp:
    def __init__(self, app):
        self._interface = app

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


class App(AppInterface):
    _MAIN_WINDOW_CLASS = MainWindow

    def __init__(self, name, app_id, startup=None, document_types=None):
        super().__init__(
            name=name,
            app_id=app_id,
            icon=None,
            startup=startup,
            document_types=document_types
        )
        self._startup()

    def _startup(self):
        # Connect this app to the PythonActivity
        self._listener = TogaApp(self)

        # Set the Python activity listener to be this app.
        self._impl = PythonActivity.setListener(self._listener)

        self.startup()

    def open_document(self, fileURL):
        print("Can't open document %s (yet)" % fileURL)

    def main_loop(self):
        # Main loop is a no-op on Android; the app loop is integrated with the
        # main Android event loop.
        pass
