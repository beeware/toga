from .base import Widget


class Tree(Widget):
    def create(self):
        self._action('create Tree')

    def insert_node(self, node):
        self._action('insert node', node=node)

    def refresh_node(self, node):
        self._action('refresh node', node=node)

    def remove_node(self, node):
        self._action('remove node', node=node)

    def refresh(self):
        self._action('refresh')

    def set_on_select(self, handler):
        self._set_value('on_select', handler)
