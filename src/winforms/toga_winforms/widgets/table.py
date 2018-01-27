from travertino.size import at_least

from toga_winforms.libs import *

from .base import Widget


class Table(Widget):
    def create(self):
        self._container = self
        self.native = WinForms.ListView()

        dataColumn = []
        for heading in self.interface.headings:
            col = WinForms.ColumnHeader()
            col.Text = heading
            dataColumn.append(col)

        self.native.View = WinForms.View.Details
        self.native.Columns.AddRange(dataColumn)

    def change_source(self, source):
        for row in self.interface.data:
            row._impl = WinForms.ListViewItem(*[
                getattr(row, attr) for attr in self.interface._accessors
            ])
            self.native.Items.Insert(index, row._impl)

    def insert(self, index, item):
        item._impl = WinForms.ListViewItem(*[
            getattr(item, attr) for attr in self.interface._accessors
        ])
        self.native.Items.Insert(index, item._impl)

    def change(self, item):
        self.interface.factory.not_implemented('Table.change()')

    def remove(self, item):
        self.interface.factory.not_implemented('Table.remove()')

    def clear(self):
        self.native.Clear()

    def set_on_select(self, handler):
        self.interface.factory.not_implemented('Table.set_on_select()')

    def scroll_to_row(self, row):
        self.interface.factory.not_implemented('Table.scroll_to_row()')

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface.MIN_HEIGHT)
