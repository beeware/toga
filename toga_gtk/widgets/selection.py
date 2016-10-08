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
        self._impl.set_entry_text_column(0)
        self._impl._interface = self

    def _remove_all_items(self):
        self._model.clear()

    def _add_item(self, item):
        self._model.append(item)

    def _select_item(self, item):
        self._impl.set_active(self._items.index(item))

    def _get_selected_item(self):
        return self._model[self._impl.get_active]

    def rehint(self):
        # print("REHINT", self, self._impl.get_preferred_width(), self._impl.get_preferred_height(), getattr(self, '_fixed_height', False), getattr(self, '_fixed_width', False))
        hints = {}
        width = self._impl.get_preferred_width()
        minimum_width = width[0]
        natural_width = width[1]

        height = self._impl.get_preferred_height()
        minimum_height = height[0]
        natural_height = height[1]

        if minimum_width > 0:
            hints['min_width'] = minimum_width
        if minimum_height > 0:
            hints['min_height'] = minimum_height
        if natural_height > 0:
            hints['height'] = natural_height

        if hints:
            self.style.hint(**hints)
