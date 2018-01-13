from .base import Widget


class TextInput(Widget):
    def create(self):
        self._action('create TextInput')

    def set_readonly(self, value):
        self._set_value('readonly', value)

    def set_placeholder(self, value):
        self._set_value('placeholder', value)

    def get_value(self):
        return self._get_value('value')

    def set_value(self, value):
        self._set_value('value', self.interface.value)

    def rehint(self):
        self._action('rehint TextInput')
