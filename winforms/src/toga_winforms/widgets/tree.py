from collections.abc import Iterable, Iterator
from ctypes import POINTER, byref, c_wchar_p, cast
from ctypes.wintypes import HDC, HWND, LPARAM, RECT, UINT, WPARAM
from functools import partial
from warnings import warn

import System.Windows.Forms as WinForms

from toga.handlers import WeakrefCallable
from toga.sources.tree_source import Node, TreeSourceT

from ..libs import win32constants as wc, win32structures as ws
from ..libs.comctl32 import DefSubclassProc, RemoveWindowSubclass
from ..libs.user32 import DrawTextW
from .table import Table


class StateNode:
    """A wrapper for a TreeSource Node that also contains display data.

    Attributes:
        node: The associated Node.
        tree: The StateTree which the StateNode is a part of.
        depth: The smallest number of nodes between the StateNode and a root.
        children: A list of child StateNode instances. This is None for leaf nodes.
        arrow_center_x (non-leaf only): The horizontal coordinate (relative to the
            client area) of the expansion/contraction arrow of the StateNode.
        mouse_hover (non-leaf only): A bool indicating whether the mouse is hovering
            over the state-change arrow.
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

        self.arrow_center_x: float = 0.0
        self.mouse_hover: bool

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
        self._focused_index: int | None = None

    @property
    def is_leaf(self) -> bool:
        """A StateTree cannot be a leaf node by definition."""
        return False

    @property
    def is_open(self) -> bool:
        """A StateTree is always open (expanded)."""
        return True

    def toggle_state(self, update_display: bool = False) -> bool:
        """A StateTree is always open (expanded)."""
        return False

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
        self,
        insert: bool,
        sublist: list[StateNode],
        start_index: int,
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

        return self._selection_and_focus_modifier(insert, start_index, len(sublist))

    def _display_list_toggle(self, state_node: StateNode) -> bool:
        """Updates the display list to reflect a node being toggled.

        :param state_node: The StateNode being toggled.
        :return: A bool indicating whether a change of selection has occurred.
        """
        try:
            start_index: int = self._display_list.index(state_node) + 1
        except ValueError:
            # state_node is not in the display list, so no need to change it.
            return False

        insert: bool = state_node.is_open
        sublist: list[StateNode] = list(state_node.branch_iter(display=True))

        return self._display_list_modifier(insert, sublist, start_index)

    #################################################################################
    # Selected indices list and focused item methods
    #################################################################################

    @property
    def selected_indices(self) -> list[int]:
        """Indices of the display list that corresponds to the ListView selection."""
        return self._selected_indices

    def selected_indices_from_ui(self, selected_indices: list[int]):
        """Updates the selected indices list of the StateNode to match the UI."""
        self._selected_indices = selected_indices

    @property
    def focused_index(self) -> int | None:
        """Index of the display list that corresponds to the focused item."""
        return self._focused_index

    def focused_index_from_ui(self, focused_index: int | None):
        """Updates the focused index of the StateTree to match the UI."""
        self._focused_index = focused_index

    def _selection_and_focus_modifier(
        self,
        insert: bool,
        start_index: int,
        range_size: int,
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
        index_modifier = extend_indices if insert else reduce_indices
        index_modifier = partial(index_modifier, start_index, range_size)

        def non_negative(x: int) -> bool:
            return x >= 0

        modified_indices = list(
            filter(non_negative, map(index_modifier, self._selected_indices))
        )
        notify_select = len(modified_indices) < len(self._selected_indices)
        self._selected_indices = modified_indices

        if self._focused_index is not None:
            modified_focus = index_modifier(self._focused_index)
            self._focused_index = None if modified_focus < 0 else modified_focus

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

        # This method is only called by _get_state_parent, where a StateNode should
        # always be found.
        return None  # pragma: no cover


def display_branch_iter(
    roots: Iterable[StateNode | StateTree],
    ignore_closed: bool = False,
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
        self._mouse_move_hit: int = -1

        # _mouse_down_hit is a record of the latest hit-test for a MouseDown event.
        # This is used by the _process_selection_change method to determine whether
        # a MouseDown event should trigger a change of selection in the UI.
        self._mouse_down_hit: int = -1

        # This is the size of the "indent" used when constructing items in _new_item
        self._indent: int = self.native.SmallImageList.ImageSize.Width

        # These measurements deal with the arrow size. They are checked/updated during
        # the drawing process. They need to be constantly monitored since a change in
        # screen scaling will produce a different sized arrow. These values are the
        # expected values for 200% scaling.
        self._arrow_indent: int = 2
        self._arrow_width: float = 21.0

        self.native.MouseMove += WeakrefCallable(self.winforms_mouse_move)
        self.native.MouseLeave += WeakrefCallable(self.winforms_mouse_leave)
        self.native.MouseDown += WeakrefCallable(self.winforms_mouse_down)
        self.native.MouseClick += WeakrefCallable(self.winforms_mouse_click)
        self.native.MouseUp += WeakrefCallable(self.winforms_mouse_up)
        self.native.KeyDown += WeakrefCallable(self.winforms_key_down)

    def _subclass_proc(
        self,
        hWnd: int,
        uMsg: int,
        wParam: int,
        lParam: int,
        uIdSubclass: int,
        dwRefData: int,
    ) -> ws.LRESULT:
        """Override from Table: Same method, but also responds to NM_CUSTOMDRAW."""
        if uMsg == wc.WM_NCDESTROY:
            # Remove the window subclass in the way recommended by Raymond Chen here:
            # devblogs.microsoft.com/oldnewthing/20031111-00/?p=41883
            RemoveWindowSubclass(hWnd, self.pfn_subclass, uIdSubclass)

        elif uMsg == wc.WM_REFLECT_NOTIFY:
            phdr = cast(lParam, POINTER(ws.NMHDR)).contents
            code = phdr.code
            if code == wc.LVN_GETDISPINFOW:
                disp_info = cast(lParam, POINTER(ws.NMLVDISPINFOW)).contents
                self._lvn_getdispinfo(disp_info.item)

            elif code == wc.NM_CUSTOMDRAW:
                # learn.microsoft.com/en-us/windows/win32/controls/nm-customdraw
                nmlvcd = cast(lParam, POINTER(ws.NMLVCUSTOMDRAW)).contents
                return_flag = self._nm_customdraw(nmlvcd)
                if return_flag is not None:
                    return return_flag

            elif code == wc.LVN_ITEMCHANGED:
                nmlv = cast(lParam, POINTER(ws.NMLISTVIEW)).contents
                self._lvn_item_changed(nmlv)

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
            lvi, icon_indices = self._construct_new_item(node)
        else:
            lvi, icon_indices = self._construct_new_item(node, use_missing_value=False)
            state_node.mouse_hover = index == self._mouse_move_hit

        lvi.IndentCount = state_node.depth + self._arrow_indent

        return (lvi, icon_indices)

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

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def insert(self, index, item, parent=None):
        import warnings

        warnings.warn(
            "The insert() method is deprecated. Use source_insert() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_insert(index=index, item=item, parent=parent)

    def source_insert(self, *, index, item, parent=None):
        state_parent = self._get_state_parent(parent)

        refresh_needed = state_parent.insert(index, item)
        self._update_list(refresh=refresh_needed)

    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def change(self, item):
        import warnings

        warnings.warn(
            "The change() method is deprecated. Use source_change() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_change(item=item)

    def source_change(self, *, item):
        self._update_list(refresh=True)

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def remove(self, index, item, parent=None):
        import warnings

        warnings.warn(
            "The remove() method is deprecated. Use source_remove() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_remove(index=index, item=item, parent=parent)

    def source_remove(self, *, index, item, parent=None):
        state_parent = self._get_state_parent(parent)

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
        return self._state_tree.selected_indices

    @property
    def focused_index(self) -> int | None:
        """The index of the currently focused item.

        Note that this is modified by the StateTree and StateNode instances."""
        return self._state_tree.focused_index

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

        x_arrow = state_node.arrow_center_x
        y_arrow = item.Bounds.Y + item.Bounds.Height / 2

        norm = (float(x - x_arrow)) ** 2 + (float(y - y_arrow)) ** 2
        if norm * 2 < float(self._arrow_width) ** 2:
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
                self.native.Invalidate(self.native.Items[i].Bounds, False)

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

    def _process_focus_change(self, focused_index: int):
        """Overrides state-change-arrow focus-change events and allows the rest."""
        if self._mouse_down_hit >= 0:
            self._focused_index_tree_to_ui()
        else:
            self._state_tree.focused_index_from_ui(focused_index)

    def _focused_index_tree_to_ui(self):
        focus_index = self.focused_index
        if focus_index is not None:
            self.native.Items[focus_index].Focused = True
        elif self.native.FocusedItem is not None:
            self.native.FocusedItem.Focused = False

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
            self.native.Invalidate(self.native.Items[hit_index].Bounds, False)

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

    def winforms_key_down(self, sender, e):
        """Opens/closes nodes by using right/left key down events."""
        if e.KeyCode == WinForms.Keys.Right:
            toggle_open = True
        elif e.KeyCode == WinForms.Keys.Left:
            toggle_open = False
        else:
            return

        index = self.focused_index
        if self.display_list[index].is_open != toggle_open:
            notify_select = self._state_tree.display_list_toggle_index(index)
            self._update_list(notify_select)
            self.native.Invalidate(self.native.Items[index].Bounds, False)

    def _check_measurments(self, hdc, rect):
        """Checks/updates arrow width and that there are enough indents."""
        text_format = wc.DT_CALCRECT | wc.DT_NOCLIP
        lengths = []

        for arrow in ["\u25bc", "\u25b6", "\u25bd", "\u25b7"]:
            DrawTextW(hdc, c_wchar_p(arrow), -1, byref(rect), text_format)
            lengths.append(rect.right - rect.left)

        self._arrow_width = max(lengths)
        quotient, remaider = divmod(self._arrow_width, self._indent)

        if remaider == 0 and self._arrow_indent != quotient:  # pragma: no cover
            # The arrow widths should be 10,21 and 31 pixels for 100%, 200% and 300%
            # scaling. Also, rect.right - rect.left should be of the form 4 + 16 * n,
            # which is not satisfied by the above widths. So under normal usage this
            # block is not accessed.
            self._arrow_indent = quotient
            self._update_list(refresh=True)
        elif remaider != 0 and self._arrow_indent != quotient + 1:
            self._arrow_indent = quotient + 1
            self._update_list(refresh=True)

    def _draw_state_change_arrow(self, hdc, rect, index: int):
        state_node: StateNode = self.display_list[index]

        # Determine the state-change arrow.
        if state_node.mouse_hover:
            arrow = "\u25bc" if state_node.is_open else "\u25b6"
        else:
            arrow = "\u25bd" if state_node.is_open else "\u25b7"

        rect.right = rect.left
        rect.left = rect.right - self._indent * self._arrow_indent

        state_node.arrow_center_x = (rect.right + rect.left) / 2

        text_format = (
            wc.DT_SINGLELINE | wc.DT_VCENTER | wc.DT_WORD_ELLIPSIS | wc.DT_HCENTER
        )
        DrawTextW(hdc, c_wchar_p(arrow), -1, byref(rect), text_format)

    def _lvn_item_changed(self, nmlv):
        """Processes List-View item changes to listen for a change of focused item."""
        # learn.microsoft.com/en-us/windows/win32/controls/lvn-itemchanged
        # learn.microsoft.com/en-us/windows/win32/api/commctrl/ns-commctrl-nmlistview
        #
        # There is no WinForms focused-item change event and the using the WinForms
        # selection change events with ListView.FocusedItem gives unreliable results
        # when deselecting items. So, the change of focus is retrieved directly from the
        # Win32 messages.
        #
        # nmlv.uChanged contains flags for the attributes have been changed. These flag
        # values come from the mask attribute of the LVITEMW structure, and a change
        # of focused index is recorded in LVIF_STATE.
        if nmlv.uChanged & wc.LVIF_STATE != 0:
            # uNewState and uOldState have values determined by List-View Item States
            # learn.microsoft.com/en-us/windows/win32/controls/list-view-item-states
            is_focused_old = nmlv.uOldState & wc.LVIS_FOCUSED != 0
            is_focused = nmlv.uNewState & wc.LVIS_FOCUSED != 0

            if is_focused and is_focused != is_focused_old:
                self._process_focus_change(nmlv.iItem)

        else:  # pragma: no cover
            # The List-View UI is in virtual mode and changes to the data occur in
            # python. At which point the cache is deleted and rebuilt. This means that
            # the only changes which trigger LVN_ITEMCHANGED are state changes. So
            # this block should never be accessed.
            pass

    def _nm_customdraw(self, nmlvcd) -> int | None:
        """Paints the non-leaf node items."""
        # learn.microsoft.com/en-us/windows/win32/controls/using-custom-draw
        draw_stage = nmlvcd.nmcd.dwDrawStage

        if draw_stage == wc.CDDS_PREPAINT:
            return wc.CDRF_NOTIFYITEMDRAW

        elif draw_stage == wc.CDDS_ITEMPREPAINT:
            index = nmlvcd.nmcd.dwItemSpec
            rect = nmlvcd.nmcd.rc

            # Account for known bugs in the custom draw process.
            if index < 0 or index >= len(self.display_list) or rect.top == rect.bottom:
                return

            # Check/update the current measurements.
            self._check_measurments(nmlvcd.nmcd.hdc, RECT.from_buffer_copy(rect))

            # Progress to next subitem draw stage for non-leaf nodes to draw arrow.
            if not self.display_list[index].is_leaf:
                return wc.CDRF_NOTIFYSUBITEMDRAW

        elif draw_stage == wc.CDDS_SUBITEM | wc.CDDS_ITEMPREPAINT:
            index = nmlvcd.nmcd.dwItemSpec

            # This draw state is only accessed when CDRF_NOTIFYSUBITEMDRAW is returned
            # during CDDS_ITEMPREPAINT. Hence this block should only be accessed when
            # self.display_list[index].is_leaf is not true. However due to the existence
            # of occasional incorrect custom draw messages, this is checked again here.
            if nmlvcd.iSubItem == 0 and not self.display_list[index].is_leaf:
                rect = RECT.from_buffer_copy(nmlvcd.nmcd.rc)
                hdc = HDC(nmlvcd.nmcd.hdc)
                self._draw_state_change_arrow(hdc, rect, index)

        else:  # pragma: no cover
            # The draw stage messages after CDDS_PREPAINT of custom draw should only be
            # received if they are requested using appropriate return flags. However,
            # custom draw is known to occasionally send incorrect messages.
            pass

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
        self._focused_index_tree_to_ui()

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
            if state_parent is None:  # pragma: no cover
                # A StateNode associated to a Node should always be found.
                raise NameError(
                    f"Could not find an object managed by {self._state_tree} that "
                    + f"corresponds to {parent}"
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
