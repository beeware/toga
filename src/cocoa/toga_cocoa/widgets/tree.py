from rubicon.objc import *
from ..libs import *
from .base import Widget


class TreeNode(object):
    def __init__(self, *data):
        self.native = NSObject.alloc().init()
        self._tree = None
        self.data = data
        self.children = []


class TogaTree(NSOutlineView):
    # OutlineViewDataSource methods
    @objc_method
    def outlineView_child_ofItem_(self, tree, child: int, item):
        if item is None:
            key = None
        else:
            key = id(item)

        node_id = self._impl.data[key]['children'][child]
        node = self._impl.data[node_id]['node']
        return node

    @objc_method
    def outlineView_isItemExpandable_(self, tree, item) -> bool:
        if item is None:
            key = None
        else:
            key = id(item)

        return self._impl.data[key]['children'] is not None

    @objc_method
    def outlineView_numberOfChildrenOfItem_(self, tree, item) -> int:
        if item is None:
            key = None
        else:
            key = id(item)

        try:
            return len(self._impl.data[key]['children'])
        except TypeError:
            return 0

    @objc_method
    def outlineView_objectValueForTableColumn_byItem_(self, tree, column, item):
        column_index = int(column.identifier)
        return self._impl.data[id(item)]['data'][column_index]

    # OutlineViewDelegate methods
    @objc_method
    def outlineViewSelectionDidChange_(self, notification) -> None:
        print("tree selection changed")


class Tree(Widget):
    def create(self):
        self.tree = None
        self.columns = None

        self.data = {
            None: {
                'children': []
            }
        }

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

        self.tree = TogaTree.alloc().init()
        self.tree.interface = self.interface
        self.tree._impl = self
        self.tree.columnAutoresizingStyle = NSTableViewUniformColumnAutoresizingStyle

        # Use autolayout for the inner widget.
        self.tree.translatesAutoresizingMaskIntoConstraints = True

        # Create columns for the tree
        self.columns = [
            NSTableColumn.alloc().initWithIdentifier_('%d' % i)
            for i, heading in enumerate(self.interface.headings)
            ]

        for heading, column in zip(self.interface.headings, self.columns):
            self.tree.addTableColumn(column)
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

    def insert(self, parent, index, *data):
        if len(data) != len(self.interface.headings):
            raise Exception('Data size does not match number of headings')

        node = NSObject.alloc().init()

        parent_node = self.data[parent]
        if parent_node['children'] is None:
            parent_node['children'] = []
        if index is None:
            parent_node['children'].append(id(node))
        else:
            parent_node['children'].insert(index, id(node))

        self.data[id(node)] = {
            'node': node,
            'data': data,
            'children': None,
        }

        self.tree.reloadData()
        return id(node)
