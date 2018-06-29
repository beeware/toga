from travertino.size import at_least

from gi.repository import Gtk

from .base import Widget


class Selection(Widget):
    def create(self):
        self.native = Gtk.ComboBoxText.new()
        self.native.interface = self.interface
        self.native.connect("changed", self.gtk_on_select)

        self.rehint()

    def gtk_on_select(self, widget):
        if self.interface.on_select:
            self.interface.on_select(widget)

    def insert(self, index, item):
        # Listener method for ListSource
        self.native.insert_text(index, item.label)

    def remove(self, item):
        # Listener method for ListSource
        self.interface.factory.not_implemented('Selection.remove()')

    def clear(self):
        # Listener method for ListSource
        self.native.remove_all()

    def change_source(self, source):
        self.native.remove_all()
        for row in source:
            self.native.append_text(row.label)
            # Gtk.ComboBox does not select the first item, so it's done here.
            if not self.get_selected_item():
                self.select_item(row)

    def select_item(self, item):
        self.native.set_active(self.interface.items.index(item))

    def get_selected_item(self):
        return self.native.get_active_text()

    def rehint(self):
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()

        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = height[1]

    def set_on_select(self, handler):
        # No special handling required
        pass
