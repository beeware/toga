from __future__ import print_function, absolute_import, division

from .libs import *
from .window import Window
from .widgets import *


_apps = {}


class MainWindow(Window):
    def __init__(self):
        super(MainWindow, self).__init__(self)
        print ("SET BACKGROUND COLOR")

    def _startup(self):
        super(MainWindow, self)._startup()
        self._impl.backgroundColor = UIColor.whiteColor()


class AppDelegate_impl(object):
    AppDelegate = ObjCSubclass('UIResponder', 'AppDelegate')

    @AppDelegate.method('v')
    def applicationDidBecomeActive(self):
        print("BECAME ACTIVE")

    @AppDelegate.method('B@@')
    def application_didFinishLaunchingWithOptions_(self, application, launchOptions):
        print("FINISHED LAUNCHING")

        # FIXME - there's got to be a better way to pass the Toga instance
        # into the delegate.
        app = _apps[None]
        app._startup()

        return True

AppDelegate = ObjCClass('AppDelegate')


class App(object):

    def __init__(self, name, app_id):
        self.name = name
        self.app_id = app_id

        _apps[None] = self

        self.main_window = MainWindow()

    def _startup(self):
        self.main_window._startup()
        self.main_window.show()

    def main_loop(self):
        print ("START MAIN LOOP")
        # Full form: uikit.UIApplicationMain(argc, argv, get_NSString("App"), get_NSString("AppDelegate"))
        uikit.UIApplicationMain(0, None, None, get_NSString("AppDelegate"))
