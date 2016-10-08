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

        self._impl = Gtk.Box()
        self._impl._interface = self

        self._comboimpl = Gtk.ComboBoxText.new()
        self._comboimpl._interface = self
        self._impl.pack_start(self._comboimpl, False, False, 0)

        for item in self._items:
            self._add_item(item)

        self.rehint()

    def _remove_all_items(self):
        self._text.clear()
        self._comboimpl.remove_all()

    def _add_item(self, item):
        self._text.append(item)
        self._comboimpl.append_text(item)

    def _select_item(self, item):
        self._comboimpl.set_active(self._text.index(item))

    def _get_selected_item(self):
        return self._comboimpl.get_active_text()

    def rehint(self):
        self.style.width = 90
        self.style.height = 32
