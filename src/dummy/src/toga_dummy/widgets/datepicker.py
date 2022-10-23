from .base import Widget


class DatePicker(Widget):
    def create(self):
        self._action('create DatePicker')

    def get_value(self):
        return self._get_value('value')

    def set_value(self, value):
        return self._set_value('value', value)

    def set_min_date(self, value):
        return self._set_value('min date', value)

    def set_max_date(self, value):
        return self._set_value('max date', value)

    def rehint(self):
        self._action('rehint DatePicker')

    def set_on_change(self, handler):
        self._set_value('on_change', handler)
