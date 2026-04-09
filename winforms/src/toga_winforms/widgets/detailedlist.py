from collections.abc import Callable
from ctypes import POINTER, byref, cast, sizeof
from ctypes.wintypes import HDC, HWND, LPARAM, POINT, RECT, SIZE, UINT, WPARAM

import System.Windows.Forms as WinForms
from System.Drawing import ColorTranslator, Size, SystemColors

from toga.handlers import WeakrefCallable

from ..colors import toga_color
from ..libs import (
    comctl32classes as cc32_cls,
    gdi32,
    user32 as u32,
    user32classes as u32_cls,
    windowconstants as wc,
)
from ..libs.comctl32 import (
    DefSubclassProc,
    ImageList_Draw,
    InitCommonControlsEx,
    RemoveWindowSubclass,
    SetWindowSubclass,
)
from ..libs.win32 import hiword, is_submessage, loword
from ..menus import ContextMenu
from .base import Widget


class DetailedList(Widget):
    # This widget is based on the Win32 List-View class with tile view, with resizing
    # of the tiles to obtain a single column. Note that tile view is not supported in
    # WinForms List-View. Here the tiles are sized dynamically, so that a change in font
    # size (for example from a change in DPI) will change the tile and the icon.
    #
    # Tile view has a bug where the tiles sizes get "stuck". Refreshing the data and
    # deleting the cache does not fix the problem. Much of the code presented here deals
    # with this issue. The approach is to handle the NM_CUSTOMDRAW message and manually
    # draw the tiles. This solves part of the problem. Other issues are:
    #   - The standard clickable area for an item is the icon and the label. However
    #     since the labels get stuck, the clickable area also becomes incorrect. This
    #     issue is overcome by handling the WM button messages (up, down, double-click).
    #     The clickable area is also improved over the standard implementation.
    #   - Tile view only repaints the icon and label regions. To repaint the whole tile
    #     during selection LVN_ITEMCHANGED is handled. To repaint when the widget loses
    #     focus, WM_SETFOCUS and WM_KILLFOCUS are handled.
    #
    # The actions are performed by use a context menu.

    @property
    def _data(self):
        return self.interface.data

    @property
    def _missing_value(self):
        return self.interface.missing_value

    def create(self):
        self.native = WinForms.Panel()

        # Create and set the Panel subclass procedure.
        self.pfn_subclass_panel = u32_cls.SUBCLASSPROC(self._subclass_proc_panel)
        self.winforms_handle_created(None, None)

        # Update the subclass procedure when the self.native handle is create/destroyed
        self.native.HandleCreated += WeakrefCallable(self.winforms_handle_created)
        self.native.HandleDestroyed += WeakrefCallable(self.winforms_handle_destroyed)

        self._default_background_color = toga_color(SystemColors.Window)
        self._first_item = 0
        self._cache = []

        self._selected_index: int | None = None
        self._focused_index: int | None = None
        self._rbuttondown_lparam: int | None = None

        # Disable all actions and refresh by default.
        self.primary_action_enabled: bool = False
        self.secondary_action_enabled: bool = False
        self.refresh_enabled: bool = False

        # Create the context menu
        self._context_menu = ContextMenu(self, self.actions)

        # According to the MicroSoft documentation, an application must call
        # InitCommonControlsEx must before creating a common control.
        self._init_common_controls_ex = cc32_cls.INITCOMMONCONTROLSEX()
        self._init_common_controls_ex.dwSize = sizeof(cc32_cls.INITCOMMONCONTROLSEX)
        self._init_common_controls_ex.dwICC = wc.ICC_LISTVIEW_CLASSES
        InitCommonControlsEx(byref(self._init_common_controls_ex))

        # Create the Win32 List-View object.
        # learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-createwindowexw
        lvs = wc.LVS_OWNERDATA | wc.LVS_SINGLESEL | wc.LVS_SHOWSELALWAYS | wc.LVS_REPORT
        self._hwnd = u32.CreateWindowExW(
            wc.LVS_EX_DOUBLEBUFFER,
            wc.WC_LISTVIEW,
            None,
            wc.WS_CHILD | wc.WS_VISIBLE | lvs,
            0,
            0,
            self._width,
            self._height,
            self._panel_hwnd,
            None,
            None,
            None,
        )

        # Change the view style to tile and configure the properties.
        # learn.microsoft.com/en-us/windows/win32/controls/use-tile-views
        lvtileviewinfo = self._tile_view_info_initial
        u32.SendMessageW(self._hwnd, wc.LVM_SETVIEW, wc.LV_VIEW_TILE, 0)
        u32.SendMessageW(self._hwnd, wc.LVM_SETTILEVIEWINFO, 0, byref(lvtileviewinfo))

        # Set the image list.
        self._image_list: WinForms.ImageList
        self._set_image_list()

        # Create and set the ListView UI (self._hwnd) subclass procedure.
        self.pfn_subclass_list = u32_cls.SUBCLASSPROC(self._subclass_proc_list)
        SetWindowSubclass(self._hwnd, self.pfn_subclass_list, 0, 0)

        # Update the image list if the font changes, and back color of the List-View UI
        # when the back color of the Panel changes.
        self.native.FontChanged += WeakrefCallable(self.winforms_font_changed)
        self.native.BackColorChanged += WeakrefCallable(
            self.winforms_back_color_changed
        )

    ####################################################################################
    # Methods dealing with the geometry of the DetailedList.
    ####################################################################################

    @property
    def _width(self) -> int:
        return self.native.Size.Width

    @property
    def _height(self) -> int:
        return self.native.Size.Height

    def _tile_width(self, width: int | None = None, height: int | None = None) -> int:
        width = self._width if width is None else width
        height = self._height if height is None else height

        if self._v_scroll_visible(height):
            return width - self._v_scroll_width
        else:
            return width

    @property
    def _tile_height(self) -> int:
        return (self._font_height + self._tile_padding) * 2

    @property
    def _tile_padding(self) -> int:
        return sum(divmod(self._font_height, 2))

    @property
    def _tile_padding_small(self) -> int:
        return sum(divmod(self._font_height, 4))

    @property
    def _font_height(self) -> int:
        return self.native.FontHeight

    @property
    def _icon(self) -> int:
        return self._font_height * 2

    @property
    def _v_scroll_width(self) -> int:
        return u32.GetSystemMetrics(wc.SM_CXVSCROLL)

    def _v_scroll_visible(self, height: int) -> bool:
        # The 2 here is undocumented, but appears to be necessary. The most likely
        # explanation is that the drawn region for each tile begins 1 pixel down and
        # ends 1 pixel up.
        #
        # Note that built in methods for determining whether the scrollbar is present
        # are reactive and lead to poor performance.
        if self._data is None:
            data_length = 0
        else:
            data_length = len(self._data)
        return height + 2 < data_length * self._tile_height

    def _tile_view_info(self, width: int, height: int) -> cc32_cls.LVTILEVIEWINFO:
        lvtileviewinfo = cc32_cls.LVTILEVIEWINFO()
        lvtileviewinfo.cbSize = sizeof(lvtileviewinfo)
        lvtileviewinfo.dwMask = wc.LVTVIM_TILESIZE | wc.LVTVIM_LABELMARGIN
        lvtileviewinfo.dwFlags = wc.LVTVIF_FIXEDSIZE
        lvtileviewinfo.sizeTile = SIZE(
            self._tile_width(width, height),
            self._tile_height,
        )
        lvtileviewinfo.rcLabelMargin = RECT(
            self._tile_padding,
            0,
            self._tile_padding,
            0,
        )

        return lvtileviewinfo

    @property
    def _tile_view_info_initial(self) -> cc32_cls.LVTILEVIEWINFO:
        return self._tile_view_info(self._width, self._height)

    @property
    def _mouse_down_x(self) -> int:
        return self._tile_padding + self._font_height

    def _drawing_icon_xy(self, x: int, y: int) -> tuple[int, int]:
        return (x + self._tile_padding_small, y + self._tile_padding)

    def _drawing_select_rect(self, x: int, y: int) -> RECT:
        return RECT(
            x + self._tile_padding_small + self._icon + self._tile_padding,
            y + self._tile_padding,
            x + self._tile_width() - self._tile_padding_small,
            y + self._tile_padding + 2 * self._font_height,
        )

    def _drawing_title_rect(self, x: int, y: int) -> RECT:
        return RECT(
            x + self._tile_padding_small + self._icon + self._tile_padding,
            y + self._tile_padding,
            x + self._tile_width() - self._tile_padding_small,
            y + self._tile_padding + self._font_height,
        )

    def _drawing_subtitle_rect(self, x: int, y: int) -> RECT:
        return RECT(
            x + self._tile_padding_small + self._icon + self._tile_padding,
            y + self._tile_padding + self._font_height,
            x + self._tile_width() - self._tile_padding_small,
            y + self._tile_padding + 2 * self._font_height,
        )

    ####################################################################################
    # WinForms event handlers.
    ####################################################################################

    def winforms_back_color_changed(self, sender, e):
        """Updates the back color of the Win32 List-View UI to match the WinForms Panel."""
        color = ColorTranslator.ToWin32(self.native.BackColor)
        u32.SendMessageW(self._hwnd, wc.LVM_SETBKCOLOR, 0, color)

    def winforms_font_changed(self, sender, e):
        """Updates the Win32 List-View UI to match the fonts of the WinForms Panel."""
        # Note that reconstructing the image list instead of simply changing the image
        # size seems to reduce selection flicker.
        self._set_image_list()
        self._update_data()

    def winforms_handle_created(self, sender, e):
        """Sets the Panel subclass process when a handle is created for the Panel."""
        self._panel_hwnd = HWND(int(self.native.Handle.ToString()))
        SetWindowSubclass(self._panel_hwnd, self.pfn_subclass_panel, 0, 0)

    def winforms_handle_destroyed(self, sender, e):  # pragma: no cover
        """Removes the Panel subclass process when the Panel's handle is destroyed.

        This is needed to prevent memory leaks.
        """
        # WinForms handles may be destroyed, but also may remain unchanged.
        RemoveWindowSubclass(self._panel_hwnd, self.pfn_subclass_panel, 0)

    ####################################################################################
    # Methods dealing with the subclass processes.
    ####################################################################################

    def __del__(self):
        # The objects self.pfn_subclass_list and self.pfn_subclass_panel are python
        # classes that are also part of the native Windows process. When a DetailedList
        # instance is removed by the python GC, these subclass processes are also
        # removed and the Windows process has a dangling pointer. Calling Dispose() here
        # fixes the problem by removing the subclass processes from the Windows process.
        self._image_list.Dispose()
        self.native.Dispose()

        # This RemoveWindowSubclass shouldn't be necessary but the testbed throws an
        # error without it.
        RemoveWindowSubclass(self._hwnd, self.pfn_subclass_list, 0)

    def _subclass_proc_panel(
        self,
        hWnd: int,
        uMsg: int,
        wParam: int,
        lParam: int,
        uIdSubclass: int,
        dwRefData: int,
    ):
        """The subclass process that receives messages sent to the WinForms Panel."""

        # Remove the window subclass in the way recommended by Raymond Chen here:
        # devblogs.microsoft.com/oldnewthing/20031111-00/?p=41883
        if uMsg == wc.WM_NCDESTROY:
            RemoveWindowSubclass(hWnd, self.pfn_subclass_panel, uIdSubclass)

        elif uMsg == wc.WM_NOTIFY:
            phdr = cast(lParam, POINTER(u32_cls.NMHDR)).contents

            # Messages from the List-View UI to itself (usually WM_REFLECT_NOTIFY).
            if phdr.hwndFrom == self._hwnd:
                code = phdr.code

                if code == wc.NM_CUSTOMDRAW:
                    nmlvcd = cast(lParam, POINTER(cc32_cls.NMLVCUSTOMDRAW)).contents
                    return_flag = self._nm_customdraw(nmlvcd)
                    if return_flag is not None:
                        return return_flag
                    else:  # pragma: no cover
                        # return_flag is None only when incorrect NM_CUSTOMDRAW have
                        # been sent. This is a known bug.
                        pass

                elif code == wc.LVN_ODCACHEHINT:
                    nmlvch = cast(lParam, POINTER(cc32_cls.NMLVCACHEHINT)).contents
                    self._lvn_odcachehint(nmlvch.iFrom, nmlvch.iTo)

                elif code == wc.LVN_ITEMCHANGED:
                    nmlv = cast(lParam, POINTER(cc32_cls.NMLISTVIEW)).contents
                    self._lvn_item_changed(nmlv)

            else:  # pragma: no cover
                # This code block is for processing WM_NOTIFY messages that are not
                # destined for the List-View UI (self._hwnd). However none of these
                # messages are sent under normal operations.
                pass

        # Resize List-View UI to be the same size as the WinForms Panel parent.
        # learn.microsoft.com/en-us/windows/win32/winmsg/wm-size
        elif uMsg == wc.WM_SIZE:
            self._wm_size(loword(lParam), hiword(lParam))

        # Call the original window procedure
        return DefSubclassProc(HWND(hWnd), UINT(uMsg), WPARAM(wParam), LPARAM(lParam))

    def _subclass_proc_list(
        self,
        hWnd: int,
        uMsg: int,
        wParam: int,
        lParam: int,
        uIdSubclass: int,
        dwRefData: int,
    ):
        # Remove the window subclass in the way recommended by Raymond Chen here:
        # devblogs.microsoft.com/oldnewthing/20031111-00/?p=41883
        if uMsg == wc.WM_NCDESTROY:
            RemoveWindowSubclass(hWnd, self.pfn_subclass_list, uIdSubclass)

        elif uMsg in wc.BUTTONDOWN:
            lParam = self._button_down_event(uMsg, lParam)

        elif uMsg in wc.BUTTONUP:
            lParam = self._button_up_event(uMsg, lParam)

        elif uMsg in wc.BUTTONDBLCLK:
            lParam = self._button_event(lParam)

        elif uMsg in (wc.WM_SETFOCUS, wc.WM_KILLFOCUS):
            if self._selected_index is not None:
                self._invalidate_tile(self._selected_index)

        # Call the original window procedure
        return DefSubclassProc(HWND(hWnd), UINT(uMsg), WPARAM(wParam), LPARAM(lParam))

    ####################################################################################
    # Methods that handle the subclass process messages.
    ####################################################################################

    def _nm_customdraw(self, nmlvcd) -> int | None:
        """Draws the tiles."""
        # learn.microsoft.com/en-us/windows/win32/controls/using-custom-draw
        draw_stage = nmlvcd.nmcd.dwDrawStage

        # Returning CDRF_NOTIFYITEMDRAW means the next message will be CDDS_ITEMPREPAINT
        # where the drawing is done.
        if draw_stage == wc.CDDS_PREPAINT:
            return wc.CDRF_NOTIFYITEMDRAW

        # This is the draw stage where the tile is drawn.
        elif draw_stage == wc.CDDS_ITEMPREPAINT:
            index = nmlvcd.nmcd.dwItemSpec

            # Account for known bugs in the custom draw process.
            if (
                self._data is None or index < 0 or index >= len(self._data)
            ):  # pragma: no cover
                # The custom draw process is known to occasionally send incorrect
                # messages.
                return

            hdc = HDC(nmlvcd.nmcd.hdc)
            rect = RECT.from_buffer_copy(nmlvcd.nmcd.rc)
            item = self._retrieve_virtual_item(index)

            text_format = wc.DT_SINGLELINE | wc.DT_VCENTER | wc.DT_WORD_ELLIPSIS
            is_selected = index == self.get_selection()
            has_focus = u32.GetFocus() == self._hwnd

            y = rect.top + divmod(self._tile_height - rect.bottom + rect.top, 2)[0]

            if is_selected:
                # Unfocused colors are undocumented.
                select_back = wc.COLOR_HIGHLIGHT if has_focus else wc.COLOR_BTNFACE
                select_text = wc.COLOR_HIGHLIGHTTEXT if has_focus else wc.COLOR_BTNTEXT
                gdi32.SetTextColor(hdc, u32.GetSysColor(select_text))

                # See documentation for "+1".
                rect = self._drawing_select_rect(x=0, y=y)
                u32.FillRect(hdc, byref(rect), select_back + 1)

            rect = self._drawing_title_rect(x=0, y=y)
            u32.DrawTextW(hdc, item[0], -1, byref(rect), text_format)

            rect = self._drawing_subtitle_rect(x=0, y=y)
            u32.DrawTextW(hdc, item[1], -1, byref(rect), text_format)

            icon_xy = self._drawing_icon_xy(x=0, y=y)
            ImageList_Draw(
                HWND(int(self._image_list.Handle.ToString())),
                item[2],
                hdc,
                icon_xy[0],
                icon_xy[1],
                wc.ILD_SELECTED if is_selected else wc.ILD_NORMAL,
            )

            # Returning CDRF_SKIPDEFAULT means that the control will not draw the item.
            return wc.CDRF_SKIPDEFAULT

        else:  # pragma: no cover
            # The draw stage messages after CDDS_PREPAINT of custom draw should only be
            # received if they are requested using appropriate return flags. However,
            # custom draw is known to occasionally send incorrect messages.
            pass

    def _lvn_odcachehint(self, index_from, index_to):
        """Processes the Win32 List-View UI cache hint."""
        # Note that this is the same method as winforms_cache_virtual_items from the
        # WinForms Table widget.
        if (
            self._cache
            and index_from >= self._first_item
            and index_to < self._first_item + len(self._cache)
        ):
            # If the newly requested cache is a subset of the old cache,
            # no need to rebuild everything, so do nothing
            return

        # Now the cache needs to be rebuilt.
        self._first_item = index_from
        new_length = index_to - index_from + 1
        self._cache = []

        # Fill the cache with appropriate items.
        for i in range(new_length):
            self._cache.append(self._new_item(i + self._first_item))

    def _lvn_item_changed(self, nmlv):
        """Processes change of selected and focused indices."""
        # learn.microsoft.com/en-us/windows/win32/controls/lvn-itemchanged
        # learn.microsoft.com/en-us/windows/win32/api/commctrl/ns-commctrl-nmlistview

        if not is_submessage(nmlv.uChanged, wc.LVIF_STATE):  # pragma: no cover
            # The List-View UI is in virtual mode and changes to the data occur in
            # python. At which point the cache is deleted and rebuilt. This means that
            # the only changes which trigger LVN_ITEMCHANGED are state changes. So
            # this block should never be accessed.
            return

        state_types = (
            (wc.LVIS_FOCUSED, self._process_focus),
            (wc.LVIS_SELECTED, self._process_select),
        )
        for state_flag, process_function in state_types:
            # uNewState and uOldState have values determined by List-View Item States
            # learn.microsoft.com/en-us/windows/win32/controls/list-view-item-states
            old_state = is_submessage(nmlv.uOldState, state_flag)
            new_state = is_submessage(nmlv.uNewState, state_flag)

            # Process change of state.
            if new_state != old_state:
                process_function(nmlv.iItem, new_state)

    def _wm_size(self, width: int, height: int):
        """Resizes the Win32 List-View UI and its tiles to match the WinForms Panel."""
        tile_view_info = self._tile_view_info(width, height)
        u32.SendMessageW(self._hwnd, wc.LVM_SETTILEVIEWINFO, 0, byref(tile_view_info))

        u32.SetWindowPos(
            self._hwnd,
            self._panel_hwnd,
            0,
            0,
            width,
            height,
            wc.SWP_NOMOVE | wc.SWP_NOZORDER | wc.SWP_SHOWWINDOW,
        )

    def _button_event(self, lParam: int) -> int:
        """Moves a button event over the icon of a tile."""
        # https://learn.microsoft.com/en-us/windows/win32/inputdev/wm-lbuttondown
        # In the documentation the LOWORD/HIWORD method used here is not recommended,
        # because it doesn't take into account the negative coordinates that arise in
        # mulit-monitor setups. However, here the coordinates are relative to the client
        # area, and hence will always be positive.
        loword_value = self._font_height
        hiword_value = hiword(lParam)
        return loword_value | (hiword_value << 16)

    def _button_down_event(self, uMsg: int, lParam: int) -> int:
        if uMsg == wc.WM_RBUTTONDOWN:
            self._rbuttondown_lparam = lParam

        u32.SetFocus(self._hwnd)
        return self._button_event(lParam)

    def _button_up_event(self, uMsg: int, lParam: int) -> int:
        if (
            uMsg == wc.WM_RBUTTONUP
            and self._rbuttondown_lparam == lParam
            and u32.GetFocus() == self._hwnd
        ):
            self.native.OnMouseClick(
                WinForms.MouseEventArgs(
                    WinForms.MouseButtons.Right,
                    clicks=1,
                    x=loword(lParam),
                    y=hiword(lParam),
                    delta=0,
                )
            )

        return self._button_event(lParam)

    ####################################################################################
    # Internal methods.
    ####################################################################################

    def actions(self, x: int, y: int) -> list[tuple[str, Callable[[], None]]]:
        hit_test_info = cc32_cls.LVHITTESTINFO()
        hit_test_info.pt = POINT(self._mouse_down_x, y)
        u32.SendMessageW(self._hwnd, wc.LVM_HITTEST, 0, byref(hit_test_info))

        # iItem will be less than 0 if there is no item when the hit test is performed.
        index = hit_test_info.iItem
        if (
            not self.primary_action_enabled
            and not self.secondary_action_enabled
            and index >= 0
        ):
            return []

        row = self.interface.data[index]
        actions_list = []

        if self.primary_action_enabled:

            def primary():
                return self.interface.on_primary_action(row=row)

            actions_list.append((self.interface._primary_action, primary))

        if self.secondary_action_enabled:

            def secondary():
                return self.interface.on_secondary_action(row=row)

            actions_list.append((self.interface._secondary_action, secondary))

        return actions_list

    def _invalidate_tile(self, index: int):
        rect = RECT()
        u32.SendMessageW(self._hwnd, wc.LVM_GETITEMRECT, index, byref(rect))
        rect.right = self._tile_width()
        u32.InvalidateRect(self._hwnd, byref(rect), True)

    def _process_focus(self, index: int, is_focused: bool):
        if is_focused:
            self._focused_index = index
        else:
            self._invalidate_tile(index)
            self._focused_index = None

    def _process_select(self, index: int, is_selected: bool):
        # The Win32 selection-change process consists of a sequence of messages.
        # (Note that since LVS_SINGLESEL is used an item can be focused but not
        # selected, but under normal operations a selected item is always focused.)
        #
        # a) If an item is selected and another item becomes selected there are 3
        #    messages:
        #   1. Old item with index=iItem loses focus.
        #   2. All items are deselected with iItem=-1.
        #   3. New item with index=iItem gains focus and selection.
        # b) If an item is selected and then no item is selected (for example when
        #    clicking in the client area where there are no items) then only message 2
        #    is sent.
        # c) If no item is selected or focused then only message 3 is sent.
        # d) If no item is selected by an item is focused then message 2 is not sent.

        # A message with a positive index corresponds to a message of type 3 (above),
        # so select the item and ensure that the tile is fully redrawn.
        if index >= 0:
            self._selected_index = index
            self._invalidate_tile(index)

        # A message with a negative index means that all items are being deselected.
        # If the focus is not None, then all items are being deselected i.e. situation
        # b) above.
        elif self._focused_index is not None:
            self._selected_index = None
            self._invalidate_tile(self._focused_index)

        # This code block corresponds to message 2 in situation a) above. The new tile
        # will be selected during message 3 so nothing needs to be done here.
        else:
            return

        u32.UpdateWindow(self._hwnd)
        self.interface.on_select()

    def _set_image_list(self):
        # Dispose of the existing image list (if it exists).
        try:
            self._image_list.Dispose()
        except AttributeError:
            pass

        # Create the image list
        self._image_list = WinForms.ImageList()
        self._image_list.ImageSize = Size(self._icon, self._icon)
        image_list_hwnd = HWND(int(self._image_list.Handle.ToString()))

        # Register the image list
        u32.SendMessageW(
            self._hwnd, wc.LVM_SETIMAGELIST, wc.LVSIL_NORMAL, image_list_hwnd
        )

    def _image_index(self, icon):
        images = self._image_list.Images
        key = str(icon.path)
        index = images.IndexOfKey(key)
        if index == -1:
            index = images.Count
            images.Add(key, icon.bitmap)
        return index

    def _new_item(self, index) -> tuple[str, str, int]:
        row = self._data[index]

        title, subtitle, icon = (
            getattr(row, attr, None) for attr in self.interface.accessors
        )

        return (
            str(self._missing_value) if title is None else str(title),
            str(self._missing_value) if subtitle is None else str(subtitle),
            -1 if icon is None else self._image_index(icon._impl),
        )

    def _retrieve_virtual_item(self, index: int):
        # Note that this is the same method as winforms_retrieve_virtual_item from the
        # WinForms Table widget.
        if (
            self._cache
            and index >= self._first_item
            and index < self._first_item + len(self._cache)
        ):
            return self._cache[index - self._first_item]
        else:
            return self._new_item(index)

    def _update_data(self):
        if self._data is None:
            data_length = 0
        else:
            data_length = len(self._data)

        u32.SendMessageW(self._hwnd, wc.LVM_SETITEMCOUNT, data_length, 0)
        self._cache = []

    ####################################################################################
    # Methods called by the Core interface
    ####################################################################################

    def scroll_to_row(self, index):
        u32.SendMessageW(self._hwnd, wc.LVM_ENSUREVISIBLE, index, False)

    def get_selection(self):
        return self._selected_index

    def change_source(self, source):
        self._update_data()

    def set_primary_action_enabled(self, enabled):
        self.primary_action_enabled = enabled

    def set_secondary_action_enabled(self, enabled):
        self.secondary_action_enabled = enabled

    def set_refresh_enabled(self, enabled):
        pass
        # self.refresh_enabled = enabled

    after_on_refresh = None

    ####################################################################################
    # Methods called by the DetailedListSource
    ####################################################################################

    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def insert(self, index, item):
        import warnings

        warnings.warn(
            "The insert() method is deprecated. Use source_insert() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_insert(index=index, item=item)

    def source_insert(self, *, index, item):
        self._update_data()

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
        index = self._data.index(item)
        self._invalidate_tile(index)
        u32.UpdateWindow(self._hwnd)
        self._update_data()

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def remove(self, index, item):
        import warnings

        warnings.warn(
            "The remove() method is deprecated. Use source_remove() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_remove(index=index, item=item)

    def source_remove(self, *, index, item):
        self._update_data()

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def clear(self):
        import warnings

        warnings.warn(
            "The clear() method is deprecated. Use source_clear() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_clear()

    def source_clear(self):
        self._update_data()
