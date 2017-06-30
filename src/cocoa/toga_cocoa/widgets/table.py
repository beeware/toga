from ..libs import *
from .base import Widget


class TogaTable(NSTableView):
    # TableDataSource methods
    @objc_method
    def numberOfRowsInTableView_(self, table) -> int:
        return len(self.interface.data)

    @objc_method
    def tableView_objectValueForTableColumn_row_(self, table, column, row: int):
        column_index = int(column.identifier)
        return self.interface.data[row][column_index]

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
        self.native.setHasVerticalScroller_(True)
        self.native.setHasHorizontalScroller_(True)
        self.native.setAutohidesScrollers_(False)
        self.native.setBorderType_(NSBezelBorder)

        self.table = TogaTable.alloc().init()
        self.table.interface = self
        self.table.setColumnAutoresizingStyle_(NSTableViewUniformColumnAutoresizingStyle)

        # Create columns for the table
        self._columns = [
            NSTableColumn.alloc().initWithIdentifier_('%d' % i)
            for i, heading in enumerate(self.interface.headings)
        ]

        for heading, column in zip(self.interface.headings, self._columns):
            self.table.addTableColumn_(column)
            cell = column.dataCell
            cell.setEditable_(False)
            cell.setSelectable_(False)
            column.headerCell.stringValue = heading

        self.table.setDelegate_(self.table)
        self.table.setDataSource_(self.table)

        # Embed the table view in the scroll view
        self.native.setDocumentView_(self.table)

        # Add the layout constraints
        self.add_constraints()
