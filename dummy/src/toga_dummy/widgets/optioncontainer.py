from .base import Widget


class Option:
    def __init__(self, text, widget, enabled, icon):
        self.text = text
        self.widget = widget
        self.enabled = enabled
        self.icon = icon


class OptionContainer(Widget):
    uses_icons = True

    def create(self):
        self._action("create OptionContainer")
        self._items = []

    def add_option(self, index, text, widget, icon):
        self._action("add option", index=index, text=text, widget=widget, icon=icon)
        self._items.insert(index, Option(text, widget, True, icon))

        # if this is the first item of content, set it as the selected item.
        if len(self._items) == 1:
            self.set_current_tab_index(0)

    def remove_option(self, index):
        self._action("remove option", index=index)
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

    def set_option_icon(self, index, icon):
        self._action("set option icon", index=index, icon=icon)
        self._items[index].icon = icon

    def get_option_icon(self, index):
        return self._items[index].icon

    def set_current_tab_index(self, current_tab_index):
        self._set_value("current_tab_index", current_tab_index)
        self.interface.on_select()

    def get_current_tab_index(self):
        return self._get_value("current_tab_index", None)

    def simulate_select_tab(self, index):
        self.set_current_tab_index(index)
