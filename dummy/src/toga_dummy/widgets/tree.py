from .base import Widget


def node_for_path(data, path):
    "Convert a path tuple into a specific node"
    if path is None:
        return None
    result = data
    for index in path:
        result = result[index]
    return result


class Tree(Widget):
    def create(self):
        self._action("create Tree")

    def change_source(self, source):
        self._action("change source", source=source)
        self.interface.on_select()

    def insert(self, index, item, parent=None):
        self._action("insert node", parent=parent, index=index, item=item)

    def change(self, item):
        self._action("change node", item=item)

    def remove(self, index, item, parent=None):
        self._action("remove node", parent=parent, index=index, item=item)

    def clear(self):
        self._action("clear")

    def get_selection(self):
        if self.interface.multiple_select:
            return [
                node_for_path(self.interface.data, path)
                for path in self._get_value("selection", [])
            ]
        else:
            return node_for_path(
                self.interface.data, self._get_value("selection", None)
            )

    def expand_node(self, node):
        self._action("expand node", node=node)

    def expand_all(self):
        self._action("expand all")

    def collapse_node(self, node):
        self._action("collapse node", node=node)

    def collapse_all(self):
        self._action("collapse all")

    def insert_column(self, index, column):
        self._action("insert column", index=index, column=column)

    def remove_column(self, index):
        self._action("remove column", index=index)

    def simulate_selection(self, path):
        self._set_value("selection", path)
        self.interface.on_select()

    def simulate_activate(self, path):
        self.interface.on_activate(node=node_for_path(self.interface.data, path))
