from rubicon.objc import *

from toga.interface import Tree as TreeInterface

from ..libs import *
from ..utils import process_callback
from .base import WidgetMixin


class TogaTree(NSOutlineView):
    # OutlineViewDataSource methods
    @objc_method
    def outlineView_child_ofItem_(self, tree, child: int, item):
        key = item if item is None else id(item)

        node_id = self.interface.tree[key].children[child]
        node = self.interface.tree[node_id]._impl
        return node

    @objc_method
    def outlineView_isItemExpandable_(self, tree, item) -> bool:
        key = item if item is None else id(item)
        return self.interface.tree[key].children is not None

    @objc_method
    def outlineView_numberOfChildrenOfItem_(self, tree, item) -> int:
        key = item if item is None else id(item)

        try:
            return len(self.interface.tree[key].children)
        except TypeError:
            return 0

    @objc_method
    def outlineView_objectValueForTableColumn_byItem_(self, tree, column, item):
        return self.interface.tree[id(item)].data['text']

    @objc_method
    def outlineView_willDisplayCell_forTableColumn_item_(self, tree, cell,
                                                        column, item):
        cell.setImage_(self.interface.tree[id(item)].data['icon']['obj'])
        cell.setLeaf_(True)

    # OutlineViewDelegate methods
    @objc_method
    def outlineViewSelectionDidChange_(self, notification) -> None:
        if self.interface.on_selection:
            nodes = []
            currentIndex = self.selectedRowIndexes.firstIndex
            for i in range(self.selectedRowIndexes.count):
                nodes.append(self.interface.tree[id(self.itemAtRow(currentIndex))])
                currentIndex = self.selectedRowIndexes.indexGreaterThanIndex(currentIndex)

            process_callback(self.interface.on_selection(nodes))


class Tree(TreeInterface, WidgetMixin):
    def __init__(self, headings, data=None, id=None, style=None,
                                on_selection=None):
        super().__init__(headings, data, id, style, on_selection)

        self._tree = None
        self._columns = None

        self._create()

    def create(self):
        # Create a tree view, and put it in a scroll view.
        # The scroll view is the _impl, because it's the outer container.
        self._impl = NSScrollView.alloc().init()
        self._impl.hasVerticalScroller = True
        self._impl.hasHorizontalScroller = False
        self._impl.autohidesScrollers = False
        self._impl.borderType = NSBezelBorder

        # Disable all autolayout functionality on the outer widget
        self._impl.translatesAutoresizingMaskIntoConstraints = False
        self._impl.autoresizesSubviews = True

        # Create the Tree widget
        self._tree = TogaTree.alloc().init()
        self._tree.interface = self
        self._tree.columnAutoresizingStyle = NSTableViewUniformColumnAutoresizingStyle

        # Use autolayout for the inner widget.
        self._tree.setTranslatesAutoresizingMaskIntoConstraints_(True)
        self._tree.setAllowsMultipleSelection_(True)

        # Create columns for the tree
        self._columns = [
            NSTableColumn.alloc().initWithIdentifier('%d' % i)
            for i, heading in enumerate(self.headings)
        ]

        custom_cell = NSBrowserCell.alloc().init()

        for heading, column in zip(self.headings, self._columns):
            self._tree.addTableColumn(column)
            cell = column.dataCell
            cell.editable = False
            cell.selectable = False
            column.headerCell.stringValue = heading
            column.setDataCell_(custom_cell)

        # Put the tree arrows in the first column.
        self._tree.outlineTableColumn = self._columns[0]

        self._tree.delegate = self._tree
        self._tree.dataSource = self._tree

        # Embed the tree view in the scroll view
        self._impl.documentView = self._tree

        # Add the layout constraints
        self._add_constraints()

    def _insert(self, node_abs):
        node = NSObject.alloc().init()
        node_abs._impl = node

        return id(node)

    def _set_icon(self, node):
        size = NSMakeSize(8,8)

        image = NSImage.alloc().initWithContentsOfFile_(node.data['icon']['url'])
        image.setSize_(size)

        node.data['icon']['obj'] = image

    def _set_collapse(self, node, status):
        if status:
            self._tree.collapseItem(node._impl)
        else:
            self._tree.expandItem(node._impl)

    def rehint(self):
        self._tree.reloadData()
