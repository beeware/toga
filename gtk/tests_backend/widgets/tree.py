import asyncio

import pytest

from toga_gtk.libs import GTK_VERSION, Gtk

from .base import SimpleProbe


class TreeProbe(SimpleProbe):
    native_class = Gtk.ScrolledWindow
    supports_keyboard_shortcuts = False
    supports_widgets = False

    def __init__(self, widget):
        super().__init__(widget)
        self.native_tree = widget._impl.native_tree
        assert isinstance(
            self.native_tree,
            Gtk.TreeView if GTK_VERSION < (4, 0, 0) else Gtk.ColumnView,
        )

    @property
    def background_color(self):
        pytest.skip("Can't set background color on GTK Tables")

    @property
    def has_focus(self):
        if GTK_VERSION < (4, 0, 0):
            return self.native_tree.has_focus()
        focused = self.native_tree.get_root().get_focus()
        return focused is not None and (
            focused == self.native_tree or focused.is_ancestor(self.native_tree)
        )

    async def expand_tree(self):
        self.impl.expand_all()
        await asyncio.sleep(0.1)

    def is_expanded(self, node):
        if GTK_VERSION >= (4, 0, 0):
            row = self.impl.visible_row(node)
            return row is not None and row.get_expanded()
        return self.native_tree.row_expanded(
            self.native_tree.get_model().get_path(node._impl)
        )

    def child_count(self, row_path=None):
        if GTK_VERSION >= (4, 0, 0):
            if row_path:
                return len(self.model_row(row_path).children)
            return len(self.impl.store)
        if row_path:
            row = self.native_tree.get_model()[row_path]
            return len(list(row.iterchildren()))
        else:
            return len(self.native_tree.get_model())

    def model_row(self, row_path):
        store = self.impl.store
        for index in row_path:
            row = store[index]
            store = row.children
        return row

    @property
    def column_count(self):
        return len(self.native_tree.get_columns())

    @property
    def header_visible(self):
        if GTK_VERSION < (4, 0, 0):
            return self.native_tree.get_headers_visible()
        return self.native_tree.get_first_child().get_visible()

    @property
    def header_titles(self):
        return [col.get_title() for col in self.native_tree.get_columns()]

    def column_width(self, col):
        if GTK_VERSION < (4, 0, 0):
            return self.native_tree.get_column(col).get_width()
        header = self.native_tree.get_first_child().get_first_child()
        for _ in range(col):
            header = header.get_next_sibling()
        return header.get_width()

    def assert_cell_content(self, row_path, col, value=None, icon=None, widget=None):
        if widget:
            pytest.skip("GTK doesn't support widgets in Tables")
        elif GTK_VERSION >= (4, 0, 0):
            row = self.model_row(row_path)
            column = self.widget.columns[col]
            # Collapsed descendants have model data but no rendered cell yet.
            assert row.text(column, self.widget.missing_value) == value
            assert column.icon(row.value) == icon

            def cells(parent):
                child = parent.get_first_child()
                while child is not None:
                    if (
                        getattr(child, "row", None) == row
                        and getattr(child, "column", None) == column
                    ):
                        yield child
                    yield from cells(child)
                    child = child.get_next_sibling()

            for cell in cells(self.native_tree):
                assert cell.text.get_text() == value
                if icon:
                    assert (
                        cell.icon.get_paintable() == icon._impl.native().get_paintable()
                    )
                else:
                    assert cell.icon.get_paintable() is None
        else:
            gtk_row = self.native_tree.get_model()[row_path]
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

    async def select_row(self, row_path, add=False):
        if GTK_VERSION >= (4, 0, 0):
            row = self.impl.visible_row(self.model_row(row_path).value)
            assert row is not None
            position = row.get_position()
            if add and self.impl.selection.is_selected(position):
                self.impl.selection.unselect_item(position)
            else:
                self.impl.selection.select_item(position, not add)
            return
        path = Gtk.TreePath(row_path)

        if add:
            if path in self.native_tree.get_selection().get_selected_rows()[1]:
                self.native_tree.get_selection().unselect_path(path)
            else:
                self.native_tree.get_selection().select_path(path)
        else:
            self.native_tree.get_selection().select_path(path)

    async def activate_row(self, row_path):
        await self.select_row(row_path)
        if GTK_VERSION < (4, 0, 0):
            self.native_tree.emit(
                "row-activated",
                Gtk.TreePath(row_path),
                self.native_tree.get_columns()[0],
            )
        else:
            row = self.impl.visible_row(self.model_row(row_path).value)
            self.native_tree.emit("activate", row.get_position())

    async def activate_header(self):
        # No action needed; header activation is unrelated to
        # and does not contain a bug for regular selection
        pass

    async def assert_item_mouse_hover(self, row_path):
        pytest.skip("Test not implemented for this platform")
