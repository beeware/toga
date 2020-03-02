from travertino.size import at_least

from toga_winforms.libs import WinForms

from .base import Widget


class Table(Widget):
    def create(self):
        self._container = self
        self.native = WinForms.ListView()
        self.native.View = WinForms.View.Details

        dataColumn = []
        for heading in self.interface.headings:
            col = WinForms.ColumnHeader()
            col.Text = heading
            dataColumn.append(col)

        self.native.FullRowSelect = True
        self.native.Multiselect = self.interface.multiple_select
        self.native.DoubleBuffered = True
        self.native.Columns.AddRange(dataColumn)

    def change_source(self, source):
        self.update_data()

    def row_data(self, item):
        # TODO: Winforms can't support icons in tree cells; so, if the data source
        # specifies an icon, strip it when converting to row data.
        def strip_icon(item, attr):
            val = getattr(item, attr)
            if isinstance(val, tuple):
                return str(val[1])
            return str(val)

        return [item] + [
            strip_icon(item, attr)
            for attr in self.interface._accessors
        ]

    def update_data(self):
        self.native.BeginUpdate()
        self.native.Items.Clear()
        items = []
        for item in self.interface.data:
            item._impl = WinForms.ListViewItem(self.row_data(item))
            items.append(item._impl)
        self.native.Items.AddRange(items)
        self.native.EndUpdate()

    def insert(self, index, item):
        self.native.BeginUpdate()
        item._impl = WinForms.ListViewItem([
            str(getattr(item, attr)) for attr in self.interface._accessors
        ])
        self.native.Items.Insert(index, item._impl)
        self.native.EndUpdate()

    def change(self, item):
        self.interface.factory.not_implemented('Table.change()')

    def remove(self, item):
        self.update_data()

    def clear(self):
        self.native.Items.Clear()

    def set_on_select(self, handler):
        self.interface.factory.not_implemented('Table.set_on_select()')

    def scroll_to_row(self, row):
        self.native.EnsureVisible(row)
        self.interface.factory.not_implemented('Table.scroll_to_row()')

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface.MIN_HEIGHT)
