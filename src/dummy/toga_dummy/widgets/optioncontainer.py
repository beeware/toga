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
        self._set_value('option_{}_enabled'.format(index), value=enabled)

    def is_option_enabled(self, index):
        return self._get_value('option_{}_enabled'.format(index))

    def set_option_label(self, index, value):
        self._set_value('option_{}_label'.format(index), value=value)

    def get_option_label(self, index):
        return self._get_value('option_{}_label'.format(index))

    def set_current_tab_index(self, current_tab_index):
        self._set_value('current_tab_index', current_tab_index)

    def get_current_tab_index(self):
        return self._get_value('current_tab_index', 0)
