from .base import Widget


class DatePicker(Widget):
    def create(self):
        self._action('create DatePicker')

    def get_value(self):
        return self._get_value('value')

    def set_value(self, value):
        return self._set_value('value', value)

    def rehint(self):
        self._action('rehint DatePicker')
