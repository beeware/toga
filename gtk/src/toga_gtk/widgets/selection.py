from contextlib import contextmanager

from travertino.size import at_least

from ..libs import Gtk, get_background_color_css, get_color_css
from .base import Widget


class Selection(Widget):
    def create(self):
        self._send_notifications = True
        self.string_list = Gtk.StringList()

        self.native = Gtk.DropDown.new(model=self.string_list)
        self.native.set_show_arrow(True)
        self.native.connect("notify::selected-item", self.gtk_on_select)

    @contextmanager
    def suspend_notifications(self):
        self._send_notifications = False
        yield
        self._send_notifications = True

    def gtk_on_select(self, widget, data):
        if self.interface.on_select and self._send_notifications:
            self.interface.on_select(widget)

    def set_color(self, color):
        self.apply_css(
            "color",
            get_color_css(color),
            selector=".toga *",
        )

    def set_background_color(self, color):
        self.apply_css(
            "background_color",
            get_background_color_css(color),
            selector=".toga *",
        )

    def change(self, item):
        index = self.interface._items.index(item)
        selection_index = self.native.get_selected()
        # Insert a new entry at the same index,
        # then delete the old entry (at the increased index)
        with self.suspend_notifications():
            self.string_list.splice(index, 1, [self.interface._title_for_item(item)])
            if selection_index == index:
                self.native.set_selected(index)

        # Changing the item text can change the layout size
        self.interface.refresh()

    def insert(self, index, item):
        with self.suspend_notifications():
            item_at_index = self.string_list.get_string(index)
            if item_at_index is None:
                self.string_list.splice(
                    index, 0, [self.interface._title_for_item(item)]
                )
            else:
                self.string_list.splice(
                    index, 1, [self.interface._title_for_item(item), item_at_index]
                )

        # If you're inserting the first item, make sure it's selected
        if self.native.get_selected() == Gtk.INVALID_LIST_POSITION:
            self.native.set_selected(0)

    def remove(self, index, item):
        selection_index = self.native.get_selected()
        with self.suspend_notifications():
            self.string_list.splice(index, 1, None)

        # If we deleted the item that is currently selected, reset the
        # selection to the first item
        if selection_index == index:
            self.native.set_selected(0)

    def clear(self):
        with self.suspend_notifications():
            items_num = self.string_list.get_n_items()
            self.string_list.splice(0, items_num, None)
        self.interface.on_change()

    def select_item(self, index, item):
        self.native.set_selected(self.interface._items.index(item))

    def get_selected_index(self):
        index = self.native.get_selected()
        if index == Gtk.INVALID_LIST_POSITION:
            return None
        return index

    def rehint(self):
        # print(
        #     "REHINT",
        #     self,
        #     self.native.get_preferred_size()[0].width,
        #     self.native.get_preferred_size()[0].height,
        # )
        min_size, size = self.native.get_preferred_size()

        self.interface.intrinsic.width = at_least(
            max(min_size.width, self.interface._MIN_WIDTH)
        )
        self.interface.intrinsic.height = size.height
