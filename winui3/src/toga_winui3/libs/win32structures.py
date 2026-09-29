import ctypes.wintypes as wt
from ctypes import WINFUNCTYPE, Structure as c_Structure, Union, c_size_t

from win32more import Guid

########################################################################################
# Types missing from wintypes
########################################################################################

LRESULT = wt.LPARAM
UINT_PTR = c_size_t
DWORD_PTR = c_size_t


########################################################################################
# Structures
########################################################################################


# https://learn.microsoft.com/windows/win32/api/shellapi/ns-shellapi-notifyicondataw
class _TIMEOUT_VERSION_UNION(Union):
    _fields_ = [
        ("uTimeout", wt.UINT),
        ("uVersion", wt.UINT),
    ]


class NOTIFYICONDATAW(c_Structure):
    _fields_ = [
        ("cbSize", wt.DWORD),
        ("hWnd", wt.HWND),
        ("uID", wt.UINT),
        ("uFlags", wt.UINT),
        ("uCallbackMessage", wt.UINT),
        ("hIcon", wt.HICON),
        ("szTip", wt.WCHAR * 128),
        ("dwState", wt.DWORD),
        ("dwStateMask", wt.DWORD),
        ("szInfo", wt.WCHAR * 256),
        ("_", _TIMEOUT_VERSION_UNION),
        ("szInfoTitle", wt.WCHAR * 64),
        ("dwInfoFlags", wt.DWORD),
        ("guidItem", Guid),
        ("hBalloonIcon", wt.HICON),
    ]


# https://learn.microsoft.com/windows/win32/api/shellapi/ns-shellapi-notifyiconidentifier
class NOTIFYICONIDENTIFIER(c_Structure):
    _fields_ = [
        ("cbSize", wt.DWORD),
        ("hWnd", wt.HWND),
        ("uID", wt.UINT),
        ("guidItem", Guid),
    ]


# https://learn.microsoft.com/windows/win32/api/commctrl/nc-commctrl-subclassproc
SUBCLASSPROC = WINFUNCTYPE(
    # Return type:
    LRESULT,
    # Argument types:
    wt.HWND,
    wt.UINT,
    wt.WPARAM,
    wt.LPARAM,
    UINT_PTR,
    DWORD_PTR,
)
