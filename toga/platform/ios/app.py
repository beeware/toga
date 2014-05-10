from __future__ import print_function, absolute_import, division

from .libs import *


UIWindow = ObjCClass('UIWindow')
UIColor = ObjCClass('UIColor')
UIScreen = ObjCClass('UIScreen')


class AppDelegate_impl(object):
    AppDelegate = ObjCSubclass('UIResponder', 'AppDelegate')

    @AppDelegate.method('v')
    def applicationDidBecomeActive(self):
        print("BECAME ACTIVE")

    @AppDelegate.method('B@@')
    def application_didFinishLaunchingWithOptions_(self, application, launchOptions):
        print("FINISHED LAUNCHING")
        window = UIWindow.alloc().initWithFrame_(UIScreen.mainScreen().bounds())
        window.backgroundColor = UIColor.whiteColor()
        window.makeKeyAndVisible()
        return True

AppDelegate = ObjCClass('AppDelegate')


class App(object):

    def __init__(self, name, app_id):
        self.name = name
        self.app_id = app_id

    def main_loop(self):
        uikit.UIApplicationMain(0, None, None, get_NSString("AppDelegate"))
