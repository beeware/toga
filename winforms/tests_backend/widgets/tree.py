import asyncio

import pytest
from System.Windows.Forms import (
    MouseButtons,
    MouseEventArgs,
)

from toga_winforms.libs import win32constants as wc
from toga_winforms.libs.user32 import SendMessageW

from .table import TableProbe


class TreeProbe(TableProbe):
    def state_node(self, row_path):
        self.state_tree = self.impl._state_tree
        return self.state_tree[row_path]

    def display_index(self, row_path):
        state_node = self.state_node(row_path)
        return self.impl.display_list.index(state_node)

    def toggle_node(self, row_path):
        state_node = self.state_node(row_path)
        state_node.toggle_state(True)

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
        self.native.Items[display_index].Focused = True

    async def activate_row(self, row_path):
        display_index = self.display_index(row_path)
        await super().select_row(row=display_index)

        bounds = self.native.Items[display_index].Bounds
        self.mouse_double_click_event(
            x=int((bounds.Left + bounds.Right) / 2),
            y=int((bounds.Top + bounds.Bottom) / 2),
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

        state_node = self.impl._state_tree
        for j, i in enumerate(row_path[:-1]):
            state_node = state_node[(i,)]

            original_state = row_path_states[j]
            if state_node.is_open != original_state:
                state_node.toggle_state(update_display=True)
                self.impl._update_list(True)

    ####################################################################################
    # The following are mouse events used for testing
    ####################################################################################

    def mouse_move_event(self, x: int, y: int):
        self.native.OnMouseMove(
            MouseEventArgs(
                getattr(MouseButtons, "None"),
                clicks=0,
                x=x,
                y=y,
                delta=0,
            )
        )

    def mouse_double_click_event(self, x: int, y: int):
        self.native.OnMouseDoubleClick(
            MouseEventArgs(
                MouseButtons.Left,
                clicks=2,
                x=x,
                y=y,
                delta=0,
            )
        )

    def full_mouse_click_event(self, x: int, y: int):
        # According to the documentation the "standard Click event behavior" is the
        # sequence MouseDown, Click, MouseClick, MouseUp.
        # https://learn.microsoft.com/en-us/dotnet/desktop/winforms/input-mouse/events

        mouse_event_args = MouseEventArgs(
            MouseButtons.Left,
            clicks=1,
            x=x,
            y=y,
            delta=0,
        )

        self.native.OnMouseDown(mouse_event_args)

        # A simulated click doesn't change selection or focused index. Note: This basic
        # implementation is not compatible with multiple_select=True.
        lvi = self.native.HitTest(x, y).Item
        if lvi is None:
            for index in self.native.SelectedIndices:
                self.native.Items[index].Selected = False
        else:
            lvi.Selected = True
            lvi.Focused = True

        self.native.OnClick(mouse_event_args)
        self.native.OnMouseClick(mouse_event_args)
        self.native.OnMouseUp(mouse_event_args)

    def mouse_leave_event(self):
        self.native.OnMouseLeave(
            MouseEventArgs(
                getattr(MouseButtons, "None"),
                clicks=0,
                x=0,
                y=0,
                delta=0,
            )
        )

    ####################################################################################
    # The following are tests based on mouse events
    ####################################################################################

    async def assert_item_mouse_hover(self, row_path):
        state_node = self.state_node(row_path)
        display_index = self.impl.display_list.index(state_node)
        lvi = self.native.Items[display_index]
        bounds = lvi.Bounds

        assert not state_node.mouse_hover
        assert self.impl._mouse_move_hit in {-1, -2}

        # Move mouse over state-change arrow
        self.mouse_move_event(
            x=int(state_node.arrow_center_x),
            y=int((bounds.Top + bounds.Bottom) / 2),
        )
        await asyncio.sleep(0.1)
        assert state_node.mouse_hover
        assert self.impl._mouse_move_hit == 0

        # Move mouse away from state-change arrow, but still on the item.
        self.mouse_move_event(
            x=int(state_node.arrow_center_x + 40),
            y=int((bounds.Top + bounds.Bottom) / 2),
        )
        await asyncio.sleep(0.1)
        assert not state_node.mouse_hover
        assert self.impl._mouse_move_hit == -1

        # Move mouse away within item range but not on arrow.
        self.mouse_move_event(
            x=int(state_node.arrow_center_x + 80),
            y=int((bounds.Top + bounds.Bottom) / 2),
        )
        await asyncio.sleep(0.1)
        assert not state_node.mouse_hover
        assert self.impl._mouse_move_hit == -1

        # Move mouse to client area with no items
        self.mouse_move_event(
            x=int(state_node.arrow_center_x),
            y=int((bounds.Top + bounds.Bottom) / 2 + 5 * (bounds.Bottom - bounds.Top)),
        )
        await asyncio.sleep(0.1)
        assert not state_node.mouse_hover
        assert self.impl._mouse_move_hit == -2

    async def single_click(self, row_path, toggle: bool, on_item: bool):
        # Item must be visible and drawing finished.
        state_node = self.state_node(row_path)
        display_index = self.impl.display_list.index(state_node)
        bounds = self.native.Items[display_index].Bounds

        old_is_open = state_node.is_open

        if toggle:
            x = int(state_node.arrow_center_x)
        else:
            x = int(state_node.arrow_center_x + 40)

        if on_item:
            y = int((bounds.Top + bounds.Bottom) / 2)
        else:
            y = int((bounds.Top + bounds.Bottom) / 2 + 3 * (bounds.Bottom - bounds.Top))
        self.full_mouse_click_event(x=x, y=y)

        await asyncio.sleep(0.1)
        if toggle and on_item:
            assert old_is_open != state_node.is_open
        else:
            assert old_is_open == state_node.is_open

    async def double_click_state_change_arrow(self, row_path):
        # Note that item drawing must be finished for state_node.arrow_center_x to be
        # correct.
        state_node = self.state_node(row_path)
        display_index = self.impl.display_list.index(state_node)
        bounds = self.native.Items[display_index].Bounds

        self.mouse_double_click_event(
            x=int(state_node.arrow_center_x),
            y=int((bounds.Top + bounds.Bottom) / 2),
        )

    async def assert_mouse_leave(self):
        self.mouse_leave_event()

        assert self.impl._mouse_move_hit == -1
        assert self.impl._mouse_down_hit == -1

    async def key_press(self, key, presses: int = 1):
        hwnd = self.impl._hwnd

        if key == "down":
            wparam = wc.VK_DOWN
        elif key == "left":
            wparam = wc.VK_LEFT
        elif key == "right":
            wparam = wc.VK_RIGHT
        else:
            return

        for _i in range(presses):
            SendMessageW(hwnd, wc.WM_KEYDOWN, wparam, 0)
            await asyncio.sleep(0.1)
            SendMessageW(hwnd, wc.WM_KEYUP, wparam, 0)
            await asyncio.sleep(0.1)
