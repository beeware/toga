from .base import Widget


class Selection(Widget):
    def create(self):
        self._action("create Selection")
        self._items = []

    def remove_all_items(self):
        self._action("remove all items")
        self._items = []

    def add_item(self, item):
        self._action("add item", item=item)
        self._items.append(item)

    def select_item(self, item):
        self._action("select item", item=item)
        self._set_value("selected_item", item)

    def get_selected_item(self):
        try:
            return self._get_value("selected_item")
        except AttributeError:
            return self._items[0]

    def set_on_select(self, handler):
        self._set_value("on_select", handler)
