from __future__ import print_function, absolute_import, division

from .libs import *




class Window(object):
    def __init__(self, position=(100, 100), size=(640, 480)):
        self._impl = None

    def _startup(self):
        print ("startup WINDOW")
        self._impl = UIWindow.alloc().initWithFrame_(UIScreen.mainScreen().bounds())

        self._content._startup()

        print("SET ROOT VIEW CONTROLLER")
        self._impl.addSubview_(self.content._impl)
        self._impl.rootViewController = self._content._controller

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget
        if self._impl:
            self._impl.addSubview_(widget._impl)

            print("SET ROOT VIEW CONTROLLER")
            self._impl.rootViewController = self._content._controller

    def show(self):
        print("MAKE KEY AND VISIBLE")
        self._impl.makeKeyAndVisible()

        # self._impl.visualizeConstraints_(self._impl.contentView().constraints())
