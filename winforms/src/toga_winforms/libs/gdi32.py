from ctypes import windll
from ctypes.wintypes import COLORREF, HDC

gdi32 = windll.GDI32


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-settextcolor
SetTextColor = gdi32.SetTextColor
SetTextColor.restype = COLORREF
SetTextColor.argtypes = [HDC, COLORREF]
