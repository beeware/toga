from rubicon.objc import *

from ..libs import *
from ..utils import process_callback
from .base import Widget
from .utils import TogaIconCell, TogaNodeData


class TogaTree(NSOutlineView):
    # OutlineViewDataSource methods
    @objc_method
    def outlineView_child_ofItem_(self, tree, child: int, item):
        if item is None:
            node = self.interface.data.root(child)
        else:
            parent = self._impl.node[item]
            node = parent.children[child]

        if node._impl is None:
            self._impl.insert_node(node)

        return node._impl

    @objc_method
    def outlineView_isItemExpandable_(self, tree, item) -> bool:
        return self._impl.node[item].children is not None

    @objc_method
    def outlineView_numberOfChildrenOfItem_(self, tree, item) -> int:
        if item is None:
            if self.interface.data:
                return len(self.interface.data.roots())
            else:
                return 0
        else:
            return len(self._impl.node[item].children)

    @objc_method
    def outlineView_objectValueForTableColumn_byItem_(self, tree, column, item):
        if column.identifier == '0':
            data = self._impl.node[item]._impl
        else:
            data = str(self._impl.node[item].data[int(column.identifier)])
        return data

    # OutlineViewDelegate methods
    @objc_method
    def outlineViewSelectionDidChange_(self, notification) -> None:
        self.interface.selected = []
        currentIndex = self.selectedRowIndexes.firstIndex
        for i in range(self.selectedRowIndexes.count):
            self.interface.selected.append(self._impl.node[self.itemAtRow(currentIndex)])
            currentIndex = self.selectedRowIndexes.indexGreaterThanIndex(currentIndex)

        # FIXME: return a list if widget allows multi-selection.
        self.interface.selected = self.interface.selected[0]

        if self.interface.on_select:
            process_callback(self.interface.on_select(self.interface))


class Tree(Widget):
    def create(self):
        # Create a tree view, and put it in a scroll view.
        # The scroll view is the _impl, because it's the outer container.
        self.native = NSScrollView.alloc().init()
        self.native.hasVerticalScroller = True
        self.native.hasHorizontalScroller = False
        self.native.autohidesScrollers = False
        self.native.borderType = NSBezelBorder

        # Disable all autolayout functionality on the outer widget
        self.native.translatesAutoresizingMaskIntoConstraints = False
        self.native.autoresizesSubviews = True

        # Set up storage for node implementations
        self.node = {}

        # Create the Tree widget
        self.tree = TogaTree.alloc().init()
        self.tree.interface = self.interface
        self.tree._impl = self
        self.tree.columnAutoresizingStyle = NSTableViewUniformColumnAutoresizingStyle

        # Use autolayout for the inner widget.
        self.tree.setTranslatesAutoresizingMaskIntoConstraints_(True)

        # FIXME: Make turning this on an option.
        # self.tree.setAllowsMultipleSelection_(True)

        # Create columns for the tree
        self.columns = []
        for i, heading in enumerate(self.interface.headings):
            column = NSTableColumn.alloc().initWithIdentifier('%d' % i)
            self.tree.addTableColumn(column)
            self.columns.append(column)

            # FIXME - Modify TogaIconCell to preserve the column ID;
            # then allow all columns to have icons and/or text.
            if i == 0:
                cell = TogaIconCell.alloc().init()
                column.dataCell = cell
            else:
                cell = column.dataCell

            cell.editable = False
            cell.selectable = False
            column.headerCell.stringValue = heading

        # Put the tree arrows in the first column.
        self.tree.outlineTableColumn = self.columns[0]

        self.tree.delegate = self.tree
        self.tree.dataSource = self.tree

        # Embed the tree view in the scroll view
        self.native.documentView = self.tree

        # Add the layout constraints
        self.add_constraints()

    def insert_node(self, node):
        node._impl = TogaNodeData.alloc().init()
        node._impl.node = node

        self.node[node._impl] = node

    def remove_node(self, node):
        del self.node[node._impl]

    def refresh_node(self, node):
        if node._expanded:
            self.tree.expandItem(node._impl)
        else:
            self.tree.collapseItem(node._impl)

    def refresh(self):
        self.tree.reloadData()
