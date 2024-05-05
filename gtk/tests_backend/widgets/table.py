import pytest

from toga_gtk.libs import Gtk

from .base import SimpleProbe


class TableProbe(SimpleProbe):
    native_class = Gtk.ScrolledWindow
    supports_icons = 2  # All columns
    supports_keyboard_shortcuts = False
    supports_widgets = False

    def __init__(self, widget):
        super().__init__(widget)
        self.native_table = widget._impl.native_table
        assert isinstance(self.native_table, Gtk.TreeView)

    @property
    def background_color(self):
        pytest.skip("Can't set background color on GTK Tables")

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
