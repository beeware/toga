from toga.interface import Table as TableInterface

from ..libs import *
from .base import WidgetMixin      

class Table(TableInterface, WidgetMixin):
    def __init__(self, headings, id=None, style=None):
        super(Table, self).__init__(headings, id=id, style=style)
        self._create()

    def create(self):
        self._container = self
        self._impl = WinForms.ListView()

        dataColumn = []
        for heading in self.headings:
            col = WinForms.ColumnHeader()
            col.Text = heading
            dataColumn.append(col)

        self._impl.View = WinForms.View.Details
        self._impl.Columns.AddRange(dataColumn)
 
    def insert(self, index, *data):
        if len(data) != len(self.headings):
            raise Exception('Data size does not match number of headings')

        if index is None:
            listViewItem = WinForms.ListViewItem(data); 
            self._impl.Items.Add(listViewItem)  
        else:
            listViewItem = WinForms.ListViewItem(data); 
            self._impl.Items.Insert(index, listViewItem)  
         




        