from __future__ import annotations

from ctypes import POINTER, Structure, byref, sizeof, windll
from ctypes.wintypes import HINSTANCE, HWND, LPARAM, LPWSTR, RECT, UINT
from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from ctypes import _CData


class TOOLINFO(Structure):
    _fields_: Sequence[tuple[str, type[_CData]] | tuple[str, type[_CData], int]] = [
        ("cbSize", UINT),
        ("uFlags", UINT),
        ("hwnd", HWND),
        ("uId", POINTER(UINT)),
        ("rect", RECT),
        ("hinst", HINSTANCE),
        ("lpszText", LPWSTR),
        ("lParam", LPARAM)
    ]


def create_tooltip(hwnd, text):
    TTS_ALWAYSTIP = 0x01
    TTM_ADDTOOL = 0x0400 + 50
    hwndTT = windll.user32.CreateWindowExW(
        0, "tooltips_class32", None, TTS_ALWAYSTIP,
        0, 0, 0, 0, hwnd, None, None, None
    )
    ti = TOOLINFO(cbSize=sizeof(TOOLINFO), hwnd=hwnd, lpszText=text)
    windll.user32.SendMessageW(hwndTT, TTM_ADDTOOL, 0, byref(ti))
    return hwndTT

# Example usage:
# hwnd = some_window_handle
# create_tooltip(hwnd, "This is a tooltip")
