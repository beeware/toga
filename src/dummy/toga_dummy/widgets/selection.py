from .base import Widget


class Selection(Widget):
    def create(self):
        self._action('create Selection')

    def change_source(self, source):
        self._action('change source', source=source)

    def select_item(self, item):
        self._action('select item', item=item)

    def get_selected_item(self):
        return self._get_value('selected_item')

    def set_on_select(self, handler):
        self._set_value('on_select', handler)

    def rehint(self):
        self._action('rehint Selection')
