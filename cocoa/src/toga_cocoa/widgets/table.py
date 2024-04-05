from rubicon.objc import SEL, NSPoint, at, objc_method, objc_property
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
)

from .base import Widget
from .internal.cells import TogaIconView


class TogaTable(NSTableView):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    # NSTableView methods
    @objc_method
    def canDragRowsWithIndexes_atPoint_(
        self,
        rowIndexes,
        mouseDownPoint: NSPoint,
    ) -> bool:
        # Disable all drags
        return False

    # TableDataSource methods
    @objc_method
    def numberOfRowsInTableView_(self, table) -> int:
        return len(self.interface.data) if self.interface.data else 0

    @objc_method
    def tableView_viewForTableColumn_row_(self, table, column, row: int):
        data_row = self.interface.data[row]
        col_identifier = str(column.identifier)

        value = getattr(data_row, col_identifier, None)

        # if the value is a widget itself, just draw the widget!
        if isinstance(value, toga.Widget):
            return value._impl.native

        # Allow for an (icon, value) tuple as the simple case
        # for encoding an icon in a table cell. Otherwise, look
        # for an icon attribute.
        elif isinstance(value, tuple):
            icon, value = value
        else:
            try:
                icon = value.icon
            except AttributeError:
                icon = None

        if value is None:
            value = self.interface.missing_value

        # creates a NSTableCellView from interface-builder template (does not exist)
        # or reuses an existing view which is currently not needed for painting
        # returns None (nil) if both fails
        identifier = at(f"CellView_{self.interface.id}")
        tcv = self.makeViewWithIdentifier(identifier, owner=self)

        if not tcv:  # there is no existing view to reuse so create a new one
            tcv = TogaIconView.alloc().init()
            tcv.identifier = identifier

            # Prevent tcv from being deallocated prematurely when no Python references
            # are left
            tcv.autorelease()

        tcv.setText(str(value))
        if icon:
            tcv.setImage(icon._impl.native)
        else:
            tcv.setImage(None)

        return tcv

    @objc_method
    def tableView_pasteboardWriterForRow_(self, table, row) -> None:  # pragma: no cover
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
        self.interface.on_select()

    # 2021-09-04: Commented out this method because it appears to be a
    # source of significant slowdown when the table has a lot of data
    # (10k rows). AFAICT, it's only needed if we want custom row heights
    # for each row. Since we don't currently support custom row heights,
    # we're paying the cost for no benefit.
    # @objc_method
    # def tableView_heightOfRow_(self, table, row: int) -> float:
    #     default_row_height = self.rowHeight
    #     margin = 2
    #
    #     # get all views in column
    #     data_row = self.interface.data[row]
    #
    #     heights = [default_row_height]
    #
    #     for column in self.tableColumns:
    #         col_identifier = str(column.identifier)
    #         value = getattr(data_row, col_identifier, None)
    #         if isinstance(value, toga.Widget):
    #             # if the cell value is a widget, use its height
    #             heights.append(value._impl.native.intrinsicContentSize().height + margin)
    #
    #     return max(heights)

    # target methods
    @objc_method
    def onDoubleClick_(self, sender) -> None:
        clicked = self.interface.data[self.clickedRow]

        self.interface.on_activate(row=clicked)


class Table(Widget):
    def create(self):
        # Create a table view, and put it in a scroll view.
        # The scroll view is the native, because it's the outer container.
        self.native = NSScrollView.alloc().init()
        self.native.hasVerticalScroller = True
        self.native.hasHorizontalScroller = False
        self.native.autohidesScrollers = False
        self.native.borderType = NSBezelBorder

        self.native_table = TogaTable.alloc().init()
        self.native_table.interface = self.interface
        self.native_table.impl = self
        self.native_table.columnAutoresizingStyle = (
            NSTableViewColumnAutoresizingStyle.Uniform
        )
        self.native_table.usesAlternatingRowBackgroundColors = True
        self.native_table.allowsMultipleSelection = self.interface.multiple_select
        self.native_table.allowsColumnReordering = False

        # Create columns for the table
        self.columns = []
        if self.interface.headings:
            for index, (heading, accessor) in enumerate(
                zip(self.interface.headings, self.interface.accessors)
            ):
                self._insert_column(index, heading, accessor)
        else:
            self.native_table.setHeaderView(None)
            for index, accessor in enumerate(self.interface.accessors):
                self._insert_column(index, None, accessor)

        self.native_table.delegate = self.native_table
        self.native_table.dataSource = self.native_table
        self.native_table.target = self.native_table
        self.native_table.doubleAction = SEL("onDoubleClick:")

        # Embed the table view in the scroll view
        self.native.documentView = self.native_table

        # Add the layout constraints
        self.add_constraints()

    def change_source(self, source):
        self.native_table.reloadData()

    def insert(self, index, item):
        # set parent = None if inserting to the root item
        index_set = NSIndexSet.indexSetWithIndex(index)

        self.native_table.insertRowsAtIndexes(
            index_set, withAnimation=NSTableViewAnimation.EffectNone
        )

    def change(self, item):
        row_index = self.interface.data.index(item)
        row_indexes = NSIndexSet.indexSetWithIndex(row_index)
        column_indexes = NSIndexSet.indexSetWithIndexesInRange(
            NSRange(0, len(self.columns))
        )

        self.native_table.reloadDataForRowIndexes(
            row_indexes, columnIndexes=column_indexes
        )

    def remove(self, index, item):
        indexes = NSIndexSet.indexSetWithIndex(index)
        self.native_table.removeRowsAtIndexes(
            indexes, withAnimation=NSTableViewAnimation.EffectNone
        )

    def clear(self):
        self.native_table.reloadData()

    def get_selection(self):
        if self.interface.multiple_select:
            selection = []

            current_index = self.native_table.selectedRowIndexes.firstIndex
            for i in range(self.native_table.selectedRowIndexes.count):
                selection.append(current_index)
                current_index = (
                    self.native_table.selectedRowIndexes.indexGreaterThanIndex(
                        current_index
                    )
                )

            return selection
        else:
            index = self.native_table.selectedRow
            if index != -1:
                return index
            else:
                return None

    def scroll_to_row(self, row):
        self.native_table.scrollRowToVisible(row)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)

    def _insert_column(self, index, heading, accessor):
        column = NSTableColumn.alloc().initWithIdentifier(accessor)
        column.minWidth = 16

        self.columns.insert(index, column)
        self.native_table.addTableColumn(column)
        if index != len(self.columns) - 1:
            self.native_table.moveColumn(len(self.columns) - 1, toColumn=index)

        if heading is not None:
            column.headerCell.stringValue = heading

    def insert_column(self, index, heading, accessor):
        self._insert_column(index, heading, accessor)
        self.native_table.sizeToFit()

    def remove_column(self, index):
        column = self.columns[index]
        self.native_table.removeTableColumn(column)

        # delete column and identifier
        self.columns.remove(column)
        self.native_table.sizeToFit()
