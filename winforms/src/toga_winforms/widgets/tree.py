from collections.abc import Iterable, Iterator
from ctypes import POINTER, byref, c_wchar_p, cast
from ctypes.wintypes import HDC, HWND, LPARAM, RECT, UINT, WPARAM
from functools import partial
from warnings import warn

import System.Windows.Forms as WinForms
from System.Drawing import ColorTranslator

from toga.handlers import WeakrefCallable
from toga.sources.tree_source import Node, TreeSourceT

from ..libs import windowconstants as wc
from ..libs.comctl32 import (
    DefSubclassProc,
    ImageList_Draw,
    RemoveWindowSubclass,
)
from ..libs.comctl32classes import NMHDR, NMLVCUSTOMDRAW, NMLVDISPINFOW
from ..libs.gdi32 import CreateSolidBrush, DeleteObject, SetTextColor
from ..libs.user32 import DrawTextW, FillRect, GetSysColor
from ..libs.win32 import LRESULT
from .table import Table


class StateNode:
    """A wrapper for a TreeSource Node that also contains display data.

    Attributes:
        node: The associated Node.
        tree: The StateTree which the StateNode is a part of.
        depth: The smallest number of nodes between the StateNode and a root.
        children: A list of child StateNode instances. This is None for leaf nodes.
        text (non-leaf only): The display text of the Node.
        arrow (non-leaf only): The expansion/contraction arrow of the StateNode.
        icon (non-leaf only): The icon of the Node.
    """

    def __init__(self, node: Node, state_tree, depth: int):
        """Initializes an instance for a given node and its relation to a StateTree.

        :param node: The underlying Node.
        :param state_tree: The StateTree of which the StateNode is a part.
        :param depth: The smallest number of nodes between the StateNode and a root.
        """

        self.node = node
        self.tree = state_tree
        self.depth = depth

        self._is_open = False

        self.children = None
        if self.node.can_have_children():
            self.children = [StateNode(child, self.tree, depth + 1) for child in node]

        self.text = c_wchar_p("")
        self.mouse_hover: bool
        self.icon: int

    def __len__(self) -> int:
        if self.children is None:
            return 0
        else:
            return len(self.children)

    def __getitem__(self, row_path: list[int] | tuple[int] | None):
        """Gets an item based on a row path list or tuple

        :param row_path: A list or tuple of indices. The first is an index of a child,
            say A, in the list of children, the next is an index in the list of children
            of A, and so on...
        :return: The StateNode at the end of the path. None returns the StateNode
            itself.
        """
        if row_path is None or len(row_path) < 1:
            return self
        elif len(row_path) == 1:
            return self.children[row_path[0]]
        else:
            return self.children[row_path[0]][row_path[1:]]

    def __iter__(self) -> Iterator:
        return iter(self.children or [])

    def branch_iter(self, display=True) -> Iterable:
        yield from display_branch_iter(self, ignore_closed=not display)

    @property
    def is_leaf(self) -> bool:
        """Can the Node (and hence StateNode) have children?"""
        return self.children is None

    @property
    def is_open(self) -> bool:
        """Is the node open (expanded)? Leaf nodes are always closed (contracted)."""
        return self._is_open

    def toggle_state(self, update_display: bool) -> bool:
        """Toggles the state (open/closed) of the StateNode.

        :param update_display: Whether the display list should be updated. If the
            StateNode is visible this should most likely be True. Otherwise this should
            be False.
        :return: A bool indicating whether a change of selection has occurred.
        """
        if not self.is_leaf:
            self._is_open = not self._is_open
            if update_display:
                return self.tree._display_list_toggle(self)

        return False

    def set_branch_state(self, set_open: bool, is_visible: bool) -> bool:
        """Sets the state (open/closed) for a StateNode and all its descendants.

        :param set_open: Should the state be set to open?
        :param is_visible: Is the state_node in the display list?
        :return: A bool indicating whether a change of selection has occurred.
        """
        if self.is_open != set_open:
            self.toggle_state(update_display=is_visible)

        notify_select = False
        for child in self:
            child_visible = self.is_open and is_visible
            notify_select = (
                child.set_branch_state(set_open, child_visible) or notify_select
            )

    def insert(self, index: int, node: Node) -> bool:
        """Inserts a child StateNode for a given Node at a given index.

        :param index: The index where the child StateNode will be placed in the children
            list.
        :param node: The Node from which to make a child StateNode.
        :return: A bool indicating whether a refresh of the ListView is needed.
        """
        refresh_needed = self.is_leaf
        child = StateNode(node, self.tree, self.depth + 1)
        if self.is_leaf:
            self.children = [child]
        else:
            self.children.insert(index, child)

        self.tree._display_list_adjust(True, child)
        return refresh_needed

    def remove(self, index: int) -> bool:
        """Removes a child at a given index.

        :param index: The index of the StateNode to be deleted.
        :return: A bool indicating whether a change of selection has occurred.
        """
        child = self.children[index]

        notify_select = self.tree._display_list_adjust(False, child)

        del self.children[index]
        return notify_select


