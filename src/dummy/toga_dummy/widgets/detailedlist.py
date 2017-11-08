from .base import Widget


class DetailedList(Widget):
    def create(self):
        self._action('create DetailedList')

    def set_refresh(self, handler):
        self._set_value('on_refresh', handler)