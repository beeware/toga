from rubicon.objc import objc_method

from .libs import *
from .window import Window


class MainWindow(Window):
    def startup(self):
        super(MainWindow, self).startup()
        self._impl.setBackgroundColor_(UIColor.whiteColor())


class PythonAppDelegate(UIResponder):
    @objc_method
    def applicationDidBecomeActive(self) -> None:
        print("BECAME ACTIVE")

    @objc_method
    def application_didFinishLaunchingWithOptions_(self, application, launchOptions) -> bool:
        print("FINISHED LAUNCHING")
        App._app._startup()

        return True

    # @objc_method
    # def application_didChangeStatusBarOrientation_(self, application, oldStatusBarOrientation: int) -> None:
    #     print("ROTATED", oldStatusBarOrientation)
    #     App._app.main_window.content._update_layout(
    #         width=App._app.main_window.content._impl.frame.size.width,
    #         height=App._app.main_window.content._impl.frame.size.height,
    #     )


class App(object):
    _app = None

    def __init__(self, name, app_id, startup=None):
        App._app = self

        self.name = name
        self.app_id = app_id
        self._startup_method = startup

    def _startup(self):
        self.main_window = MainWindow()
        self.main_window.app = self

        self.startup()

        self.main_window.show()

    def startup(self):
        if self._startup_method:
            self.main_window.content = self._startup_method(self)

    def show_dialog(self, dialog):
        controller = UINavigationController.alloc().initWithRootViewController_(dialog._impl)
        self.main_window.content._impl.presentModalViewController_animated_(controller, True)
