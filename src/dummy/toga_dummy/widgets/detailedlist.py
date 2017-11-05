from .base import Widget


class DetailedList(Widget):
    def create(self):
        self._action('create DetailedList')

    def set_data(self, data):
        self._set_value('data', data)

    def add(self, item):
        self._action('add item', item=item)
