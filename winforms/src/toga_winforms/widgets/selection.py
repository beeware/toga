from contextlib import contextmanager
from decimal import ROUND_UP

import System.Windows.Forms as WinForms

from ..libs.wrapper import WeakrefCallable
from .base import Widget


class TogaComboBox(WinForms.ComboBox):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl
        self.DropDownStyle = WinForms.ComboBoxStyle.DropDownList
        self.SelectedIndexChanged += WeakrefCallable(
            self.winforms_selected_index_changed
        )

    def winforms_selected_index_changed(self, sender, event):
        self.impl.on_change()


class Selection(Widget):
    _background_supports_alpha = False

    def create(self):
        self.native = TogaComboBox(self)
        self._send_notifications = True

    @contextmanager
    def suspend_notifications(self):
        self._send_notifications = False
        yield
        self._send_notifications = True

    def on_change(self):
        if self._send_notifications:
            self.interface.on_change()

    def clear(self):
        self.native.Items.Clear()
        self.on_change()

    def insert(self, index, item):
        self.native.Items.Insert(index, self.interface._title_for_item(item))

        # WinfForm.ComboBox does not select the first item, so it's done here.
        if self.native.SelectedIndex == -1:
            self.native.SelectedIndex = 0

    def change(self, item):
        index = self.interface._items.index(item)
        with self.suspend_notifications():
            self.insert(index, item)
            self.remove(index + 1, item)

        # Changing the item text can change the layout size.
        self.interface.refresh()

    def remove(self, index, item):
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
