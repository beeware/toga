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
        App._app._startup()
        return True

    @objc_method
    def application_didChangeStatusBarOrientation_(self, application, oldStatusBarOrientation: int) -> None:
        print("ROTATED", oldStatusBarOrientation)
        # The width and height are swapped here, because the window will
        # still be reporting the un-rotated window size.
        App._app.main_window.content._update_layout(
            width=App._app.main_window.content._impl.frame.size.height,
            height=App._app.main_window.content._impl.frame.size.width,
        )


class App(AppInterface):
    _app = None

    def __init__(self, name, app_id, startup=None, document_types=None):
        App._app = self

        self.name = name
        self.app_id = app_id
        self._startup_method = startup

    def _startup(self):
        self.startup()

    def startup(self):
        self.main_window = MainWindow(self.name)
        self.main_window.app = self

        if self._startup_method:
            self.main_window.content = self._startup_method(self)

        self.main_window.show()

    def show_dialog(self, dialog):
        controller = UINavigationController.alloc().initWithRootViewController_(dialog._impl)
        self.main_window.content._impl.presentModalViewController_animated_(controller, True)

    def main_loop(self):
        # Main loop is a no-op on iOS; the app loop is integrated with the
        # main iOS event loop.
        pass