class StateTree(StateNode):
    """A wrapper for a TreeSourceT that also contains display data.

    A StateTree manages the current status of the Tree widget via instances of the
    StateNode class. This information is used to construct a display list, which will
    be displayed by the ListView UI. Selections on the ListView UI are recorded via
    their index in the display list. Changes to the StateNodes are sent to the
    StateTree and then both the display list and the selected index list are updated
    appropriately.

    Attributes:
        tree_source: The TreeSourceT used to build the StateTree.
        tree: The StateTree itself (from StateNode).
        children: A list of root StateNodes, None for leaf nodes.
        depth: -1 (from StateNode).

        text (non-leaf only): The display text of the Node.
        arrow (non-leaf only): The expansion/contraction arrow of the StateNode.
        icon (non-leaf only): The icon of the Node.
    """

    #################################################################################
    # Overrides/extensions of StateNode methods
    #################################################################################

    def __init__(self, tree_source: TreeSourceT):
        """Initializes the instance for a TreeSourceT.

        :param tree_source: The TreeSourceT used to build the StateTree.
        """
        self.tree_source = tree_source
        self.children = [
            StateNode(tree_source[i], self, 0) for i in range(len(tree_source))
        ]

        self.tree = self
        self.depth = -1
        self._display_list: list[StateNode] = []
        self.display_list_refresh()
        self._selected_indices: list[int] = []

    @property
    def is_leaf(self) -> bool:
        """A StateTree cannot be a leaf node by definition."""
        return False

    @property
    def is_open(self) -> bool:
        """A StateTree is always open (expanded)."""
        return True

    @is_open.setter
    def is_open(self, value) -> None:
        pass

    def toggle_state(self, update_display: bool = False) -> bool:
        """A StateTree is always open (expanded)."""
        return False

    def set_all_states(self, all_open: bool) -> None:
        """Sets the state (open/closed) of all the child StateNode instances.

        :param all_open: Should the children be open (expanded) or closed (contracted)?
        """
        super().set_all_states(all_open)
        self.display_list_refresh()

    #################################################################################
    # Display list methods
    #################################################################################

    @property
    def display_list(self) -> list[StateNode]:
        """The list of StateNodes which is displayed on the ListView instance."""
        return self._display_list

    def display_list_refresh(self):
        """Refreshes the display list to reflect the current StateTree properties."""
        self._display_list: list[StateNode] = list(self.branch_iter(display=True))

    def display_list_toggle_index(self, index) -> bool:
        """Toggles the state (open/closed) of a StateNode in the display list.

        :param index: The index of the StateNode in the display list.
        :return: A bool indicating whether a change of selection has occurred.
        """
        state_node = self._display_list[index]
        state_node.toggle_state(update_display=False)

        insert: bool = state_node.is_open
        sublist: list[StateNode] = list(state_node.branch_iter(display=True))
        start_index: int = index + 1

        return self._display_list_modifier(insert, sublist, start_index)

    def _display_list_adjust(self, insert: bool, state_node: StateNode) -> bool:
        """Adjusts the display list based on an item insertion or removal.

        :param insert: Is an item being inserted or removed?
        :param item: The item being inserted or removed.
        :return: For insert=True, a bool indicating whether a ListView refresh is
            needed. For insert=False, a bool indicating whether a change of selection
            has occurred.
        """
        # Find the index of state_node in the display list.
        index = -1
        for index_loop, state_node_loop in enumerate(self.branch_iter(display=True)):
            if state_node == state_node_loop:
                index = index_loop

        # If state_node is not in the display list there's no need to modify the
        # display list.
        if index == -1:
            return False

        # The remainder of this code block is only accessed if state_node is visible.
        notify_select = False

        # If state_node is open and being removed, also remove its branch.
        if state_node.is_open and not insert:
            notify_select = self.display_list_toggle_index(index) or notify_select

        notify_select = (
            self._display_list_modifier(insert, [state_node], index) or notify_select
        )
        if not insert:
            return notify_select

        return False

    def _display_list_modifier(
        self, insert: bool, sublist: list[StateNode], start_index: int
    ) -> bool:
        """Modifies the display list by either inserting or removing a sublist.

        The sublist contains either a single element, or a whole branch which will be
        expanded/contracted during a toggle operation.

        :param insert: Is the sublist being inserted or removed?
        :param start_index: The index in the display list where the first item of the
            sublist is/will be.
        :return: A bool indicating whether a change of selection has occurred.
        """
        if insert:
            self._display_list = (
                self._display_list[:start_index]
                + sublist
                + self._display_list[start_index:]
            )
        else:
            self._display_list = (
                self._display_list[:start_index]
                + self._display_list[start_index + len(sublist) :]
            )

        return self._selection_modifier(insert, start_index, len(sublist))

    def _display_list_toggle(self, state_node: StateNode) -> bool:
        """Updates the display list to reflect a node being toggled.

        :param state_node: The StateNode being toggled.
        :return: A bool indicating whether a change of selection has occurred.
        """
        insert: bool = state_node.is_open
        sublist: list[StateNode] = list(state_node.branch_iter(display=True))
        try:
            start_index: int = self._display_list.index(state_node) + 1
        except ValueError:
            # state_node is not in the display list, so no need to change it.
            return False

        return self._display_list_modifier(insert, sublist, start_index)

    #################################################################################
    # Selected Indices list methods
    #################################################################################

    @property
    def selected_indices(self) -> list[int]:
        """Indices of the display list that corresponds to the ListView selection."""
        return self._selected_indices

    def selected_indices_from_ui(self, selected_indices: list[int]):
        """Updates the selected indices list of the StateNode to match the UI."""
        self._selected_indices = selected_indices

    def _selection_modifier(
        self, insert: bool, start_index: int, range_size: int
    ) -> bool:
        """Modifies the selected indices list based on changes to the display list.

        Indices are changed based on the size and position of the sublist, as well as
        if the sublist is inserted or removed. Indices smaller than the start index
        are not changed. If the sublist is removed, any index corresponding to an
        item in the sublist is also removed. The other indices are shifted up or
        down based on the size of the sublist.

        :param insert: Is the sublist being inserted or removed?
        :param start_index: The index in the display list where the first item of the
            sublist is/will be.
        :param range_size: The size of the sublist being inserted/removed.
        :return: A bool indicating whether a change of selection has occurred.
        """
        selection_updater = extend_indices if insert else reduce_indices
        selection_updater = partial(selection_updater, start_index, range_size)

        def non_negative(x: int) -> bool:
            return x >= 0

        modified_indices = list(
            filter(non_negative, map(selection_updater, self._selected_indices))
        )
        notify_select = len(modified_indices) < len(self._selected_indices)

        self._selected_indices = modified_indices
        return notify_select

    #################################################################################
    # Utility methods
    #################################################################################

    def find_state_node(self, node: Node) -> StateNode | None:
        """Searches in the StateTree for a StateNode associated to a given Node.

        :param node: The node for which to find the corresponding StateNode.
        :return: If found the StateNode is returned, otherwise None is returned.
        """
        for state_node in self.branch_iter(display=False):
            if state_node.node == node:
                return state_node

        return None


