import ctypes.wintypes as wt
from ctypes import windll

from . import win32structures as ws

comctl32 = windll.comctl32


# https://learn.microsoft.com/en-us/windows/win32/api/commctrl/nf-commctrl-defsubclassproc
DefSubclassProc = comctl32.DefSubclassProc
DefSubclassProc.restype = ws.LRESULT
DefSubclassProc.argtypes = [wt.HWND, wt.UINT, wt.WPARAM, wt.LPARAM]


# https://learn.microsoft.com/en-us/windows/win32/api/commctrl/nf-commctrl-setwindowsubclass
RemoveWindowSubclass = comctl32.RemoveWindowSubclass
RemoveWindowSubclass.restype = wt.BOOL
RemoveWindowSubclass.argtypes = [wt.HWND, ws.SUBCLASSPROC, ws.UINT_PTR]


# https://learn.microsoft.com/en-us/windows/win32/api/commctrl/nf-commctrl-setwindowsubclass
SetWindowSubclass = comctl32.SetWindowSubclass
SetWindowSubclass.restype = wt.BOOL
SetWindowSubclass.argtypes = [wt.HWND, ws.SUBCLASSPROC, ws.UINT_PTR, ws.DWORD_PTR]
