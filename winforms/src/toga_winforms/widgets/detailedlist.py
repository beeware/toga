from collections.abc import Callable
from ctypes import POINTER, byref, cast, sizeof
from ctypes.wintypes import HDC, HFONT, HWND, LPARAM, POINT, RECT, SIZE, UINT, WPARAM

import System.Windows.Forms as WinForms
from System.Drawing import ColorTranslator, Size, SystemColors

from toga.handlers import WeakrefCallable

from ..colors import toga_color
from ..libs import gdi32, user32 as u32, win32constants as wc, win32structures as ws
from ..libs.comctl32 import (
    DefSubclassProc,
    ImageList_Draw,
    InitCommonControlsEx,
    RemoveWindowSubclass,
    SetWindowSubclass,
)
from ..libs.fonts import FontDeviceContext
from ..libs.win32misc import hiword, is_submessage, loword
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
    #     during selection, LVN_ITEMCHANGED is handled. To repaint when the widget loses
    #     focus, WM_SETFOCUS and WM_KILLFOCUS are handled.
    #
    # The handling of the mouse events to overcome the incorrect clickable area spawns a
    # new issue where the LVN_RCLICK and WM_RBUTTONUP become unreliable, affecting the
    # ability to use a context menu. The processing of mouse down events by the ListView
    # UI is somewhat complicated. For example, the window messages WM_LBUTTONDOWN and
    # WM_RBUTTONDOWN start new modal event loops to detect dragging (for details see
    # learn.microsoft.com/en-us/windows/win32/controls/listview-message-processing).
    #
    # To overcome the unreliability, all mouse events are handled completely and not
    # forwarded to the default WndProc. Note, that the selection process could be
    # simplified here, but the built-in LVN_ITEMCHANGED messages would still need to be
    # processed for keyboard input. A choice is made to replicate the built-in selection
    # message procedure.
    #
    # The actions are performed by a context menu.

    @property
    def _data(self):
        return self.interface.data

    @property
    def _missing_value(self):
        return self.interface.missing_value

    def create(self):
        self.native = WinForms.Panel()

        # Create and set the Panel subclass procedure.
        self.pfn_subclass_panel = ws.SUBCLASSPROC(self._subclass_proc_panel)
        self.winforms_handle_created(None, None)

        # Update the subclass procedure when the self.native handle is create/destroyed
        self.native.HandleCreated += WeakrefCallable(self.winforms_handle_created)
        self.native.HandleDestroyed += WeakrefCallable(self.winforms_handle_destroyed)

        self._default_background_color = toga_color(SystemColors.Window)
        self._first_item = 0
        self._cache = []

        self._selected_index: int = -1
        self._focused_index: int = -1
        self._rbuttondown_lparam: int | None = None

        # Disable all actions and refresh by default.
        self.primary_action_enabled: bool = False
        self.secondary_action_enabled: bool = False
        self.refresh_enabled: bool = False

        # Create the context menu
        self._context_menu = ContextMenu(self, self._menu_items)

        # According to the MicroSoft documentation, an application must call
        # InitCommonControlsEx before creating a common control. For details as to the
        # purpose of this function call, see Raymond Chen's blog:
        # https://devblogs.microsoft.com/oldnewthing/20050718-16/?p=34913
        init_common_controls_ex = ws.INITCOMMONCONTROLSEX()
        init_common_controls_ex.dwSize = sizeof(ws.INITCOMMONCONTROLSEX)
        init_common_controls_ex.dwICC = wc.ICC_LISTVIEW_CLASSES
        InitCommonControlsEx(byref(init_common_controls_ex))

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

        # Change the view style to tile.
        # learn.microsoft.com/en-us/windows/win32/controls/use-tile-views
        u32.SendMessageW(self._hwnd, wc.LVM_SETVIEW, wc.LV_VIEW_TILE, 0)

        # Configure the tile properties and the image list via winforms_font_changed.
        self.winforms_font_changed(None, None)

        # Create and set the ListView UI (self._hwnd) subclass procedure.
        self.pfn_subclass_list = ws.SUBCLASSPROC(self._subclass_proc_list)
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

    def _tile_view_info(self, width: int, height: int) -> ws.LVTILEVIEWINFO:
        lvtileviewinfo = ws.LVTILEVIEWINFO()
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
        """Matches the back color of the Win32 List-View UI to the WinForms Panel."""
        color = ColorTranslator.ToWin32(self.native.BackColor)
        u32.SendMessageW(self._hwnd, wc.LVM_SETBKCOLOR, 0, color)

    def winforms_font_changed(self, sender, e):
        """Matches the font of the Win32 List-View UI to the WinForms Panel."""
        # Update the tile size.
        tile_view_info = self._tile_view_info(self._width, self._height)
        u32.SendMessageW(self._hwnd, wc.LVM_SETTILEVIEWINFO, 0, byref(tile_view_info))

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
            phdr = cast(lParam, POINTER(ws.NMHDR)).contents

            # Messages from the List-View UI to itself (usually WM_REFLECT_NOTIFY).
            if phdr.hwndFrom == self._hwnd:
                code = phdr.code

                if code == wc.NM_CUSTOMDRAW:
                    nmlvcd = cast(lParam, POINTER(ws.NMLVCUSTOMDRAW)).contents
                    return_flag = self._nm_custom_draw(nmlvcd)
                    if return_flag is not None:
                        return return_flag
                    else:  # pragma: no cover
                        # return_flag is None only when incorrect NM_CUSTOMDRAW have
                        # been sent. This is a known bug.
                        pass

                elif code == wc.LVN_ODCACHEHINT:
                    nmlvch = cast(lParam, POINTER(ws.NMLVCACHEHINT)).contents
                    self._lvn_od_cache_hint(nmlvch.iFrom, nmlvch.iTo)

                elif code == wc.LVN_ITEMCHANGED:
                    nmlv = cast(lParam, POINTER(ws.NMLISTVIEW)).contents
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

        elif uMsg == wc.WM_LBUTTONDOWN:
            return self._wm_l_button_down(lParam)

        elif uMsg == wc.WM_RBUTTONDOWN:
            return self._wm_r_button_down(lParam)

        elif uMsg == wc.WM_RBUTTONUP:
            return self._wm_r_button_up(lParam)

        elif uMsg in wc.WM_BUTTON:
            return 0

        elif uMsg in (wc.WM_SETFOCUS, wc.WM_KILLFOCUS):
            if self._selected_index >= 0:
                self._invalidate_tile(self._selected_index)

        # Call the original window procedure
        return DefSubclassProc(HWND(hWnd), UINT(uMsg), WPARAM(wParam), LPARAM(lParam))

    ####################################################################################
    # Methods that handle the subclass process messages.
    ####################################################################################

    def _nm_custom_draw(self, nmlvcd) -> int | None:
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
            hfont = HFONT(int(self.native.Font.ToHfont().ToString()))
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

            with FontDeviceContext(hdc, hfont):
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

    def _lvn_od_cache_hint(self, index_from, index_to):
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

    def _wm_l_button_down(self, lParam: int) -> int:
        u32.SetFocus(self._hwnd)
        index = self._item_hit_test(hiword(lParam))
        self._set_selection(index)

        return 0

    def _wm_r_button_down(self, lParam: int) -> int:
        self._rbuttondown_lparam = lParam
        return self._wm_l_button_down(lParam)

    def _wm_r_button_up(self, lParam: int) -> int:
        # This is a simple implementation of a mouse "click" event.
        if self._rbuttondown_lparam == lParam and u32.GetFocus() == self._hwnd:
            self.native.OnMouseClick(
                WinForms.MouseEventArgs(
                    WinForms.MouseButtons.Right,
                    clicks=1,
                    x=loword(lParam),
                    y=hiword(lParam),
                    delta=0,
                )
            )

        self._rbuttondown_lparam = None
        return 0

    ####################################################################################
    # Methods dealing with the selection process.
    ####################################################################################

    def _set_selection(self, index: int):
        """Replicates the built-in ListView selection setting procedure."""
        # Only update selection if index differs from the existing selection.
        if index == self._selected_index:
            return

        # The selection setting procedure consists of a subsequence of the sequence:
        #   message_1, message_2, message_3
        # with:
        #   message_1 - Focused item loses focus. Sent when there is an existing focused
        #       item and the new selection is not None (i.e. index != -1).
        #   message_2 - All items are deselected. Sent when there is an existing
        #       selected item.
        #   message_3 - Item with index=index gains focus and selection. Sent when the
        #       new selection is not None (i.e. index != -1).
        send_message_1 = self._focused_index >= 0 and index != -1
        send_message_2 = self._selected_index >= 0
        send_message_3 = index != -1

        uMsg = wc.LVM_SETITEMSTATE
        lvitem = ws.LVITEMW()
        lvitem.mask = wc.LVIF_STATE
        lvitem.state = 0

        if send_message_1:
            lvitem.stateMask = wc.LVIS_FOCUSED
            u32.SendMessageW(self._hwnd, uMsg, self._focused_index, byref(lvitem))

        if send_message_2:
            lvitem.stateMask = wc.LVIS_SELECTED
            u32.SendMessageW(self._hwnd, uMsg, -1, byref(lvitem))

        if send_message_3:
            lvitem.stateMask = wc.LVIS_FOCUSED | wc.LVIS_SELECTED
            lvitem.state = wc.LVIS_FOCUSED | wc.LVIS_SELECTED
            u32.SendMessageW(self._hwnd, uMsg, index, byref(lvitem))

    def _process_focus(self, index: int, is_gaining_focus: bool):
        # The Win32 selection-change process consists of a sequence of messages as
        # described in _set_selection.
        #
        # Only message_1 and message_3 are processed by _process_focus.

        # If is_gaining_focus=True then this is message_3.
        if is_gaining_focus:
            self._focused_index = index

        # If is_gaining_focus=False then this is message_1.
        else:
            self._invalidate_tile(index)
            self._focused_index = -1

    def _process_select(self, index: int, is_selected: bool):
        # The Win32 selection-change process consists of a sequence of messages as
        # described in _set_selection. There are 4 scenarios:
        # a) An item is selected and another item becomes selected. All 3 messages are
        #    sent.
        # b) An item is selected and then no item is selected (for example when clicking
        #    in the client area where there are no items). Only message_2 is sent.
        # c) No item is selected or focused. Only message_3 is sent.
        # d) No item is selected, but an item is focused. Messages 1 and 3 are sent.
        #
        # Notes:
        # - Since LVS_SINGLESEL is used an item can be focused but not selected,
        #   but under normal operations a selected item is always focused.
        # - Only message_2 and message_3 are processed by _process_select.

        # A message with a positive index corresponds to message_3, so select the item
        # and ensure that the tile is fully redrawn.
        if index >= 0:
            self._selected_index = index
            self._invalidate_tile(index)

        # A message with a negative index means that all items are being deselected.
        # If the existing focus is non-negative, then all items are being deselected
        # i.e. situation b) above.
        elif self._focused_index >= 0:
            self._selected_index = -1
            self._invalidate_tile(self._focused_index)

        # This code block corresponds to message 2 in situation a) above. The new tile
        # will be selected during message 3 so nothing needs to be done here.
        else:
            return

        u32.UpdateWindow(self._hwnd)
        self.interface.on_select()

    ####################################################################################
    # Internal methods.
    ####################################################################################

    def _item_hit_test(self, y: int) -> int:
        hit_test_info = ws.LVHITTESTINFO()
        hit_test_info.pt = POINT(self._mouse_down_x, y)
        u32.SendMessageW(self._hwnd, wc.LVM_HITTEST, 0, byref(hit_test_info))

        return hit_test_info.iItem

    def _menu_items(
        self,
        x: int,
        y: int,
    ) -> list[None | tuple[str, Callable[[], None]]]:
        menu_items_list = []

        # Append refresh to the menu items list.
        if self.refresh_enabled:

            def refresh():
                return self.interface.on_refresh()

            menu_items_list.append(("Refresh list", refresh))

        index = self._item_hit_test(y)
        # index will be less than 0 if there is no item where the hit test is performed.
        if (
            not (self.primary_action_enabled or self.secondary_action_enabled)
            or index < 0
        ):
            return menu_items_list

        # Append a space between refresh and the actions if refresh is enabled.
        elif self.refresh_enabled:
            menu_items_list.append(None)

        # Since index is greater than or equal to zero, get the row.
        row = self.interface.data[index]

        if self.primary_action_enabled:

            def primary():
                return self.interface.on_primary_action(row=row)

            menu_items_list.append((self.interface._primary_action, primary))

        if self.secondary_action_enabled:

            def secondary():
                return self.interface.on_secondary_action(row=row)

            menu_items_list.append((self.interface._secondary_action, secondary))

        return menu_items_list

    def _invalidate_tile(self, index: int):
        rect = RECT()
        u32.SendMessageW(self._hwnd, wc.LVM_GETITEMRECT, index, byref(rect))
        rect.right = self._tile_width()
        u32.InvalidateRect(self._hwnd, byref(rect), True)

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
        if self._selected_index < 0:
            return None

        return self._selected_index

    def change_source(self, source):
        self._update_data()

    def set_primary_action_enabled(self, enabled):
        self.primary_action_enabled = enabled

    def set_secondary_action_enabled(self, enabled):
        self.secondary_action_enabled = enabled

    def set_refresh_enabled(self, enabled):
        self.refresh_enabled = enabled

    def after_on_refresh(self, widget, result):
        pass

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
