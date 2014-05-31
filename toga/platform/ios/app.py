from __future__ import print_function, absolute_import, division

from .libs import *
from .window import Window
from .widgets import *

# The global variable used to store the app instance.
_app = None


class MainWindow(Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        print ("SET BACKGROUND COLOR")

    def on_startup(self):
        self._impl.backgroundColor = UIColor.whiteColor()


class AppDelegate_impl(object):
    AppDelegate = ObjCSubclass('UIResponder', 'AppDelegate')

    @AppDelegate.method('v')
    def applicationDidBecomeActive(self):
        print("BECAME ACTIVE")

    @AppDelegate.method('B@@')
    def application_didFinishLaunchingWithOptions_(self, application, launchOptions):
        print("FINISHED LAUNCHING")
        _app._startup()

        return True

AppDelegate = ObjCClass('AppDelegate')


class App(object):

    def __init__(self, name, app_id):
        global _app
        _app = self

        self.name = name
        self.app_id = app_id

        self.main_window = MainWindow()

    def _startup(self):
        # Assign the window to the app; this initiates startup
        self.main_window.app = self
        self.main_window.show()

    def main_loop(self):
        print ("START MAIN LOOP")
        # Full form: uikit.UIApplicationMain(argc, argv, get_NSString("App"), get_NSString("AppDelegate"))
        uikit.UIApplicationMain(0, None, None, get_NSString("AppDelegate"))
