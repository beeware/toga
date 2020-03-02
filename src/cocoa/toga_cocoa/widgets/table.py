from rubicon.objc import at
from travertino.size import at_least

from toga_cocoa.libs import (
    objc_method,
    NSBezelBorder,
    NSScrollView,
    NSTableColumn,
    NSTableView,
    NSTableViewColumnAutoresizingStyle
)
from .base import Widget
from .internal.cells import TogaIconCell
from .internal.data import TogaData


class TogaTable(NSTableView):
    # TableDataSource methods
    @objc_method
    def numberOfRowsInTableView_(self, table) -> int:
        return len(self.interface.data) if self.interface.data else 0

    @objc_method
    def tableView_objectValueForTableColumn_row_(self, table, column, row: int):
        data_row = self.interface.data[row]

        # Obtain (constructing, if it doesn't already exist) the
        # impl for the data row.
        try:
            data = data_row._impl
        except AttributeError:
            data = {
                attr: TogaData.alloc().init()
                for attr in self.interface._accessors
            }
            data_row._impl = data

        col_identifier = str(column.identifier)

        datum = data[col_identifier]
        value = getattr(data_row, col_identifier)

        # Allow for an (icon, value) tuple as the simple case
        # for encoding an icon in a table cell.
        if isinstance(value, tuple):
            icon, value = value
        else:
            # If the value has an icon attribute, get the _impl.
            # Icons are deferred resources, so we bind to the factory.
            try:
                icon = value.icon.bind(self.interface.factory)
            except AttributeError:
                icon = None

        datum.attrs = {
            'label': str(value),
            'icon': icon,
        }

        return datum

    # TableDelegate methods
    @objc_method
    def selectionShouldChangeInTableView_(self, table) -> bool:
        # Explicitly allow selection on the table.
        # TODO: return False to disable selection.
        return True

    @objc_method
    def tableViewSelectionDidChange_(self, notification) -> None:
        selection = []
        current_index = self.selectedRowIndexes.firstIndex
        for i in range(self.selectedRowIndexes.count):
            selection.append(self.interface.data[current_index])
            current_index = self.selectedRowIndexes.indexGreaterThanIndex(current_index)

        if not self.interface.multiple_select:
            try:
                self.interface._selection = selection[0]
            except IndexError:
                self.interface._selection = None
        else:
            self.interface._selection = selection

        if notification.object.selectedRow == -1:
            selected = None
        else:
            selected = self.interface.data[notification.object.selectedRow]

        if self.interface.on_select:
            self.interface.on_select(self.interface, row=selected)


class Table(Widget):
    def create(self):
        # Create a table view, and put it in a scroll view.
        # The scroll view is the native, because it's the outer container.
        self.native = NSScrollView.alloc().init()
        self.native.hasVerticalScroller = True
        self.native.hasHorizontalScroller = False
        self.native.autohidesScrollers = False
        self.native.borderType = NSBezelBorder

        self.table = TogaTable.alloc().init()
        self.table.interface = self.interface
        self.table._impl = self
        self.table.columnAutoresizingStyle = NSTableViewColumnAutoresizingStyle.Uniform

        self.table.allowsMultipleSelection = self.interface.multiple_select

        # Create columns for the table
        self.columns = []
        # Cocoa identifies columns by an accessor; to avoid repeated
        # conversion from ObjC string to Python String, create the
        # ObjC string once and cache it.
        self.column_identifiers = {}
        for i, (heading, accessor) in enumerate(zip(
                    self.interface.headings,
                    self.interface._accessors
                )):

            column_identifier = at(accessor)
            self.column_identifiers[id(column_identifier)] = accessor
            column = NSTableColumn.alloc().initWithIdentifier(column_identifier)
            self.table.addTableColumn(column)
            self.columns.append(column)

            cell = TogaIconCell.alloc().init()
            column.dataCell = cell

            column.headerCell.stringValue = heading

        self.table.delegate = self.table
        self.table.dataSource = self.table

        # Embed the table view in the scroll view
        self.native.documentView = self.table

        # Add the layout constraints
        self.add_constraints()

    def change_source(self, source):
        self.table.reloadData()

    def insert(self, index, item):
        self.table.reloadData()

    def change(self, item):
        self.table.reloadData()

    def remove(self, item):
        self.table.reloadData()

    def clear(self):
        self.table.reloadData()

    def set_on_select(self, handler):
        pass

    def scroll_to_row(self, row):
        self.table.scrollRowToVisible(row)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface.MIN_HEIGHT)
