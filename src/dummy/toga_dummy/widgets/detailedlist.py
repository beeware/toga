from .base import Widget


class DetailedList(Widget):
    def create(self):
        self._action('create DetailedList')

    def change_source(self, source):
        self._action('change source', source=source)

    def insert(self, item):
        self._action('insert', item=item)

    def change(self, item):
        self._action('change', item=item)

    def remove(self, item):
        self._action('remove', item=item)

    def clear(self):
        self._action('clear')

    def set_on_refresh(self, handler):
        self._set_value('on_refresh', handler)

    def after_on_refresh(self):
        self._action('after on refresh')

    def set_on_delete(self, handler):
        self._set_value('on_delete', handler)

    def set_on_select(self, handler):
        self._set_value('on_select', handler)
