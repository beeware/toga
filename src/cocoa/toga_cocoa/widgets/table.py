from travertino.size import at_least

import toga
from toga_cocoa.libs import (
    CGRectMake,
    NSBezelBorder,
    NSIndexSet,
    NSRange,
    NSScrollView,
    NSTableColumn,
    NSTableView,
    NSTableViewAnimation,
    NSTableViewColumnAutoresizingStyle,
    at,
    objc_method
)

from .base import Widget
from .internal.cells import TogaIconView


class TogaTable(NSTableView):
    # TableDataSource methods
    @objc_method
    def numberOfRowsInTableView_(self, table) -> int:
        return len(self.interface.data) if self.interface.data else 0

    @objc_method
    def tableView_viewForTableColumn_row_(self, table, column, row: int):
        data_row = self.interface.data[row]
        col_identifier = str(column.identifier)

        try:
            value = getattr(data_row, col_identifier)

            # if the value is a widget itself, just draw the widget!
            if isinstance(value, toga.Widget):
                return value._impl.native

            # Allow for an (icon, value) tuple as the simple case
            # for encoding an icon in a table cell. Otherwise, look
            # for an icon attribute.
            elif isinstance(value, tuple):
                icon_iface, value = value
            else:
                try:
                    icon_iface = value.icon
                except AttributeError:
                    icon_iface = None
        except AttributeError:
            # The accessor doesn't exist in the data. Use the missing value.
            try:
                value = self.interface.missing_value
            except ValueError as e:
                # There is no explicit missing value. Warn the user.
                message, value = e.args
                print(message.format(row, col_identifier))
            icon_iface = None

        # If the value has an icon, get the _impl.
        # Icons are deferred resources, so we provide the factory.
        if icon_iface:
            icon = icon_iface.bind(self.interface.factory)
        else:
            icon = None

        # creates a NSTableCellView from interface-builder template (does not exist)
        # or reuses an existing view which is currently not needed for painting
        # returns None (nil) if both fails
        identifier = at('CellView_{}'.format(self.interface.id))
        tcv = self.makeViewWithIdentifier(identifier, owner=self)

        if not tcv:  # there is no existing view to reuse so create a new one
            tcv = TogaIconView.alloc().initWithFrame_(CGRectMake(0, 0, column.width, 16))
            tcv.identifier = identifier

        tcv.setText(str(value))
        if icon:
            tcv.setImage(icon.native)
        else:
            tcv.setImage(None)

        # Keep track of last visible view for row
        self._impl._view_for_row[data_row] = tcv

        return tcv

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

    @objc_method
    def tableView_heightOfRow_(self, table, row: int) -> float:

        min_row_height = 18
        margin = 2

        # get all views in column
        views = [self.tableView_viewForTableColumn_row_(table, col, row) for col in self.tableColumns]

        max_widget_size = max(view.intrinsicContentSize().height + margin for view in views)
        return max(min_row_height, max_widget_size)


class Table(Widget):
    def create(self):

        self._view_for_row = dict()

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
        for heading, accessor in zip(self.interface.headings, self.interface._accessors):
            self._add_column(heading, accessor)

        self.table.delegate = self.table
        self.table.dataSource = self.table

        # Embed the table view in the scroll view
        self.native.documentView = self.table

        # Add the layout constraints
        self.add_constraints()

    def change_source(self, source):
        self.table.reloadData()

    def insert(self, index, item):
        # set parent = None if inserting to the root item
        index_set = NSIndexSet.indexSetWithIndex(index)

        self.table.insertRowsAtIndexes(
            index_set,
            withAnimation=NSTableViewAnimation.SlideDown
        )

    def change(self, item):
        row_index = self.table.rowForView(self._view_for_row[item])
        row_indexes = NSIndexSet.indexSetWithIndex(row_index)
        column_indexes = NSIndexSet.indexSetWithIndexesInRange(NSRange(0, len(self.columns)))
        self.table.reloadDataForRowIndexes(
            row_indexes,
            columnIndexes=column_indexes
        )

    def remove(self, item):
        try:
            # We can't get the index from self.interface.data because the
            # row has already been removed. Instead we look up the index
            # from an associated view.
            view = self._view_for_row.pop(item)
            index = self.table.rowForView(view)
        except KeyError:
            pass
        else:
            indexes = NSIndexSet.indexSetWithIndex(index)
            self.table.removeRowsAtIndexes(
                indexes,
                withAnimation=NSTableViewAnimation.SlideUp
            )

    def clear(self):
        self._view_for_row.clear()
        self.table.reloadData()

    def set_on_select(self, handler):
        pass

    def scroll_to_row(self, row):
        self.table.scrollRowToVisible(row)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface.MIN_HEIGHT)

    def _add_column(self, heading, accessor):
        column_identifier = at(accessor)
        self.column_identifiers[accessor] = column_identifier
        column = NSTableColumn.alloc().initWithIdentifier(column_identifier)
        self.table.addTableColumn(column)
        self.columns.append(column)

        column.headerCell.stringValue = heading

    def add_column(self, heading, accessor):
        self._add_column(heading, accessor)
        self.table.sizeToFit()

    def remove_column(self, accessor):
        column_identifier = self.column_identifiers[accessor]
        column = self.table.tableColumnWithIdentifier(column_identifier)
        self.table.removeTableColumn(column)

        # delete column and identifier
        self.columns.remove(column)
        del self.column_identifiers[accessor]

        self.table.sizeToFit()
