from .base import Widget


class Column(Widget):
    def create(self):
        self._action('create Column')

    def set_title(self, value):
        self._set_value('title', value)

    def set_editable(self, value):
        self._set_value('editable', value)

    def set_on_toggle(self, handler):
        self._set_value('on_toggle', handler)

    def set_on_change(self, handler):
        self._set_value('on_change', handler)
