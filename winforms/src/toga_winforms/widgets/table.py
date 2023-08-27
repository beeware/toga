import System.Windows.Forms as WinForms
from travertino.size import at_least

from .base import Widget


class Table(Widget):
    _background_supports_alpha = False

    def create(self):
        self.native = WinForms.ListView()
        self.native.View = WinForms.View.Details
        self._cache = []
        self._first_item = 0
        self._pending_resize = True

        headings = self.interface.headings
        self.native.HeaderStyle = (
            getattr(WinForms.ColumnHeaderStyle, "None")
            if headings is None
            else WinForms.ColumnHeaderStyle.Nonclickable
        )

        dataColumn = []
        for i, accessor in enumerate(self.interface.accessors):
            heading = None if headings is None else headings[i]
            dataColumn.append(self._create_column(heading, accessor))

        self.native.FullRowSelect = True
        self.native.MultiSelect = self.interface.multiple_select
        self.native.DoubleBuffered = True
        self.native.VirtualMode = True
        self.native.Columns.AddRange(dataColumn)

        self.native.ItemSelectionChanged += self.winforms_item_selection_changed
        self.native.RetrieveVirtualItem += self.winforms_retrieve_virtual_item
        self.native.CacheVirtualItems += self.winforms_cache_virtual_items
        self.native.MouseDoubleClick += self.winforms_double_click
        self.native.VirtualItemsSelectionRangeChanged += (
            self.winforms_item_selection_changed
        )

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
            e.Item = WinForms.ListViewItem(
                self.row_data(self.interface.data[e.ItemIndex])
            )

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
            self._cache.append(
                WinForms.ListViewItem(
                    self.row_data(self.interface.data[i + self._first_item])
                )
            )

    def winforms_item_selection_changed(self, sender, e):
        self.interface.on_select(None)

    def winforms_double_click(self, sender, e):
        hit_test = self.native.HitTest(e.X, e.Y)
        item = hit_test.Item
        self.interface.on_activate(None, row=self.interface.data[item.Index])

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

    def row_data(self, item):
        # TODO: ListView only has built-in support for one icon per row. One possible
        # workaround is in https://stackoverflow.com/a/46128593.
        def strip_icon(item, attr):
            val = getattr(item, attr, self.interface.missing_value)

            if isinstance(val, tuple):
                return str(val[1])
            return str(val)

        return [strip_icon(item, attr) for attr in self.interface._accessors]

    def update_data(self):
        self.native.VirtualListSize = len(self.interface.data)
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
        if self.interface.multiple_select:
            return selected_indices
        elif len(selected_indices) == 0:
            return None
        else:
            return selected_indices[0]

    def scroll_to_row(self, index):
        self.native.EnsureVisible(index)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)

    def remove_column(self, index):
        self.native.Columns.RemoveAt(index)
        self.update_data()
        self._resize_columns()

    def insert_column(self, index, heading, accessor):
        self.native.Columns.Insert(index, self._create_column(heading, accessor))
        self.update_data()
        self._resize_columns()
