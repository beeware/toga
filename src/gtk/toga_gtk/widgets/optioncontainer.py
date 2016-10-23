from gi.repository import Gtk

from toga.interface import OptionContainer as OptionContainerInterface

from ..container import Container
from .base import WidgetMixin


class OptionContainer(OptionContainerInterface, WidgetMixin):
    _CONTAINER_CLASS = Container

    def __init__(self, id=None, style=None, content=None):
        super(OptionContainer, self).__init__(id=id, style=style, content=content)
        self._create()

    def create(self):
        # We want a single unified widget; the vbox is the representation of that widget.
        self._impl = Gtk.Notebook()

    def _add_content(self, label, container, widget):
        self._impl.append_page(container._impl, Gtk.Label(label))
