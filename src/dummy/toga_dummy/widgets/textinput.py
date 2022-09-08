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
        self._set_value('value', value)

    def set_font(self, font):
        self._set_value('font', font=font)

    def set_alignment(self, value):
        self._set_value('alignment', value)

    def rehint(self):
        self._action('rehint TextInput')

    def set_on_change(self, handler):
        self._set_value('on_change', handler)

    def set_on_gain_focus(self, handler):
        self._set_value('on_gain_focus', handler)

    def set_on_lose_focus(self, handler):
        self._set_value('on_lose_focus', handler)

    def set_error(self, error_message):
        self._set_value('error', error_message)
        self._set_value('valid', False)

    def clear_error(self):
        self._action('clear_error')
        self._set_value('valid', True)

    def is_valid(self):
        return self._get_value('valid')
