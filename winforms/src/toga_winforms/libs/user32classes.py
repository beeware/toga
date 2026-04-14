from ctypes import WINFUNCTYPE, Structure as c_Structure, Union
from ctypes.wintypes import DWORD, HWND, INT, LONG, LPARAM, UINT, WORD, WPARAM

from .comctl32classes import LVITEMW
from .win32 import DWORD_PTR, LRESULT, UINT_PTR, ULONG_PTR


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-hardwareinput
class HARDWAREINPUT(c_Structure):
    _fields_ = [
        ("uMsg", DWORD),
        ("wParamL", WORD),
        ("wParamH", WORD),
    ]


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-keybdinput
class KEYBDINPUT(c_Structure):
    _fields_ = [
        ("wVk", WORD),
        ("wScan", WORD),
        ("dwFlags", DWORD),
        ("time", DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-mouseinput
class MOUSEINPUT(c_Structure):
    _fields_ = [
        ("dx", LONG),
        ("dy", LONG),
        ("mouseData", DWORD),
        ("dwFlags", DWORD),
        ("time", DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-input
class _INPUT_UNION(Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
        ("hi", HARDWAREINPUT),
    ]


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-input
class INPUT(c_Structure):
    _fields_ = [
        ("type", DWORD),
        ("_", _INPUT_UNION),
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
