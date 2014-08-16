from __future__ import print_function, absolute_import, division

from .debug import DebugLibrary
from .types import *

# gdi32
gdi32 = DebugLibrary(windll.gdi32)

gdi32.AddFontMemResourceEx.restype = HANDLE
gdi32.AddFontMemResourceEx.argtypes = [PVOID, DWORD, PVOID, POINTER(DWORD)]
gdi32.ChoosePixelFormat.restype = c_int
gdi32.ChoosePixelFormat.argtypes = [HDC, POINTER(PIXELFORMATDESCRIPTOR)]
gdi32.CreateBitmap.restype = HBITMAP
gdi32.CreateBitmap.argtypes = [c_int, c_int, UINT, UINT, c_void_p]
gdi32.CreateCompatibleDC.restype = HDC
gdi32.CreateCompatibleDC.argtypes = [HDC]
gdi32.CreateDIBitmap.restype = HBITMAP
gdi32.CreateDIBitmap.argtypes = [HDC, POINTER(BITMAPINFOHEADER), DWORD, c_void_p, POINTER(BITMAPINFO), UINT]
gdi32.CreateDIBSection.restype = HBITMAP
gdi32.CreateDIBSection.argtypes = [HDC, c_void_p, UINT, c_void_p, HANDLE, DWORD]  # POINTER(BITMAPINFO)
gdi32.CreateFontIndirectA.restype = HFONT
gdi32.CreateFontIndirectA.argtypes = [POINTER(LOGFONT)]
gdi32.DeleteDC.restype = BOOL
gdi32.DeleteDC.argtypes = [HDC]
gdi32.DeleteObject.restype = BOOL
gdi32.DeleteObject.argtypes = [HGDIOBJ]
gdi32.DescribePixelFormat.restype = c_int
gdi32.DescribePixelFormat.argtypes = [HDC, c_int, UINT, POINTER(PIXELFORMATDESCRIPTOR)]
gdi32.ExtTextOutA.restype = BOOL
gdi32.ExtTextOutA.argtypes = [HDC, c_int, c_int, UINT, LPRECT, c_char_p, UINT, POINTER(INT)]
gdi32.GdiFlush.restype = BOOL
gdi32.GdiFlush.argtypes = []
gdi32.GetCharABCWidthsW.restype = BOOL
gdi32.GetCharABCWidthsW.argtypes = [HDC, UINT, UINT, POINTER(ABC)]
gdi32.GetCharWidth32W.restype = BOOL
gdi32.GetCharWidth32W.argtypes = [HDC, UINT, UINT, POINTER(INT)]
gdi32.GetStockObject.restype =  HGDIOBJ
gdi32.GetStockObject.argtypes = [c_int]
gdi32.GetTextMetricsA.restype = BOOL
gdi32.GetTextMetricsA.argtypes = [HDC, POINTER(TEXTMETRIC)]
gdi32.SelectObject.restype = HGDIOBJ
gdi32.SelectObject.argtypes = [HDC, HGDIOBJ]
gdi32.SetBkColor.restype = COLORREF
gdi32.SetBkColor.argtypes = [HDC, COLORREF]
gdi32.SetBkMode.restype = c_int
gdi32.SetBkMode.argtypes = [HDC, c_int]
gdi32.SetPixelFormat.restype = BOOL
gdi32.SetPixelFormat.argtypes = [HDC, c_int, POINTER(PIXELFORMATDESCRIPTOR)]
gdi32.SetTextColor.restype = COLORREF
gdi32.SetTextColor.argtypes = [HDC, COLORREF]
