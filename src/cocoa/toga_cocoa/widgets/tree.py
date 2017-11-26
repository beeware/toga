from rubicon.objc import *

from toga.sources import to_accessor

from ..libs import *
from .base import Widget
from .internal.cells import TogaIconCell
from .internal.data import TogaData


class TogaTree(NSOutlineView):
    # OutlineViewDataSource methods
    @objc_method
    def outlineView_child_ofItem_(self, tree, child: int, item):
        # Get the object representing the row
        if item is None:
            node = self.interface.data[child]
        else:
            node = item.attrs['node'][child]

        # Get the Cocoa implementation for the row. If an _impl
        # doesn't exist, create a data object for it, and
        # populate it with initial values for each column.
        try:
            node_impl = node._impl
        except AttributeError:
            node_impl = TogaData.alloc().init()
            node_impl.attrs = {
                'node': node,
                'values': {
                    attr: None
                    for attr in self.interface._accessors
                }
            }
            node._impl = node_impl

        return node_impl

    @objc_method
    def outlineView_isItemExpandable_(self, tree, item) -> bool:
        try:
            return item.attrs['node'].has_children()
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
            return len(item.attrs['node'])

    @objc_method
    def outlineView_objectValueForTableColumn_byItem_(self, tree, column, item):
        try:
            value = getattr(item.attrs['node'], column.identifier)

            # Allow for an (icon, value) tuple as the simple case
            # for encoding an icon in a table cell.
            if isinstance(value, tuple):
                icon, value = value
            else:
                # If the value has an icon attribute, get the _impl.
                # Icons are deferred resources, so we provide the factory.
                try:
                    icon = value.icon._impl(self.interface.factory)
                except AttributeError:
                    icon = None
        except AttributeError:
            # If the node doesn't have a property with the
            # accessor name, assume an empty string value.
            value = ''
            icon = None

        # Now construct the data object for the cell.
        # If the datum already exists, reuse and update it.
        # If an icon is present, create a TogaData object.
        # Otherwise, just use the string (because a Python string)
        # is transparently an ObjC object, so it works as a value.
        obj = item.attrs['values'][column.identifier]
        if obj is None or isinstance(obj, str):
            if icon:
                # Create a TogaData value
                obj = TogaData.alloc().init()
                obj.attrs = {
                    'label': str(value),
                    'icon': icon,
                }
            else:
                # Create/Update the string value
                obj = str(value)
            item.attrs['values'][column.identifier] = obj
        else:
            # Datum exists, and is currently an icon.
            if icon:
                # Update TogaData values
                obj.attrs = {
                    'label': str(value),
                    'icon': icon,
                }
            else:
                # Convert to a simple string.
                obj = str(value)
                item.attrs['values'][column.identifier] = obj

        return obj

    # OutlineViewDelegate methods
    @objc_method
    def outlineViewSelectionDidChange_(self, notification) -> None:
        self.interface.selected = []
        currentIndex = self.selectedRowIndexes.firstIndex
        for i in range(self.selectedRowIndexes.count):
            # self.interface.selected.append(self._impl.node[self.itemAtRow(currentIndex)])
            currentIndex = self.selectedRowIndexes.indexGreaterThanIndex(currentIndex)

        # FIXME: return a list if widget allows multi-selection.
        self.interface.selected = self.interface.selected[0]

        if self.interface.on_select:
            self.interface.on_select(self.interface)


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
        self.tree.columnAutoresizingStyle = NSTableViewUniformColumnAutoresizingStyle

        # TODO: Make turning this on an option.
        self.tree.allowsMultipleSelection = False

        # Create columns for the tree
        self.columns = []
        for i, heading in enumerate(self.interface.headings):
            column = NSTableColumn.alloc().initWithIdentifier(to_accessor(heading))
            self.tree.addTableColumn(column)
            self.columns.append(column)

            cell = TogaIconCell.alloc().init()
            column.dataCell = cell

            column.headerCell.stringValue = heading

        # Put the tree arrows in the first column.
        self.tree.outlineTableColumn = self.columns[0]

        self.tree.delegate = self.tree
        self.tree.dataSource = self.tree

        # Embed the tree view in the scroll view
        self.native.documentView = self.tree

        # Add the layout constraints
        self.add_constraints()

    # def data_changed(self, node=None):
    #     if node:
    #         if node._expanded:
    #             self.tree.expandItem(node._impl)
    #         else:
    #             self.tree.collapseItem(node._impl)

    def change_source(self, source):
        self.tree.reloadData()

    def insert(self, parent, index, item):
        self.tree.reloadData()

    def change(self, item):
        self.tree.reloadData()

    def remove(self, item):
        self.tree.reloadData()

    def clear(self):
        self.tree.reloadData()

    def set_on_select(self, handler):
        pass
