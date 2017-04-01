from toga.interface.window import Window as WindowInterface
from .container import Container
from . import dialogs


class Window(WindowInterface):
    _CONTAINER_CLASS = Container
    _DIALOG_MODULE = dialogs

    def __init__(self, title=None, position=(100, 100), size=(640, 480), toolbar=None, resizeable=True, closeable=True, minimizable=True):
        super().__init__(title=None, position=(100, 100), size=(640, 480), toolbar=None, resizeable=True, closeable=False, minimizable=False)

    def create(self):
        pass

    def _set_app(self, app):
        self._create()

    def _set_content(self, widget):
        self.app._impl.setContentView(self._container._impl)

    def show(self):
        pass

    def _set_title(self, title):
        pass
