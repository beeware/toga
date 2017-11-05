from .base import Widget


class Table(Widget):
    def create(self):
        self._action('create Table')

    def refresh(self):
        self._action('refresh')

    def set_on_select(self, handler):
        self._set_value('on_select', handler)
