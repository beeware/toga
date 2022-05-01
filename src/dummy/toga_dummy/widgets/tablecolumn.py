from .base import Widget


class Column(Widget):
    def create(self):
        self._action('create Column')

    def set_title(self, value):
        self._set_value('title', value)

    def set_editable(self, value):
        self._set_value('editable', value)
