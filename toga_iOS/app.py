from rubicon.objc import objc_method

from toga.interface.app import App as AppInterface

from .libs import *
from .window import Window


class MainWindow(Window):
    def __init__(self, title=None, position=(100, 100), size=(640, 480)):
        super().__init__(title, position, size)

    def startup(self):
        super(MainWindow, self).startup()
        self._impl.setBackgroundColor_(UIColor.whiteColor())


class PythonAppDelegate(UIResponder):
    @objc_method
    def applicationDidBecomeActive(self) -> None:
        print("App became active.")

    @objc_method
    def application_didFinishLaunchingWithOptions_(self, application, launchOptions) -> bool:
        print("App finished launching.")
        App.app._startup()
        return True

    @objc_method
    def application_didChangeStatusBarOrientation_(self, application, oldStatusBarOrientation: int) -> None:
        print("ROTATED", oldStatusBarOrientation)
        App.app.main_window.content._update_layout(
            width=App.app.main_window._screen.bounds.size.width,
            height=App.app.main_window._screen.bounds.size.height,
        )


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

    def _startup(self):
        self.startup()

    def main_loop(self):
        # Main loop is a no-op on iOS; the app loop is integrated with the
        # main iOS event loop.
        pass
