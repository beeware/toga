from .base import Widget


class Selection(Widget):
    def create(self):
        self._action('create Selection')

    def remove_all_items(self):
        self._action('remove all items')

    def add_item(self, item):
        self._action('add item', item=item)

    def select_item(self, item):
        self._action('select item', item=item)

    def get_selected_item(self):
        return self._get_value('selected_item')

    def set_on_select(self, handler):
        self._set_value('on_select', handler)

    def rehint(self):
        self._action('rehint Selection')
