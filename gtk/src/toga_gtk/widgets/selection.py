from contextlib import contextmanager

from travertino.size import at_least

from ..libs import Gtk
from .base import Widget


class Selection(Widget):
    def create(self):
        self.native = Gtk.ComboBoxText.new()
        self.native.connect("changed", self.gtk_on_changed)
        self._send_notifications = True

    @contextmanager
    def suspend_notifications(self):
        self._send_notifications = False
        yield
        self._send_notifications = True

    def gtk_on_changed(self, widget):
        if self._send_notifications:
            self.interface.on_change()

    # FIXME: 2023-05-31 Everything I can find in documentation, and every test I
    # do with manual stylesheet in the GTK Inspector, says that `.toga button`
    # should target the colors of a GTK ComboBoxText widget. But when applied to
    # the widget, it either doesn't hit, or it's being overridden, and I can't
    # work out why.

    # def set_color(self, color):
    #     self.apply_css(
    #         "color",
    #         get_color_css(color),
    #         selector=".toga, .toga button",
    #     )

    # def set_background_color(self, color):
    #     self.apply_css(
    #         "background_color",
    #         get_background_color_css(color),
    #         selector=".toga, .toga button",
    #     )

    def change(self, item):
        index = self.interface._items.index(item)
        selection = self.native.get_active()
        # Insert a new entry at the same index,
        # then delete the old entry (at the increased index)
        with self.suspend_notifications():
            self.native.insert_text(index, self.interface._title_for_item(item))
            self.native.remove(index + 1)
            if selection == index:
                self.native.set_active(index)

        # Changing the item text can change the layout size
        self.interface.refresh()

    def insert(self, index, item):
        with self.suspend_notifications():
            self.native.insert_text(index, self.interface._title_for_item(item))

        # If you're inserting the first item, make sure it's selected
        if self.native.get_active() == -1:
            self.native.set_active(0)

    def remove(self, index, item):
        selection = self.native.get_active()
        with self.suspend_notifications():
            self.native.remove(index)

        # If we deleted the item that is currently selected, reset the
        # selection to the first item
        if index == selection:
            self.native.set_active(0)

    def clear(self):
        with self.suspend_notifications():
            self.native.remove_all()
        self.interface.on_change()

    def select_item(self, index, item):
        self.native.set_active(index)

    def get_selected_index(self):
        index = self.native.get_active()
        if index == -1:
            return None
        return index

    def rehint(self):
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()

        # FIXME: 2023-05-31 This will always provide a size that is big enough,
        # but sometimes it will be *too* big. For example, if you set the font size
        # large, then reduce it again, the widget *could* reduce in size. However,
        # I can't find any way to prod GTK to perform a resize that will reduce
        # it's minimum size. This is the reason the test probe has a `shrink_on_resize`
        # property; if we can fix this resize issue, `shrink_on_resize` may not
        # be necessary.
        self.interface.intrinsic.width = at_least(
            max(self.interface._MIN_WIDTH, width[1])
        )
        self.interface.intrinsic.height = height[1]
