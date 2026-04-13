import asyncio
from ctypes import byref
from ctypes.wintypes import HWND, POINT, RECT

import System.Windows.Forms as WinForms
from System.Drawing import Bitmap, Point

from toga_winforms.libs import windowconstants as wc
from toga_winforms.libs.user32 import (
    ClientToScreen,
    PostMessageW,
    SendMessageW,
    SetFocus,
    SetForegroundWindow,
)

from .base import SimpleProbe


class DetailedListProbe(SimpleProbe):
    native_class = WinForms.Panel
    supports_actions = True
    supports_refresh = False

    @property
    def row_count(self):
        LVM_GETITEMCOUNT = 0x1000 + 4

        return SendMessageW(self.impl._hwnd, LVM_GETITEMCOUNT, 0, 0)

    def assert_cell_content(self, row, title, subtitle, icon=None):
        title_value, subtitle_value, icon_index = self.impl._retrieve_virtual_item(row)

        assert title_value == title
        assert subtitle_value == subtitle

        if icon is not None:
            imagelist = self.impl._image_list
            size = imagelist.ImageSize
            assert size.Width == size.Height == self.impl._icon

            # The image is resized and copied, so we need to compare the actual
            # pixels.
            actual = imagelist.Images[icon_index]
            expected = Bitmap(icon._impl.bitmap, size)
            count = 0
            for x in range(size.Width):
                for y in range(size.Height):
                    if actual.GetPixel(x, y) == expected.GetPixel(x, y):
                        count += 1

            # There are potentially different algorithms for resizing the icons so
            # assert that at least 94% of the pixels match.
            assert count / (size.Width * size.Height) > 0.94

    def row_rect(self, row) -> RECT:
        LVM_GETITEMRECT = 0x1000 + 14
        rect = RECT()
        SendMessageW(self.impl._hwnd, LVM_GETITEMRECT, row, byref(rect))
        rect.right = self.impl._tile_width()
        return rect

    def row_midpoint(self, row) -> tuple[int, int]:
        # Pick a point half way across horizontally, and half way down the row.
        rect = self.row_rect(row)

        return (
            divmod(rect.right + rect.left, 2)[0],
            divmod(rect.bottom + rect.top, 2)[0],
        )

    @property
    def max_scroll_position(self):
        top = self.row_rect(0).top
        bottom = self.row_rect(self.row_count - 1).bottom
        document_height = bottom - top

        return (document_height - self.native.ClientSize.Height) / self.scale_factor

    @property
    def scroll_position(self):
        top = self.row_rect(0).top

        return -round(top / self.scale_factor)

    def scroll_to_top(self):
        LVM_ENSUREVISIBLE = 0x1000 + 19

        SendMessageW(self.impl._hwnd, LVM_ENSUREVISIBLE, 0, 0)

    async def wait_for_scroll_completion(self):
        # No animation associated with scroll, so this is a no-op
        pass

    async def select_row(self, row, add=False):
        x, y = self.row_midpoint(row)
        await self.perform_click(x, y, use_modifier=add)

    async def deselect_all(self):
        # Assume there is blank space at the bottom of the client area.
        row_count = self.row_count
        x, y = self.row_midpoint(row_count - 1)
        y = y + self.impl._tile_height

        await self.perform_double_click(x, y)

    async def _perform_action(self, row, index):
        x, y = self.row_midpoint(row)

        # This code is to exercise a code block within the context menu class.
        # TODO: Remove this when it is not needed.
        self.impl.native.OnMouseClick(
            WinForms.MouseEventArgs(
                WinForms.MouseButtons.Left,
                clicks=1,
                x=x,
                y=y,
                delta=0,
            )
        )

        # Perform the right click that opens the context menu.
        await self.perform_click(x, y, is_right=True)

        context_actions_list = self.impl._context_menu.actions(x, y)
        if index + 1 > len(context_actions_list):
            self.select_with_keyboard(-1)
            await self.redraw("Action menu displayed and exited.", delay=0.1)
        else:
            self.select_with_keyboard(index)
            await self.redraw("Action menu displayed and action selected.", delay=0.1)

    async def perform_primary_action(self, row, active=True):
        await self._perform_action(row, 0)

    async def perform_secondary_action(self, row, active=True):
        await self._perform_action(row, 1 if self.impl.primary_action_enabled else 0)

    async def perform_click(self, x, y, is_right=False, use_modifier=False):
        hwnd = self.impl._hwnd
        window_hwnd = HWND(int(self.widget.window._impl.native.Handle.ToString()))

        SetForegroundWindow(window_hwnd)
        SetFocus(hwnd)

        # To perform a "click" using Window messages, the mouse must be over the window.
        point = POINT(x, y)
        ClientToScreen(hwnd, point)
        WinForms.Cursor.Position = Point(point.x, point.y)

        # Virtual key codes
        MK_LBUTTON = 0x0001
        MK_RBUTTON = 0x0002
        MK_CONTROL = 0x0008

        # Set the code messages, lparam is the coordinates and wparam is determined by
        # the virtual keys down.
        lparam = x | (y << 16)
        up_wparam = MK_CONTROL if use_modifier else 0
        if is_right:
            down_message = wc.WM_RBUTTONDOWN
            down_wparam = MK_RBUTTON | MK_CONTROL if use_modifier else MK_RBUTTON
            up_message = wc.WM_RBUTTONUP

        else:
            down_message = wc.WM_LBUTTONDOWN
            down_wparam = MK_LBUTTON | MK_CONTROL if use_modifier else MK_LBUTTON
            up_message = wc.WM_LBUTTONUP

        # Perform the click and wait for the messages from PostMessage to be received.
        PostMessageW(hwnd, down_message, down_wparam, lparam)
        await asyncio.sleep(0.1)
        PostMessageW(hwnd, up_message, up_wparam, lparam)
        await asyncio.sleep(0.1)

    async def perform_double_click(self, x, y, is_right=False):
        hwnd = self.impl._hwnd
        window_hwnd = HWND(int(self.widget.window._impl.native.Handle.ToString()))

        SetForegroundWindow(window_hwnd)
        SetFocus(hwnd)

        # To perform a "click" using Window messages, the mouse must be over the window.
        point = POINT(x, y)
        ClientToScreen(hwnd, point)
        WinForms.Cursor.Position = Point(point.x, point.y)

        # Virtual key codes
        MK_LBUTTON = 0x0001
        MK_RBUTTON = 0x0002

        # Set the code messages, lparam is the coordinates and wparam is determined by
        # the virtual keys down.
        lparam = x | (y << 16)
        if is_right:
            message = wc.WM_RBUTTONDBLCLK
            wparam = MK_RBUTTON
        else:
            message = wc.WM_LBUTTONDBLCLK
            wparam = MK_LBUTTON

        # Perform the click and wait for the messages from PostMessage to be received.
        PostMessageW(hwnd, message, wparam, lparam)
        await asyncio.sleep(0.1)

    def select_with_keyboard(self, index):
        hwnd = self.impl._hwnd
        # For some reason we have to use PostMessage and not SendMessage here. This
        # is most likely because TrackPopupMenu is thread blocking.
        if index < 0:
            PostMessageW(hwnd, wc.WM_KEYDOWN, wc.VK_ESCAPE, 0)
            PostMessageW(hwnd, wc.WM_KEYUP, wc.VK_ESCAPE, 0)
            return

        for _i in range(index + 1):
            PostMessageW(hwnd, wc.WM_KEYDOWN, wc.VK_DOWN, 0)
            PostMessageW(hwnd, wc.WM_KEYUP, wc.VK_DOWN, 0)

        PostMessageW(hwnd, wc.WM_KEYDOWN, wc.VK_RETURN, 0)
        PostMessageW(hwnd, wc.WM_KEYUP, wc.VK_RETURN, 0)
