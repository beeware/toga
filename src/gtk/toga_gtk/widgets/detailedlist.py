from ..libs import Gtk, GLib, Gdk, Gio
from .base import Widget
from .internal.rows import TextIconRow
from .internal.buttons import RefreshButton, ScrollButton


# hide the buttons when the user left clicks somewhere else (use _on_select?)

class DetailedList(Widget):
    """
    Gtk DetailedList implementation.
    Gtk.ListBox inside a Gtk.ScrolledWindow.
    """

    def create(self):
        self._on_refresh_handler = None
        self._on_select_handler = None
        self._on_delete_handler = None
        
        # Not the same as selected row. _active_row is the one with its buttons exposed.
        self._active_row = None

        self._on_select_signal_handler = None

        self.list_box = Gtk.ListBox()

        self.list_box.set_selection_mode(Gtk.SelectionMode.NONE)

        self.store = Gio.ListStore()
        self.list_box.bind_model(self.store, lambda a: a)

        self.scrolled_window = Gtk.ScrolledWindow()

        self.scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scrolled_window.set_min_content_width(self.interface.MIN_WIDTH)
        self.scrolled_window.set_min_content_height(self.interface.MIN_HEIGHT)

        self.scrolled_window.add(self.list_box)

        self.refresh_button = RefreshButton(self.scrolled_window.get_vadjustment())

        self.scroll_button = ScrollButton(self.scrolled_window.get_vadjustment())
        self.scroll_button.set_scroll(lambda: self.scroll_to_row(-1))
        
        self.native = Gtk.Overlay()
        self.native.add_overlay(self.scrolled_window)

        self.refresh_button.overlay_over(self.native)
        self.scroll_button.overlay_over(self.native)

        self.native.interface = self.interface

        self._on_select_signal_handler = self.list_box.connect(
            'row-selected', lambda w, item: self._on_select(item))

        self.right_click_gesture = Gtk.GestureMultiPress.new(self.list_box)
        self.right_click_gesture.set_button(3)
        self.right_click_gesture.set_propagation_phase(Gtk.PropagationPhase.BUBBLE)
        self.right_click_gesture.connect("pressed", self._on_right_click)

    @property
    def on_delete(self):
        return self._on_delete

    def row_factory(self, item: 'Row'):
        return TextIconRow(self.interface.factory, self, item)

    def destroy(self):
        self.disconnect(self._on_select_signal_handler)
        super().destroy()

    def change_source(self, source: 'ListSource'):
        self.store.remove_all()
        for item in source:
            self.store.append(
                self.row_factory(item))

        # We have to wait until the rows are actually added decide how to position the
        # refresh button
        GLib.idle_add(lambda: not self._changed())

    def insert(self, index: int, item: 'Row'):
        self.store.insert(index, self.row_factory(item))
        self.list_box.show_all()
        self._changed()

    def change(self, item: 'Row'):
        list_box_row = self.row_factory(item)
        _, index = self._find(item)
        self.store.insert(index, list_box_row)
        
    def remove(self, item: 'Row', index: int):
        if item is not None:
            list_box_row, index = self._find(item)

        if self._active_row == list_box_row:
            self._active_row = None

        self.store.remove(index)
        list_box_row.destroy()
        self._changed()
        
    def clear(self):
        self.store.remove_all()
        self._changed()

    def get_selection(self):
        item = self.list_box.get_selected_row()
        if item is None:
            return item
        else:
            return item.interface

    def scroll_to_row(self, row: int):
        item = self.store[row]
        item.scroll_to_center()

    def set_on_refresh(self, handler: callable):
        if handler is not None:
            self._on_refresh_handler = handler
            self.refresh_button.set_on_refresh(self._on_refresh)

    def set_on_select(self, handler: callable):
        self._on_select_handler = handler
        if handler is not None:
            self.list_box.set_selection_mode(Gtk.SelectionMode.SINGLE)

    def set_on_delete(self, handler: callable):
        self._on_delete_handler = handler

    def after_on_refresh(self):
        # No special handling required
        pass

    def _on_refresh(self):
        if self._on_refresh_handler is not None:
            self._on_refresh_handler(self.interface)

    def _on_select(self, item: Gtk.ListBoxRow):
        if self._on_select_handler is not None and item is not None:
            self._on_select_handler(self.interface, item.interface)

        if self._active_row is not None and self._active_row != item:
            self._active_row.hide_buttons()
            self._active_row = None

    def _on_delete(self, item: Gtk.ListBoxRow):
        if self._on_delete_handler is not None:
            if self._active_row == item:
                self._active_row = None

            self.interface.data.remove(item.interface)
            self._on_delete_handler(self.interface, item.interface)

    def _changed(self):
        self.refresh_button.list_changed()
        self.scroll_button.list_changed()
        return True

    def _on_right_click(self, gesture, n_press, x, y):
        item = self.list_box.get_row_at_y(y)

        rect = Gdk.Rectangle()
        rect.x, rect.y = item.translate_coordinates(self.list_box, x, y)
        
        if self._active_row is not None and self._active_row != item:
            self._active_row.hide_buttons()

        self._active_row = item

        item.toggle_content()
        
        if self._on_select_handler is not None:
            self.list_box.select_row(item)

    def _find(self, item: 'Row'):
        # Maybe this could be replaced by self.interface.data.index(item)
        for index in range(0, len(self.store)):
            if item == self.store[index].interface:
                return self.store[index], index

        return None
