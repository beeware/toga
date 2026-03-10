from ctypes import windll
from ctypes.wintypes import BOOL, COLORREF, HDC

from .win32 import HBRUSH, HGDIOBJ

gdi32 = windll.GDI32


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-createsolidbrush
CreateSolidBrush = gdi32.CreateSolidBrush
CreateSolidBrush.restype = HBRUSH
CreateSolidBrush.argtypes = [COLORREF]


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-deleteobject
DeleteObject = gdi32.DeleteObject
DeleteObject.restype = BOOL
DeleteObject.argtypes = [HGDIOBJ]


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-settextcolor
SetTextColor = gdi32.SetTextColor
SetTextColor.restype = COLORREF
SetTextColor.argtypes = [HDC, COLORREF]
