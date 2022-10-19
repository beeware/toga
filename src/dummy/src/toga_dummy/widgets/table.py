from .base import Widget


class Table(Widget):
    def create(self):
        self._action('create Table')

    def change_source(self, source):
        self._action('change source', source=source)

    def insert(self, index, item):
        self._action('insert row', index=index, item=item)

    def change(self, item):
        self._action('change row', item=item)

    def remove(self, index, item):
        self._action('remove row', item=item, index=index)

    def clear(self):
        self._action('clear')

    def get_selection(self):
        self._action('get selection')
        return None

    def set_on_select(self, handler):
        self._set_value('on_select', handler)

    def set_on_double_click(self, handler):
        self._set_value('on_double_click', handler)

    def scroll_to_row(self, row):
        self._set_value('scroll to', row)

    def add_column(self, heading, accessor):
        self._action('add column', heading=heading, accessor=accessor)

    def remove_column(self, accessor):
        self._action('remove column', accessor=accessor)
