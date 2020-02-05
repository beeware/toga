from .base import Widget


class Button(Widget):
    def create(self):
        self._action('create Button')

    def set_label(self, label):
        self._set_value('label', self.interface.label)

    def rehint(self):
        self._action('rehint Button')
