from travertino.size import at_least

from toga_winforms.libs import WinForms

from .base import Widget


class Table(Widget):
    def create(self):
        self._container = self
        self.native = WinForms.ListView()
        self.native.View = WinForms.View.Details

        dataColumn = []
        for i, (heading, accessor) in enumerate(zip(
                    self.interface.headings,
                    self.interface._accessors
                )):
            dataColumn.append(self._create_column(heading, accessor))

        self.native.FullRowSelect = True
        self.native.MultiSelect = self.interface.multiple_select
        self.native.DoubleBuffered = True
        self.native.VirtualMode = True
        self.native.Columns.AddRange(dataColumn)

        self.native.ItemSelectionChanged += self._handle_native_on_select
        self.native.RetrieveVirtualItem += self._handle_native_retrieve_virtual_item
        self.native.VirtualItemsSelectionRangeChanged += self._handle_virtual_range_selection

    def _handle_virtual_range_selection(self, sender, e):
        # `Shift` key or Range selection handler
        if self.interface.multiple_select and self.interface.on_select:
            selected = None
            if e.IsSelected:
                selected = self.interface.data[e.StartIndex:e.EndIndex+1]
            self.interface.on_select(self.interface, row=selected)

    def _handle_native_retrieve_virtual_item(self, sender, e):
        # Because ListView is in VirtualMode, it's necessary implement
        # VirtualItemsSelectionRangeChanged event to create ListViewItem when it's needed
        e.Item = WinForms.ListViewItem(self.row_data(self.interface.data[e.ItemIndex]))

    def _handle_native_on_select(self, sender, e):
        # Normal selection, can be one item or multiple items with `Ctrl` Key
        if not self.interface.on_select:
            return

        if not e.IsSelected:
            self.interface.on_select(self.interface, row=None)

        if self.interface.multiple_select:
            selected_indexes = [index for index in self.native.SelectedIndices]
            selected = [row for i, row in enumerate(self.interface.data) if i in selected_indexes]
            self.interface.on_select(self.interface, row=selected) 
        else:
            self.interface.on_select(self.interface, row=self.interface.data[e.get_ItemIndex()])

    def _create_column(self, heading, accessor):
        col = WinForms.ColumnHeader()
        col.Text = heading
        col.Name = accessor
        return col

    def change_source(self, source):
        self.update_data()

    def row_data(self, item):
        # TODO: Winforms can't support icons in tree cells; so, if the data source
        # specifies an icon, strip it when converting to row data.
        def strip_icon(item, attr):
            try:
                val = getattr(item, attr)
            except AttributeError:
                try:
                    val = self.interface.missing_value
                except ValueError as e:
                    # There is no explicit missing value. Warn the user.
                    message, val = e.args
                    print(message.format('?', attr))

            if isinstance(val, tuple):
                return str(val[1])
            return str(val)

        return [
            strip_icon(item, attr)
            for attr in self.interface._accessors
        ]

    def update_data(self):
        self.native.VirtualListSize = len(self.interface.data)
        """
        self.native.BeginUpdate()
        self.native.Items.Clear()
        items = []
        for item in self.interface.data:
            item._impl = WinForms.ListViewItem(self.row_data(item))
            items.append(item._impl)
            
        self.native.Items.AddRange(items)
        self.native.EndUpdate()
        """

    def insert(self, index, item):
        self.update_data()
        """
        self.native.BeginUpdate()
        item._impl = WinForms.ListViewItem(self.row_data(item))
        self.native.Items.Insert(index, item._impl)
        self.native.EndUpdate()
        """

    def change(self, item):
        self.interface.factory.not_implemented('Table.change()')

    def remove(self, item):
        self.update_data()

    def clear(self):
        self.native.Items.Clear()

    def set_on_select(self, handler):
        pass

    def scroll_to_row(self, row):
        self.native.EnsureVisible(row)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface.MIN_HEIGHT)

    def remove_column(self, accessor):
        self.native.Columns.RemoveByKey(accessor)

    def add_column(self, heading, accessor):
        self.native.Columns.Add(self._create_column(heading, accessor))
        self.update_data()
