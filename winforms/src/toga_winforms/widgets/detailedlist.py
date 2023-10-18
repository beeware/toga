from toga.sources import Row

from .table import Table


# Wrap a DetailedList source to make it compatible with a Table.
class TableSource:
    def __init__(self, interface):
        self.interface = interface

    def __len__(self):
        return len(self.interface.data)

    def __getitem__(self, index):
        row = self.interface.data[index]
        title, subtitle, icon = (
            getattr(row, attr, None) for attr in self.interface.accessors
        )
        return Row(title=(icon, title), subtitle=subtitle)


class DetailedList(Table):
    # The following methods are overridden from Table.
    @property
    def _headings(self):
        return None

    @property
    def _accessors(self):
        return ("title", "subtitle")

    @property
    def _multiple_select(self):
        return False

    @property
    def _data(self):
        return self._table_source

    def create(self):
        super().create()
        self._table_source = TableSource(self.interface)

    def add_action_events(self):
        # DetailedList doesn't have an on_activate_handler.
        pass

    def set_primary_action_enabled(self, enabled):
        self.primary_action_enabled = enabled

    def set_secondary_action_enabled(self, enabled):
        self.secondary_action_enabled = enabled

    def set_refresh_enabled(self, enabled):
        self.refresh_enabled = enabled

    after_on_refresh = None
