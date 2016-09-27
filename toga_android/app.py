from android import PythonActivity

from .window import Window


class MainWindow(Window):
    def show(self):
        self.app._impl.setContentView(self.content._impl)


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

    def __init__(self, name, app_id, icon=None, startup=None, document_types=None):
        # Set the icon for the app
        # Icon.app_icon = Icon.load(icon, default=TIBERIUS_ICON)

        super().__init__(
            name=name,
            app_id=app_id,
            icon=Icon.app_icon,
            startup=startup,
            document_types=document_types
        )
        self._startup()

    def _startup(self):
        # Connect this app to the PythonActivity
        self._listener = TogaApp(self)
        self._impl = PythonActivity.setApp(self._listener)
        # Call user code to populate the main window
        self.startup()

    def main_loop(self):
        # Main loop is a no-op on Android; the app loop is integrated with the
        # main Android event loop.
        pass
