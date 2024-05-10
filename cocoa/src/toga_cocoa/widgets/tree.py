from rubicon.objc import SEL, at, objc_method, objc_property
from travertino.size import at_least

import toga
from toga_cocoa.libs import (
    NSBezelBorder,
    NSIndexSet,
    NSOutlineView,
    NSScrollView,
    NSTableColumn,
    NSTableViewAnimation,
    NSTableViewColumnAutoresizingStyle,
)
from toga_cocoa.widgets.base import Widget
from toga_cocoa.widgets.internal.cells import TogaIconView
from toga_cocoa.widgets.internal.data import TogaData


def node_impl(node):
    try:
        return node._impl
    except AttributeError:
        node._impl = TogaData.alloc().init()
        node._impl.attrs = {"node": node}
        return node._impl


class TogaTree(NSOutlineView):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    # OutlineViewDataSource methods
    @objc_method
    def outlineView_child_ofItem_(self, tree, child: int, item):
        # Get the object representing the row
        if item is None:
            node = self.interface.data[child]
        else:
            node = item.attrs["node"][child]

        # Get the Cocoa implementation for the row. If an _impl
        # doesn't exist, create a data object for it, and
        # populate it with initial values for each column.

        return node_impl(node)

    @objc_method
    def outlineView_isItemExpandable_(self, tree, item) -> bool:
        return item.attrs["node"].can_have_children()

    @objc_method
    def outlineView_numberOfChildrenOfItem_(self, tree, item) -> int:
        if item is None:
            # How many root elements are there?
            # If we're starting up, the source may not exist yet.
            if self.interface.data is not None:
                return len(self.interface.data)
            else:
                return 0
        else:
            # How many children does this node have?
            return len(item.attrs["node"])

    @objc_method
    def outlineView_viewForTableColumn_item_(self, tree, column, item):
        col_identifier = str(column.identifier)

        try:
            value = getattr(item.attrs["node"], col_identifier)

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
        except AttributeError:
            # If the node doesn't have a property with the
            # accessor name, assume an empty string value.
            value = self.interface.missing_value
            icon = None

        # creates a NSTableCellView from interface-builder template (does not exist)
        # or reuses an existing view which is currently not needed for painting
        # returns None (nil) if both fails
        identifier = at(f"CellView_{self.interface.id}")
        tcv = self.makeViewWithIdentifier(identifier, owner=self)

        if not tcv:  # there is no existing view to reuse so create a new one
            # tcv = TogaIconView.alloc().initWithFrame(CGRectMake(0, 0, column.width, 16))
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

    # 2023-06-29: Commented out this method because it appears to be a
    # source of significant slowdown when the table has a lot of data
    # (10k rows). AFAICT, it's only needed if we want custom row heights
    # for each row. Since we don't currently support custom row heights,
    # we're paying the cost for no benefit.
    # @objc_method
    # def outlineView_heightOfRowByItem_(self, tree, item) -> float:
    #     default_row_height = self.rowHeight

    #     if item is self:
    #         return default_row_height

    #     heights = [default_row_height]

    #     for column in self.tableColumns:
    #         value = getattr(
    #             item.attrs["node"], str(column.identifier), self.interface.missing_value
    #         )

    #         if isinstance(value, toga.Widget):
    #             # if the cell value is a widget, use its height
    #             heights.append(value._impl.native.intrinsicContentSize().height)

    #     return max(heights)

    @objc_method
    def outlineView_pasteboardWriterForItem_(
        self, tree, item
    ) -> None:  # pragma: no cover
        # this seems to be required to prevent issue 21562075 in AppKit
        return None

    # @objc_method
    # def outlineView_sortDescriptorsDidChange_(self, tableView, oldDescriptors) -> None:
    #
    #     for descriptor in self.sortDescriptors[::-1]:
    #         accessor = descriptor.key
    #         reverse = descriptor.ascending == 1
    #         key = self.interface._sort_keys[str(accessor)]
    #         try:
    #             self.interface.data.sort(str(accessor), reverse=reverse, key=key)
    #         except AttributeError:
    #             pass
    #         else:
    #             self.reloadData()

    # OutlineViewDelegate methods
    @objc_method
    def outlineViewSelectionDidChange_(self, notification) -> None:
        self.interface.on_select()

    # target methods
    @objc_method
    def onDoubleClick_(self, sender) -> None:
        node = self.itemAtRow(self.clickedRow).attrs["node"]
        self.interface.on_activate(node=node)


