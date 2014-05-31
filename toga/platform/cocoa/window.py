from __future__ import print_function, absolute_import, division

from .libs import *


NSWindow = ObjCClass('NSWindow')


class WindowDelegate_impl(object):
    WindowDelegate = ObjCSubclass('NSObject', 'WindowDelegate')

    @WindowDelegate.method('v@')
    def windowWillClose_(self, notification):
        self.interface.on_close()

WindowDelegate = ObjCClass('WindowDelegate')


class Window(object):
    def __init__(self, position=(100, 100), size=(640, 480)):
        self.position = position
        self.size = size
        self._impl = None
        self._app = None

    def _startup(self):
        self._impl = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(self.position[0], self.position[1], self.size[0], self.size[1]),
            NSTitledWindowMask | NSClosableWindowMask | NSResizableWindowMask | NSMiniaturizableWindowMask,
            NSBackingStoreBuffered,
            False)

        self._delegate = WindowDelegate.alloc().init()
        self._delegate.interface = self

        self._impl.setDelegate_(self._delegate)

        self.on_startup()

        if self.content:
            # Assign the widget to the same app as the window.
            # This initiates startup logic.
            self.content.app = self.app

            self._impl.setContentView_(self._content._impl)

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

            self._impl.setContentView_(self._content._impl)

    def show(self):
        self._impl.makeKeyAndOrderFront_(None)
        # self._impl.visualizeConstraints_(self._impl.contentView().constraints())

    def on_startup(self):
        pass

    def on_close(self):
        pass
