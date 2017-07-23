from .libs import *
from toga.window import Window
from rubicon.objc import objc_method


class MainWindow(Window):
    def __init__(self, title=None, position=(100, 100), size=(640, 480)):
        super().__init__(title, position, size)

    def startup(self):
        super(MainWindow, self).startup()
        self.native.setBackgroundColor_(UIColor.whiteColor())


class PythonAppDelegate(UIResponder):
    @objc_method
    def applicationDidBecomeActive(self) -> None:
        print("App became active.")

    @objc_method
    def application_didFinishLaunchingWithOptions_(self, application, launchOptions) -> bool:
        print("App finished launching.")
        App.app.create()
        return True

    @objc_method
    def application_didChangeStatusBarOrientation_(self, application, oldStatusBarOrientation: int) -> None:
        """ This callback is invoked when rotating the device from landscape to portrait and vice versa. """
        print("ROTATED", oldStatusBarOrientation)
        App.app.interface.main_window.content._update_layout(
            width=App.app.interface.main_window._impl.screen.bounds.size.width,
            height=App.app.interface.main_window._impl.screen.bounds.size.height,
        )


class App:
    _MAIN_WINDOW_CLASS = MainWindow

    def __init__(self, interface):
        self.interface = interface
        App.app = self  # Add a reference for the PythonAppDelegate class to use.

    def create(self):
        """ Calls the startup method on the interface """
        self.interface.startup()

    def open_document(self, fileURL):
        """ Add a new document to this app."""
        pass

    def main_loop(self):
        # Main loop is a no-op on iOS; the app loop is integrated with the
        # main iOS event loop.
        pass
