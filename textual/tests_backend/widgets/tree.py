import pytest
from textual.widgets import Tree as TextualTree

from .base import SimpleProbe


def node_for_path(data, path):
    node = data
    for index in path:
        node = node[index]
    return node


class TreeProbe(SimpleProbe):
    native_class = TextualTree
    supports_keyboard_shortcuts = False
    supports_widgets = False

    async def redraw(self, message=None, delay=0, wait_for=None):
        await super().redraw(message=message, delay=delay, wait_for=wait_for)
        await self.widget.app._impl.wait_for_dom_operations()

    @property
    def width(self):
        return self.impl._tree_width

    async def expand_tree(self):
        self.impl.expand_all()

    def is_expanded(self, node):
        return node._impl.is_expanded

    def child_count(self, row_path=None):
        if row_path is None:
            return len(self.native.root.children)
        return len(node_for_path(self.widget.data, row_path)._impl.children)

    @property
    def column_count(self):
        return len(self.widget.columns)

    @property
    def header_visible(self):
        return self.widget.show_headings

    @property
    def header_titles(self):
        return [column.heading for column in self.widget.columns]

    def column_width(self, col):
        return self.impl.column_width(col)

    def assert_cell_content(self, row_path, col, value=None, icon=None, widget=None):
        if widget:
            pytest.xfail("Textual doesn't support widgets in Trees.")

        node = node_for_path(self.widget.data, row_path)
        column = self.widget.columns[col]
        assert self.impl.cell_text(node, column, warn=False) == value
        assert self.impl.cell_icon(node, column) is icon

    async def wait_for_scroll_completion(self):
        # No animation associated with scroll, so this is a no-op.
        pass

    async def select_row(self, row_path, add=False):
        self.impl.select_node(node_for_path(self.widget.data, row_path), add=add)

    async def activate_row(self, row_path):
        self.impl.activate_node(node_for_path(self.widget.data, row_path))

    async def assert_item_mouse_hover(self, row_path):
        pytest.skip("Mouse hover is not implemented on Textual Trees.")
