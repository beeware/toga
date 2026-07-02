import pytest
from textual.widgets import DataTable as TextualDataTable

from .base import SimpleProbe


class TableProbe(SimpleProbe):
    native_class = TextualDataTable
    supports_icons = 0
    supports_keyboard_boundary_shortcuts = False
    supports_keyboard_shortcuts = False
    supports_widgets = False

    async def redraw(self, message=None, delay=0, wait_for=None):
        await super().redraw(message=message, delay=delay, wait_for=wait_for)
        await self.widget.app._impl.wait_for_dom_operations()

    @property
    def row_count(self):
        return len(self.impl._rows)

    @property
    def width(self):
        return self.impl._table_width

    @property
    def column_count(self):
        return len(self.impl._column_keys)

    @property
    def header_visible(self):
        return self.native.show_header

    @property
    def header_titles(self):
        return [column.heading for column in self.widget.columns]

    def column_width(self, col):
        return self.impl.column_width(col)

    async def resize_column(self, index, width):
        self.impl.resize_column(index, width)

    def assert_cell_content(self, row, col, value=None, icon=None, widget=None):
        if widget:
            pytest.xfail("Textual doesn't support widgets in Tables.")

        row_key = self.impl._row_keys[row]
        column_key = self.impl._column_keys[col]
        assert self.native.get_cell(row_key, column_key) == value
        assert icon is None

    @property
    def max_scroll_position(self):
        return self.impl.max_scroll_position

    @property
    def scroll_position(self):
        return self.impl._scroll_position

    async def wait_for_scroll_completion(self):
        # No animation associated with scroll, so this is a no-op.
        pass

    async def select_row(self, row, add=False):
        self.impl.select_row(row, add=add)

    async def activate_row(self, row):
        self.impl.activate_row(row)

    async def activate_header(self):
        # Header activation should not select or activate a row.
        pass

    async def select_first_row_keyboard(self):
        pytest.skip("Keyboard navigation is not implemented on Textual Tables.")
