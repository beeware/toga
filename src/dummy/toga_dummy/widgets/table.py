from .base import Widget


class Table(Widget):
    def create(self):
        self._action('create Table')

    def data_changed(self):
        self._action('data changed')

    def set_on_select(self, handler):
        self._set_value('on_select', handler)
