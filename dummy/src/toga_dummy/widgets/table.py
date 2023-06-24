from ..utils import not_required
from .base import Widget


@not_required  # Testbed coverage is complete for this widget.
class Table(Widget):
    def create(self):
        self._action("create Table")

    def change_source(self, source):
        self._action("change source", source=source)
        self.interface.on_select(None)

    def insert(self, index, item):
        self._action("insert row", index=index, item=item)

    def change(self, item):
        self._action("change row", item=item)

    def remove(self, index, item):
        self._action("remove row", item=item, index=index)

    def clear(self):
        self._action("clear")

    def get_selection(self):
        return self._get_value(
            "selection",
            [] if self.interface.multiple_select else None,
        )

    def scroll_to_row(self, row):
        self._action("scroll to row", row=row)

    def insert_column(self, index, heading, accessor):
        self._action("insert column", index=index, heading=heading, accessor=accessor)

    def remove_column(self, index):
        self._action("remove column", index=index)

    def simulate_selection(self, row):
        self._set_value("selection", row)
        self.interface.on_select(None)

    def simulate_activate(self, row):
        self.interface.on_activate(None, row=self.interface.data[row])
