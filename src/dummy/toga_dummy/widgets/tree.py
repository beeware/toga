from .base import Widget


class Tree(Widget):
    def create(self):
        self._action('create Tree')

    def change_source(self, source):
        self._action('change source', source=source)

    def insert(self, parent, index, node):
        self._action('insert node', parent=parent, index=index, node=node)

    def change(self, node):
        self._action('change node', node=node)

    def remove(self, node):
        self._action('remove node', node=node)

    def clear(self):
        self._action('clear')

    def set_on_select(self, handler):
        self._set_value('on_select', handler)
