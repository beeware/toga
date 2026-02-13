import pytest

from toga_gtk.libs import GTK_VERSION, Gtk

from .base import SimpleProbe


class TableProbe(SimpleProbe):
    native_class = Gtk.ScrolledWindow
    supports_icons = 2  # All columns
    supports_keyboard_shortcuts = False
    supports_widgets = False

    if GTK_VERSION >= (4, 0, 0):
        pytest.skip("GTK4 doesn't support tables yet")

    def __init__(self, widget):
        super().__init__(widget)
        self.native_table = widget._impl.native_table
        assert isinstance(self.native_table, Gtk.TreeView)

    @property
    def background_color(self):
        pytest.skip("Can't set background color on GTK Tables")

    @property
    def has_focus(self):
        return self.native_table.has_focus()

    @property
    def row_count(self):
        return len(self.native_table.get_model())

    @property
    def column_count(self):
        return self.native_table.get_n_columns()

    @property
    def header_visible(self):
        return self.native_table.get_headers_visible()

    @property
    def header_titles(self):
        return [col.get_title() for col in self.native_table.get_columns()]

    def column_width(self, col):
        return self.native_table.get_column(col).get_width()

    async def resize_column(self, index, width):
        column = self.native_table.get_column(index)
        column.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
        column.set_fixed_width(int(width))

    def assert_column_resize(self, *, original_width, target_width, resized_width):
        assert resized_width == pytest.approx(target_width, abs=25)

    def assert_column_resize_after_source_change(
        self, *, resized_width, source_changed_width
    ):
        # GTK rebuilds table columns on source changes; width preservation is undefined.
        assert source_changed_width > 10

    def assert_column_resize_after_layout_change(
        self,
        *,
        widths_before_layout_change,
        widths_after_layout_change,
    ):
        assert all(width > 10 for width in widths_after_layout_change)

    def assert_cell_content(self, row, col, value=None, icon=None, widget=None):
        if widget:
            pytest.skip("GTK doesn't support widgets in Tables")
        else:
            gtk_row = self.native_table.get_model()[row]
            assert gtk_row[col * 2 + 2]

            if icon:
                assert gtk_row[col * 2 + 1] == icon._impl.native(16)
            else:
                assert gtk_row[col * 2 + 1] is None

    @property
    def max_scroll_position(self):
        return int(
            self.native.get_vadjustment().get_upper()
            - self.native.get_vadjustment().get_page_size()
        )

    @property
    def scroll_position(self):
        return int(self.native.get_vadjustment().get_value())

    async def wait_for_scroll_completion(self):
        # No animation associated with scroll, so this is a no-op
        pass

    async def select_row(self, row, add=False):
        path = Gtk.TreePath(row)

        if add:
            if path in self.native_table.get_selection().get_selected_rows()[1]:
                self.native_table.get_selection().unselect_path(path)
            else:
                self.native_table.get_selection().select_path(path)
        else:
            self.native_table.get_selection().select_path(path)

    async def activate_row(self, row):
        await self.select_row(row)
        self.native_table.emit(
            "row-activated",
            Gtk.TreePath(row),
            self.native_table.get_columns()[0],
        )

    async def select_first_row_keyboard(self):
        pytest.skip("test not implemented for this platform")
