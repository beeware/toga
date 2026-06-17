import ctypes.wintypes as wt
from ctypes import WINFUNCTYPE, Structure as c_Structure, Union, c_size_t, c_void_p

########################################################################################
# Types missing from wintypes
########################################################################################

HIMAGELIST = wt.HANDLE
LRESULT = wt.LPARAM
UINT_PTR = c_size_t
ULONG_PTR = c_size_t
DWORD_PTR = c_size_t
INT_PTR = c_size_t
LPARAM_OBJECT = c_void_p


########################################################################################
# Structures Group 0: Structures not containing structures from other groups.
########################################################################################


# https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-actctxw
class ACTCTXW(c_Structure):
    _fields_ = [
        ("cbSize", wt.ULONG),
        ("dwFlags", wt.DWORD),
        ("lpSource", wt.LPCWSTR),
        ("wProcessorArchitecture", wt.USHORT),
        ("wLangId", wt.LANGID),
        ("lpAssemblyDirectory", wt.LPCWSTR),
        ("lpResourceName", wt.LPCWSTR),
        ("lpApplicationName", wt.LPCWSTR),
        ("hModule", wt.HMODULE),
    ]


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-hardwareinput
class HARDWAREINPUT(c_Structure):
    _fields_ = [
        ("uMsg", wt.DWORD),
        ("wParamL", wt.WORD),
        ("wParamH", wt.WORD),
    ]


# learn.microsoft.com/en-us/windows/win32/api/commctrl/ns-commctrl-initcommoncontrolsex
class INITCOMMONCONTROLSEX(c_Structure):
    _fields_ = [
        ("dwSize", wt.DWORD),
        ("dwICC", wt.DWORD),
    ]


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-keybdinput
class KEYBDINPUT(c_Structure):
    _fields_ = [
        ("wVk", wt.WORD),
        ("wScan", wt.WORD),
        ("dwFlags", wt.DWORD),
        ("time", wt.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]


# https://learn.microsoft.com/en-us/windows/win32/api/commctrl/ns-commctrl-lvitemw
class LVITEMW(c_Structure):
    _fields_ = [
        ("mask", wt.UINT),
        ("iItem", wt.INT),
        ("iSubItem", wt.INT),
        ("state", wt.UINT),
        ("stateMask", wt.UINT),
        ("pszText", wt.LPWSTR),
        ("cchTextMax", wt.INT),
        ("iImage", wt.INT),
        ("lParam", wt.LPARAM),
        ("iIndent", wt.INT),
        ("iGroupId", wt.INT),
        ("cColumns", wt.UINT),
        ("puColumns", wt.PUINT),
        ("piColFmt", INT_PTR),
        ("iGroup", wt.INT),
    ]


# learn.microsoft.com/en-us/windows/win32/api/commctrl/ns-commctrl-lvhittestinfo
class LVHITTESTINFO(c_Structure):
    _fields_ = [
        ("pt", wt.POINT),
        ("flags", wt.UINT),
        ("iItem", wt.INT),
        ("iSubItem", wt.INT),
        ("iGroup", wt.INT),
    ]


# learn.microsoft.com/en-us/windows/win32/api/commctrl/ns-commctrl-lvtileviewinfo
class LVTILEVIEWINFO(c_Structure):
    _fields_ = [
        ("cbSize", wt.UINT),
        ("dwMask", wt.DWORD),
        ("dwFlags", wt.DWORD),
        ("sizeTile", wt.SIZE),
        ("cLines", wt.INT),
        ("rcLabelMargin", wt.RECT),
    ]


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-mouseinput
class MOUSEINPUT(c_Structure):
    _fields_ = [
        ("dx", wt.LONG),
        ("dy", wt.LONG),
        ("mouseData", wt.DWORD),
        ("dwFlags", wt.DWORD),
        ("time", wt.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-nmhdr
class NMHDR(c_Structure):
    _fields_ = [
        ("hwndFrom", wt.HWND),
        ("idFrom", UINT_PTR),
        ("code", wt.UINT),
    ]


# https://learn.microsoft.com/en-us/windows/win32/api/commctrl/nc-commctrl-subclassproc
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


########################################################################################
# Structures Group 1: Structures containing structures from group 0.
########################################################################################


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
        ("type", wt.DWORD),
        ("_", _INPUT_UNION),
    ]


# https://learn.microsoft.com/en-us/windows/win32/api/commctrl/ns-commctrl-nmcustomdraw
class NMCUSTOMDRAW(c_Structure):
    _fields_ = [
        ("hdr", NMHDR),
        ("dwDrawStage", wt.DWORD),
        ("hdc", wt.HDC),
        ("rc", wt.RECT),
        ("dwItemSpec", DWORD_PTR),
        ("uItemState", wt.UINT),
        ("lItemlParam", wt.LPARAM),
    ]


# learn.microsoft.com/en-us/windows/win32/api/commctrl/ns-commctrl-nmitemactivate
class NMITEMACTIVATE(c_Structure):
    _fields_ = [
        ("hdr", NMHDR),
        ("iItem", wt.INT),
        ("iSubItem", wt.INT),
        ("uNewState", wt.UINT),
        ("uOldState", wt.UINT),
        ("uChanged", wt.UINT),
        ("ptAction", wt.POINT),
        ("lParam", wt.LPARAM),
        ("uKeyFlags", wt.UINT),
    ]


# https://learn.microsoft.com/en-us/windows/win32/api/commctrl/ns-commctrl-nmlistview
class NMLISTVIEW(c_Structure):
    _fields_ = [
        ("hdr", NMHDR),
        ("iItem", wt.INT),
        ("iSubItem", wt.INT),
        ("uNewState", wt.UINT),
        ("uOldState", wt.UINT),
        ("uChanged", wt.UINT),
        ("ptAction", wt.POINT),
        ("lParam", wt.LPARAM),
    ]


# https://learn.microsoft.com/en-us/windows/win32/api/commctrl/ns-commctrl-nmlvcachehint
class NMLVCACHEHINT(c_Structure):
    _fields_ = [
        ("hdr", NMHDR),
        ("iFrom", wt.INT),
        ("iTo", wt.INT),
    ]


# https://learn.microsoft.com/en-us/windows/win32/api/commctrl/ns-commctrl-nmlvcustomdraw
class NMLVCUSTOMDRAW(c_Structure):
    _fields_ = [
        ("nmcd", NMCUSTOMDRAW),
        ("clrText", wt.COLORREF),
        ("clrTextBk", wt.COLORREF),
        ("iSubItem", wt.INT),
        ("dwItemType", wt.DWORD),
        ("clrFace", wt.COLORREF),
        ("iIconEffect", wt.INT),
        ("iIconPhase", wt.INT),
        ("iPartId", wt.INT),
        ("iStateId", wt.INT),
        ("rcText", wt.RECT),
        ("uAlign", wt.UINT),
    ]


# https://learn.microsoft.com/en-us/windows/win32/api/commctrl/ns-commctrl-nmlvdispinfow
class NMLVDISPINFOW(c_Structure):
    _fields_ = [
        ("hdr", NMHDR),
        ("item", LVITEMW),
    ]
