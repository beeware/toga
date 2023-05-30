from ..utils import not_required
from .base import Widget


@not_required  # Testbed coverage is complete for this widget.
class Selection(Widget):
    def create(self):
        self._action("create Selection")
        self._items = []

    def change_source(self, source):
        self._action("change source", source=source)
        for item in source:
            self._items.append(item)

        # Source has changed; reset the selection and invoke the change handler
        try:
            selected = source[0]
        except IndexError:
            selected = None

        self.simulate_selection(selected)

    def insert(self, index, item):
        self._action("insert item", index=index, item=item)
        self._items.insert(index, item)

    def change(self, item):
        self._action("change item", item=item)

    def remove(self, index, item):
        self._action("remove item", index=index, item=item)
        del self._items[index]

        # If we deleted the selected item, reset the selection.
        if self.get_selected_item() == item:
            try:
                selected = self._items[0]
            except IndexError:
                selected = None
            self.simulate_selection(selected)

    def clear(self):
        self._action("clear")
        self._items = []
        self.simulate_selection(None)

    def select_item(self, item):
        # Confirm the item is valid. If it isn't, raise a ValueError.
        self._items.index(item)
        self._action("select item", item=item)
        self.simulate_selection(item)

    def get_selected_item(self):
        try:
            return self._get_value("selected_item", self._items[0])
        except IndexError:
            return None

    def simulate_selection(self, item):
        self._set_value("selected_item", item)
        self.interface.on_change(None)
