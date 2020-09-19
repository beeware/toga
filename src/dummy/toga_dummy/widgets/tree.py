from .base import Widget


class Tree(Widget):
    def create(self):
        self._action('create Tree')

    def change_source(self, source):
        self._action('change source', source=source)

    def insert(self, parent, index, item):
        self._action('insert node', parent=parent, index=index, item=item)

    def change(self, item):
        self._action('change node', item=item)

    def remove(self, parent, item, index):
        self._action('remove node', parent=parent, index=index, item=item)

    def clear(self):
        self._action('clear')

    def get_selection(self):
        self._action('get selection')
        return None

    def set_on_select(self, handler):
        self._set_value('on_select', handler)

    def set_on_double_click(self, handler):
        self._set_value('on_double_click', handler)
