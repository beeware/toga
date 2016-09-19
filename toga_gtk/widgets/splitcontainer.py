from gi.repository import Gtk

from toga.interface import SplitContainer as SplitContainerInterface

from ..container import Container
from .base import WidgetMixin


class SplitContainer(SplitContainerInterface, WidgetMixin):
    _CONTAINER_CLASS = Container

    def __init__(self, id=None, style=None, direction=SplitContainerInterface.VERTICAL):
        super().__init__(id=None, style=None, direction=direction)
        self._create()

    def create(self):
        if self.direction == self.HORIZONTAL:
            self._impl = Gtk.VPaned()
        else:
            self._impl = Gtk.HPaned()
        self._impl._interface = self

    def _add_content(self, position, container):
        if position >= 2:
            raise ValueError('SplitContainer content must be a 2-tuple')

        if position == 0:
            add = self._impl.add1
        elif position == 1:
            add = self._impl.add2

        add(container._impl)

    def _set_app(self, app):
        if self._content:
            self._content[0].app = self.app
            self._content[1].app = self.app

    def _set_window(self, window):
        if self._content:
            self._content[0].window = self.window
            self._content[1].window = self.window

    def _set_direction(self, value):
        pass
