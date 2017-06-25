# from toga.interface.window import Window as WindowInterface

from .container import Container
from .libs import *
from . import dialogs


class Window():
    _IMPL_CLASS = UIWindow
    _CONTAINER_CLASS = Container
    _DIALOG_MODULE = dialogs

    def __init__(self, interface):
        self._interface = interface
        self._create()

    def _create(self):
        self._screen = UIScreen.mainScreen
        self._impl = self._IMPL_CLASS.alloc().initWithFrame_(self._screen.bounds)
        self._impl._interface = self

    def _set_content(self, widget):
        if getattr(widget, '_controller', None):
            self._controller = widget._controller
        else:
            self._controller = UIViewController.alloc().init()

        self._impl.rootViewController = self._controller
        self._controller.view = self._interface._container._native

    def set_title(self, title):
        pass

    def _set_position(self, position):
        pass

    def _set_size(self, size):
        pass

    def set_app(self, app):
        pass

    def show(self):
        self._impl.makeKeyAndVisible()

        # self._impl.visualizeConstraints_(self._impl.contentView().constraints())
        # Do the first layout render.
        self._interface.content._update_layout(
            width=self._screen.bounds.size.width,
            height=self._screen.bounds.size.height
        )
