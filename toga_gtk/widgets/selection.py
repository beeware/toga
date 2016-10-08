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

        if hints:
            self.style.hint(**hints)
