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
        self._source.notify("change", item=node)

    def insert(self, index, value):
        self._source.insert(self, index, value)

    def append(self, value):
        self._source.append(self, value)

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
        self.notify("change", item=root)

    def __iter__(self):
        return iter(self._roots)

    def clear(self):
        self._roots = []
        self.notify("clear")

    def insert(self, parent, index, value):
        node = self._create_node(value)

        if parent is None:
            self._roots.insert(index, node)
        else:
            if parent._children is None:
                parent._children = []
            parent._children.insert(index, node)

        node._parent = parent
        self.notify("insert", parent=parent, index=index, item=node)
        return node

    def append(self, parent, value):
        return self.insert(parent, len(parent or self), value)

    def remove(self, node):
        i = self.index(node)
        parent = node._parent
        if node._parent is None:
            del self._roots[i]
        else:
            del node._parent._children[i]
            # node is not in parent's children so it shouldn't keep a link to parent
            del node._parent

        self.notify("remove", parent=parent, index=i, item=node)
        return node

    def index(self, node):
        if node._parent:
            return node._parent._children.index(node)
        else:
            return self._roots.index(node)
