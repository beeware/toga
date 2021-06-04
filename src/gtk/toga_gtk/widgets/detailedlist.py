from ..libs import Gtk, GLib, Gdk, GObject
from .base import Widget
from .internal.rows import TextIconRow
from .internal.buttons import RefreshButton, ScrollButton
from .internal.sourcelistmodel import SourceListModel


class DetailedList(Widget, GObject.GObject):
    """
    Gtk DetailedList implementation.
    Gtk.ListBox inside a Gtk.ScrolledWindow.
    """
    __gsignals__ = {
        # signal for rows to hide their buttons when the user right clicks somewhere else
        'right-clicked': (GObject.SIGNAL_RUN_FIRST, None, tuple()),
        # signal for update the delete method on rows
        'set-on-delete': (GObject.SIGNAL_RUN_LAST, None, (bool,))
    }
    
    def __init__(self, *args, **kwargs):
        GObject.GObject.__init__(self)
        super().__init__(*args, **kwargs)

    def create(self):
        self._on_refresh_handler = None
        self._on_select_handler = None
        self._on_delete_handler = None

        self.list_box = Gtk.ListBox()

        self.list_box.set_selection_mode(Gtk.SelectionMode.NONE)

        self.store = SourceListModel(TextIconRow, self.interface.factory)
        self.store.bind_to_list(self.list_box)
        self.store.set_on_select(self._on_select)

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

        self.right_click_gesture = Gtk.GestureMultiPress.new(self.list_box)
        self.right_click_gesture.set_button(3)
        self.right_click_gesture.set_propagation_phase(Gtk.PropagationPhase.BUBBLE)
        self.right_click_gesture.connect("pressed", self._on_right_click)

        # create row and liststore factories that sets up signals and stuff?

        # move everything in sourcelistmodel back here?

    def change_source(self, source: 'ListSource'):
        self.store.change_source(source)

        # We have to wait until the rows are actually added decide how to position the
        # refresh button
        GLib.idle_add(lambda: not self._changed())

    def insert(self, index: int, item: 'Row'):
        self.store.insert(index, item)
        self.list_box.show_all()
        self._changed()

    def change(self, item: 'Row'):
        self.store.change(item)
        self._changed()
        
    def remove(self, item: 'Row', index: int):
        self._on_delete(item)
        self._changed()
        
    def clear(self):
        self.store.remove_all()
        self._changed()

    def get_selection(self):
        return self.store.get_selection()

    def scroll_to_row(self, row: int):
        self.store.scroll_to_row(row)

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
        if self._on_delete_handler is not None:
            self.store.set_on_delete(self._on_delete)
            self.emit('set-on-delete', True)
        else:
            self.emit('set-on-delete', False)

    def after_on_refresh(self):
        # No special handling required
        pass

    def _on_refresh(self):
        if self._on_refresh_handler is not None:
            self._on_refresh_handler(self.interface)

    def _on_select(self, item: 'Row'):
        if self._on_select_handler is not None:
            self._on_select_handler(self.interface, item)

    def _on_delete(self, item: 'Row', index: int = None):
        if self._on_delete_handler is not None:
            self.store.remove(item, index)
            self._on_delete_handler(self.interface, item)

    def _changed(self):
        self.refresh_button.list_changed()
        self.scroll_button.list_changed()
        return True

    def _on_right_click(self, gesture, n_press, x, y):
        self.emit('right-clicked')
        item = self.list_box.get_row_at_y(y)

        if self._on_select_handler is not None:
            self.list_box.select_row(item)

        if item is not None:
            rect = Gdk.Rectangle()
            rect.x, rect.y = item.translate_coordinates(self.list_box, x, y)
            item.on_right_click(rect)
