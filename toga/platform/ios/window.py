from __future__ import print_function, absolute_import, division

from .libs import *


class Window(object):
    def __init__(self, position=(100, 100), size=(640, 480)):
        self._app = None
        self._content = None
        self._impl = None

    def _startup(self):
        print ("startup WINDOW")
        self._impl = UIWindow.alloc().initWithFrame_(UIScreen.mainScreen().bounds())
        self.on_startup()

        if self.content:
            # Assign the widget to the same app as the window.
            # This initiates startup logic.
            self.content.app = self.app

            print("SET ROOT VIEW CONTROLLER")
            self._impl.addSubview_(self.content._impl)
            self._impl.rootViewController = self.content._controller

    @property
    def app(self):
        return self._app

    @app.setter
    def app(self, app):
        if self._app:
            raise Exception("Window is already associated with an App")

        self._app = app
        self._startup()

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget
        self._content.window = self
        if self._impl:
            # Assign the widget to the same app as the window.
            # This initiates startup logic.
            widget.app = self.app

            # We now know the widget impl exists; add it.
            self._impl.addSubview_(widget._impl)

            print("SET ROOT VIEW CONTROLLER")
            self._impl.rootViewController = self._content._controller

    def show(self):
        print("MAKE KEY AND VISIBLE")
        self._impl.makeKeyAndVisible()

        # self._impl.visualizeConstraints_(self._impl.contentView().constraints())

    def on_startup(self):
        pass
