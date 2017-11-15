from .base import Widget


class Table(Widget):
    def create(self):
        self._action('create Table')

    def change_source(self, source):
        self._action('change source', source=source)

    def insert(self, index, row):
        self._action('insert row', index=index, row=row)

    def change(self, row):
        self._action('change row', row=row)

    def remove(self, row):
        self._action('remove row', row=row)

    def clear(self):
        self._action('clear')

    def set_on_select(self, handler):
        self._set_value('on_select', handler)
