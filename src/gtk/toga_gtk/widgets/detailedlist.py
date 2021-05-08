from ..libs import Gtk, Gio, GLib
from .base import Widget
from .internal.rows import TextIconRow
from .internal.buttons import RefreshButton


class DetailedList(Widget):
    """
    Gtk DetailedList implementation.
    Gtk.ListBox inside a Gtk.ScrolledWindow.
    The rows inherit from .internal.rows.ScrollableRow which inherits from Gtk.ListBoxRow, 
    they are kept inside a Gio.ListStore.
    toga.sources.ListSource is converted to Gtk.ListBoxRow in self.change_source.
    """
    def create(self):
        self._on_refresh_handler = None
        self._on_select_handler = None
        self._on_delete_handler = None

        self.store = None

        self.list_box = Gtk.ListBox()

        self.list_box.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.list_box.connect("row-selected", self._on_row_selected)

        self.scrolled_window = Gtk.ScrolledWindow()

        self.scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scrolled_window.set_min_content_width(self.interface.MIN_WIDTH)
        self.scrolled_window.set_min_content_height(self.interface.MIN_HEIGHT)

        self.scrolled_window.add(self.list_box)

        self.refresh_button = RefreshButton(self._on_refresh,
                                            self.scrolled_window.get_vadjustment())
        
        self.native = Gtk.Overlay()
        self.native.add_overlay(self.scrolled_window)
        self.refresh_button.attach_to(self.native)

        self.native.interface = self.interface
      
    def change_source(self, source: 'ListSource'):
        if self.store is not None:
            self.store.remove_all()
        else:
            self.store = Gio.ListStore()
        for row in source:
            self.store.append(
                TextIconRow(row, self))

        # Gtk.ListBox.bind_model() requires a function to convert the objects in the store
        # to presentation objects.But the objects in the store are already what we want.
        # Thus the identity function.
        # ListStore only accepts GObjects so we can't put toga.sources.Row in it.
        self.list_box.bind_model(self.store, lambda a: a)

        # We have to wait until the rows are actually added decide how to position the
        # refresh button
        GLib.idle_add(lambda: not self.refresh_button.list_changed())

    def insert(self, index: int, item: 'Row'):
        row = TextIconRow(item, self)
        self.store.insert(index, row)
        self.list_box.show_all()
        self.refresh_button.list_changed()

    def change(self, item: 'Row'):
        new_item = TextIconRow(item, self)
        index = self._find(item)
        self.insert(index, new_item)
        
    def remove(self, item: 'Row', index: int):
        self.store.remove(index)
        self._on_delete(item)
        
    def clear(self):
        self.store.remove_all()

    def set_on_refresh(self, handler: callable):
        self._on_refresh_handler = handler

    def after_on_refresh(self):
        # No special handling required
        pass

    def get_selection(self):
        list_box_row = self.list_box.get_selected_row()
        if list_box_row is None:
            return list_box_row
        else:
            return list_box_row.interface

    def set_on_select(self, handler: callable):
        self._on_select_handler = handler

    def set_on_delete(self, handler: callable):
        self._on_delete_handler = handler

    def scroll_to_row(self, row: int):
        list_box_row = self.store[row]
        list_box_row.scroll_to_center()

    def _on_row_selected(self, widget: 'GObject', list_box_row: 'ListBoxRow'):
        if list_box_row is not None:
            self._on_select(list_box_row.interface)

    def _on_refresh(self):
        if self._on_refresh_handler is not None:
            self._on_refresh_handler(self.interface)

    def _on_select(self, row: 'Row'):
        if self._on_select_handler is not None:
            self._on_select_handler(self.interface, row)

    def _on_delete(self, row: 'Row'):
        if self._on_delete_handler is not None:
            self._on_delete_handler(self.interface, row)

    def _find(self, item: 'Row') -> int:
        found, index = self.store.find_with_equal_func(
            item,
            lambda a, b: a == b.interface
        )

        if not found:
            return -1
        else:
            return index
