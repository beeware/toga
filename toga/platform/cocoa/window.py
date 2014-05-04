from __future__ import print_function, unicode_literals, absolute_import, division

from toga.platform.cocoa.libs import *


NSWindow = ObjCClass('NSWindow')


class WindowDelegate_impl(object):
    WindowDelegate = ObjCSubclass('NSObject', 'WindowDelegate')

    @WindowDelegate.method('v@')
    def windowWillClose_(self, notification):
        self.interface.on_close()

WindowDelegate = ObjCClass('WindowDelegate')


class Window(object):
    def __init__(self, position=(100, 100), size=(640, 480)):
        self._impl = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(position[0], position[1], size[0], size[1]),
            NSTitledWindowMask | NSClosableWindowMask | NSResizableWindowMask | NSMiniaturizableWindowMask,
            NSBackingStoreBuffered,
            False)

        self._delegate = WindowDelegate.alloc().init()
        self._delegate.interface = self

        self._impl.setDelegate_(self._delegate)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget
        self._impl.setContentView_(self._content._impl)

    def show(self):
        self._impl.makeKeyAndOrderFront_(None)
        # self._impl.visualizeConstraints_(self._impl.contentView().constraints())

    def on_close(self):
        pass
