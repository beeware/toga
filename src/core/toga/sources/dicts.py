from .base import Source, Node, Value


class DictSource(Source):
    def __init__(self, data, accessors):
        super().__init__()
        self._accessors = accessors
        self._roots = self._create_nodes(data)

    ######################################################################
    # Methods required by the ListSource interface
    ######################################################################

    def __len__(self):
        return len(self._roots)

    def __getitem__(self, index):
        return self._roots[index]

    ######################################################################
    # Factory methods for new nodes
    ######################################################################

    def _create_node(self, data, children=None):
        if isinstance(data, dict):
            node = Node(self, **data)
        else:
            node = Node(self, **{
                accessor: value
                for accessor, value in zip(self._accessors, data)
            })

        if children is not None:
            node._children = []
            for child_node in self._create_nodes(children):
                node._children.append(child_node)
                child_node._parent = node

        return node

    def _create_nodes(self, data):
        if isinstance(data, dict):
            return [
                self._create_node(value, children)
                for value, children in sorted(data.items())
            ]
        else:
            return [
                self._create_node(value)
                for value in data
            ]

    ######################################################################
    # Utility methods to make ListSources more list-like
    ######################################################################

    def __setitem__(self, index, value):
        self._roots[index] = self._create_node(value)
        self._notify('data_changed')

    def __iter__(self):
        return iter(self._roots)

    def insert(self, parent, index, *values, **named):
        node = self._create_node(dict(
            named,
            **{
                accessor: value
                for accessor, value in zip(self._accessors, values)
            }
        ))
        if parent is None:
            self._roots.insert(index, node)
        else:
            if parent._children is None:
                parent._children = []
            parent._children.insert(index, node)
        node._parent = parent
        self._notify('data_changed')
        return node

    def prepend(self, parent, *value, **named):
        return self.insert(parent, 0, *value, **named)

    def append(self, parent, *value, **named):
        return self.insert(parent, len(self) if parent is None else len(parent), *value, **named)

    def remove(self, node):
        if node._parent is None:
            result = self._roots.remove(node)
        else:
            result = node._parent._children.remove(node)
        self._notify('data_changed')
        return result
