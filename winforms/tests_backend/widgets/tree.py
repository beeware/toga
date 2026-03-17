import asyncio

import pytest
from System.Windows.Forms import (
    MouseButtons,
    MouseEventArgs,
)

from .table import TableProbe


class TreeProbe(TableProbe):
    def state_node(self, row_path):
        self.state_tree = self.impl._state_tree
        return self.state_tree[row_path]

    def display_index(self, row_path):
        state_node = self.state_node(row_path)
        return self.impl.display_list.index(state_node)

    async def expand_tree(self):
        self.impl.expand_all()
        await asyncio.sleep(0.1)

    def is_expanded(self, node):
        self.state_tree = self.impl._state_tree
        state_node = self.state_tree.find_state_node(node)

        return state_node.is_open

    def child_count(self, row_path=None):
        state_node = self.state_node(row_path)
        return len(state_node)

    async def select_row(self, row_path, add=False):
        display_index = self.display_index(row_path)
        await super().select_row(row=display_index, add=add)

    async def activate_row(self, row_path):
        display_index = self.display_index(row_path)
        await super().select_row(row=display_index)

        bounds = self.native.Items[display_index].Bounds
        self.native.OnMouseDoubleClick(
            MouseEventArgs(
                MouseButtons.Left,
                clicks=2,
                x=int((bounds.Left + bounds.Right) / 2),
                y=int((bounds.Top + bounds.Bottom) / 2),
                delta=0,
            )
        )

    def assert_cell_content(self, row_path, col, value=None, icon=None, widget=None):
        if widget:
            pytest.skip("This backend doesn't support widgets in Tables")
            return
        # Use the table  assert_cell_content for non-leaf cells. However, the branch
        # containing the node must be expanded to check that (otherwise the node is
        # not in the display list). So expand that branch and then restore it after.

        state_node = self.state_node(row_path)
        row_path_states = self.open_row_path(row_path)

        display_index = self.impl.display_list.index(state_node)

        super().assert_cell_content(display_index, col, value, icon, widget)

        self.restore_row_path(row_path, row_path_states)

    def open_row_path(self, row_path):
        # Expand all nodes along a row_path to make the specified node visible.

        # Keep a record of the node states along the row_path:
        # True=Open/Expanded, False=Closed/Collapsed.
        row_path_states = []

        if row_path is None or len(row_path) < 2:
            return row_path_states

        state_node = self.impl._state_tree
        for i in row_path[:-1]:
            state_node = state_node[(i,)]

            row_path_states.append(state_node.is_open)
            if not state_node.is_open:
                state_node.toggle_state(update_display=True)
                self.impl._update_list(True)

        return row_path_states

    def restore_row_path(self, row_path, row_path_states):
        if row_path is None or len(row_path) < 2:
            return

        state_tree = self.impl._state_tree
        for i, _ in enumerate(row_path[:-1]):
            if i == 0:
                state_node = state_tree[row_path[:-1]]
            else:
                state_node = state_tree[row_path[: -(i + 1)]]

            original_state = row_path_states[-(i + 1)]

            if state_node.is_open != original_state:
                state_node.toggle_state(update_display=True)
                self.impl._update_list(True)
