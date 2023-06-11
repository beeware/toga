from travertino.size import at_least

from ..libs import Gtk
from .base import Widget


class Selection(Widget):
    def create(self):
        self.string_list = Gtk.StringList()

        self.native = Gtk.DropDown.new(model=self.string_list)
        self.native.set_show_arrow(True)
        self.native.connect("notify::selected-item", self.gtk_on_select)

    def gtk_on_select(self, widget, data):
        if self.interface.on_select:
            self.interface.on_select(widget)

    def remove_all_items(self):
        items_num = self.string_list.get_n_items()
        self.string_list.splice(0, items_num, None)

    def add_item(self, item):
        self.string_list.take(item)

        # Gtk.ComboBox does not select the first item, so it's done here.
        if not self.get_selected_item():
            self.select_item(item)

    def select_item(self, item):
        self.native.set_selected(self.interface.items.index(item))

    def get_selected_item(self):
        item = self.native.get_selected_item()
        if item:
            return item.get_string()
        return None

    def rehint(self):
        # print(
        #     "REHINT",
        #     self,
        #     self.native.get_preferred_size()[0].width,
        #     self.native.get_preferred_size()[0].height,
        # )
        min_size, size = self.native.get_preferred_size()

        if min_size.width > self.interface._MIN_WIDTH:
            self.interface._MIN_WIDTH = min_size.width

        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = size.height

    def set_on_select(self, handler):
        # No special handling required
        pass
