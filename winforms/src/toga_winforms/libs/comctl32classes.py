from ctypes import (
    WINFUNCTYPE,
    Structure as c_Structure,
)
from ctypes.wintypes import HWND, INT, LPARAM, LPWSTR, UINT, WPARAM

from .win32 import DWORD_PTR, INT_PTR, LRESULT, PUINT, UINT_PTR


# https://learn.microsoft.com/en-us/windows/win32/api/commctrl/ns-commctrl-lvitemw
class LVITEMW(c_Structure):
    _fields_ = [
        ("uiMask", UINT),
        ("iItem", INT),
        ("iSubItem", INT),
        ("state", UINT),
        ("stateMask", UINT),
        ("pszText", LPWSTR),
        ("cchTextMax", INT),
        ("iImage", INT),
        ("lParam", LPARAM),
        ("iIndent", INT),
        ("iGroupId", INT),
        ("cColumns", UINT),
        ("puColumns", PUINT),
        ("piColFmt", INT_PTR),
        ("iGroup", INT),
    ]


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-nmhdr
class NMHDR(c_Structure):
    _fields_ = [
        ("hwndFrom", HWND),
        ("idFrom", UINT_PTR),
        ("code", UINT),
    ]


# https://learn.microsoft.com/en-us/windows/win32/api/commctrl/ns-commctrl-nmlvdispinfow
class NMLVDISPINFOW(c_Structure):
    _fields_ = [
        ("hdr", NMHDR),
        ("item", LVITEMW),
    ]


# https://learn.microsoft.com/en-us/windows/win32/api/commctrl/nc-commctrl-subclassproc
SUBCLASSPROC = WINFUNCTYPE(
    # Return type:
    LRESULT,
    # Argument types:
    HWND,
    UINT,
    WPARAM,
    LPARAM,
    UINT_PTR,
    DWORD_PTR,
)
