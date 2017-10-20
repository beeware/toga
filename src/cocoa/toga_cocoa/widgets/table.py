from ..libs import *
from ..utils import process_callback
from .base import Widget


class TogaTable(NSTableView):
    # TableDataSource methods
    @objc_method
    def numberOfRowsInTableView_(self, table) -> int:
        return len(self.interface.data.rows()) if self.interface.data else 0

    @objc_method
    def tableView_objectValueForTableColumn_row_(self, table, column, row: int):
        column_index = int(column.identifier)
        return self.interface.data.item(row, column_index)

    # TableDelegate methods
    @objc_method
    def tableViewSelectionDidChange_(self, notification) -> None:
        self.interface.selection = notification.object.selectedRow
        self.interface.selected = self.interface.data.row(notification.object.selectedRow)
        if self.interface.on_select:
            row = notification.object.selectedRow if notification.object.selectedRow != -1 else None
            process_callback(self.interface.on_select(self.interface, row))


class Table(Widget):
    def create(self):
        self.nodes = {}
        # Create a table view, and put it in a scroll view.
        # The scroll view is the native, because it's the outer container.
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
        self.columns = []
        for i, heading in enumerate(self.interface.headings):
            column = NSTableColumn.alloc().initWithIdentifier('%d' % i)
            self.table.addTableColumn(column)
            self.columns.append(column)

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

    def refresh(self):
        self.table.reloadData()
