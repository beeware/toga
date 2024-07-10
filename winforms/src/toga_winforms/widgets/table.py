from warnings import warn

import System.Windows.Forms as WinForms

import toga

from ..libs.wrapper import WeakrefCallable
from .base import Widget


class Table(Widget):
    _background_supports_alpha = False

    # The following methods are overridden in DetailedList.
    @property
    def _headings(self):
        return self.interface.headings

    @property
    def _accessors(self):
        return self.interface.accessors

    @property
    def _multiple_select(self):
        return self.interface.multiple_select

    @property
    def _data(self):
        return self.interface.data

    def create(self):
        self.native = WinForms.ListView()
        self.native.View = WinForms.View.Details
        self._cache = []
        self._first_item = 0
        self._pending_resize = True

        headings = self._headings
        self.native.HeaderStyle = (
            getattr(WinForms.ColumnHeaderStyle, "None")
            if headings is None
            else WinForms.ColumnHeaderStyle.Nonclickable
        )

        dataColumn = []
        for i, accessor in enumerate(self._accessors):
            heading = None if headings is None else headings[i]
            dataColumn.append(self._create_column(heading, accessor))

        self.native.FullRowSelect = True
        self.native.MultiSelect = self._multiple_select
        self.native.DoubleBuffered = True
        self.native.VirtualMode = True
        self.native.Columns.AddRange(dataColumn)
        self.native.SmallImageList = WinForms.ImageList()

        self.native.ItemSelectionChanged += WeakrefCallable(
            self.winforms_item_selection_changed
        )
        self.native.RetrieveVirtualItem += WeakrefCallable(
            self.winforms_retrieve_virtual_item
        )
        self.native.CacheVirtualItems += WeakrefCallable(
            self.winforms_cache_virtual_items
        )
        self.native.VirtualItemsSelectionRangeChanged += WeakrefCallable(
            self.winforms_item_selection_changed
        )
        self.add_action_events()

    def add_action_events(self):
        self.native.MouseDoubleClick += WeakrefCallable(self.winforms_double_click)

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)
        if self._pending_resize:
            self._pending_resize = False
            self._resize_columns()

    def winforms_retrieve_virtual_item(self, sender, e):
        # Because ListView is in VirtualMode, it's necessary implement
        # VirtualItemsSelectionRangeChanged event to create ListViewItem when it's needed
        if (
            self._cache
            and e.ItemIndex >= self._first_item
            and e.ItemIndex < self._first_item + len(self._cache)
        ):
            e.Item = self._cache[e.ItemIndex - self._first_item]
        else:
            e.Item = self._new_item(e.ItemIndex)

    def winforms_cache_virtual_items(self, sender, e):
        if (
            self._cache
            and e.StartIndex >= self._first_item
            and e.EndIndex < self._first_item + len(self._cache)
        ):
            # If the newly requested cache is a subset of the old cache,
            # no need to rebuild everything, so do nothing
            return

        # Now we need to rebuild the cache.
        self._first_item = e.StartIndex
        new_length = e.EndIndex - e.StartIndex + 1
        self._cache = []

        # Fill the cache with the appropriate ListViewItems.
        for i in range(new_length):
            self._cache.append(self._new_item(i + self._first_item))

    def winforms_item_selection_changed(self, sender, e):
        self.interface.on_select()

    def winforms_double_click(self, sender, e):
        hit_test = self.native.HitTest(e.X, e.Y)
        item = hit_test.Item
        if item is not None:
            self.interface.on_activate(row=self._data[item.Index])
        else:  # pragma: no cover
            # Double clicking outside of an item apparently doesn't raise the event, but
            # that isn't guaranteed by the documentation.
            pass

    def _create_column(self, heading, accessor):
        col = WinForms.ColumnHeader()
        col.Text = heading
        col.Name = accessor
        return col

    def _resize_columns(self):
        num_cols = len(self.native.Columns)
        if num_cols == 0:
            return

        width = int(self.native.ClientSize.Width / num_cols)
        for col in self.native.Columns:
            col.Width = width

    def change_source(self, source):
        self.update_data()

    def _new_item(self, index):
        item = self._data[index]

        def icon(attr):
            val = getattr(item, attr, None)
            icon = None
            if isinstance(val, tuple):
                if val[0] is not None:
                    icon = val[0]
            else:
                try:
                    icon = val.icon
                except AttributeError:
                    pass

            return None if icon is None else icon._impl

        def text(attr):
            val = getattr(item, attr, None)
            if isinstance(val, toga.Widget):
                warn("Winforms does not support the use of widgets in cells")
                val = None
            if isinstance(val, tuple):
                val = val[1]
            if val is None:
                val = self.interface.missing_value
            return str(val)

        lvi = WinForms.ListViewItem(
            [text(attr) for attr in self._accessors],
        )

        # If the table has accessors, populate the icons for the table.
        if self._accessors:
            # TODO: ListView only has built-in support for one icon per row. One possible
            # workaround is in https://stackoverflow.com/a/46128593.
            icon = icon(self._accessors[0])
            if icon is not None:
                lvi.ImageIndex = self._image_index(icon)

        return lvi

    def _image_index(self, icon):
        images = self.native.SmallImageList.Images
        key = str(icon.path)
        index = images.IndexOfKey(key)
        if index == -1:
            index = images.Count
            images.Add(key, icon.bitmap)
        return index

    def update_data(self):
        self.native.VirtualListSize = len(self._data)
        self._cache = []

    def insert(self, index, item):
        self.update_data()

    def change(self, item):
        self.update_data()

    def remove(self, index, item):
        self.update_data()

    def clear(self):
        self.update_data()

    def get_selection(self):
        selected_indices = list(self.native.SelectedIndices)
        if self._multiple_select:
            return selected_indices
        elif len(selected_indices) == 0:
            return None
        else:
            return selected_indices[0]

    def scroll_to_row(self, index):
        self.native.EnsureVisible(index)

    def remove_column(self, index):
        self.native.Columns.RemoveAt(index)
        self.update_data()
        self._resize_columns()

    def insert_column(self, index, heading, accessor):
        self.native.Columns.Insert(index, self._create_column(heading, accessor))
        self.update_data()
        self._resize_columns()
