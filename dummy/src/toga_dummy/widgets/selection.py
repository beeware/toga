from .base import Widget


class Selection(Widget):
    def create(self):
        self._action("create Selection")
        self._items = []

    def insert(self, index, item):
        self._action("insert item", index=index, item=item)
        self._items.insert(index, item)
        # If this is the first item to be inserted, it should be selected.
        if len(self._items) == 1:
            self.simulate_selection(self._items[0])

    def change(self, item):
        self._action("change item", item=item)

    def remove(self, index, item):
        self._action("remove item", index=index, item=item)
        del self._items[index]

        # If we deleted the selected item, reset the selection.
        if self._get_value("selected_item", None) == item:
            try:
                selected = self._items[0]
            except IndexError:
                selected = None
            self.simulate_selection(selected)

    def clear(self):
        self._action("clear")
        self._items = []
        self.simulate_selection(None)

    def select_item(self, index, item):
        self._action("select item", item=item)
        self.simulate_selection(item)

    def get_selected_index(self):
        try:
            return self._items.index(self._get_value("selected_item", self._items[0]))
        except IndexError:
            return None

    def simulate_selection(self, item):
        self._set_value("selected_item", item)
        self.interface.on_change()
