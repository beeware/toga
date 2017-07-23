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
        self._impl.hasVerticalScroller = True
        self._impl.hasHorizontalScroller = False
        self._impl.autohidesScrollers = False
        self._impl.borderType = NSBezelBorder

        self._table = TogaTable.alloc().init()
        self._table._interface = self
        self._table.columnAutoresizingStyle = NSTableViewUniformColumnAutoresizingStyle

        # Use autolayout for the inner widget.
        self._table.translatesAutoresizingMaskIntoConstraints = True

        # Create columns for the table
        self._columns = [
            NSTableColumn.alloc().initWithIdentifier('%d' % i)
            for i, heading in enumerate(self.headings)
        ]

        for heading, column in zip(self.headings, self._columns):
            self._table.addTableColumn(column)
            cell = column.dataCell
            cell.editable = False
            cell.selectable = False
            column.headerCell.stringValue = heading

        self._table.delegate = self._table
        self._table.dataSource = self._table

        # Embed the table view in the scroll view
        self._impl.documentView = self._table

        # Add the layout constraints
        self._add_constraints()
