from .container import Container
from . import dialogs


class Window:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.container = None
        self.create()

    def create(self):
        pass

    def set_app(self, app):
        self._create()

    def set_content(self, widget):
        self.app._impl.setContentView(self._container._impl)

    def show(self):
        pass

    def set_title(self, title):
        pass
