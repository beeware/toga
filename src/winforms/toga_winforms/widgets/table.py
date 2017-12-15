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
        raise NotImplementedError()

    def remove(self, item):
        raise NotImplementedError()

    def clear(self):
        self.native.Clear()

    def set_on_select(self, handler):
        pass

    def scroll_to_row(self, row):
        raise NotImplementedError()
