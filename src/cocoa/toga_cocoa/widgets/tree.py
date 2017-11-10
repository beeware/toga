from rubicon.objc import *

from toga.sources import to_accessor

from ..libs import *
from .base import Widget
from .utils import TogaIconCell, TogaData


class TogaTree(NSOutlineView):
    # OutlineViewDataSource methods
    @objc_method
    def outlineView_child_ofItem_(self, tree, child: int, item):
        if item is None:
            node = self.interface.data.root(child)
        else:
            node = item.attrs['node']._children[child]

        try:
            node_impl = node._impl
        except AttributeError:
            node_impl = TogaData.alloc().init()
            node_impl.attrs = {
                'node': node,
                'values': {
                    attr: TogaData.alloc().init()
                    for attr in self.interface._accessors
                }
            }
            node._impl = node_impl

        return node_impl

    @objc_method
    def outlineView_isItemExpandable_(self, tree, item) -> bool:
        return item.attrs['node']._children is not None

    @objc_method
    def outlineView_numberOfChildrenOfItem_(self, tree, item) -> int:
        if item is None:
            if self.interface.data:
                return len(self.interface.data.roots())
            else:
                return 0
        else:
            return len(item.attrs['node']._children)

    @objc_method
    def outlineView_objectValueForTableColumn_byItem_(self, tree, column, item):
        node = item.attrs['node']
        value = getattr(node, column.identifier)

        datum = item.attrs['values'][column.identifier]
        # If the value has an icon attribute, get the _impl.
        # Icons are deferred resources, so we provide the factory.
        try:
            icon = value.icon._impl(self.interface.factory)
        except AttributeError:
            icon = None

        datum.attrs = {
            'label': str(value),
            'icon': icon,
        }

        return datum

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

        # Disable all autolayout functionality on the outer widget
        self.native.translatesAutoresizingMaskIntoConstraints = False
        self.native.autoresizesSubviews = True

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
            column = NSTableColumn.alloc().initWithIdentifier(to_accessor(heading))
            self.tree.addTableColumn(column)
            self.columns.append(column)

            cell = TogaIconCell.alloc().init()
            column.dataCell = cell

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

    # def insert_node(self, node):
    #     node._impl = TogaData.alloc().init()
    #     node._impl.data = node

    #     self.node[node._impl] = node

    # def remove_node(self, node):
    #     del self.node[node._impl]

    def refresh_node(self, node):
        if node._expanded:
            self.tree.expandItem(node._impl)
        else:
            self.tree.collapseItem(node._impl)

    def refresh(self):
        self.tree.reloadData()

    def set_on_select(self, handler):
        pass
