from travertino.size import at_least
from rubicon.objc import py_from_ns

from toga.keys import Key
from ..keys import toga_key
from ..libs import (
    NSBezelBorder,
    NSIndexSet,
    NSOutlineView,
    NSScrollView,
    NSTableViewAnimation,
    NSTableViewColumnAutoresizingStyle,
    objc_method,
    send_super,
    SEL,
)
from .base import Widget
from .internal.cells import TogaTableCellView
from .internal.data import TogaData


class TogaTree(NSOutlineView):
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
        try:
            node_impl = node._impl
        except AttributeError:
            node_impl = TogaData.alloc().init()
            node_impl.attrs = {"node": node}
            node._impl = node_impl

        return node_impl

    @objc_method
    def outlineView_isItemExpandable_(self, tree, item) -> bool:
        try:
            return item.attrs["node"].can_have_children()
        except AttributeError:
            return False

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

        node = item.attrs["node"]

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

        text = column.interface.get_data_for_node(node, "text")
        checked_state = column.interface.get_data_for_node(node, "checked_state")
        icon = column.interface.get_data_for_node(node, "icon")
        native_icon = icon.bind(self.interface.factory).native if icon else None

        tcv.setText(text)
        tcv.setImage(native_icon)
        tcv.setCheckedState(checked_state)

        return tcv

    @objc_method
    def outlineView_heightOfRowByItem_(self, tree, item) -> float:
        return self.rowHeight

    @objc_method
    def outlineView_pasteboardWriterForItem_(self, tree, item) -> None:
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

    @objc_method
    def keyDown_(self, event) -> None:
        # any time this table is in focus and a key is pressed, this method will be called
        if toga_key(event) == {"key": Key.A, "modifiers": {Key.MOD_1}}:
            if self.interface.multiple_select:
                self.selectAll(self)
        else:
            # forward call to super
            send_super(__class__, self, "keyDown:", event)

    # OutlineViewDelegate methods
    @objc_method
    def outlineViewSelectionDidChange_(self, notification) -> None:
        if notification.object.selectedRow == -1:
            selected = None
        else:
            selected = self.itemAtRow(notification.object.selectedRow).attrs["node"]

        if self.interface.on_select:
            self.interface.on_select(self.interface, node=selected)

    # target methods
    @objc_method
    def onDoubleClick_(self, sender) -> None:
        if self.clickedRow == -1:
            node = None
        else:
            node = self.itemAtRow(self.clickedRow).attrs["node"]

        if self.interface.on_double_click:
            self.interface.on_double_click(self.interface, node=node)

    @objc_method
    def onTextEdited_(self, sender) -> None:
        row_index = self.rowForView(sender)
        column_index = self.columnForView(sender)

        column = self.interface.columns[column_index]
        node = self.itemAtRow(row_index).attrs["node"]

        new_text = py_from_ns(sender.textField.stringValue)
        column.set_data_for_node(node, "text", new_text)

    @objc_method
    def onToggled_(self, sender) -> None:
        row_index = self.rowForView(sender)
        column_index = self.columnForView(sender)

        column = self.interface.columns[column_index]
        node = self.itemAtRow(row_index).attrs["node"]

        checked_state = int(py_from_ns(sender.checkbox.state))
        column.set_data_for_node(node, "checked_state", checked_state)


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
        self.tree = TogaTree.alloc().init()
        self.tree.interface = self.interface
        self.tree._impl = self
        self.tree.columnAutoresizingStyle = NSTableViewColumnAutoresizingStyle.Uniform
        self.tree.usesAlternatingRowBackgroundColors = True
        self.tree.allowsMultipleSelection = self.interface.multiple_select

        for column in self.interface.columns:
            self.tree.addTableColumn(column._impl.native)

        # Put the tree arrows in the first column.
        self.tree.outlineTableColumn = self.tree.tableColumns[0]

        self.tree.delegate = self.tree
        self.tree.dataSource = self.tree
        self.tree.target = self.tree
        self.tree.doubleAction = SEL("onDoubleClick:")

        # Embed the tree view in the scroll view
        self.native.documentView = self.tree

        # Add the layout constraints
        self.add_constraints()

    def change_source(self, source):
        self.tree.reloadData()

    def insert(self, parent, index, item):
        # set parent = None if inserting to the root item
        index_set = NSIndexSet.indexSetWithIndex(index)
        if parent is self.interface.data:
            parent = None
        else:
            parent = getattr(parent, "_impl", None)

        self.tree.insertItemsAtIndexes(
            index_set,
            inParent=parent,
            withAnimation=NSTableViewAnimation.SlideDown.value,
        )

    def change(self, item):
        try:
            self.tree.reloadItem(item._impl)
        except AttributeError:
            pass

    def remove(self, parent, index, item):
        try:
            index = self.tree.childIndexForItem(item._impl)
        except AttributeError:
            pass
        else:
            index_set = NSIndexSet.indexSetWithIndex(index)
            parent = self.tree.parentForItem(item._impl)
            self.tree.removeItemsAtIndexes(
                index_set,
                inParent=parent,
                withAnimation=NSTableViewAnimation.SlideUp.value,
            )

    def clear(self):
        self.tree.reloadData()

    def get_selection(self):
        if self.interface.multiple_select:
            selection = []

            current_index = self.tree.selectedRowIndexes.firstIndex
            for i in range(self.tree.selectedRowIndexes.count):
                selection.append(self.tree.itemAtRow(current_index).attrs["node"])
                current_index = self.tree.selectedRowIndexes.indexGreaterThanIndex(
                    current_index
                )

            return selection
        else:
            index = self.tree.selectedRow
            if index != -1:
                return self.tree.itemAtRow(index).attrs["node"]
            else:
                return None

    def set_on_select(self, handler):
        pass

    def set_on_double_click(self, handler):
        pass

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface.MIN_HEIGHT)
