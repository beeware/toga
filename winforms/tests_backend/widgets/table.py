import pytest
from System.Windows.Forms import (
    ColumnHeaderStyle,
    ListView,
    MouseButtons,
    MouseEventArgs,
)

from .base import SimpleProbe


class TableProbe(SimpleProbe):
    native_class = ListView
    background_supports_alpha = False
    supports_icons = False
    supports_keyboard_shortcuts = False
    supports_widgets = False

    @property
    def row_count(self):
        return self.native.VirtualListSize

    @property
    def column_count(self):
        return len(self.native.Columns)

    def assert_cell_content(self, row, col, value=None, icon=None, widget=None):
        if widget:
            pytest.skip("This backend doesn't support widgets in Tables")
        else:
            assert self.native.Items[row].SubItems[col].Text == value
            assert icon is None

    @property
    def max_scroll_position(self):
        document_height = (
            self.native.Items[self.row_count - 1].Bounds.Bottom
            - self.native.Items[0].Bounds.Top
        )
        return (document_height - self.native.ClientSize.Height) / self.scale_factor

    @property
    def scroll_position(self):
        return -(self.native.Items[0].Bounds.Top) / self.scale_factor

    async def wait_for_scroll_completion(self):
        # No animation associated with scroll, so this is a no-op
        pass

    @property
    def header_visible(self):
        return self.native.HeaderStyle != getattr(ColumnHeaderStyle, "None")

    @property
    def header_titles(self):
        return [col.Text for col in self.native.Columns]

    def column_width(self, index):
        return self.native.Columns[index].Width / self.scale_factor

    async def select_row(self, row, add=False):
        item = self.native.Items[row]
        if add:
            item.Selected = not item.Selected
        else:
            item.Selected = True

    async def activate_row(self, row):
        await self.select_row(row)

        bounds = self.native.Items[row].Bounds
        self.native.OnMouseDoubleClick(
            MouseEventArgs(
                MouseButtons.Left,
                clicks=2,
                x=int((bounds.Left + bounds.Right) / 2),
                y=int((bounds.Top + bounds.Bottom) / 2),
                delta=0,
            )
        )
