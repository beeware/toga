from warnings import warn

import System.Windows.Forms as WinForms

import toga

from ..libs.wrapper import WeakrefCallable
from .base import Widget


class Table(Widget):
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
        self.native.HideSelection = False

        self.native.ItemSelectionChanged += WeakrefCallable(
            self.winforms_item_selection_changed
        )
        self.native.RetrieveVirtualItem += WeakrefCallable(
            self.winforms_retrieve_virtual_item
        )
        self.native.CacheVirtualItems += WeakrefCallable(
            self.winforms_cache_virtual_items
        )
        self.native.SearchForVirtualItem += WeakrefCallable(
            self.winforms_search_for_virtual_item
        )
        self.native.VirtualItemsSelectionRangeChanged += WeakrefCallable(
            self.winforms_virtual_items_selection_range_changed
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
        # VirtualItemsSelectionRangeChanged event to create ListViewItem
        # when it's needed
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

    def winforms_search_for_virtual_item(self, sender, e):
        if (
            not e.IsTextSearch or not self._accessors or not self._data
        ):  # pragma: no cover
            # If this list is empty, or has no columns, or it's an unsupported search
            # type, there's no search to be done. These situation are difficult to
            # trigger in CI; they're here as a safety catch.
            return
        find_previous = e.Direction in [
            WinForms.SearchDirectionHint.Up,
            WinForms.SearchDirectionHint.Left,
        ]
        i = e.StartIndex
        found_item = False
        while True:
            # It is possible for e.StartIndex to be received out-of-range if the user
            # performs keyboard navigation at its edge, so check before accessing data
            if i < 0:  # pragma: no cover
                # This could happen if this event is fired searching backwards,
                # however this should not happen in Toga's use of it.
                # i = len(self._data) - 1
                raise NotImplementedError("backwards search unsupported")
            elif i >= len(self._data):
                i = 0
            if (
                self._item_text(self._data[i], self._accessors[0])[
                    : len(e.Text)
                ].lower()
                == e.Text.lower()
            ):
                found_item = True
                break
            if find_previous:  # pragma: no cover
                # Toga does not currently need backwards searching functionality.
                # i -= 1
                raise NotImplementedError("backwards search unsupported")
            else:
                i += 1
            if i == e.StartIndex:
                break
        if found_item:
            e.Index = i

    def winforms_item_selection_changed(self, sender, e):
        self.interface.on_select()

    def winforms_virtual_items_selection_range_changed(self, sender, e):
        # Event handler for the ListView.VirtualItemsSelectionRangeChanged
        # with condition that only multiple items (>1) are selected.
        # A ListView.VirtualItemsSelectionRangeChanged event will also be raised
        # alongside a ListView.ItemSelectionChanged event when selecting a new
        # item to replace an already selected item. This is due to the new selection
        # action causing multiple items' selection state being changed.
        # The number of selected items is checked before the on_select() is called.
        # This is a workaround to avoid calling the on_select() method twice
        # when selecting a new item to replace an already selected item.
        if len(list(self.native.SelectedIndices)) > 1:
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

        lvi = WinForms.ListViewItem(
            [self._item_text(item, attr) for attr in self._accessors],
        )

        # If the table has accessors, populate the icons for the table.
        if self._accessors:
            # TODO: ListView only has built-in support for one icon per row. One
            # possible workaround is in https://stackoverflow.com/a/46128593.
            icon = icon(self._accessors[0])
            if icon is not None:
                lvi.ImageIndex = self._image_index(icon)

        return lvi

    def _item_text(self, item, attr):
        val = getattr(item, attr, None)
        if isinstance(val, toga.Widget):
            warn(
                "Winforms does not support the use of widgets in cells",
                stacklevel=2,
            )
            val = None
        if isinstance(val, tuple):
            val = val[1]
        if val is None:
            val = self.interface.missing_value
        return str(val)

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
