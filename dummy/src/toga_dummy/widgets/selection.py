from .base import Widget


class Selection(Widget):
    def create(self):
        self._action("create Selection")
        self._items = []

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def insert(self, index, item):
        import warnings

        warnings.warn(
            "The insert() method is deprecated. Use source_insert() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_insert(index=index, item=item)

    def source_insert(self, *, index, item):
        self._action("insert item", index=index, item=item)
        self._items.insert(index, item)
        # If this is the first item to be inserted, it should be selected.
        if len(self._items) == 1:
            self.simulate_selection(self._items[0])

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def change(self, item):
        import warnings

        warnings.warn(
            "The change() method is deprecated. Use source_change() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_change(item=item)

    def source_change(self, *, item):
        self._action("change item", item=item)

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def remove(self, index, item):
        import warnings

        warnings.warn(
            "The remove() method is deprecated. Use source_remove() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_remove(index=index, item=item)

    def source_remove(self, *, index, item):
        self._action("remove item", index=index, item=item)
        del self._items[index]

        # If we deleted the selected item, reset the selection.
        if self._get_value("selected_item", None) == item:
            try:
                selected = self._items[0]
            except IndexError:
                selected = None
            self.simulate_selection(selected)

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def clear(self):
        import warnings

        warnings.warn(
            "The clear() method is deprecated. Use source_clear() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_clear()

    def source_clear(self):
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
