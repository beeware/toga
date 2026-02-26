from ctypes import POINTER, cast
from ctypes.wintypes import HWND, LPARAM, UINT, WPARAM
from warnings import warn

import System.Windows.Forms as WinForms

from toga.handlers import WeakrefCallable

from ..libs import windowconstants as wc
from ..libs.comctl32 import DefSubclassProc, RemoveWindowSubclass, SetWindowSubclass
from ..libs.comctl32classes import LVITEMW, NMHDR, NMLVDISPINFOW, SUBCLASSPROC
from ..libs.user32 import SendMessageW
from ..libs.win32 import LRESULT
from .base import Widget


class Table(Widget):
    # The following methods are overridden in DetailedList.
    @property
    def _show_headings(self):
        return self.interface._show_headings

    @property
    def _columns(self):
        return self.interface._columns

    @property
    def _multiple_select(self):
        return self.interface.multiple_select

    @property
    def _data(self):
        return self.interface.data

    def __del__(self):
        # The object self.pfn_subclass is a python class and is part of the native
        # Windows process. When a Table is removed by the python GC, self.pfn_subclass
        # is also removed and the Windows process has a dangling pointer. Calling
        # Dispose() here fixes the problem by removing the self.pfn_subclass from the
        # Windows process.
        self.native.Dispose()

    def create(self):
        self.pfn_subclass = SUBCLASSPROC(self._subclass_proc)
        self.native = WinForms.ListView()
        self._set_subclass()

        self.native.HandleCreated += WeakrefCallable(self.handle_created)
        self.native.HandleDestroyed += WeakrefCallable(self.handle_destroyed)

        self.native.View = WinForms.View.Details
        self._enable_multi_icon_style()
        self._cache = []
        self._first_item = 0
        self._pending_resize = True

        self.native.HeaderStyle = (
            WinForms.ColumnHeaderStyle.Nonclickable
            if self._show_headings
            else getattr(WinForms.ColumnHeaderStyle, "None")
        )

        dataColumn = []
        for column in self._columns:
            dataColumn.append(self._create_column(column))

        self.native.FullRowSelect = True
        self.native.MultiSelect = self._multiple_select
        self.native.DoubleBuffered = True
        self.native.VirtualMode = True
        self.native.Columns.AddRange(dataColumn)
        self.native.SmallImageList = WinForms.ImageList()
        self.native.HideSelection = False

        self.native.ItemSelectionChanged += WeakrefCallable(
            self.winforms_item_selection_changed
        )
        self.native.RetrieveVirtualItem += WeakrefCallable(
            self.winforms_retrieve_virtual_item
        )
        self.native.CacheVirtualItems += WeakrefCallable(
            self.winforms_cache_virtual_items
        )
        self.native.SearchForVirtualItem += WeakrefCallable(
            self.winforms_search_for_virtual_item
        )
        self.native.VirtualItemsSelectionRangeChanged += WeakrefCallable(
            self.winforms_virtual_items_selection_range_changed
        )
        self.add_action_events()

    def _enable_multi_icon_style(self):
        list_view_handle = int(self.native.Handle.ToString())

        # Use SendMessage over PostMessage since the ListView object is on the same
        # thread as the messaging call.
        old_style = SendMessageW(
            list_view_handle, wc.LVM_GETEXTENDEDLISTVIEWSTYLE, 0, 0
        )
        new_style = old_style | wc.LVS_EX_SUBITEMIMAGES

        SendMessageW(list_view_handle, wc.LVM_SETEXTENDEDLISTVIEWSTYLE, 0, new_style)

    def handle_created(self, sender, e):
        self._set_subclass()

    def handle_destroyed(self, sender, e):
        # Remove the subclass when a handle is destroyed to prevent a memory leak.
        self._remove_subclass()

    def _set_subclass(self):
        SetWindowSubclass(int(self.native.Handle.ToString()), self.pfn_subclass, 0, 0)

    def _remove_subclass(self):
        RemoveWindowSubclass(int(self.native.Handle.ToString()), self.pfn_subclass, 0)

    def _subclass_proc(
        self,
        hWnd: int,
        uMsg: int,
        wParam: int,
        lParam: int,
        uIdSubclass: int,
        dwRefData: int,
    ) -> LRESULT:
        # Remove the window subclass in the way recommended by Raymond Chen here:
        # https://devblogs.microsoft.com/oldnewthing/20031111-00/?p=41883
        if uMsg == wc.WM_NCDESTROY:
            RemoveWindowSubclass(hWnd, self.pfn_subclass, uIdSubclass)

        if uMsg == wc.WM_REFLECT_NOTIFY:
            phdr = cast(lParam, POINTER(NMHDR)).contents
            code = phdr.code
            if code == wc.LVN_GETDISPINFOW:
                disp_info = cast(lParam, POINTER(NMLVDISPINFOW)).contents
                self._set_subitem_icon(disp_info.item)

        # Call the original window procedure
        return DefSubclassProc(HWND(hWnd), UINT(uMsg), WPARAM(wParam), LPARAM(lParam))

    def _set_subitem_icon(self, lvitem: LVITEMW):
        row_index = lvitem.iItem
        column_index = lvitem.iSubItem

        _, icon_indices = self._toga_retrieve_virtual_item(row_index)

        # Add the icon property if it doesn't exist.
        if lvitem.uiMask == (wc.LVIF_TEXT | wc.LVIF_STATE):
            lvitem.uiMask = wc.LVIF_TEXT | wc.LVIF_STATE | wc.LVIF_IMAGE

        if lvitem.uiMask & wc.LVIF_IMAGE != 0 and icon_indices[column_index] > -1:
            lvitem.iImage = icon_indices[column_index]

    def add_action_events(self):
        self.native.MouseDoubleClick += WeakrefCallable(self.winforms_double_click)

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)
        if self._pending_resize:
            self._pending_resize = False
            self._resize_columns()

    def winforms_retrieve_virtual_item(self, sender, e):
        # Because ListView is in VirtualMode, it's necessary implement
        # VirtualItemsSelectionRangeChanged event to create ListViewItem
        # when it's needed
        e.Item, _ = self._toga_retrieve_virtual_item(e.ItemIndex)

    def _toga_retrieve_virtual_item(self, item_index):
        if (
            self._cache
            and item_index >= self._first_item
            and item_index < self._first_item + len(self._cache)
        ):
            return self._cache[item_index - self._first_item]
        else:
            return self._new_item(item_index)

    def winforms_cache_virtual_items(self, sender, e):
        if (
            self._cache
            and e.StartIndex >= self._first_item
            and e.EndIndex < self._first_item + len(self._cache)
        ):
            # If the newly requested cache is a subset of the old cache,
            # no need to rebuild everything, so do nothing
            return

        # Now we need to rebuild the cache.
        self._first_item = e.StartIndex
        new_length = e.EndIndex - e.StartIndex + 1
        self._cache = []

        # Fill the cache with the appropriate ListViewItems.
        for i in range(new_length):
            self._cache.append(self._new_item(i + self._first_item))

    def winforms_search_for_virtual_item(self, sender, e):
        if (
            not e.IsTextSearch or not self._columns or not self._data
        ):  # pragma: no cover
            # If this list is empty, or has no columns, or it's an unsupported search
            # type, there's no search to be done. These situation are difficult to
            # trigger in CI; they're here as a safety catch.
            return
        find_previous = e.Direction in [
            WinForms.SearchDirectionHint.Up,
            WinForms.SearchDirectionHint.Left,
        ]
        i = e.StartIndex
        found_item = False
        while True:
            # It is possible for e.StartIndex to be received out-of-range if the user
            # performs keyboard navigation at its edge, so check before accessing data
            if i < 0:  # pragma: no cover
                # This could happen if this event is fired searching backwards,
                # however this should not happen in Toga's use of it.
                # i = len(self._data) - 1
                raise NotImplementedError("backwards search unsupported")
            elif i >= len(self._data):
                i = 0
            if (
                self._columns[0].text(self._data[i])[: len(e.Text)].lower()
                == e.Text.lower()
            ):
                found_item = True
                break
            if find_previous:  # pragma: no cover
                # Toga does not currently need backwards searching functionality.
                # i -= 1
                raise NotImplementedError("backwards search unsupported")
            else:
                i += 1
            if i == e.StartIndex:
                break
        if found_item:
            e.Index = i

    def winforms_item_selection_changed(self, sender, e):
        self.interface.on_select()

    def winforms_virtual_items_selection_range_changed(self, sender, e):
        # Event handler for the ListView.VirtualItemsSelectionRangeChanged
        # with condition that only multiple items (>1) are selected.
        # A ListView.VirtualItemsSelectionRangeChanged event will also be raised
        # alongside a ListView.ItemSelectionChanged event when selecting a new
        # item to replace an already selected item. This is due to the new selection
        # action causing multiple items' selection state being changed.
        # The number of selected items is checked before the on_select() is called.
        # This is a workaround to avoid calling the on_select() method twice
        # when selecting a new item to replace an already selected item.
        if len(list(self.native.SelectedIndices)) > 1:
            self.interface.on_select()

    def winforms_double_click(self, sender, e):
        hit_test = self.native.HitTest(e.X, e.Y)
        item = hit_test.Item
        if item is not None:
            self.interface.on_activate(row=self._data[item.Index])
        else:  # pragma: no cover
            # Double clicking outside of an item apparently doesn't raise the event, but
            # that isn't guaranteed by the documentation.
            pass

    def _create_column(self, toga_column):
        col = WinForms.ColumnHeader()
        if self._show_headings:
            col.Text = toga_column.heading
        col.Name = str(id(toga_column))
        return col

    def _resize_columns(self):
        num_cols = len(self.native.Columns)
        if num_cols == 0:
            return

        width = int(self.native.ClientSize.Width / num_cols)
        for col in self.native.Columns:
            col.Width = width

    def change_source(self, source):
        self.update_data()

    def _icon_index(self, row, column) -> int:
        icon = column.icon(row)
        return -1 if icon is None else self._image_index(icon._impl)

    def _new_item(self, index):
        row = self._data[index]

        missing_value = self.interface.missing_value
        lvi = WinForms.ListViewItem(
            [column.text(row, missing_value) for column in self._columns],
        )
        if any(column.widget(row) is not None for column in self._columns):
            warn(
                "Winforms does not support the use of widgets in cells",
                stacklevel=1,
            )

        icon_indices = tuple(self._icon_index(row, column) for column in self._columns)

        return (lvi, icon_indices)

    def _image_index(self, icon):
        images = self.native.SmallImageList.Images
        key = str(icon.path)
        index = images.IndexOfKey(key)
        if index == -1:
            index = images.Count
            images.Add(key, icon.bitmap)
        return index

    def update_data(self):
        self.native.VirtualListSize = len(self._data)
        self._cache = []

    def insert(self, index, item):
        self.update_data()

    def change(self, item):
        self.update_data()

    def remove(self, index, item):
        self.update_data()

    def clear(self):
        self.update_data()

    def get_selection(self):
        selected_indices = list(self.native.SelectedIndices)
        if self._multiple_select:
            return selected_indices
        elif len(selected_indices) == 0:
            return None
        else:
            return selected_indices[0]

    def scroll_to_row(self, index):
        self.native.EnsureVisible(index)

    def remove_column(self, index):
        self.native.Columns.RemoveAt(index)
        self.update_data()
        self._resize_columns()

    def insert_column(self, index, heading, accessor):
        column = self.interface._columns[index]
        self.native.Columns.Insert(index, self._create_column(column))
        self.update_data()
        self._resize_columns()
