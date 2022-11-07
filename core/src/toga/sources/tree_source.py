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
        self._source._notify("change", item=node)

    def insert(self, index, *values, **named):
        self._source.insert(self, index, *values, **named)

    def prepend(self, *values, **named):
        self._source.prepend(self, *values, **named)

    def append(self, *values, **named):
        self._source.append(self, *values, **named)

    def remove(self, node):
        self._source.remove(self, node)


class TreeSource(Source):
    def __init__(self, data, accessors):
        super().__init__()
        self._accessors = accessors
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
        else:
            node = Node(**dict(zip(self._accessors, data)))

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
                self._create_node(value, children)
                for value, children in sorted(data.items())
            ]
        else:
            return [self._create_node(value) for value in data]

    ######################################################################
    # Utility methods to make TreeSources more dict-like
    ######################################################################

    def __setitem__(self, index, value):
        root = self._create_node(value)
        self._roots[index] = root
        self._notify("change", item=root)

    def __iter__(self):
        return iter(self._roots)

    def clear(self):
        self._roots = []
        self._notify("clear")

    def insert(self, parent, index, *values, **named):
        node = self._create_node(dict(zip(self._accessors, values), **named))

        if parent is None:
            self._roots.insert(index, node)
        else:
            if parent._children is None:
                parent._children = []
            parent._children.insert(index, node)

        node._parent = parent
        self._notify("insert", parent=parent, index=index, item=node)
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

        self._notify("remove", parent=parent, index=i, item=node)
        return node

    def index(self, node):
        if node._parent:
            return node._parent._children.index(node)
        else:
            return self._roots.index(node)
