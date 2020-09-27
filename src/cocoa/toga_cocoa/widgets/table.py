from travertino.size import at_least

import toga
from toga_cocoa.libs import (
    NSBezelBorder,
    NSIndexSet,
    NSRange,
    NSScrollView,
    NSTableColumn,
    NSTableView,
    NSTableViewAnimation,
    NSTableViewColumnAutoresizingStyle,
    at,
    objc_method,
    SEL
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
            tcv = TogaIconView.alloc().init()
            tcv.identifier = identifier

        tcv.setText(str(value))
        if icon:
            tcv.setImage(icon.native)
        else:
            tcv.setImage(None)

        # Keep track of last visible view for row
        self._impl._view_for_row[data_row] = tcv

        return tcv

    @objc_method
    def tableView_pasteboardWriterForRow_(self, table, row) -> None:
        # this seems to be required to prevent issue 21562075 in AppKit
        return None

    # TableDelegate methods
    @objc_method
    def selectionShouldChangeInTableView_(self, table) -> bool:
        # Explicitly allow selection on the table.
        # TODO: return False to disable selection.
        return True

    @objc_method
    def tableViewSelectionDidChange_(self, notification) -> None:
        if notification.object.selectedRow == -1:
            selected = None
        else:
            selected = self.interface.data[notification.object.selectedRow]

        if self.interface.on_select:
            self.interface.on_select(self.interface, row=selected)

    @objc_method
    def tableView_heightOfRow_(self, table, row: int) -> float:

        default_row_height = self.rowHeight
        margin = 2

        # get all views in column
        data_row = self.interface.data[row]

        heights = [default_row_height]

        for column in self.tableColumns:
            col_identifier = str(column.identifier)
            value = getattr(data_row, col_identifier, None)
            if isinstance(value, toga.Widget):
                # if the cell value is a widget, use its height
                heights.append(value._impl.native.intrinsicContentSize().height + margin)

        return max(heights)

    # target methods
    @objc_method
    def onDoubleClick_(self, sender) -> None:
        if self.clickedRow == -1:
            clicked = None
        else:
            clicked = self.interface.data[self.clickedRow]

        if self.interface.on_double_click:
            self.interface.on_double_click(self.interface, row=clicked)


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
        self.table.usesAlternatingRowBackgroundColors = True
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
        self.table.target = self.table
        self.table.doubleAction = SEL('onDoubleClick:')

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
            withAnimation=NSTableViewAnimation.EffectNone
        )

    def change(self, item):
        row_index = self.table.rowForView(self._view_for_row[item])
        row_indexes = NSIndexSet.indexSetWithIndex(row_index)
        column_indexes = NSIndexSet.indexSetWithIndexesInRange(NSRange(0, len(self.columns)))
        self.table.reloadDataForRowIndexes(
            row_indexes,
            columnIndexes=column_indexes
        )

    def remove(self, index, item):
        indexes = NSIndexSet.indexSetWithIndex(index)
        self.table.removeRowsAtIndexes(
            indexes,
            withAnimation=NSTableViewAnimation.EffectNone
        )

    def clear(self):
        self._view_for_row.clear()
        self.table.reloadData()

    def get_selection(self):
        if self.interface.multiple_select:
            selection = []

            current_index = self.table.selectedRowIndexes.firstIndex
            for i in range(self.table.selectedRowIndexes.count):
                selection.append(self.interface.data[current_index])
                current_index = self.table.selectedRowIndexes.indexGreaterThanIndex(current_index)

            return selection
        else:
            index = self.table.selectedRow
            if index != -1:
                return self.interface.data[index]
            else:
                return None

    def set_on_select(self, handler):
        pass

    def set_on_double_click(self, handler):
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
        column.minWidth = 16
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
