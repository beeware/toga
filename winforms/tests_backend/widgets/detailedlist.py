import asyncio
from ctypes import byref, sizeof, windll
from ctypes.wintypes import HWND, POINT, RECT, UINT

import System.Windows.Forms as WinForms
from System.Drawing import Bitmap, Point

from toga_winforms.libs import win32constants as wc, win32structures as ws
from toga_winforms.libs.user32 import (
    ClientToScreen,
    PostMessageW,
    SendMessageW,
    SetFocus,
    SetForegroundWindow,
)

from .base import SimpleProbe

# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendinput
# Note that the argtypes attribute has not been set since one of the arguments is
# a variable length array.
SendInput = windll.user32.SendInput
SendInput.restype = UINT


class DetailedListProbe(SimpleProbe):
    native_class = WinForms.Panel
    supports_actions = True
    supports_refresh = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._click_shift = 0

    @property
    def row_count(self):
        return SendMessageW(self.impl._hwnd, wc.LVM_GETITEMCOUNT, 0, 0)

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

    def _row_rect(self, row) -> RECT:
        rect = RECT()
        SendMessageW(self.impl._hwnd, wc.LVM_GETITEMRECT, row, byref(rect))
        rect.right = self.impl._tile_width()
        return rect

    def _row_midpoint(self, row) -> tuple[int, int]:
        # Pick a point half way across horizontally, and half way down the row.
        rect = self._row_rect(row)

        return (
            divmod(rect.right + rect.left, 2)[0],
            divmod(rect.bottom + rect.top, 2)[0],
        )

    @property
    def client_midpoint(self) -> tuple[int, int]:
        native = self.impl.native
        client_rect = native.ClientRectangle

        return (
            divmod(client_rect.Left + client_rect.Right, 2)[0],
            divmod(client_rect.Top + client_rect.Bottom, 2)[0],
        )

    @property
    def max_scroll_position(self):
        top = self._row_rect(0).top
        bottom = self._row_rect(self.row_count - 1).bottom
        document_height = bottom - top

        return (document_height - self.native.ClientSize.Height) / self.scale_factor

    @property
    def scroll_position(self):
        top = self._row_rect(0).top

        return -round(top / self.scale_factor)

    def scroll_to_top(self):
        SendMessageW(self.impl._hwnd, wc.LVM_ENSUREVISIBLE, 0, 0)

    async def wait_for_scroll_completion(self):
        # No animation associated with scroll, so this is a no-op
        pass

    async def select_row(self, row, add=False):
        x, y = self._row_midpoint(row)
        await self._perform_click(x, y, modifier=add)

    async def deselect_all(self):
        # Assume there is blank space at the bottom of the client area.
        row_count = self.row_count
        x, y = self._row_midpoint(row_count - 1)
        y = y + self.impl._tile_height

        delta = (int(self.scale_factor) * 5,) * 2
        await self._perform_click(x, y, right=True, delta=delta)

    async def _perform_action(self, row, index):
        x, y = self._row_midpoint(row)

        ################################################################################
        # This code is to exercise the non-right click branch of the MouseClick handler
        # for the context menu class.
        #
        # TODO: Move/remove this code if general context menus are implement in Toga or
        # if a WinForms widget is implemented which uses a context menu and which can
        # naturally receive WinForms MouseClick events. The WinForms Panel used for the
        # DetailedList widget is at the back so doesn't receive clicks unless they are
        # forwarded.
        self.impl.native.OnMouseClick(
            WinForms.MouseEventArgs(
                WinForms.MouseButtons.Left,
                clicks=1,
                x=x,
                y=y,
                delta=0,
            )
        )
        ################################################################################

        context_menu_list = self.impl._context_menu.actions(x, y)
        context_menu_index = index + 1 if self.impl.refresh_enabled else index
        if context_menu_index >= len(context_menu_list) - 1:
            context_menu_index = -1

        await self._select_from_context_menu(x, y, context_menu_index)

    async def perform_primary_action(self, row, active=True):
        await self._perform_action(row, 0)

    async def perform_secondary_action(self, row, active=True):
        await self._perform_action(row, 1 if self.impl.primary_action_enabled else 0)

    def refresh_available(self):
        # This test is mainly for scroll refresh at the top of the list.
        # return self.impl.refresh_enabled
        return self.scroll_position <= 0

    async def non_refresh_action(self):
        x, y = self.client_midpoint

        await self._select_from_context_menu(x, y, -1)

    async def refresh_action(self, active=True):
        x, y = self.client_midpoint

        # Get the item index for the context menu. -1 closes the context menu.
        if (
            self.impl.primary_action_enabled or self.impl.secondary_action_enabled
        ) and len(self.impl._context_menu.actions(x, y)) < 3:
            index = -1
        else:
            index = 0

        await self._select_from_context_menu(x, y, index)

        # Extra delay to ensure that the refresh occurs.
        await asyncio.sleep(0.2)

    async def _select_from_context_menu(self, x, y, index):
        # Perform the right click that opens the context menu.
        await self._perform_click(x, y, right=True)

        await self.redraw("Context menu displayed.", delay=0.2)

        # Select menu item with keyboard.
        await self._select_with_keyboard(index)

        if index < 0:
            await self.redraw("Context menu exited with the 'Esc' key.", delay=0.1)
        else:
            await self.redraw("Context menu item selected via the keyboard.", delay=0.1)

    async def _perform_click(
        self,
        x,
        y,
        right=False,
        double=False,
        modifier=False,
        delta=(0, 0),
    ):
        window_hwnd = HWND(int(self.widget.window._impl.native.Handle.ToString()))
        SetForegroundWindow(window_hwnd)

        hwnd = self.impl._hwnd
        SetFocus(hwnd)

        # Move the cursor to the click location and shift the location to prevent
        # unwanted double clicks
        point = POINT(x + self._click_shift, y)
        ClientToScreen(hwnd, point)
        WinForms.Cursor.Position = Point(point.x, point.y)

        INPUT_ARRAY = ws.INPUT * 1
        mouse_inputs = INPUT_ARRAY()
        mouse_inputs[0] = ws.INPUT()
        mouse_inputs[0].type = 0
        mouse_inputs[0]._.mi = ws.MOUSEINPUT(0, 0, 0, 0, 0)

        if modifier:
            modifier_inputs = INPUT_ARRAY()
            modifier_inputs[0] = ws.INPUT()
            modifier_inputs[0].type = 1
            modifier_inputs[0]._.ki = ws.KEYBDINPUT(wc.VK_CONTROL, 0, 0, 0, 0)

            return_value = SendInput(1, modifier_inputs, sizeof(ws.INPUT))
            if return_value != 1:
                raise Exception(
                    "SendInput failed. Type: Keyboard, Keys: VK_CONTROL (down)."
                )
            await asyncio.sleep(0.05)

        if right:
            message_list = [wc.MOUSEEVENTF_RIGHTDOWN, wc.MOUSEEVENTF_RIGHTUP]
        else:
            message_list = [wc.MOUSEEVENTF_LEFTDOWN, wc.MOUSEEVENTF_LEFTUP]

        async def click():
            for i, message in enumerate(message_list):
                mouse_inputs[0]._.mi.dwFlags = message
                return_value = SendInput(1, mouse_inputs, sizeof(ws.INPUT))
                if return_value != 1:
                    raise Exception(
                        f"SendInput failed. Type: Mouse, right button: {right}."
                    )

                if i == 0:
                    point.x = point.x + delta[0]
                    point.y = point.y + delta[1]
                    WinForms.Cursor.Position = Point(point.x, point.y)

                await asyncio.sleep(0.05)

        await click()

        if double:
            await asyncio.sleep(0.2)
            await click()

        if modifier:
            modifier_inputs[0]._.ki.dwFlags = wc.KEYEVENTF_KEYUP

            return_value = SendInput(1, modifier_inputs, sizeof(ws.INPUT))
            if return_value != 1:
                raise Exception(
                    "SendInput failed. Type: Keyboard, Keys: VK_CONTROL (up)."
                )
            await asyncio.sleep(0.05)

        self._click_shift += int(self.scale_factor)

        await asyncio.sleep(0.1)

    async def _select_with_keyboard(self, index):
        hwnd = self.impl._hwnd
        # For some reason we have to use PostMessage and not SendMessage here. This
        # is most likely because TrackPopupMenu is thread blocking.
        if index < 0:
            PostMessageW(hwnd, wc.WM_KEYDOWN, wc.VK_ESCAPE, 0)
            await asyncio.sleep(0.1)
            PostMessageW(hwnd, wc.WM_KEYUP, wc.VK_ESCAPE, 0)
            await asyncio.sleep(0.1)
            return

        for _i in range(index + 1):
            PostMessageW(hwnd, wc.WM_KEYDOWN, wc.VK_DOWN, 0)
            await asyncio.sleep(0.1)
            PostMessageW(hwnd, wc.WM_KEYUP, wc.VK_DOWN, 0)
            await asyncio.sleep(0.1)

        PostMessageW(hwnd, wc.WM_KEYDOWN, wc.VK_RETURN, 0)
        await asyncio.sleep(0.1)
        PostMessageW(hwnd, wc.WM_KEYUP, wc.VK_RETURN, 0)
        await asyncio.sleep(0.1)
