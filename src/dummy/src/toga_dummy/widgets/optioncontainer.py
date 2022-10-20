from .base import Widget
from ..utils import not_required


@not_required
class Option:
    def __init__(self, text, widget, enabled):
        self.text = text
        self.widget = widget
        self.enabled = enabled


class OptionContainer(Widget):
    def create(self):
        self._action('create OptionContainer')
        self._items = []
        self._current_index = 0

    def add_content(self, index, text, widget):
        self._action('add content', index=index, text=text, widget=widget)
        self._items.insert(index, Option(text, widget, True))

    def remove_content(self, index):
        if index == self._current_index:
            # Don't allow removal of a selected tab
            raise self.interface.OptionException(
                'Currently selected option cannot be removed'
            )
        self._action('remove content', index=index)
        del self._items[index]

    def set_on_select(self, handler):
        self._set_value('on_select', handler)

    def set_option_enabled(self, index, enabled):
        self._set_value('option_{}_enabled'.format(index), value=enabled)
        self._items[index].enabled = enabled

    def is_option_enabled(self, index):
        self._get_value('option_{}_enabled'.format(index))
        return self._items[index].enabled

    def set_option_text(self, index, value):
        self._set_value('option_{}_text'.format(index), value=value)
        self._items[index].text = value

    def get_option_text(self, index):
        self._get_value('option_{}_text'.format(index))
        return self._items[index].text

    def set_current_tab_index(self, current_tab_index):
        self._set_value('current_tab_index', current_tab_index)
        self._current_index = current_tab_index

    def get_current_tab_index(self):
        self._get_value('current_tab_index', 0)
        return self._current_index
