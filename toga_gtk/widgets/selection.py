from gi.repository import Gtk

from toga.interface import Selection as SelectionInterface

from .base import WidgetMixin

class Selection(SelectionInterface, WidgetMixin):

    def __init__(self, id=None, style=None, items=list()):
        super().__init__(id=id, style=style, items=items)
        self._model = Gtk.ListStore(str)
        self._items = items
        self._text = []
        self._create()

    def create(self):
        self._impl = Gtk.ComboBoxText.new()
        self._impl._interface = self

        for item in self._items:
            self._add_item(item)

        self.rehint()

    def _remove_all_items(self):
        self._text.clear()
        self._impl.remove_all()

    def _add_item(self, item):
        self._text.append(item)
        self._impl.append_text(item)

    def _select_item(self, item):
        self._impl.set_active(self._text.index(item))

    def _get_selected_item(self):
        return self._impl.get_active_text()

    def rehint(self):
        self.style.min_width = 90
        self.style.height = 32
