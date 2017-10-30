from gi.repository import Gtk
from .base import Widget


class Selection(Widget):
    def create(self):
        self.native = Gtk.ComboBoxText.new()
        self.native.interface = self.interface

        self.rehint()

    def remove_all_items(self):
        # self._text.clear()
        self.native.remove_all()

    def add_item(self, item):
        # self._text.append(item)
        self.native.append_text(item)

    def select_item(self, item):
        self.native.set_active(self.interface.items.index(item))

    def get_selected_item(self):
        return self.native.get_active_text()

    def rehint(self):
        self.interface.style.min_width = 90
        self.interface.style.height = 32

    def set_on_select(self):
        pass
