from .base import Widget


class Tree(Widget):
    def create(self):
        self._action('create Tree')

    def data_changed(self):
        self._action('data changed')

    def set_on_select(self, handler):
        self._set_value('on_select', handler)
