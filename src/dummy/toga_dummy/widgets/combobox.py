from .base import Widget


class ComboBox(Widget):
    def create(self):
        self._action('create ComboBox')

    def remove_all_items(self):
        self._action('remove all items')

    def add_item(self, item):
        self._action('add item', item=item)

    def get_value(self):
        return self._get_value('value')

    def set_placeholder(self, value):
        self._set_value('placeholder', value)

    def set_value(self, value):
        self._set_value('value', value)

    def set_font(self, value):
        self._set_value('font', value)

    def set_alignment(self, value):
        self._set_value('alignment', value)

    def rehint(self):
        self._action('rehint ComboBox')

    def set_on_change(self, handler):
        self._set_value('on_change', handler)
