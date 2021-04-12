from .base import Source
from .list_source import Row


class Node(Row):
    def __init__(self, **data):
        super().__init__(**data)
        self._children = None
        self._parent = None

    ######################################################################
    # Methods required by the TreeSource interface
    ######################################################################

    def __getitem__(self, index):
        return self._children[index]

    def __len__(self):
        if self.can_have_children():
            return len(self._children)
        else:
            return 0

    def can_have_children(self):
        return self._children is not None

    ######################################################################
    # Utility methods to make TreeSource more dict-like
    ######################################################################

    def __iter__(self):
        return iter(self._children or [])

    def __setitem__(self, index, value):
        node = self._source._create_node(value)
        self._children[index] = node
        self._source._notify('change', item=node)

    def insert(self, index, *values, **named):
        self._source.insert(self, index, *values, **named)

    def prepend(self, *values, **named):
        self._source.prepend(self, *values, **named)

    def append(self, *values, **named):
        self._source.append(self, *values, **named)

    def remove(self, node):
        self._source.remove(self, node)


class TreeSource(Source):
    """A data source to store a tree of data. The ``TreeSource`` acts like Python list
    where entries are ``Node``s. Data values of each node are accessible as attributes of
     the node and the attribute names are defined by ``accessor``s.

    :param data: The data in the tree. Each entry in the list should have the same number
        of entries as there are accessors.
    :param accessors: A list of attribute names for accessing the value in each column of
        the row.

    Examples:

        Data can is provided as a dictionary where the keys represent nodes and the values
        are lists of their child nodes. Nodes can be provided  as iterables with accessors
        provided separately:

        >>> data = {
        >>>    ('father', 38): [('child 1', 17), ('child 1', 15)],
        >>>    ('mother', 42): [('child 1', 17)],
        >>> }
        >>> accessors = ['name', 'age']
        >>> source = TreeSource(data, accessors)

        Nodes in the source can be accessed by index:

        >>> node = source[0]
        >>> print(node)
        <Node(name='father', age=38)>

        Data values can be accessed as row attributes:

        >>> print(node.name)
        'father'

        Children can be accessed by iterating over a parent:

        >>> for child in node:
        >>>     print(child)
        <Node(name='child 1', age=17)>
        <Node(name='child 2', age=15)>
    """

    def __init__(self, data, accessors):
        super().__init__()
        self.accessors = list(accessors)
        self._roots = self._create_nodes(data)

    ######################################################################
    # Methods required by the TreeSource interface
    ######################################################################

    def __len__(self):
        return len(self._roots)

    def __getitem__(self, index):
        return self._roots[index]

    def can_have_children(self):
        return True

    ######################################################################
    # Factory methods for new nodes
    ######################################################################

    def _create_node(self, data, children=None):

        if isinstance(data, dict):
            node = Node(**data)
        elif hasattr(data, '__iter__') and not isinstance(data, str):
            node = Node(**dict(zip(self.accessors, data)))
        else:
            raise ValueError('Invalid data format')

        node._source = self

        if children is not None:
            node._children = []
            for child_node in self._create_nodes(children):
                node._children.append(child_node)
                child_node._parent = node
                child_node._source = self

        return node

    def _create_nodes(self, data):
        if isinstance(data, dict):
            return [
                self._create_node(value, children) for value, children in data.items()
            ]
        else:
            return [
                self._create_node(value)
                for value in data
            ]

    ######################################################################
    # Utility methods to make TreeSources more dict-like
    ######################################################################

    def __setitem__(self, index, value):
        root = self._create_node(value)
        self._roots[index] = root
        self._notify('change', item=root)

    def __iter__(self):
        return iter(self._roots)

    def clear(self):
        self._roots = []
        self._notify('clear')

    def insert(self, parent, index, *values, **named):
        node = self._create_node(dict(zip(self.accessors, values), **named))

        if parent is None:
            self._roots.insert(index, node)
        else:
            if parent._children is None:
                parent._children = []
            parent._children.insert(index, node)

        node._parent = parent
        self._notify('insert', parent=parent, index=index, item=node)
        return node

    def prepend(self, parent, *values, **named):
        return self.insert(parent, 0, *values, **named)

    def append(self, parent, *values, **named):
        return self.insert(parent, len(parent or self), *values, **named)

    def remove(self, node):
        i = self.index(node)
        parent = node._parent
        if node._parent is None:
            del self._roots[i]
        else:
            del node._parent._children[i]
            # node is not in parent's children so it shouldn't keep a link to parent
            del node._parent

        self._notify('remove', parent=parent, index=i, item=node)
        return node

    def index(self, node):
        if node._parent:
            return node._parent._children.index(node)
        else:
            return self._roots.index(node)
