from .base import Widget


class NumberInput(Widget):
    def create(self):
        self._action('create NumberInput')

    def set_readonly(self, value):
        self._set_value('readonly', value)

    def set_step(self, step):
        self._set_value('step', step)

    def set_min_value(self, value):
        self._set_value('min value', value)

    def set_max_value(self, value):
        self._set_value('max value', value)

    def set_value(self, value):
        self._set_value('value', value)

    def set_font(self, font):
        self._set_value('font', font=font)

    def set_alignment(self, value):
        self._set_value('alignment', value)

    def set_on_change(self, handler):
        self._set_value('on_change', handler)