def display_branch_iter(
    roots: Iterable[StateNode | StateTree], ignore_closed: bool = False
):
    """An iterator for a branch of a StateTree or Node."""
    for root in roots:
        yield from display_branch_recursive(root, ignore_closed)


def display_branch_recursive(branch: StateNode, ignore_closed: bool = False):
    """A recursive element to be used with the iterator display_branch_iter."""
    if branch.is_leaf:
        yield branch
    else:
        yield branch

        if branch.is_open or ignore_closed:
            for sub_branch in branch:
                yield from display_branch_recursive(sub_branch, ignore_closed)


def reduce_indices(reduction_start_index: int, reduction_size: int, index: int) -> int:
    if index < reduction_start_index:
        return index
    elif index < reduction_start_index + reduction_size:
        return -1
    else:
        return index - reduction_size


def extend_indices(extension_start_index: int, extension_size: int, index: int) -> int:
    if index < extension_start_index:
        return index
    else:
        return index + extension_size


def index_modifier(
    indices: list[int], insert: bool, start_index: int, range_size: int
) -> list[int]:
    selection_updater = extend_indices if insert else reduce_indices
    selection_updater = partial(selection_updater, start_index, range_size)

    def non_negative(x: int) -> bool:
        return x >= 0

    return list(filter(non_negative, map(selection_updater, indices)))


