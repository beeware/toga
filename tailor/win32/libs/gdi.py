from .types import *

# _gdi32
_gdi32 = DebugLibrary(windll.gdi32)

_gdi32.AddFontMemResourceEx.restype = HANDLE
_gdi32.AddFontMemResourceEx.argtypes = [PVOID, DWORD, PVOID, POINTER(DWORD)]
_gdi32.ChoosePixelFormat.restype = c_int
_gdi32.ChoosePixelFormat.argtypes = [HDC, POINTER(PIXELFORMATDESCRIPTOR)]
_gdi32.CreateBitmap.restype = HBITMAP
_gdi32.CreateBitmap.argtypes = [c_int, c_int, UINT, UINT, c_void_p]
_gdi32.CreateCompatibleDC.restype = HDC
_gdi32.CreateCompatibleDC.argtypes = [HDC]
_gdi32.CreateDIBitmap.restype = HBITMAP
_gdi32.CreateDIBitmap.argtypes = [HDC, POINTER(BITMAPINFOHEADER), DWORD, c_void_p, POINTER(BITMAPINFO), UINT]
_gdi32.CreateDIBSection.restype = HBITMAP
_gdi32.CreateDIBSection.argtypes = [HDC, c_void_p, UINT, c_void_p, HANDLE, DWORD]  # POINTER(BITMAPINFO)
_gdi32.CreateFontIndirectA.restype = HFONT
_gdi32.CreateFontIndirectA.argtypes = [POINTER(LOGFONT)]
_gdi32.DeleteDC.restype = BOOL
_gdi32.DeleteDC.argtypes = [HDC]
_gdi32.DeleteObject.restype = BOOL
_gdi32.DeleteObject.argtypes = [HGDIOBJ]
_gdi32.DescribePixelFormat.restype = c_int
_gdi32.DescribePixelFormat.argtypes = [HDC, c_int, UINT, POINTER(PIXELFORMATDESCRIPTOR)]
_gdi32.ExtTextOutA.restype = BOOL
_gdi32.ExtTextOutA.argtypes = [HDC, c_int, c_int, UINT, LPRECT, c_char_p, UINT, POINTER(INT)]
_gdi32.GdiFlush.restype = BOOL
_gdi32.GdiFlush.argtypes = []
_gdi32.GetCharABCWidthsW.restype = BOOL
_gdi32.GetCharABCWidthsW.argtypes = [HDC, UINT, UINT, POINTER(ABC)]
_gdi32.GetCharWidth32W.restype = BOOL
_gdi32.GetCharWidth32W.argtypes = [HDC, UINT, UINT, POINTER(INT)]
_gdi32.GetStockObject.restype =  HGDIOBJ
_gdi32.GetStockObject.argtypes = [c_int]
_gdi32.GetTextMetricsA.restype = BOOL
_gdi32.GetTextMetricsA.argtypes = [HDC, POINTER(TEXTMETRIC)]
_gdi32.SelectObject.restype = HGDIOBJ
_gdi32.SelectObject.argtypes = [HDC, HGDIOBJ]
_gdi32.SetBkColor.restype = COLORREF
_gdi32.SetBkColor.argtypes = [HDC, COLORREF]
_gdi32.SetBkMode.restype = c_int
_gdi32.SetBkMode.argtypes = [HDC, c_int]
_gdi32.SetPixelFormat.restype = BOOL
_gdi32.SetPixelFormat.argtypes = [HDC, c_int, POINTER(PIXELFORMATDESCRIPTOR)]
_gdi32.SetTextColor.restype = COLORREF
_gdi32.SetTextColor.argtypes = [HDC, COLORREF]
