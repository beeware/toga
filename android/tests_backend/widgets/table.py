import pytest
from android.widget import ScrollView, TableLayout, TextView

from .base import SimpleProbe

HEADER = "HEADER"


class TableProbe(SimpleProbe):
    native_class = ScrollView
    supports_icons = False
    supports_keyboard_shortcuts = False
    supports_widgets = False

    def __init__(self, widget):
        super().__init__(widget)
        assert self.native.getChildCount() == 1
        self.native_table = self.native.getChildAt(0)
        assert isinstance(self.native_table, TableLayout)

    @property
    def row_count(self):
        count = self.native_table.getChildCount()
        if (count > 0) and self.header_visible:
            count -= 1
        return count

    @property
    def column_count(self):
        return self._row_view(HEADER).getChildCount()

    def assert_cell_content(self, row, col, value=None, icon=None, widget=None):
        if widget:
            pytest.skip("This backend doesn't support widgets in Tables")
        else:
            assert self._cell_text(row, col) == value
            assert icon is None

    def _cell_text(self, row, col):
        tv = self._row_view(row).getChildAt(col)
        assert isinstance(tv, TextView)
        return str(tv.getText())

    def _row_view(self, row):
        if row == HEADER:
            row = 0
        elif self.header_visible:
            row += 1
        return self.native_table.getChildAt(row)

    @property
    def max_scroll_position(self):
        return (
            self.native_table.getHeight() - self.native.getHeight()
        ) / self.scale_factor

    @property
    def scroll_position(self):
        return self.native.getScrollY() / self.scale_factor

    async def wait_for_scroll_completion(self):
        # No animation associated with scroll, so this is a no-op
        pass

    @property
    def header_visible(self):
        return self._row_view(HEADER).getChildAt(0).getTypeface().isBold()

    @property
    def header_titles(self):
        return [self._cell_text(HEADER, i) for i in range(self.column_count)]

    # The TextViews do not fill the columns, so we have to calculate their spacing
    # rather than their internal width.
    def column_width(self, index):
        row = self._row_view(HEADER)
        left = row.getChildAt(index).getLeft()
        if index < self.column_count - 1:
            right = row.getChildAt(index + 1).getLeft()
        else:
            right = row.getWidth()
        return (right - left) / self.scale_factor

    async def select_row(self, row, add=False):
        self._row_view(row).performClick()

    async def activate_row(self, row):
        self._row_view(row).performLongClick()

    @property
    def typeface(self):
        return self._row_view(0).getChildAt(0).getTypeface()

    @property
    def text_size(self):
        return self._row_view(0).getChildAt(0).getTextSize()
