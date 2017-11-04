from .base import Widget


class SplitContainer(Widget):
    def create(self):
        self._action('create SplitContainer')

    def add_content(self, position, widget):
        self._action('add content', position=position, widget=widget)

    def apply_sub_layout(self):
        self._action('apply sub layout')

    def set_direction(self, value):
        self._set_value('direction', value)
