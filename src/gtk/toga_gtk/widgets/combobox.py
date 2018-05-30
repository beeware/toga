from gi.repository import Gtk
from travertino.size import at_least

from .base import Widget


class ComboBox(Widget):

    def create(self):
        self.native = Gtk.ComboBoxText.new_with_entry()
        self.native.interface = self.interface
        self.native.connect('changed', self._on_select)
        self.native.connect('show', lambda event: self.rehint())


    # v- add to dummy
    def _on_select(self, widget):
        if self.interface.on_select:
            self.interface.on_select(widget)

    def remove_all_items(self):
        self.native.remove_all()

    def add_item(self, item):
        self.native.append_text(item)

        # Gtk.ComboBox does not select the first item, so it's done here.
        if not self.get_selected_item():
            self.select_item(item)

    def select_item(self, item):
        self.native.set_active(self.interface.items.index(item))
    # ^- add to dummy

    def get_value(self):
        pass

    def set_value(self, value):
        pass

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
        # No special handling required
        pass
