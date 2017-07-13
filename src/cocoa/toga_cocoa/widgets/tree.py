from rubicon.objc import *

from toga.interface import Tree as TreeInterface

from ..libs import *
from .base import WidgetMixin


class TreeNode(object):
    def __init__(self, *data):
        self._impl = NSObject.alloc().init()
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

        node_id = self.interface._data[key]['children'][child]
        node = self.interface._data[node_id]['node']
        return node

    @objc_method
    def outlineView_isItemExpandable_(self, tree, item) -> bool:
        if item is None:
            key = None
        else:
            key = id(item)

        return self.interface._data[key]['children'] is not None

    @objc_method
    def outlineView_numberOfChildrenOfItem_(self, tree, item) -> int:
        if item is None:
            key = None
        else:
            key = id(item)

        try:
            return len(self.interface._data[key]['children'])
        except TypeError:
            return 0

    @objc_method
    def outlineView_objectValueForTableColumn_byItem_(self, tree, column, item):
        column_index = int(column.identifier)
        return self.interface._data[id(item)]['data'][column_index]

    @objc_method
    def outlineView_willDisplayCell_forTableColumn_item_(self, tree, cell,
                                                        column, item):
        cell.setImage_(self.interface._cell_icons[id(item)])
        cell.setLeaf_(True)

    # OutlineViewDelegate methods
    @objc_method
    def outlineViewSelectionDidChange_(self, notification) -> None:
        print ("tree selection changed")


class Tree(TreeInterface, WidgetMixin):
    def __init__(self, headings, id=None, style=None):
        super(Tree, self).__init__(headings, id=id, style=style)

        self._tree = None
        self._columns = None
        self._cell_icons = {}

        self._data = {
            None: {
                'children': []
            }
        }

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

    def insert(self, parent, index, *data):
        if len(data) != len(self.headings):
            raise Exception('Data size does not match number of headings')

        node = NSObject.alloc().init()

        parent_node = self._data[parent]
        if parent_node['children'] is None:
            parent_node['children'] = []
        if index is None:
            parent_node['children'].append(id(node))
        else:
            parent_node['children'].insert(index, id(node))

        self._data[id(node)] = {
            'node': node,
            'data': data,
            'children': None,
        }

        self._cell_icons[id(node)] = None

        self._tree.reloadData()
        return id(node)

    def set_icon(self, image_url, index=None):
        size = NSMakeSize(8,8)

        image = NSImage.alloc().initWithContentsOfFile_(image_url)
        image.setSize_(size)

        if index is None:
            for cell in self._cell_icons.keys():
                self._cell_icons[cell] = image
        else:
            self._cell_icons[index] = image
            
        self._tree.reloadData()
