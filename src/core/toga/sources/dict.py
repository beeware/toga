

class DictionaryDataSource:
    def __init__(self, data, node_class):
        self._roots = self.create_nodes(data)
        self.interface = None
        self.NodeClass = node_class

    def create_nodes(self, data):
        if isinstance(data, dict):
            return [
                self.NodeClass(source=self, data=item, children=self.create_nodes(children))
                for item, children in sorted(data.items())
            ]
        else:
            return [
                self.NodeClass(source=self, data=item)
                for item in data
            ]

    def roots(self):
        return self._roots

    def root(self, index):
        return self._roots[index]

    def insert(self, parent, index, data, icon=None):
        return parent.insert(index, data=data, icon=icon)

    def remove(self, node):
        return node.parent.remove(node)