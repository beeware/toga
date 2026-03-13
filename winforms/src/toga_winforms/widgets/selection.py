from contextlib import contextmanager
from decimal import ROUND_UP

import System.Windows.Forms as WinForms

from toga.handlers import WeakrefCallable

from .base import Widget


class Selection(Widget):
    def create(self):
        self.native = WinForms.ComboBox()
        self.native.DropDownStyle = WinForms.ComboBoxStyle.DropDownList
        self.native.SelectedIndexChanged += WeakrefCallable(
            self.winforms_selected_index_changed
        )
        self._send_notifications = True

    def winforms_selected_index_changed(self, sender, event):
        self.on_change()

    @contextmanager
    def suspend_notifications(self):
        self._send_notifications = False
        yield
        self._send_notifications = True

    def on_change(self):
        if self._send_notifications:
            self.interface.on_change()

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
        self.native.Items.Clear()
        self.on_change()

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
        self.native.Items.Insert(index, self.interface._title_for_item(item))

        # WinfForm.ComboBox does not select the first item, so it's done here.
        if self.native.SelectedIndex == -1:
            self.native.SelectedIndex = 0

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
        with self.suspend_notifications():
            self.insert(index, item)
            self.remove(index + 1, item)

        # Changing the item text can change the layout size.
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
        selection_change = self.get_selected_index() == index
        self.native.Items.RemoveAt(index)

        # Removing the selected item will initially cause *nothing* to be selected.
        # Select an adjacent item if there is one.
        if selection_change:
            if self.native.Items.Count == 0:
                self.on_change()
            else:
                self.native.SelectedIndex = max(0, index - 1)

    def select_item(self, index, item):
        self.native.SelectedIndex = index

    def get_selected_index(self):
        index = self.native.SelectedIndex
        return None if index == -1 else index

    def rehint(self):
        self.interface.intrinsic.height = self.scale_out(
            self.native.PreferredSize.Height, ROUND_UP
        )
