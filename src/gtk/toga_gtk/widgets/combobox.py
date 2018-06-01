from gi.repository import Gtk
from travertino.size import at_least

from .base import Widget


class ComboBox(Widget):

    def create(self):
        self.native = Gtk.ComboBoxText.new_with_entry()
        self.native.interface = self.interface
        self.native.connect('changed', self._on_change)
        self.native.connect('show', lambda event: self.rehint())

    def _on_change(self, widget):
        if self.interface.on_change:
            self.interface.on_change(self.interface)

    def remove_all_items(self):
        self.native.remove_all()

    def add_item(self, item):
        self.native.append_text(item)

    def select_item(self, item):
        # here we rely on the fact that the first item is the entry
        self.native.set_active(self.interface.items.index(item) + 1)

    def set_placeholder(self, value):
        self.interface.factory.not_implemented('ComboBox.set_placeholder()')

    def get_value(self):
        # TODO: Confirm this does not leak memory (not sure if the ctypes/cffi
        # wrapper is handling). See:
        # https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/ComboBoxText.html#Gtk.ComboBoxText.get_active_text
        return self.native.get_active_text()

    def set_value(self, value):
        # Set the active item to the entry
        entry_id = self.native.get_entry_text_column()
        self.native.set_active(entry_id)

        # Pull out the ListStore
        model = self.native.get_model()

        # Get the TreeIter object for setting values in a TreeModel
        tree_iter = model.get_iter_first()
        model.set_value(tree_iter, entry_id, value)

    def set_font(self, value):
        self.interface.factory.not_implemented('ComboBox.set_font()')

    def set_alignment(self, value):
        self.interface.factory.not_implemented('ComboBox.set_alignment()')

    def rehint(self):
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()

        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = height[1]

    def set_on_change(self, handler):
        '''No special handling required'''
