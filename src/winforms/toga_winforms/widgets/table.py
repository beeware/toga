from toga.interface import Table as TableInterface

from ..libs import *
from .base import WidgetMixin      

class Table(TableInterface, WidgetMixin):
    def __init__(self, headings, id=None, style=None):
        super(Table, self).__init__(headings, id=id, style=style)
        self._create()

    def create(self):
        self._container = self
        self._impl = WinForms.DataGridView()
        self._impl = WinForms.DataGridView()
        self._impl.ColumnHeadersHeightSizeMode = WinForms.DataGridViewColumnHeadersHeightSizeMode.AutoSize
        self._impl.ReadOnly = True
        dataGridViewColumn = []
        for heading in self.headings:
            col = WinForms.DataGridViewTextBoxColumn()
            col.HeaderText = heading
            dataGridViewColumn.append(col)

        self._impl.Columns.AddRange(dataGridViewColumn)
 
    def insert(self, index, *data):
        if len(data) != len(self.headings):
            raise Exception('Data size does not match number of headings')

        if index is None:
            self._impl.Rows.Add(*data)  
        else:
            self._impl.Rows.Insert(index,*data)  
         




        