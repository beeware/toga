from .base import Widget


class DetailedList(Widget):
    def create(self):
        self._action('create DetailedList')

    def refresh(self):
        self._action('refresh DetailedList')

    def set_on_refresh(self, handler):
        self._set_value('on_refresh', handler)

    def set_on_delete(self, handler):
        self._set_value('on_delete', handler)

    def set_on_select(self, handler):
        self._set_value('on_select', handler)
