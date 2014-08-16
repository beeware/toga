from __future__ import print_function, absolute_import, division

from ..libs import *
from .base import Widget


NSObject = ObjCClass('NSObject')

class TreeNode(object):
    def __init__(self, *data):
        self._impl = NSObject.alloc().init()
        self._tree = None
        self.data = data
        self.children = []


class TreeImpl_impl(object):
    TreeImpl = ObjCSubclass('NSOutlineView', 'TreeImpl')

    # OutlineViewDataSource methods
    @TreeImpl.method('@@i@')
    def outlineView_child_ofItem_(self, tree, child, item):
        if item is None:
            key = None
        else:
            key = id(item)

        node_id = self.interface._data[key]['children'][child]
        node = self.interface._data[node_id]['node']
        return node

    @TreeImpl.method('B@@')
    def outlineView_isItemExpandable_(self, tree, item):
        if item is None:
            key = None
        else:
            key = id(item)

        return self.interface._data[key]['children'] is not None

    @TreeImpl.method('i@@')
    def outlineView_numberOfChildrenOfItem_(self, tree, item):
        if item is None:
            key = None
        else:
            key = id(item)

        try:
            return len(self.interface._data[key]['children'])
        except TypeError:
            return 0

    @TreeImpl.method('@@@@')
    def outlineView_objectValueForTableColumn_byItem_(self, tree, column, item):
        column_index = int(cfstring_to_string(column.identifier))
        return get_NSString(str(self.interface._data[id(item)]['data'][column_index]))

    # OutlineViewDelegate methods
    @TreeImpl.method('v@')
    def outlineViewSelectionDidChange_(self, notification):
        print ("tree selection changed")


TreeImpl = ObjCClass('TreeImpl')


class Tree(Widget):
    def __init__(self, headings):
        super(Tree, self).__init__()
        self.headings = headings

        self._tree = None
        self._columns = None

        self._data = {
            None: {
                'children': []
            }
        }

        self.startup()

    def startup(self):
        # Create a tree view, and put it in a scroll view.
        # The scroll view is the _impl, because it's the outer container.
        self._impl = NSScrollView.alloc().init()
        self._impl.setHasVerticalScroller_(True)
        self._impl.setHasHorizontalScroller_(True)
        self._impl.setAutohidesScrollers_(False)
        self._impl.setBorderType_(NSBezelBorder)
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)

        self._tree = TreeImpl.alloc().init()
        self._tree.interface = self
        self._tree.setColumnAutoresizingStyle_(NSTableViewUniformColumnAutoresizingStyle)

        # Create columns for the tree
        self._columns = [
            NSTableColumn.alloc().initWithIdentifier_(get_NSString('%d' % i))
            for i, heading in enumerate(self.headings)
        ]

        for heading, column in zip(self.headings, self._columns):
            self._tree.addTableColumn_(column)
            cell = column.dataCell()
            cell.setEditable_(False)
            cell.setSelectable_(False)
            column.headerCell.stringValue = get_NSString(heading)

        # Put the tree arrows in the first column.
        self._tree.setOutlineTableColumn_(self._columns[0])

        self._tree.setDelegate_(self._tree)
        self._tree.setDataSource_(self._tree)

        # Embed the tree view in the scroll view
        self._impl.setDocumentView_(self._tree)

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

        return id(node)
