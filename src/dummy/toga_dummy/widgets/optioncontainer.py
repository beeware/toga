from .base import Widget


class OptionContainer(Widget):
    def create(self):
        self._action('create OptionContainer')

    def add_content(self, label, widget):
        self._action('add content', label=label, widget=widget)

    def set_on_select(self, handler):
        self._set_value('on_select', handler)
