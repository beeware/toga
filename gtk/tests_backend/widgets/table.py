import pytest

from toga_gtk.libs import GTK_VERSION, Gtk

from .base import SimpleProbe


class TableProbe(SimpleProbe):
    native_class = Gtk.ScrolledWindow
    supports_icons = 2  # All columns
    supports_keyboard_shortcuts = False
    supports_widgets = False

    def __init__(self, widget):
        super().__init__(widget)
        self.native_table = widget._impl.native_table
        assert isinstance(
            self.native_table,
            Gtk.TreeView if GTK_VERSION < (4, 0, 0) else Gtk.ColumnView,
        )

    @property
    def background_color(self):
        pytest.skip("Can't set background color on GTK Tables")

    @property
    def has_focus(self):
        if GTK_VERSION < (4, 0, 0):
            return self.native_table.has_focus()
        root = self.native_table.get_root()
        focused = root.get_focus()
        return focused is not None and (
            focused == self.native_table or focused.is_ancestor(self.native_table)
        )

    @property
    def row_count(self):
        return len(self.native_table.get_model())

    @property
    def column_count(self):
        return len(self.native_table.get_columns())

    @property
    def header_visible(self):
        if GTK_VERSION < (4, 0, 0):
            return self.native_table.get_headers_visible()
        return self.native_table.get_first_child().get_visible()

    @property
    def header_titles(self):
        return [col.get_title() for col in self.native_table.get_columns()]

    def column_width(self, col):
        if GTK_VERSION < (4, 0, 0):
            return self.native_table.get_column(col).get_width()
        header = self.native_table.get_first_child().get_first_child()
        for _ in range(col):
            header = header.get_next_sibling()
        return header.get_width()

    async def resize_column(self, index, width):
        self.native_table.get_columns()[index].set_fixed_width(round(width))

    def assert_cell_content(self, row, col, value=None, icon=None, widget=None):
        if widget:
            pytest.skip("GTK doesn't support widgets in Tables")
        elif GTK_VERSION >= (4, 0, 0):

            def cells(parent):
                child = parent.get_first_child()
                while child is not None:
                    if (
                        getattr(child, "row", None) == self.impl.store[row]
                        and getattr(child, "column", None) == self.widget.columns[col]
                    ):
                        yield child
                    yield from cells(child)
                    child = child.get_next_sibling()

            cell = next(cells(self.native_table))
            assert cell.text.get_text() == value
            if icon:
                assert cell.icon.get_paintable() == icon._impl.native().get_paintable()
            else:
                assert cell.icon.get_paintable() is None
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
        if GTK_VERSION >= (4, 0, 0):
            if add and self.impl.selection.is_selected(row):
                self.impl.selection.unselect_item(row)
            else:
                self.impl.selection.select_item(row, not add)
            return
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
        if GTK_VERSION < (4, 0, 0):
            self.native_table.emit(
                "row-activated", Gtk.TreePath(row), self.native_table.get_columns()[0]
            )
        else:
            self.native_table.emit("activate", row)

    async def select_first_row_keyboard(self):
        pytest.skip("test not implemented for this platform")

    async def activate_header(self):
        # No action needed; header activation is unrelated to
        # and does not contain a bug for regular selection
        pass
