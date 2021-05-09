from ..libs import Gtk, GLib
from .base import Widget
from .internal.rows import TextIconRow
from .internal.buttons import RefreshButton
from .internal.sourcelistmodel import SourceListModel


class DetailedList(Widget):
    """
    Gtk DetailedList implementation.
    Gtk.ListBox inside a Gtk.ScrolledWindow.
    """
    def create(self):
        self._on_refresh_handler = None
        self._on_select_handler = None
        self._on_delete_handler = None

        self.list_box = Gtk.ListBox()

        self.list_box.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.list_box.connect("row-selected", self._on_row_selected)

        self.store = SourceListModel(TextIconRow, self.interface.factory)
        self.store.bind_to_list(self.list_box)

        self.scrolled_window = Gtk.ScrolledWindow()

        self.scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scrolled_window.set_min_content_width(self.interface.MIN_WIDTH)
        self.scrolled_window.set_min_content_height(self.interface.MIN_HEIGHT)

        self.scrolled_window.add(self.list_box)

        self.refresh_button = RefreshButton(self.scrolled_window.get_vadjustment())
        self.refresh_button.set_on_refresh(self._on_refresh)
        
        self.native = Gtk.Overlay()
        self.native.add_overlay(self.scrolled_window)
        self.refresh_button.add_to(self.native)

        self.native.interface = self.interface
      
    def change_source(self, source: 'ListSource'):
        self.store.change_source(source)

        # We have to wait until the rows are actually added decide how to position the
        # refresh button
        GLib.idle_add(lambda: not self.refresh_button.list_changed())

    def insert(self, index: int, item: 'Row'):
        self.store.insert(index, item)
        self.list_box.show_all()
        self.refresh_button.list_changed()

    def change(self, item: 'Row'):
        self.store.change(item)
        self.refresh_button.list_changed()
        
    def remove(self, item: 'Row', index: int):
        self.store.remove(item, index)
        self.refresh_button.list_changed()
        self._on_delete(item)
        
    def clear(self):
        self.store.remove_all()
        self.refresh_button.list_changed()

    def get_selection(self):
        self.store.get_selection()

    def scroll_to_row(self, row: int):
        self.store.scroll_to_row(row)

    def set_on_refresh(self, handler: callable):
        self._on_refresh_handler = handler

    def set_on_select(self, handler: callable):
        self._on_select_handler = handler

    def set_on_delete(self, handler: callable):
        self._on_delete_handler = handler

    def after_on_refresh(self):
        # No special handling required
        pass

    def _on_refresh(self):
        if self._on_refresh_handler is not None:
            self._on_refresh_handler(self.interface)

    def _on_select(self, row: 'Row'):
        if self._on_select_handler is not None:
            self._on_select_handler(self.interface, row)

    def _on_delete(self, row: 'Row'):
        if self._on_delete_handler is not None:
            self._on_delete_handler(self.interface, row)

    def _on_row_selected(self, widget: 'GObject', list_box_row: 'ListBoxRow'):
        if list_box_row is not None:
            self._on_select(list_box_row.interface)

