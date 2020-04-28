from .base import Widget


class OptionContainer(Widget):
    def create(self):
        self._action('create OptionContainer')

    def add_content(self, label, widget):
        self._action('add content', label=label, widget=widget)

    def remove_content(self, index):
        self._action('remove content', index=index)

    def set_on_select(self, handler):
        self._set_value('on_select', handler)

    def set_option_enabled(self, index, enabled):
        self._action('set option enabled', index=index)

    def is_option_enabled(self, index):
        self._action('is enabled', index=index)

    def set_option_label(self, index, value):
        self._action('set option label', index=index, value=value)

    def get_option_label(self, index):
        self._action('get label', index=index)
