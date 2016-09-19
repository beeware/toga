from toga.interface import Table as TableInterface

from ..libs import *
from .base import WidgetMixin


class TogaTable(NSTableView):
    # TableDataSource methods
    @objc_method
    def numberOfRowsInTableView_(self, table) -> int:
        return len(self._interface._data)

    @objc_method
    def tableView_objectValueForTableColumn_row_(self, table, column, row: int):
        column_index = int(column.identifier)
        return self._interface._data[row][column_index]

    # TableDelegate methods
    @objc_method
    def tableViewSelectionDidChange_(self, notification) -> None:
        print ("selection changed")


class Table(TableInterface, WidgetMixin):
    def __init__(self, headings, id=None, style=None):
        super(Table, self).__init__(headings, id=id, style=style)
        self._create()

    def create(self):
        self._data = []
        # Create a table view, and put it in a scroll view.
        # The scroll view is the _impl, because it's the outer container.
        self._impl = NSScrollView.alloc().init()
        self._impl.setHasVerticalScroller_(True)
        self._impl.setHasHorizontalScroller_(True)
        self._impl.setAutohidesScrollers_(False)
        self._impl.setBorderType_(NSBezelBorder)

        self._table = TogaTable.alloc().init()
        self._table._interface = self
        self._table.setColumnAutoresizingStyle_(NSTableViewUniformColumnAutoresizingStyle)

        # Create columns for the table
        self._columns = [
            NSTableColumn.alloc().initWithIdentifier_('%d' % i)
            for i, heading in enumerate(self.headings)
        ]

        for heading, column in zip(self.headings, self._columns):
            self._table.addTableColumn_(column)
            cell = column.dataCell
            cell.setEditable_(False)
            cell.setSelectable_(False)
            column.headerCell.stringValue = heading

        self._table.setDelegate_(self._table)
        self._table.setDataSource_(self._table)

        # Embed the table view in the scroll view
        self._impl.setDocumentView_(self._table)

        # Add the layout constraints
        self._add_constraints()
