from travertino.size import at_least

from toga_winforms.libs import WinForms

from .base import Widget


class DetailedList(Widget):
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

        self.native.ItemSelectionChanged += self.winforms_item_selection_changed
        self.native.RetrieveVirtualItem += self.winforms_retrieve_virtual_item
        self.native.CacheVirtualItems += self.winforms_cache_virtual_items

    def winforms_retrieve_virtual_item(self, sender, e):
        # Because ListView is in VirtualMode, it's necessary implement
        # VirtualItemsSelectionRangeChanged event to create ListViewItem when it's needed
        if self._cache and e.ItemIndex >= self._first_item and \
                e.ItemIndex < self._first_item + len(self._cache):
            e.Item = self._cache[e.ItemIndex - self._first_item]
        else:
            row = self.interface.data[e.ItemIndex]
            e.Item = self.build_item(row=row, index=e.ItemIndex)

    def winforms_cache_virtual_items(self, sender, e):
        if self._cache and e.StartIndex >= self._first_item and \
                e.EndIndex < self._first_item + len(self._cache):
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
            self.interface.on_select(self.interface, row=self.interface.data[e.ItemIndex])

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
                item.icon.bind(self.interface.factory)
                image_list.Images.Add(item.icon._impl.native)
                self._list_index_to_image_index[i] = counter
                counter += 1
        self.native.SmallImageList = image_list
        self._cache = []

    def insert(self, index, item):
        self.update_data()

    def change(self, item):
        self.interface.factory.not_implemented('Table.change()')

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

    def set_font(self, font):
        if font:
            self.native.Font = font.bind(self.interface.factory).native

    def set_on_double_click(self, handler):
        self.interface.factory.not_implemented('Table.set_on_double_click()')

    def set_on_refresh(self, handler):
        pass

    def after_on_refresh(self, widget, result):
        pass

    def scroll_to_row(self, row):
        self.native.EnsureVisible(row)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface.MIN_HEIGHT)

    def build_item(self, row, index):
        item = WinForms.ListViewItem(row.title)
        image_index = self._list_index_to_image_index.get(index)
        if image_index is not None:
            item.ImageIndex = image_index
        if row.subtitle is not None:
            item.SubItems.Add(row.subtitle)
        return item
