import pytest
from System.Drawing import Bitmap
from System.Windows.Forms import (
    ColumnHeaderStyle,
    ListView,
    MouseButtons,
    MouseEventArgs,
)

from .base import SimpleProbe


class TableProbe(SimpleProbe):
    native_class = ListView
    supports_icons = 1  # First column only
    supports_keyboard_shortcuts = False
    supports_keyboard_boundary_shortcuts = True
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
            lvi = self.native.Items[row]
            assert lvi.SubItems[col].Text == value
            if col == 0:
                if icon is None:
                    assert lvi.ImageIndex == -1
                    assert lvi.ImageKey == ""
                else:
                    imagelist = self.native.SmallImageList
                    size = imagelist.ImageSize
                    assert size.Width == size.Height == 16

                    # The image is resized and copied, so we need to compare the actual
                    # pixels.
                    actual = imagelist.Images[lvi.ImageIndex]
                    expected = Bitmap(icon._impl.bitmap, size)
                    for x in range(size.Width):
                        for y in range(size.Height):
                            assert actual.GetPixel(x, y) == expected.GetPixel(x, y)
            else:
                assert icon is None

    @property
    def max_scroll_position(self):
        document_height = (
            self.native.Items[self.row_count - 1].Bounds.Bottom
            - self.native.Items[0].Bounds.Top
        )
        return round(
            (document_height - self.native.ClientSize.Height) / self.scale_factor
        )

    @property
    def scroll_position(self):
        return -round((self.native.Items[0].Bounds.Top) / self.scale_factor)

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
        return round(self.native.Columns[index].Width / self.scale_factor)

    async def resize_column(self, index, width):
        self.native.Columns[index].Width = round(width * self.scale_factor)

    def assert_column_resize(self, *, original_width, target_width, resized_width):
        assert resized_width == pytest.approx(target_width, abs=8)

    def assert_column_resize_after_source_change(
        self, *, resized_width, source_changed_width
    ):
        assert source_changed_width == pytest.approx(resized_width, abs=8)

    def assert_column_resize_after_layout_change(
        self,
        *,
        widths_before_layout_change,
        widths_after_layout_change,
    ):
        assert widths_after_layout_change[0] == pytest.approx(
            widths_before_layout_change[0], abs=8
        )

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

    async def select_first_row_keyboard(self):
        # Use the keyboard to ensure first row is selected.
        await self.type_character(" ")
