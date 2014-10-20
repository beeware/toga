from __future__ import print_function, absolute_import, division, unicode_literals

from rubicon.objc import objc_method

from .libs import *
from .window import Window


class MainWindow(Window):
    def startup(self):
        super(MainWindow, self).startup()
        self._impl.setBackgroundColor_(UIColor.whiteColor())


class PythonAppDelegate(UIResponder):
    @objc_method('v')
    def applicationDidBecomeActive(self):
        print("BECAME ACTIVE")

    @objc_method('B@@')
    def application_didFinishLaunchingWithOptions_(self, application, launchOptions):
        print("FINISHED LAUNCHING")
        MobileApp._app._startup()

        return True


class MobileApp(object):
    _app = None

    def __init__(self, name, app_id, startup=None):
        MobileApp._app = self

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