class Tree(Widget):
    def create(self):
        # Create a tree view, and put it in a scroll view.
        # The scroll view is the _impl, because it's the outer container.
        self.native = NSScrollView.alloc().init()
        self.native.hasVerticalScroller = True
        self.native.hasHorizontalScroller = False
        self.native.autohidesScrollers = False
        self.native.borderType = NSBezelBorder

        # Create the Tree widget
        self.native_tree = TogaTree.alloc().init()
        self.native_tree.interface = self.interface
        self.native_tree.impl = self
        self.native_tree.columnAutoresizingStyle = (
            NSTableViewColumnAutoresizingStyle.Uniform
        )
        self.native_tree.usesAlternatingRowBackgroundColors = True
        self.native_tree.allowsMultipleSelection = self.interface.multiple_select

        # Create columns for the table
        self.columns = []
        if self.interface.headings:
            for index, (heading, accessor) in enumerate(
                zip(self.interface.headings, self.interface.accessors)
            ):
                self._insert_column(index, heading, accessor)
        else:
            self.native_tree.setHeaderView(None)
            for index, accessor in enumerate(self.interface.accessors):
                self._insert_column(index, None, accessor)

        # Put the tree arrows in the first column.
        self.native_tree.outlineTableColumn = self.columns[0]

        self.native_tree.delegate = self.native_tree
        self.native_tree.dataSource = self.native_tree
        self.native_tree.target = self.native_tree
        self.native_tree.doubleAction = SEL("onDoubleClick:")

        # Embed the tree view in the scroll view
        self.native.documentView = self.native_tree

        # Add the layout constraints
        self.add_constraints()

    def change_source(self, source):
        self.native_tree.reloadData()

    def insert(self, parent, index, item):
        index_set = NSIndexSet.indexSetWithIndex(index)
        self.native_tree.insertItemsAtIndexes(
            index_set,
            inParent=node_impl(parent) if parent else None,
            withAnimation=NSTableViewAnimation.SlideDown.value,
        )

    def change(self, item):
        self.native_tree.reloadItem(node_impl(item))

    def remove(self, parent, index, item):
        try:
            index = self.native_tree.childIndexForItem(item._impl)
            index_set = NSIndexSet.indexSetWithIndex(index)
            parent = self.native_tree.parentForItem(item._impl)
            self.native_tree.removeItemsAtIndexes(
                index_set,
                inParent=parent,
                withAnimation=NSTableViewAnimation.SlideUp.value,
            )
        except AttributeError:
            pass

    def clear(self):
        self.native_tree.reloadData()

    def get_selection(self):
        if self.interface.multiple_select:
            selection = []

            current_index = self.native_tree.selectedRowIndexes.firstIndex
            for i in range(self.native_tree.selectedRowIndexes.count):
                selection.append(
                    self.native_tree.itemAtRow(current_index).attrs["node"]
                )
                current_index = (
                    self.native_tree.selectedRowIndexes.indexGreaterThanIndex(
                        current_index
                    )
                )

            return selection
        else:
            index = self.native_tree.selectedRow
            if index != -1:
                return self.native_tree.itemAtRow(index).attrs["node"]
            else:
                return None

    def expand_node(self, node):
        self.native_tree.expandItem(node_impl(node), expandChildren=True)

    def expand_all(self):
        self.native_tree.expandItem(None, expandChildren=True)

    def collapse_node(self, node):
        self.native_tree.collapseItem(node_impl(node), collapseChildren=True)

    def collapse_all(self):
        self.native_tree.collapseItem(None, collapseChildren=True)

    def _insert_column(self, index, heading, accessor):
        column = NSTableColumn.alloc().initWithIdentifier(accessor)
        column.minWidth = 16

        self.columns.insert(index, column)
        self.native_tree.addTableColumn(column)
        if index != len(self.columns) - 1:
            self.native_tree.moveColumn(len(self.columns) - 1, toColumn=index)

        if heading is not None:
            column.headerCell.stringValue = heading

    def insert_column(self, index, heading, accessor):
        self._insert_column(index, heading, accessor)
        self.native_tree.sizeToFit()

    def remove_column(self, index):
        column = self.columns[index]
        self.native_tree.removeTableColumn(column)

        # delete column and identifier
        self.columns.remove(column)
        self.native_tree.sizeToFit()

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
