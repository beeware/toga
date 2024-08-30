from __future__ import annotations

import ctypes
from ctypes import wintypes
from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from ctypes import _CData

CHOOSECOLOR = ctypes.windll.comdlg32.ChooseColorW
class COLORREF(ctypes.Structure):
    _fields_ = [("rgb", wintypes.DWORD)]

class CHOOSECOLOR(ctypes.Structure):
    _fields_: Sequence[tuple[str, type[_CData]] | tuple[str, type[_CData], int]] = [
        ("lStructSize", wintypes.DWORD),
        ("hwndOwner", wintypes.HWND),
        ("hInstance", wintypes.HINSTANCE),
        ("rgbResult", COLORREF),
        ("lpCustColors", ctypes.POINTER(COLORREF)),
        ("Flags", wintypes.DWORD),
        ("lCustData", wintypes.LPARAM),
        ("lpfnHook", wintypes.LPVOID),
        ("lpTemplateName", wintypes.LPCWSTR)
    ]

def color_picker():
    cc = CHOOSECOLOR()
    cc.lStructSize = ctypes.sizeof(CHOOSECOLOR)
    cc.Flags = 0x00000100  # CC_RGBINIT
    custom_colors = (COLORREF * 16)()
    cc.lpCustColors = custom_colors
    cc.rgbResult = COLORREF()
    if CHOOSECOLOR(ctypes.byref(cc)):
        return (cc.rgbResult.rgb & 0xFF, (cc.rgbResult.rgb >> 8) & 0xFF, (cc.rgbResult.rgb >> 16) & 0xFF)
    return None

color = color_picker()
print(f"Selected color: {color}")
