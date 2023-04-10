from ..libs import Gdk, Gio, GLib, Gtk
from .base import Widget
from .internal.buttons.refresh import RefreshButton
from .internal.buttons.scroll import ScrollButton
from .internal.rows.texticon import TextIconRow


# TODO: Verify if right clicking a row currently works with touch screens, if not,
# use Gtk.GestureLongPress
class DetailedList(Widget):
    """Gtk DetailedList implementation.

    Gtk.ListBox inside a Gtk.ScrolledWindow.
    """

    def create(self):
        # Not the same as selected row. _active_row is the one with its buttons exposed.
        self._active_row = None

        self.gtk_on_select_signal_handler = None

        self.list_box = Gtk.ListBox()

        self.list_box.set_selection_mode(Gtk.SelectionMode.SINGLE)

        self.store = Gio.ListStore()
        # We need to provide a function that transforms whatever is in the store into
        # a `Gtk.ListBoxRow`, but the items in the store already are `Gtk.ListBoxRow` thus
        # the identity function.
        self.list_box.bind_model(self.store, lambda a: a)

        self.scrolled_window = Gtk.ScrolledWindow()

        self.scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scrolled_window.set_min_content_width(self.interface._MIN_WIDTH)
        self.scrolled_window.set_min_content_height(self.interface._MIN_HEIGHT)

        self.scrolled_window.add(self.list_box)

        self.refresh_button = RefreshButton(self.scrolled_window.get_vadjustment())

        self.scroll_button = ScrollButton(self.scrolled_window.get_vadjustment())
        self.scroll_button.set_scroll(lambda: self.scroll_to_row(-1))

        self.native = Gtk.Overlay()
        self.native.add_overlay(self.scrolled_window)

        self.refresh_button.overlay_over(self.native)
        self.scroll_button.overlay_over(self.native)

        self.gtk_on_select_signal_handler = self.list_box.connect(
            "row-selected", self.gtk_on_row_selected
        )

        self.right_click_gesture = Gtk.GestureMultiPress.new(self.list_box)
        self.right_click_gesture.set_button(3)
        self.right_click_gesture.set_propagation_phase(Gtk.PropagationPhase.BUBBLE)
        self.right_click_gesture.connect("pressed", self.gtk_on_right_click)

    def row_factory(self, item):
        """
        Args:
            item (:obj:`Row`)
        Returns:
            Returns a (:obj:`TextIconRow`)
        """
        return TextIconRow(self.interface.factory, self, item)

    def destroy(self):
        self.disconnect(self.gtk_on_select_signal_handler)
        super().destroy()

    def change_source(self, source):
        """
        Args:
            source (:obj:`ListSource`)
        """
        self.store.remove_all()
        for item in source:
            self.store.append(self.row_factory(item))

        # We can't know the dimensions of each row (and thus of the list) until gtk allocates
        # space for it. Gtk does emit `size-allocate` after allocation, but I couldn't find any
        # guarantees that the rows have their sizes allocated in the order they are inserted
        # in the `ListStore` and in my opinion that's unlikely to be the case.

        # Therefore we would need to wait for `size-allocate` on all rows and either update
        # the visibility of the buttons on all `size-allocates` or have a counter and only do
        # it on the last `size-allocate`. Obviously none of those options are desirable.

        # Fortunately functions added with `idle_add` are run when gtk is idle and thus after
        # any size allocation. This solves our problem and from the perspective of the user
        # happens immediately.

        # Even though we are adding the callback to the global loop, it only runs once.
        # This is what the lambda is for. If a callback returns `False` then it's not ran again.
        # I used a lambda because returning `False` from `self._list_items_changed()` would mean
        # returning `False` on success.
        GLib.idle_add(lambda: not self._list_items_changed())

    def insert(self, index, item):
        """
        Args:
            index (int)
            item (:obj:`Row`)
        """
        item_impl = self.row_factory(item)
        self.store.insert(index, item_impl)
        self.list_box.show_all()
        self._list_items_changed()

    def change(self, item):
        """
        Args:
            item (:obj:`Row`)
        """
        index = item._impl.get_index()
        self.remove(item, index)
        item_impl = self.row_factory(item)
        self.store.insert(index, item_impl)

    def remove(self, item, index):
        """Removes a row from the store. Doesn't remove the row from the
        interface.

        Args:
            item (:obj:`Row`)
            index (int)
        """
        if index is None:
            index = item._impl.get_index()

        if self._active_row == item._impl:
            self._active_row = None

        self.store.remove(index)

        if self.interface.on_delete is not None:
            self.interface.on_delete(self.interface, item._impl.interface)

        item._impl.destroy()
        self._list_items_changed()

    def clear(self):
        self.store.remove_all()
        self._list_items_changed()

    def get_selection(self):
        item_impl = self.list_box.get_selected_row()
        if item_impl is None:
            return None
        else:
            return item_impl.interface

    def scroll_to_row(self, row: int):
        item = self.store[row]
        item.scroll_to_center()

    def set_on_refresh(self, handler: callable):
        if handler is not None:
            self.refresh_button.set_on_refresh(self.gtk_on_refresh_clicked)

    def set_on_select(self, handler: callable):
        pass

    def set_on_delete(self, handler: callable):
        pass

    def after_on_refresh(self, widget, result):
        # No special handling required
        pass

    def gtk_on_refresh_clicked(self):
        if self.interface.on_refresh is not None:
            self.interface.on_refresh(self.interface)

    def gtk_on_row_selected(self, w: Gtk.ListBox, item_impl: Gtk.ListBoxRow):
        if self.interface.on_select is not None:
            if item_impl is not None:
                self.interface.on_select(self.interface, item_impl.interface)
            else:
                self.interface.on_select(self.interface, None)

        if self._active_row is not None and self._active_row != item_impl:
            self._active_row.hide_buttons()
            self._active_row = None

    def gtk_on_right_click(self, gesture, n_press, x, y):
        item_impl = self.list_box.get_row_at_y(y)

        if item_impl is None:
            return

        rect = Gdk.Rectangle()
        rect.x, rect.y = item_impl.translate_coordinates(self.list_box, x, y)

        if self._active_row is not None and self._active_row != item_impl:
            self._active_row.hide_buttons()

        self._active_row = item_impl
        item_impl.on_right_click(rect)

        if self.interface.on_select is not None:
            self.list_box.select_row(item_impl)

    def _list_items_changed(self):
        """Some components such as the refresh button and scroll button change
        their appearance based on how many items there are on the list or the
        size of the items.

        If either of those things changes the buttons need to be
        notified to recalculate their positions.
        """
        self.refresh_button.list_changed()
        self.scroll_button.list_changed()
        return True
