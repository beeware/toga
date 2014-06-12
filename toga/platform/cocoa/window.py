from __future__ import print_function, absolute_import, division

from .libs import *





class WindowDelegate_impl(object):
    WindowDelegate = ObjCSubclass('NSObject', 'WindowDelegate')

    @WindowDelegate.method('v@')
    def windowWillClose_(self, notification):
        self.interface.on_close()

WindowDelegate = ObjCClass('WindowDelegate')


class Window(object):
    def __init__(self, title=None, position=(100, 100), size=(640, 480)):
        self._impl = None
        self._app = None

        self.title = title
        self.position = position
        self.size = size

    def _startup(self):
        # OSX origin is bottom left of screen, and the screen might be
        # offset relative to other screens. Adjust for this.
        screen = NSScreen.mainScreen().visibleFrame()
        position = NSMakeRect(
            screen.origin.x + self.position[0],
            screen.size.height + screen.origin.y - self.position[1] - self.size[1],
            self.size[0],
            self.size[1]
        )
        self._impl = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            position,
            NSTitledWindowMask | NSClosableWindowMask | NSResizableWindowMask | NSMiniaturizableWindowMask,
            NSBackingStoreBuffered,
            False)
        self._set_title()
        self._impl.setFrame_display_animate_(position, True, False)

        self._delegate = WindowDelegate.alloc().init()
        self._delegate.interface = self

        self._impl.setDelegate_(self._delegate)

        self.on_startup()

        if self.content:
            self._set_content()

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
            self._set_content()

    def _set_content(self):
        # Assign the widget to the same app as the window.
        # This initiates startup logic.
        self.content.app = self.app
        self._impl.setContentView_(self._content._impl)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title
        if self._impl:
            self._set_title()

    def _set_title(self):
        if self._title:
            self._impl.setTitle_(get_NSString(self._title))

    def show(self):
        self._impl.makeKeyAndOrderFront_(None)
        # self._impl.visualizeConstraints_(self._impl.contentView.constraints())

    def on_startup(self):
        pass

    def on_close(self):
        pass
