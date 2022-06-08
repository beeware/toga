from .base import Widget


class Label(Widget):
    def create(self):
        self._action('create Label')

    def set_alignment(self, value):
        self._set_value('alignment', value)

    def set_text(self, value):
        self._set_value('text', self.interface._text)

    def rehint(self):
        self._action('rehint Label')
