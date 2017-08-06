from ..libs import *
from .base import Widget


class TogaTable(NSTableView):
    # TableDataSource methods
    @objc_method
    def numberOfRowsInTableView_(self, table) -> int:
        return len(self._impl.data)

    @objc_method
    def tableView_objectValueForTableColumn_row_(self, table, column, row: int):
        column_index = int(column.identifier)
        return self._impl.data[row][column_index]

    # TableDelegate methods
    @objc_method
    def tableViewSelectionDidChange_(self, notification) -> None:
        print ("selection changed")


class Table(Widget):
    def create(self):
        self.data = []
        # Create a table view, and put it in a scroll view.
        # The scroll view is the _impl, because it's the outer container.
        self.native = NSScrollView.alloc().init()
        self.native.hasVerticalScroller = True
        self.native.hasHorizontalScroller = True
        self.native.autohidesScrollers = False
        self.native.borderType = NSBezelBorder

        self.table = TogaTable.alloc().init()
        self.table.interface = self.interface
        self.table._impl = self
        self.table.columnAutoresizingStyle = NSTableViewUniformColumnAutoresizingStyle

        # Create columns for the table
        self._columns = [
            NSTableColumn.alloc().initWithIdentifier_('%d' % i)
            for i, heading in enumerate(self.interface.headings)
        ]

        for heading, column in zip(self.interface.headings, self._columns):
            self.table.addTableColumn(column)
            cell = column.dataCell
            cell.editable = False
            cell.selectable = False
            column.headerCell.stringValue = heading

        self.table.delegate = self.table
        self.table.dataSource = self.table

        # Embed the table view in the scroll view
        self.native.documentView = self.table

        # Add the layout constraints
        self.add_constraints()
