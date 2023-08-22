from ..utils import not_required
from .base import Widget


@not_required
class Option:
    def __init__(self, text, widget, enabled):
        self.text = text
        self.widget = widget
        self.enabled = enabled


@not_required  # Testbed coverage is complete for this widget.
class OptionContainer(Widget):
    def create(self):
        self._action("create OptionContainer")
        self._items = []

    def add_content(self, index, text, widget):
        self._action("add content", index=index, text=text, widget=widget)
        self._items.insert(index, Option(text, widget, True))

        # if this is the first item of content, set it as the selected item.
        if len(self._items) == 1:
            self.set_current_tab_index(0)

    def remove_content(self, index):
        self._action("remove content", index=index)
        del self._items[index]

    def set_option_enabled(self, index, enabled):
        self._action("set option enabled", index=index, value=enabled)
        self._items[index].enabled = enabled

    def is_option_enabled(self, index):
        return self._items[index].enabled

    def set_option_text(self, index, value):
        self._action("set option text", index=index, value=value)
        self._items[index].text = value

    def get_option_text(self, index):
        return self._items[index].text

    def set_current_tab_index(self, current_tab_index):
        self._set_value("current_tab_index", current_tab_index)
        self.interface.on_select(None)

    def get_current_tab_index(self):
        return self._get_value("current_tab_index", None)

    def simulate_select_tab(self, index):
        self.set_current_tab_index(index)
