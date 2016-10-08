from gi.repository import Gtk

from toga.interface import Selection as SelectionInterface

from .base import WidgetMixin

class Selection(WidgetMixin, SelectionInterface):

    def __init__(self, id=None, style=None, items=list()):
        super().__init__(id=id, style=style, items=items)
        self._model = Gtk.ListStore(str)
        self._items = items
        self._create()

    def create(self):

        for item in self._items:
            self._model.append([item])

        self._impl = Gtk.ComboBox.new_with_model_and_entry(self._model)

        self.add_constraints()

    def _remove_all_items(self):
        self._model.clear()

    def _add_item(self, item):
        self._model.append(item)

    def _select_item(self, item):
        self._impl.set_active(self._model.index(item))

    def _get_selected_item(self):
        return self._model[self._impl.get_active]
