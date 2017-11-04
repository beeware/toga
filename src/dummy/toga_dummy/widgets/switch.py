from .base import Widget


class Switch(Widget):
    def create(self):
        self._action('create Switch')

    def set_label(self, label):
        self._set_value('label', label)

    def set_is_on(self, value):
        self._set_value('is_on', value)

    def get_is_on(self):
        return self._get_value('is_on')

    def rehint(self):
        self._action('rehint Switch')

    def set_on_toggle(self, handler):
        self._set_value('on_toggle', handler)
