from .base import Widget


class Button(Widget):
    def create(self):
        self._action('create Button')

    def set_text(self, text):
        self._set_value('text', self.interface.text)

    def set_on_press(self, handler):
        self._set_value('on_press', handler)

    def rehint(self):
        self._action('rehint Button')
