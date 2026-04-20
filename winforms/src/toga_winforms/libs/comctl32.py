from ctypes import POINTER
from ctypes.wintypes import BOOL, HDC, HWND, INT, LPARAM, UINT, WPARAM

from .activationcontext import WinDLL_activation_context
from .comctl32classes import INITCOMMONCONTROLSEX, SUBCLASSPROC
from .win32 import DWORD_PTR, HIMAGELIST, LRESULT, UINT_PTR

comctl32 = WinDLL_activation_context("comctl32")

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
