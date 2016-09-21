from .window import Window


class MainWindow(Window):
    def show(self):
        self.app._impl.setContentView(self.content._impl)


class App(extends=android.app.Activity):
    _app = None
    _impl = None

    def __init__(self, name, app_id, startup=None):
        self.name = name
        self.app_id = app_id
        self._startup_method = startup

    def _startup(self):

        App._app = self
        App._impl = self

        self.main_window = MainWindow()
        self.main_window.app = self

        self.startup()

        self.main_window.show()

    def startup(self):
        if self._startup_method:
            self.main_window.content = self._startup_method(self)

    def onCreate(self, savedInstanceState: android.os.Bundle) -> void:
        super().onCreate(savedInstanceState)

        self._startup()

