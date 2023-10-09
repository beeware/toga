import System.Windows.Forms as WinForms

from toga.sources import Row

from ..internal.wrappers import WeakrefCallable
from .table import Table


# Wrap a DetailedList source to make it compatible with a Table.
class TableSource:
    def __init__(self, interface):
        self.interface = interface

    def __len__(self):
        return len(self.interface.data)

    def __getitem__(self, index):
        row = self.interface.data[index]
        title, subtitle, icon = (
            getattr(row, attr, None) for attr in self.interface.accessors
        )
        return Row(title=(icon, title), subtitle=subtitle)


class DetailedList(Table):
    # The following methods are overridden from Table.
    @property
    def _headings(self):
        return None

    @property
    def _accessors(self):
        return ("title", "subtitle")

    @property
    def _multiple_select(self):
        return False

    @property
    def _data(self):
        return self._table_source

    def create(self):
        self.native = WinForms.ListView()
        self.native.View = WinForms.View.Details
        self.native.HeaderStyle = getattr(WinForms.ColumnHeaderStyle, "None")
        self._list_index_to_image_index = {}
        self._cache = []
        self._first_item = 0

        self.native.Columns.Add(self._create_column("title"))
        self.native.Columns.Add(self._create_column("subtitle"))

        self.native.FullRowSelect = True
        self.native.DoubleBuffered = True
        self.native.VirtualMode = True

        self.native.ItemSelectionChanged += WeakrefCallable(
            self.winforms_item_selection_changed
        )
        self.native.RetrieveVirtualItem += WeakrefCallable(
            self.winforms_retrieve_virtual_item
        )
        self.native.CacheVirtualItems += WeakrefCallable(
            self.winforms_cache_virtual_items
        )

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
            row = self.interface.data[e.ItemIndex]
            e.Item = self.build_item(row=row, index=e.ItemIndex)

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
            index = i + self._first_item
            row = self.interface.data[index]
            self._cache.append(self.build_item(row=row, index=index))

    def winforms_item_selection_changed(self, sender, e):
        if self.interface.on_select:
            self.interface.on_select(
                self.interface, row=self.interface.data[e.ItemIndex]
            )

    def _create_column(self, accessor):
        col = WinForms.ColumnHeader()
        col.Name = accessor
        col.Width = -2
        return col

    def change_source(self, source):
        self.update_data()

    def update_data(self):
        self.native.VirtualListSize = len(self.interface.data)
        image_list = WinForms.ImageList()
        self._list_index_to_image_index = {}
        counter = 0
        for i, item in enumerate(self.interface.data):
            if item.icon is not None:
                image_list.Images.Add(item.icon._impl.native)
                self._list_index_to_image_index[i] = counter
                counter += 1
        self.native.SmallImageList = image_list
        self._cache = []

    def insert(self, index, item):
        self.update_data()

    def change(self, item):
        self.interface.factory.not_implemented("Table.change()")

    def remove(self, item, index):
        self.update_data()

    def clear(self):
        self.native.Items.Clear()

    def get_selection(self):
        if not self.native.SelectedIndices.Count:
            return None
        return self.interface.data[self.native.SelectedIndices[0]]

    def set_on_delete(self, handler):
        pass

    def set_on_select(self, handler):
        pass

    def set_on_double_click(self, handler):
        self.interface.factory.not_implemented("Table.set_on_double_click()")

    def set_refresh_enabled(self, enabled):
        self.refresh_enabled = enabled

    after_on_refresh = None
