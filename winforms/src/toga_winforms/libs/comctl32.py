from ctypes import POINTER, windll
from ctypes.wintypes import BOOL, HDC, HWND, INT, LPARAM, UINT, WPARAM

from .win32misc import activation_context
from .win32structures import (
    DWORD_PTR,
    HIMAGELIST,
    INITCOMMONCONTROLSEX,
    LRESULT,
    SUBCLASSPROC,
    UINT_PTR,
)

with activation_context:
    comctl32 = windll.comctl32


# https://learn.microsoft.com/en-us/windows/win32/api/commctrl/nf-commctrl-initcommoncontrolsex
InitCommonControlsEx = comctl32.InitCommonControlsEx
InitCommonControlsEx.restype = BOOL
InitCommonControlsEx.argtypes = [POINTER(INITCOMMONCONTROLSEX)]


# https://learn.microsoft.com/en-us/windows/win32/api/commctrl/nf-commctrl-imagelist_draw
ImageList_Draw = comctl32.ImageList_Draw
ImageList_Draw.restype = BOOL
ImageList_Draw.argtypes = [HIMAGELIST, INT, HDC, INT, INT, UINT]


# https://learn.microsoft.com/en-us/windows/win32/api/commctrl/nf-commctrl-defsubclassproc
DefSubclassProc = comctl32.DefSubclassProc
DefSubclassProc.restype = LRESULT
DefSubclassProc.argtypes = [HWND, UINT, WPARAM, LPARAM]


# https://learn.microsoft.com/en-us/windows/win32/api/commctrl/nf-commctrl-setwindowsubclass
RemoveWindowSubclass = comctl32.RemoveWindowSubclass
RemoveWindowSubclass.restype = BOOL
RemoveWindowSubclass.argtypes = [HWND, SUBCLASSPROC, UINT_PTR]


# https://learn.microsoft.com/en-us/windows/win32/api/commctrl/nf-commctrl-setwindowsubclass
SetWindowSubclass = comctl32.SetWindowSubclass
SetWindowSubclass.restype = BOOL
SetWindowSubclass.argtypes = [HWND, SUBCLASSPROC, UINT_PTR, DWORD_PTR]
