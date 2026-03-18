from .base import Widget


class Table(Widget):
    def create(self):
        self._action("create Table")

    def change_source(self, source):
        self._action("change source", source=source)
        self.interface.on_select()

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
        self._action("insert row", index=index, item=item)

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
        self._action("change row", item=item)

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
        self._action("remove row", item=item, index=index)

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

    def get_selection(self):
        return self._get_value(
            "selection",
            [] if self.interface.multiple_select else None,
        )

    def scroll_to_row(self, row):
        self._action("scroll to row", row=row)

    def insert_column(self, index, column):
        self._action("insert column", index=index, column=column)

    def remove_column(self, index):
        self._action("remove column", index=index)

    def simulate_selection(self, row):
        self._set_value("selection", row)
        self.interface.on_select()

    def simulate_activate(self, row):
        self.interface.on_activate(row=self.interface.data[row])