class Tree(Table):
    """The Tree widget works by storing the tree structure in a StateNode instance.
    This instance creates and updates a list of StateNodes which is then displayed by
    a ListView UI.

    The displayed rows for non-leaf nodes contain a state-change arrow which toggles
    the node state when clicked, and highlights on mouse hover. This functionality is
    achieved by a hit-test which is initiated by the mouse events.

    Since clicks on the state-change arrows shouldn't affect the selection, the list
    of selected indices of the ListView UI is overridden on these clicks.

    The displayed rows for non-leaf nodes are custom painted by responding to the
    NM_CUSTOMDRAW message.
    """

    #################################################################################
    # The following methods override/extend methods from Table.
    #################################################################################

    def create(self):
        super().create()
        self._state_tree: StateTree

        # _mouse_move_hit is a record of the latest hit-test for a MouseMove event.
        # This is used in the _new_branch method to assign the correct state-change
        # arrow to the non-leaf node display rows.
        self._mouse_move_hit = -1

        # _mouse_down_hit is a record of the latest hit-test for a MouseDown event.
        # This is used by the _process_selection_change method to determine whether
        # a MouseDown event should trigger a change of selection in the UI.
        self._mouse_down_hit = -1

        # These are widths that are used in the painting of the non-leaf node rows.
        # The 4 here is undocumented left padding of the ListView UI. The amount is
        # confirmed/updated during the drawing process.
        self._left_padding = 4
        self._arrow_width = 21
        self._widths_set = False
        self._indent = self.native.SmallImageList.ImageSize.Width
        self._rect_right = 0

        self._hbrush_back = CreateSolidBrush(
            ColorTranslator.ToWin32(self.native.BackColor)
        )
        self.native.BackColorChanged += WeakrefCallable(
            self.winforms_back_color_changed
        )

        self.native.MouseMove += WeakrefCallable(self.winforms_mouse_move)
        self.native.MouseLeave += WeakrefCallable(self.winforms_mouse_leave)
        self.native.MouseDown += WeakrefCallable(self.winforms_mouse_down)
        self.native.MouseClick += WeakrefCallable(self.winforms_mouse_click)
        self.native.MouseUp += WeakrefCallable(self.winforms_mouse_up)

    def _subclass_proc(
        self,
        hWnd: int,
        uMsg: int,
        wParam: int,
        lParam: int,
        uIdSubclass: int,
        dwRefData: int,
    ) -> LRESULT:
        """Override from Table: Same method, but also responds to NM_CUSTOMDRAW."""
        if uMsg == wc.WM_NCDESTROY:
            # Delete the brushes
            DeleteObject(self._hbrush_back)

            # Remove the window subclass in the way recommended by Raymond Chen here:
            # devblogs.microsoft.com/oldnewthing/20031111-00/?p=41883
            RemoveWindowSubclass(hWnd, self.pfn_subclass, uIdSubclass)

        elif uMsg == wc.WM_REFLECT_NOTIFY:
            phdr = cast(lParam, POINTER(NMHDR)).contents
            code = phdr.code
            if code == wc.LVN_GETDISPINFOW:
                disp_info = cast(lParam, POINTER(NMLVDISPINFOW)).contents
                self._lvn_getdispinfo(disp_info.item)

            elif code == wc.NM_CUSTOMDRAW:
                # learn.microsoft.com/en-us/windows/win32/controls/nm-customdraw
                nmlvcd = cast(lParam, POINTER(NMLVCUSTOMDRAW)).contents
                return_flag = self._nm_customdraw(nmlvcd)
                if return_flag is not None:
                    return self._nm_customdraw(nmlvcd)

        # Call the original window procedure
        return DefSubclassProc(HWND(hWnd), UINT(uMsg), WPARAM(wParam), LPARAM(lParam))

    def _new_item(self, index):
        """Override from Table: Same method for leaf nodes, but new for non-leaf."""
        state_node = self.display_list[index]
        node = state_node.node
        if any(column.widget(node) is not None for column in self._columns):
            warn(
                "Winforms does not support the use of widgets in cells",
                stacklevel=1,
            )

        if state_node.is_leaf:
            return self._construct_new_item(node, state_node.depth)

        return self._new_branch(index, state_node)

    def _process_activation(self, x, y, list_view_item):
        """Activates for double-click on an item but not on state-change arrows."""
        if self._hit_test_arrow(x, y) == -1:
            self.interface.on_activate(
                node=self.display_list[list_view_item.Index].node
            )

    def _process_selection_change(self):
        """Overrides state-change-arrow selection events and allows the rest."""
        if self._mouse_down_hit >= 0:
            # If this _selected_indices_tree_to_ui was missing, the winforms "change
            # of selection" event would override the selection.
            self._selected_indices_tree_to_ui()
        else:
            self._selected_indices_ui_to_tree()
            self.interface.on_select()

    def update_data(self):
        self._state_tree = StateTree(self._data)
        self.native.VirtualListSize = len(self.display_list)
        self._cache = []

    def insert(self, index, item, parent=None):
        state_parent = self._get_state_parent(parent)
        if state_parent is None:
            return

        refresh_needed = state_parent.insert(index, item)
        self._update_list(refresh=refresh_needed)

    def change(self, item):
        self._update_list(refresh=True)

    def remove(self, index, item, parent=None):
        state_parent = self._get_state_parent(parent)
        if state_parent is None:
            return

        notify_select = state_parent.remove(index)
        self._update_list(notify_select)

    def get_selection(self):
        if self._multiple_select:
            return [self.display_list[i].node for i in self.selected_indices]
        elif len(self.selected_indices) == 0:
            return None
        else:
            return self.display_list[self.selected_indices[0]].node

    #################################################################################
    # The following methods are not from Table.
    #################################################################################

    @property
    def display_list(self) -> list[StateNode]:
        """The list of StateNodes which is currently being displayed by the UI.

        Note that display_list should only be modified using the methods of StateTree
        and StateNode that don't have preceding underscores.
        """
        return self._state_tree.display_list

    @property
    def selected_indices(self) -> list[int]:
        """The list of currently selected indices.

        Note that this list is modified by the StateTree and StateNode instances."""
        return self._state_tree._selected_indices

    @selected_indices.setter
    def selected_indices(self, indices: list[int]):
        notify_select = self._state_tree._selected_indices != indices
        self._state_tree._selected_indices = indices
        self._selected_indices_tree_to_ui(notify_select)

    def _hit_test_arrow(self, x: int, y: int) -> int:
        """Tests whether given coordinates are over a state-change arrow.

        :param x: The horizontal coordinate relative to the UI client area.
        :param y: The vertical coordinate relative to the UI client area.
        :return: If the (x,y) position is over a state-change arrow then the test
            returns the index of the StateNode. If the (x,y) position is not over
            any items -2 is returned. Otherwise -1 is returned (this corresponds
            to a normal click on a ListView item).
        """
        item = self.native.HitTest(x, y).Item
        if item is None:
            return -2

        state_node = self.display_list[item.Index]
        if state_node.is_leaf:
            return -1

        x_arrow = self._left_padding + state_node.depth * self._indent
        x_arrow += self._arrow_width / 2
        y_arrow = item.Bounds.Y + item.Bounds.Height / 2

        norm = (float(x - x_arrow)) ** 2 + (float(y - y_arrow)) ** 2
        if norm < (self._arrow_width**2) / 2:
            return item.Index

        return -1

    def _set_mouse_move_hit(self, index):
        if index == self._mouse_move_hit:
            return

        old_index = self._mouse_move_hit
        self._mouse_move_hit = index
        self._cache = []
        for i in {index, old_index}:
            if i >= 0:
                self.native.RedrawItems(i, i, False)

    def _selected_indices_ui_to_tree(self):
        """This method updates the state tree to reflect the UI selection."""
        self._state_tree.selected_indices_from_ui(list(self.native.SelectedIndices))

    def _selected_indices_tree_to_ui(self, notify_select: bool = False):
        """Updates the UI to reflect the selected indices list from StateTree."""
        self.native.ItemSelectionChanged -= self.selection_listener_single
        self.native.VirtualItemsSelectionRangeChanged -= self.selection_listener_multi

        for index in self.native.SelectedIndices:
            self.native.Items[index].Selected = False

        for index in self.selected_indices:
            self.native.Items[index].Selected = True

        self.native.ItemSelectionChanged += self.selection_listener_single
        self.native.VirtualItemsSelectionRangeChanged += self.selection_listener_multi

        if notify_select:
            self.interface.on_select()

    def winforms_mouse_move(self, sender, e):
        self._set_mouse_move_hit(self._hit_test_arrow(e.X, e.Y))

    def winforms_mouse_leave(self, sender, e):
        """Resets hit test variables when mouse leaves the client area.

        This methods is needed because quick mouse movements, beginning at the state-
        change arrow and ending outside the ListView client area, may not register
        as MouseMove events (since the cursor is not within the client area).

        Similarly, there is a need to reset _mouse_down_hit since a click and drag
        movement beginning at the state-change arrow will not register as a
        MouseClick or MouseUp event.
        """
        self._mouse_down_hit = -1
        self._set_mouse_move_hit(-1)

    def winforms_mouse_down(self, sender, e):
        """Sets _mouse_down_hit and toggles a state change if it is at least 0."""
        hit_index = self._hit_test_arrow(e.X, e.Y)
        self._mouse_down_hit = hit_index

        if hit_index >= 0:
            notify_select = self._state_tree.display_list_toggle_index(hit_index)
            self._update_list(notify_select)
            self.native.RedrawItems(hit_index, hit_index, False)

    def winforms_mouse_click(self, sender, e):
        """Corrects the UI selection based on the hit-test.

        A MouseClick event is triggered when a MouseDown and MouseUp event occurs
        without the cursor moving in between. If this method where not present, the
        MouseClick event over a state-change arrow clears the UI selection when the
        clicked row is not selected.
        """
        hit_index = self._hit_test_arrow(e.X, e.Y)

        if hit_index != -1:
            self._selected_indices_tree_to_ui()

    def winforms_mouse_up(self, sender, e):
        """Resets the _mouse_down_hit attribute."""
        if self._mouse_down_hit < -1:
            self._process_selection_change()

        self._mouse_down_hit = -1

    def winforms_back_color_changed(self, sender, e):
        """Updates the win32 brush for the background color"""
        # Delete the old brush
        DeleteObject(self._hbrush_back)
        # Create the new brush
        self._hbrush_back = CreateSolidBrush(
            ColorTranslator.ToWin32(self.native.BackColor)
        )

    def _set_widths(self, hdc, rect):
        """Determines _left_padding and _arrow_width during the first custom draw."""
        text_format = wc.DT_CALCRECT | wc.DT_NOCLIP
        lengths = []

        for arrow in ["\u25bc", "\u25b6", "\u25bd", "\u25b7"]:
            rect_copy = RECT.from_buffer_copy(rect)
            DrawTextW(hdc, c_wchar_p(arrow), -1, byref(rect_copy), text_format)
            lengths.append(rect_copy.right - rect_copy.left)

        self._left_padding = rect.left
        self._arrow_width = max(lengths)
        self._widths_set = True

    def _nm_customdraw(self, nmlvcd) -> int | None:
        """Paints the non-leaf node items."""
        # learn.microsoft.com/en-us/windows/win32/controls/using-custom-draw
        if nmlvcd.nmcd.dwDrawStage == wc.CDDS_PREPAINT:
            return wc.CDRF_NOTIFYITEMDRAW

        elif nmlvcd.nmcd.dwDrawStage == wc.CDDS_ITEMPREPAINT:
            index = nmlvcd.nmcd.dwItemSpec
            state_node = self.display_list[index]
            if not state_node.is_leaf:
                hdc = HDC(nmlvcd.nmcd.hdc)
                FillRect(hdc, byref(nmlvcd.nmcd.rc), self._hbrush_back)

                self._rect_right = nmlvcd.nmcd.rc.right

                return wc.CDRF_NOTIFYSUBITEMDRAW

        elif wc.CDDS_SUBITEM | wc.CDDS_ITEMPREPAINT:
            # Don't need to check state_node.is_leaf since this block is only
            # accessed after CDRF_NOTIFYSUBITEMDRAW is returned.

            # Skip drawing for subitems
            if nmlvcd.iSubItem > 0:
                return wc.CDRF_SKIPDEFAULT

            hdc = HDC(nmlvcd.nmcd.hdc)
            rect = RECT.from_buffer_copy(nmlvcd.nmcd.rc)
            index = nmlvcd.nmcd.dwItemSpec
            state_node = self.display_list[index]
            is_selected = self.native.Items[index].Selected

            # Set the width constants
            if not self._widths_set:
                self._set_widths(hdc, nmlvcd.nmcd.rc)

            # Set the colors based on whether the item is selected.
            # The "+1" is needed for system brushes with FillRect, documented here:
            # learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-fillrect
            if is_selected:
                if self.native.Focused:
                    text_color = wc.COLOR_HIGHLIGHTTEXT
                    back_color = wc.COLOR_HIGHLIGHT + 1
                else:
                    text_color = wc.COLOR_BTNTEXT  # Color is undocumented
                    back_color = wc.COLOR_BTNFACE + 1  # Color is undocumented
            else:
                text_color = wc.COLOR_HOTLIGHT
                back_color = self._hbrush_back

            # Determine the state-change arrow.
            if state_node.mouse_hover:
                arrow = "\u25bc" if state_node.is_open else "\u25b6"
            else:
                arrow = "\u25bd" if state_node.is_open else "\u25b7"

            # Draw the arrow, making sure the click location is in its center.
            rect.left = rect.left + state_node.depth * self._indent
            rect.right = rect.left + self._arrow_width
            SetTextColor(hdc, GetSysColor(wc.COLOR_HOTLIGHT))
            text_format = wc.DT_SINGLELINE | wc.DT_VCENTER | wc.DT_WORD_ELLIPSIS
            DrawTextW(hdc, arrow, -1, byref(rect), text_format | wc.DT_HCENTER)

            # Draw the icon
            rect.left = rect.right + 2
            if state_node.icon >= 0:
                ImageList_Draw(
                    HWND(int(self.native.SmallImageList.Handle.ToString())),
                    state_node.icon,
                    hdc,
                    rect.left,
                    divmod(rect.top + rect.bottom - self._indent, 2)[0],
                    wc.ILD_SELECTED if is_selected else wc.ILD_NORMAL,
                )

            # Draw the background (mainly for selection)
            rect.left = rect.left + self._indent
            rect.right = self._rect_right
            FillRect(hdc, byref(rect), back_color)

            # Draw the text
            rect.left = rect.left + 2
            rect.right = self._rect_right
            SetTextColor(hdc, GetSysColor(text_color))
            DrawTextW(hdc, state_node.text, -1, byref(rect), text_format)

            # Get the bounding rectangle of the drawn text.
            DrawTextW(
                hdc, state_node.text, -1, byref(rect), text_format | wc.DT_CALCRECT
            )

            rect.left = rect.right + self._indent
            rect.top = (
                nmlvcd.nmcd.rc.top
                + divmod(nmlvcd.nmcd.rc.bottom - nmlvcd.nmcd.rc.top, 2)[0]
            )
            rect.right = self._rect_right - self._indent
            rect.bottom = rect.top + 1

            if rect.left < rect.right:
                FillRect(hdc, byref(rect), text_color + 1)

            return wc.CDRF_SKIPDEFAULT

    def _new_branch(self, index: int, state_node: StateNode):
        """Collects the data corresponding to a non-leaf node item.

        The state-change arrow, text and icon index are all stored on the StateTree.
        A blank listview item is returned so that the ListView instance doesn't throw
        errors.
        """
        missing_value = self.interface.missing_value
        column = self._columns[0]
        node = state_node.node

        # Store the c_wchar_p objects on the StateNodes to prevent them from being
        # garbage collected.
        state_node.mouse_hover = index == self._mouse_move_hit
        state_node.text = c_wchar_p(column.text(node, missing_value))
        state_node.icon = self._icon_index(node, column)

        return (
            WinForms.ListViewItem([""] * len(self._columns)),
            (-1,) * len(self._columns),
        )

    def _update_list(self, notify_select: bool = False, refresh: bool = False):
        """Updates the display list and the UI.

        This method is called when toggling a StateNode, when adding/removing nodes,
        and when modifying an item.

        :param notify_select: A bool indicating whether a change of selection has
            occurred, and hence whether self.interface should be notified.
        :param refresh: A bool indicating whether the ListView needs to be repainted.
        """
        self.native.VirtualListSize = len(self.display_list)
        self._cache = []
        # This _selected_indices_tree_to_ui is needed for responsiveness.
        self._selected_indices_tree_to_ui(notify_select)

        if refresh:
            self.native.Refresh()

    def _get_state_parent(self, parent: Node | None = None):
        """Gets the StateNode/StateTree associated to parent.

        :param parent: The object for which to find the associated StateNode/StateTree.
        :return: If parent=None, then the state tree is returned. If parent is a Node
            and no corresponding StateNode can be found None is returned.
            Otherwise the StateNode corresponding to node is returned.
        """
        if parent is None:
            return self._state_tree
        else:
            state_parent = self._state_tree.find_state_node(parent)
            if state_parent is None:
                warn(
                    f"Could not find an object managed by {self._state_tree} that "
                    + f"corresponds to {parent}",
                    stacklevel=1,
                )

            return state_parent

    def set_branch_state(self, set_open: bool, branch: Node | None):
        if branch is None:
            state_node = self._state_tree
        else:
            state_node = self._state_tree.find_state_node(branch)

        if state_node is None or state_node.is_leaf:
            return

        if isinstance(state_node, StateTree):
            is_visible = True
        else:
            try:
                self.display_list.index(state_node)
                is_visible = True
            except ValueError:
                is_visible = False

        notify_select = state_node.set_branch_state(set_open, is_visible)
        self._update_list(notify_select)

    def expand_node(self, node):
        self.set_branch_state(set_open=True, branch=node)

    def expand_all(self):
        self.set_branch_state(set_open=True, branch=None)

    def collapse_node(self, node):
        self.set_branch_state(set_open=False, branch=node)

    def collapse_all(self):
        self.set_branch_state(set_open=False, branch=None)
