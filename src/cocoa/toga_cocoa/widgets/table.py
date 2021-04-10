from travertino.size import at_least
from rubicon.objc import py_from_ns

from toga_cocoa.libs import (
    NSBezelBorder,
    NSIndexSet,
    NSRange,
    NSScrollView,
    NSTableView,
    NSTableViewAnimation,
    NSTableViewColumnAutoresizingStyle,
    objc_method,
    SEL,
)

from .base import Widget
from .internal.cells import TogaTableCellView


class TogaTable(NSTableView):
    # TableDataSource methods
    @objc_method
    def numberOfRowsInTableView_(self, table) -> int:
        return len(self.interface.data) if self.interface.data else 0

    @objc_method
    def tableView_viewForTableColumn_row_(self, table, column, row: int):
        data_row = self.interface.data[row]

        # creates a NSTableCellView from interface-builder template (does not exist)
        # or reuses an existing view which is currently not needed for painting
        # returns None (nil) if both fails
        tcv = self.makeViewWithIdentifier(column.identifier, owner=self)

        if not tcv:  # there is no existing view to reuse so create a new one
            tcv = TogaTableCellView.alloc().initWithLayout()
            tcv.identifier = column.identifier

			# Prevent tcv from being deallocated prematurely when no Python references
            # are left
			tcv.retain()
			tcv.autorelease()

            tcv.checkbox.target = self
            tcv.textField.target = self
            tcv.checkbox.action = SEL('onToggled:')
            tcv.textField.action = SEL('onTextEdited:')

        text = column.interface.get_data_for_node(data_row, "text")
        checked_state = column.interface.get_data_for_node(data_row, "checked_state")
        icon = column.interface.get_data_for_node(data_row, "icon")
        native_icon = icon.bind(self.interface.factory).native if icon else None

        tcv.setText(text)
        tcv.setImage(native_icon)
        tcv.setCheckState(checked_state)

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

    # target methods
    @objc_method
    def onDoubleClick_(self, sender) -> None:
        if self.clickedRow == -1:
            clicked = None
        else:
            clicked = self.interface.data[self.clickedRow]

        if self.interface.on_double_click:
            self.interface.on_double_click(self.interface, row=clicked)

    @objc_method
    def onTextEdited_(self, sender) -> None:
        row_index = self.rowForView(sender)
        column_index = self.columnForView(sender)

        column = self.interface.columns[column_index]
        node = self.interface.data[row_index]

        new_text = py_from_ns(sender.stringValue)
        column.set_data_for_node(node, "text", new_text)

    @objc_method
    def onToggled_(self, sender) -> None:
        row_index = self.rowForView(sender)
        column_index = self.columnForView(sender)

        column = self.interface.columns[column_index]
        node = self.interface.data[row_index]

        checked_state = bool(py_from_ns(sender.state))
        column.set_data_for_node(node, "checked_state", checked_state)


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

        for column in self.interface._columns:
            self.table.addTableColumn(column._impl.native)

        self.table.delegate = self.table
        self.table.dataSource = self.table
        self.table.target = self.table

        if self.interface.on_double_click:
            # otherwise don't set doubleAction to begin editing
            self.table.doubleAction = SEL("onDoubleClick:")

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
            index_set, withAnimation=NSTableViewAnimation.EffectNone
        )

    def change(self, item):
        row_index = self.table.rowForView(self._view_for_row[item])
        row_indexes = NSIndexSet.indexSetWithIndex(row_index)
        column_indexes = NSIndexSet.indexSetWithIndexesInRange(
            NSRange(0, len(self.interface.columns))
        )
        self.table.reloadDataForRowIndexes(row_indexes, columnIndexes=column_indexes)

    def remove(self, index, item):
        indexes = NSIndexSet.indexSetWithIndex(index)
        self.table.removeRowsAtIndexes(
            indexes, withAnimation=NSTableViewAnimation.EffectNone
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
                current_index = self.table.selectedRowIndexes.indexGreaterThanIndex(
                    current_index
                )

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

    def add_column(self, column):
        self.table.addTableColumn(column._impl.native)
        self.table.sizeToFit()

    def remove_column(self, column):
        self.table.removeTableColumn(column._impl.native)
        self.table.sizeToFit()
