from .base import Widget


class DetailedList(Widget):
    def create(self):
        self._action('create DetailedList')

    def change_source(self, source):
        self._action('change source', source=source)

    def insert(self, index, item):
        self._action('insert', index=index, item=item)

    def change(self, item):
        self._action('change', item=item)

    def remove(self, index, item):
        self._action('remove', index=index, item=item)

    def clear(self):
        self._action('clear')

    def get_selection(self):
        self._action('get selection')
        return None

    def set_on_refresh(self, handler):
        self._set_value('on_refresh', handler)

    def after_on_refresh(self, widget, result):
        self._action('after on refresh', widget=widget, result=result)

    def set_on_delete(self, handler):
        self._set_value('on_delete', handler)

    def set_on_select(self, handler):
        self._set_value('on_select', handler)

    def scroll_to_row(self, row):
        self._set_value('scroll to', row)
