from rubicon.objc import *

from toga.interface import Tree as TreeInterface

from ..libs import *
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
        cell.setImage_(self.interface.tree[id(item)]._icon['obj'])
        cell.setLeaf_(True)

    # OutlineViewDelegate methods
    @objc_method
    def outlineViewSelectionDidChange_(self, notification) -> None:
        print ("tree selection changed")


class Tree(TreeInterface, WidgetMixin):
    def __init__(self, headings, data=None, id=None, style=None):
        super().__init__(headings, data, id, style)

        self._tree = None
        self._columns = None

        self._create()

    def create(self):
        # Create a tree view, and put it in a scroll view.
        # The scroll view is the _impl, because it's the outer container.
        self._impl = NSScrollView.alloc().init()
        self._impl.setHasVerticalScroller_(True)
        self._impl.setHasHorizontalScroller_(True)
        self._impl.setAutohidesScrollers_(False)
        self._impl.setBorderType_(NSBezelBorder)

        # Disable all autolayout functionality on the outer widget
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)

        self._tree = TogaTree.alloc().init()
        self._tree.interface = self
        self._tree.setColumnAutoresizingStyle_(NSTableViewUniformColumnAutoresizingStyle)
        # Use autolayout for the inner widget.
        self._tree.setTranslatesAutoresizingMaskIntoConstraints_(True)

        # Create columns for the tree
        self._columns = [
            NSTableColumn.alloc().initWithIdentifier_('%d' % i)
            for i, heading in enumerate(self.headings)
        ]

        custom_cell = NSBrowserCell.alloc().init()

        for heading, column in zip(self.headings, self._columns):
            self._tree.addTableColumn_(column)
            cell = column.dataCell
            cell.setEditable_(False)
            cell.setSelectable_(False)
            column.headerCell.stringValue = heading
            column.setDataCell_(custom_cell)

        # Put the tree arrows in the first column.
        self._tree.setOutlineTableColumn_(self._columns[0])

        self._tree.setDelegate_(self._tree)
        self._tree.setDataSource_(self._tree)

        # Embed the tree view in the scroll view
        self._impl.setDocumentView_(self._tree)

        # Add the layout constraints
        self._add_constraints()

    def _insert(self, node_abs):
        node = NSObject.alloc().init()
        node_abs._impl = node

        return id(node)

    def _set_icon(self, node):
        size = NSMakeSize(8,8)

        image = NSImage.alloc().initWithContentsOfFile_(node._icon['url'])
        image.setSize_(size)

        node._icon['obj'] = image

    def _set_collapse(self, node, status):
        if status:
            self._tree.collapseItem(node._impl)
        else:
            self._tree.expandItem(node._impl)

    def rehint(self):
        self._tree.reloadData()
