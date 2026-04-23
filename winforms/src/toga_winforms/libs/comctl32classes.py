from ctypes import (
    WINFUNCTYPE,
    Structure as c_Structure,
)
from ctypes.wintypes import (
    COLORREF,
    DWORD,
    HDC,
    HWND,
    INT,
    LPARAM,
    LPWSTR,
    POINT,
    RECT,
    SIZE,
    UINT,
    WPARAM,
)

from .win32 import DWORD_PTR, INT_PTR, LRESULT, PUINT, UINT_PTR


# learn.microsoft.com/en-us/windows/win32/api/commctrl/ns-commctrl-initcommoncontrolsex
class INITCOMMONCONTROLSEX(c_Structure):
    _fields_ = [
        ("dwSize", DWORD),
        ("dwICC", DWORD),
    ]


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


# learn.microsoft.com/en-us/windows/win32/api/commctrl/ns-commctrl-lvhittestinfo
class LVHITTESTINFO(c_Structure):
    _fields_ = [
        ("pt", POINT),
        ("flags", UINT),
        ("iItem", INT),
        ("iSubItem", INT),
        ("iGroup", INT),
    ]


# learn.microsoft.com/en-us/windows/win32/api/commctrl/ns-commctrl-lvtileviewinfo
class LVTILEVIEWINFO(c_Structure):
    _fields_ = [
        ("cbSize", UINT),
        ("dwMask", DWORD),
        ("dwFlags", DWORD),
        ("sizeTile", SIZE),
        ("cLines", INT),
        ("rcLabelMargin", RECT),
    ]


# Import .user32classes here to avoid circular reference.
from .user32classes import NMHDR  # noqa


# https://learn.microsoft.com/en-us/windows/win32/api/commctrl/ns-commctrl-nmcustomdraw
class NMCUSTOMDRAW(c_Structure):
    _fields_ = [
        ("hdr", NMHDR),
        ("dwDrawStage", DWORD),
        ("hdc", HDC),
        ("rc", RECT),
        ("dwItemSpec", DWORD_PTR),
        ("uItemState", UINT),
        ("lItemlParam", LPARAM),
    ]


# learn.microsoft.com/en-us/windows/win32/api/commctrl/ns-commctrl-nmitemactivate
class NMITEMACTIVATE(c_Structure):
    _fields_ = [
        ("hdr", NMHDR),
        ("iItem", INT),
        ("iSubItem", INT),
        ("uNewState", UINT),
        ("uOldState", UINT),
        ("uChanged", UINT),
        ("ptAction", POINT),
        ("lParam", LPARAM),
        ("uKeyFlags", UINT),
    ]


# https://learn.microsoft.com/en-us/windows/win32/api/commctrl/ns-commctrl-nmlistview
class NMLISTVIEW(c_Structure):
    _fields_ = [
        ("hdr", NMHDR),
        ("iItem", INT),
        ("iSubItem", INT),
        ("uNewState", UINT),
        ("uOldState", UINT),
        ("uChanged", UINT),
        ("ptAction", POINT),
        ("lParam", LPARAM),
    ]


# https://learn.microsoft.com/en-us/windows/win32/api/commctrl/ns-commctrl-nmlvcachehint
class NMLVCACHEHINT(c_Structure):
    _fields_ = [
        ("hdr", NMHDR),
        ("iFrom", INT),
        ("iTo", INT),
    ]


# https://learn.microsoft.com/en-us/windows/win32/api/commctrl/ns-commctrl-nmlvcustomdraw
class NMLVCUSTOMDRAW(c_Structure):
    _fields_ = [
        ("nmcd", NMCUSTOMDRAW),
        ("clrText", COLORREF),
        ("clrTextBk", COLORREF),
        ("iSubItem", INT),
        ("dwItemType", DWORD),
        ("clrFace", COLORREF),
        ("iIconEffect", INT),
        ("iIconPhase", INT),
        ("iPartId", INT),
        ("iStateId", INT),
        ("rcText", RECT),
        ("uAlign", UINT),
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
