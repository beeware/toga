from .base import Source, Node, Datum, to_accessor


class BaseDictSource(Source):
    def __init__(self, accessors):
        super().__init__()
        self._accessors = accessors

    def append(self, parent, *values, **data):

        return self.insert(parent, len(parent) if parent else len(self), *values, **data)


class DictSource(BaseDictSource):
    def __init__(self, accessors, data):
        super().__init__(accessors)
        self._roots = self.create_nodes(data)

    def __len__(self):
        return len(self._roots)

    def __getitem__(self, index):
        return self._data[index]

    def create_node(self, datum, children=None):
        if isinstance(datum, dict):
            node = Node(**datum)
        elif isinstance(datum, (list, tuple)):
            node = Node(**{
                accessor: value
                for accessor, value in zip(self._accessors, datum)
            })
        else:
            node = datum

        if children is not None:
            node._children = []
            for child_node in self.create_nodes(children):
                node._children.append(child_node)
                child_node.parent = node

        return node

    def create_nodes(self, data):
        if isinstance(data, dict):
            return [
                self.create_node(datum, children)
                for datum, children in data.items()
            ]
        else:
            return [
                self.create_node(datum)
                for datum in data
            ]

    def roots(self):
        return self._roots

    def root(self, index):
        return self._roots[index]

    def insert(self, parent, index, *values, **datum):
        node = self.create_node(dict(
            datum,
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
        node.parent = parent
        self._notify('refresh')
        return node

    def remove(self, node):
        result = node.parent._children.remove(node)
        self._notify('refresh')
        return result