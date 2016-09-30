from toga.interface.window import Window as WindowInterface

from .container import Container
from .libs import *
from . import dialogs


class Window(WindowInterface):
    _IMPL_CLASS = UIWindow
    _CONTAINER_CLASS = Container
    _DIALOG_MODULE = dialogs

    def __init__(self, title=None, position=(100, 100), size=(640, 480), toolbar=None, resizeable=True, closeable=True, minimizable=True):
        super().__init__(title=None, position=(100, 100), size=(640, 480), toolbar=None, resizeable=True, closeable=False, minimizable=False)
        self._create()

    def create(self):
        self._screen = UIScreen.mainScreen()
        self._impl = self._IMPL_CLASS.alloc().initWithFrame_(self._screen.bounds)
        self._impl._interface = self

        self._controller = UIViewController.alloc().init()
        self._impl.rootViewController = self._controller

    def _set_content(self, widget):
        self._controller.view = self._container._impl

    def _set_title(self, title):
        pass

    def show(self):
        self._impl.makeKeyAndVisible()

        # self._impl.visualizeConstraints_(self._impl.contentView().constraints())
        # Do the first layout render.
        self.content._update_layout(
            width=self._screen.bounds.size.width,
            height=self._screen.bounds.size.height
        )
