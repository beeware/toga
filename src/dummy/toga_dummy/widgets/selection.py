from .base import Widget


class Selection(Widget):
    def create(self):
        self._action('create Selection')

    def change_source(self, source):
        self._action('change source', source=source)

    def insert(self, index, item):
        # Listener method for ListSource
        self._action('insert', index=index, item=item)

    def remove(self, item):
        # Listener method for ListSource
        self._action('remove', item=item)

    def clear(self):
        # Listener method for ListSource
        self._action('clear')

    def select_item(self, item):
        self._action('select item', item=item)

    def get_selected_item(self):
        return self._get_value('selected_item')

    def set_on_select(self, handler):
        self._set_value('on_select', handler)

    def rehint(self):
        self._action('rehint Selection')
