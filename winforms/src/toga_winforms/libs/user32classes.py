from ctypes import WINFUNCTYPE, Structure as c_Structure
from ctypes.wintypes import HWND, INT, LPARAM, UINT, WPARAM

from .comctl32classes import LVITEMW
from .win32 import DWORD_PTR, LRESULT, UINT_PTR


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


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-scrollinfo
class SCROLLINFO(c_Structure):
    _fields_ = [
        ("cbSize", UINT),
        ("fMask", UINT),
        ("nMin", INT),
        ("nMax", INT),
        ("nPage", UINT),
        ("nPos", INT),
        ("nTrackPos", INT),
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
