from functools import lru_cache

from toga.sources import Row

from .table import Table


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
    @lru_cache
    def _data(self):
        interface = self.interface

        class TableData:
            def __len__(self):
                return len(interface.data)

            def __getitem__(self, index):
                row = interface.data[index]
                title, subtitle, icon = (
                    getattr(row, attr, None) for attr in interface.accessors
                )
                return Row(title=(icon, title), subtitle=subtitle)

        return TableData()

    def create(self):
        super().create()

        # DetailedList doesn't have an on_activate handler.
        self.native.MouseDoubleClick -= self.winforms_double_click

    def set_primary_action_enabled(self, enabled):
        self.primary_action_enabled = enabled

    def set_secondary_action_enabled(self, enabled):
        self.secondary_action_enabled = enabled

    def set_refresh_enabled(self, enabled):
        self.refresh_enabled = enabled

    after_on_refresh = None
