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
        self.native.Columns.AddRange(dataColumn)

    def change_source(self, source):
        for index, row in enumerate(self.interface.data):
            row._impl = WinForms.ListViewItem([
                getattr(row, attr) for attr in self.interface._accessors
            ])
            self.native.Items.Insert(index, row._impl)

    def update_data(self):
        self.native.Items.Clear()
        for index, row in enumerate(self.interface.data):
            row._impl = WinForms.ListViewItem([
                getattr(row, attr) for attr in self.interface._accessors
            ])
            self.native.Items.Insert(index, row._impl)

    def insert(self, index, item):
        item._impl = WinForms.ListViewItem([
            getattr(item, attr) for attr in self.interface._accessors
        ])
        self.native.Items.Insert(index, item._impl)

    def change(self, item):
        # This event doesnt exist for a listview item
        pass

    def remove(self, item):
        self.update_data()

    def clear(self):
        self.native.Items.Clear()

    def set_on_select(self, handler):
        self.native.SelectedIndexChanged += self.interface.on_select

    def scroll_to_row(self, row):
        self.native.EnsureVisible(row)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface.MIN_HEIGHT)
