from contextlib import contextmanager

from travertino.size import at_least

from toga.handlers import WeakrefCallable

from ..libs import GTK_VERSION, Gtk
from .base import Widget


class Selection(Widget):
    def create(self):
        self._send_notifications = True
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.native = Gtk.ComboBoxText.new()
            self.native.connect("changed", self.gtk_on_changed)
        else:  # pragma: no-cover-if-gtk3
            self.model = Gtk.StringList.new([])
            self.native = Gtk.DropDown(model=self.model)
            self.native.connect(
                "notify::selected", WeakrefCallable(self.gtk_on_changed)
            )

    @contextmanager
    def suspend_notifications(self):
        previous = self._send_notifications
        self._send_notifications = False
        try:
            yield
        finally:
            self._send_notifications = previous

    def gtk_on_changed(self, *_args):
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

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def change(self, item):
        import warnings

        warnings.warn(
            "The change() method is deprecated. Use source_change() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_change(item=item)

    def source_change(self, *, item):
        index = self.interface._items.index(item)
        selection = self.get_selected_index()
        with self.suspend_notifications():
            if GTK_VERSION < (4, 0, 0):
                # Insert a new entry at the same index, then delete the old entry.
                self.native.insert_text(index, self.interface._title_for_item(item))
                self.native.remove(index + 1)
                if selection == index:
                    self.native.set_active(index)
            else:
                self.model.splice(index, 1, [self.interface._title_for_item(item)])
                if selection == index:
                    self.native.set_selected(index)

        # Changing the item text can change the layout size
        self.interface.refresh()

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def insert(self, index, item):
        import warnings

        warnings.warn(
            "The insert() method is deprecated. Use source_insert() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_insert(index=index, item=item)

    def source_insert(self, *, index, item):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            with self.suspend_notifications():
                self.native.insert_text(index, self.interface._title_for_item(item))

            # If you're inserting the first item, make sure it's selected
            if self.native.get_active() == -1:
                self.native.set_active(0)
        else:  # pragma: no-cover-if-gtk3
            selection = self.get_selected_index()
            with self.suspend_notifications():
                self.model.splice(index, 0, [self.interface._title_for_item(item)])
                if selection is None:
                    self.native.set_selected(0)
                else:
                    self.native.set_selected(selection + (index <= selection))

            if selection is None:
                self.interface.on_change()
            self.interface.refresh()

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def remove(self, index, item):
        import warnings

        warnings.warn(
            "The remove() method is deprecated. Use source_remove() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_remove(index=index, item=item)

    def source_remove(self, *, index, item):
        selection = self.get_selected_index()
        with self.suspend_notifications():
            if GTK_VERSION < (4, 0, 0):
                self.native.remove(index)
            else:
                self.model.remove(index)
                if selection == index:
                    self.native.set_selected(
                        0 if self.model.get_n_items() else Gtk.INVALID_LIST_POSITION
                    )

        # If we deleted the item that is currently selected, reset the
        # selection to the first item
        if index == selection:
            if GTK_VERSION < (4, 0, 0):
                self.native.set_active(0)
            else:
                self.interface.on_change()

        self.interface.refresh()

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def clear(self):
        import warnings

        warnings.warn(
            "The clear() method is deprecated. Use source_clear() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_clear()

    def source_clear(self):
        with self.suspend_notifications():
            if GTK_VERSION < (4, 0, 0):
                self.native.remove_all()
            else:
                self.model.splice(0, self.model.get_n_items(), [])
        self.interface.on_change()

    def select_item(self, index, item):
        if GTK_VERSION < (4, 0, 0):
            self.native.set_active(index)
        else:
            self.native.set_selected(index)

    def get_selected_index(self):
        if GTK_VERSION < (4, 0, 0):
            index = self.native.get_active()
            return None if index == -1 else index
        else:
            index = self.native.get_selected()
            return None if index == Gtk.INVALID_LIST_POSITION else index

    def rehint(self):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            width = self.native.get_preferred_width()
            height = self.native.get_preferred_height()

            # FIXME: 2023-05-31 This will always provide a size that is big enough,
            # but sometimes it will be *too* big. For example, if you set the font size
            # large, then reduce it again, the widget *could* reduce in size. However,
            # I can't find any way to prod GTK to perform a resize that will reduce
            # it's minimum size. This is the reason the test probe has a
            # `shrink_on_resize` property; if we can fix this resize issue,
            # `shrink_on_resize` may not be necessary.
            self.interface.intrinsic.width = at_least(
                max(self.interface._MIN_WIDTH, width[1])
            )
            self.interface.intrinsic.height = height[1]
        else:  # pragma: no-cover-if-gtk3
            _, size = self.native.get_preferred_size()
            # DropDown measures only its selected item. Reserve enough room for
            # every option, while retaining the native arrow and theme padding.
            layout = self.native.create_pango_layout("")
            widths = []
            for index in range(self.model.get_n_items()):
                layout.set_text(self.model.get_string(index), -1)
                widths.append(layout.get_pixel_size()[0])
            selection = self.get_selected_index()
            selected_width = widths[selection] if selection is not None else 0
            width = size.width + max(widths, default=0) - selected_width
            self.interface.intrinsic.width = at_least(
                max(self.interface._MIN_WIDTH, width)
            )
            self.interface.intrinsic.height = size.height
