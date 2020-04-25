from .base import Widget


class TimePicker(Widget):
    def create(self):
        self._action('create TimePicker')

    def get_value(self):
        return self._get_value('value')

    def set_value(self, value):
        return self._set_value('value', value)

    def set_min_time(self, value):
        return self._set_value('min time', value)

    def set_max_time(self, value):
        return self._set_value('max time', value)

    def rehint(self):
        self._action('rehint TimePicker')

    def set_on_change(self, handler):
        self._set_value('on_change', handler)
