from __future__ import print_function, absolute_import, division

from ctypes import *
from ctypes.wintypes import *


INT = c_int
LPVOID = c_void_p
HCURSOR = HANDLE
LRESULT = LPARAM
COLORREF = DWORD
PVOID = c_void_p
WCHAR = c_wchar
BCHAR = c_wchar
LPRECT = POINTER(RECT)
LPPOINT = POINTER(POINT)
LPMSG = POINTER(MSG)
UINT_PTR = HANDLE
LONG_PTR = HANDLE

LF_FACESIZE = 32
CCHDEVICENAME = 32
CCHFORMNAME = 32

WNDPROC = WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM)
TIMERPROC = WINFUNCTYPE(None, HWND, UINT, POINTER(UINT), DWORD)
TIMERAPCPROC = WINFUNCTYPE(None, PVOID, DWORD, DWORD)
MONITORENUMPROC = WINFUNCTYPE(BOOL, HMONITOR, HDC, LPRECT, LPARAM)

def MAKEINTRESOURCE(i):
    return cast(c_void_p(i&0xFFFF), c_wchar_p)

def LOWORD(dword):
    return dword & 0x0000ffff

def HIWORD(dword):
    return dword >> 16

class WNDCLASS(Structure):
    _fields_ = [
        ('style', UINT),
        ('lpfnWndProc', WNDPROC),
        ('cbClsExtra', c_int),
        ('cbWndExtra', c_int),
        ('hInstance', HINSTANCE),
        ('hIcon', HICON),
        ('hCursor', HCURSOR),
        ('hbrBackground', HBRUSH),
        ('lpszMenuName', c_char_p),
        ('lpszClassName', c_wchar_p)
    ]

class SECURITY_ATTRIBUTES(Structure):
    _fields_ = [
        ("nLength", DWORD),
        ("lpSecurityDescriptor", c_void_p),
        ("bInheritHandle", BOOL)
    ]
    __slots__ = [f[0] for f in _fields_]

class PIXELFORMATDESCRIPTOR(Structure):
    _fields_ = [
        ('nSize', WORD),
        ('nVersion', WORD),
        ('dwFlags', DWORD),
        ('iPixelType', BYTE),
        ('cColorBits', BYTE),
        ('cRedBits', BYTE),
        ('cRedShift', BYTE),
        ('cGreenBits', BYTE),
        ('cGreenShift', BYTE),
        ('cBlueBits', BYTE),
        ('cBlueShift', BYTE),
        ('cAlphaBits', BYTE),
        ('cAlphaShift', BYTE),
        ('cAccumBits', BYTE),
        ('cAccumRedBits', BYTE),
        ('cAccumGreenBits', BYTE),
        ('cAccumBlueBits', BYTE),
        ('cAccumAlphaBits', BYTE),
        ('cDepthBits', BYTE),
        ('cStencilBits', BYTE),
        ('cAuxBuffers', BYTE),
        ('iLayerType', BYTE),
        ('bReserved', BYTE),
        ('dwLayerMask', DWORD),
        ('dwVisibleMask', DWORD),
        ('dwDamageMask', DWORD)
    ]

class RGBQUAD(Structure):
    _fields_ = [
        ('rgbBlue', BYTE),
        ('rgbGreen', BYTE),
        ('rgbRed', BYTE),
        ('rgbReserved', BYTE),
    ]
    __slots__ = [f[0] for f in _fields_]

class CIEXYZ(Structure):
    _fields_ = [
        ('ciexyzX', DWORD),
        ('ciexyzY', DWORD),
        ('ciexyzZ', DWORD),
    ]
    __slots__ = [f[0] for f in _fields_]

class CIEXYZTRIPLE(Structure):
    _fields_ = [
        ('ciexyzRed', CIEXYZ),
        ('ciexyzBlue', CIEXYZ),
        ('ciexyzGreen', CIEXYZ),
    ]
    __slots__ = [f[0] for f in _fields_]

class BITMAPINFOHEADER(Structure):
    _fields_ = [
        ('biSize', DWORD),
        ('biWidth', LONG),
        ('biHeight', LONG),
        ('biPlanes', WORD),
        ('biBitCount', WORD),
        ('biCompression', DWORD),
        ('biSizeImage', DWORD),
        ('biXPelsPerMeter', LONG),
        ('biYPelsPerMeter', LONG),
        ('biClrUsed', DWORD),
        ('biClrImportant', DWORD),
    ]

class BITMAPV5HEADER(Structure):
    _fields_ = [
        ('bV5Size', DWORD),
        ('bV5Width', LONG),
        ('bV5Height', LONG),
        ('bV5Planes', WORD),
        ('bV5BitCount', WORD),
        ('bV5Compression', DWORD),
        ('bV5SizeImage', DWORD),
        ('bV5XPelsPerMeter', LONG),
        ('bV5YPelsPerMeter', LONG),
        ('bV5ClrUsed', DWORD),
        ('bV5ClrImportant', DWORD),
        ('bV5RedMask', DWORD),
        ('bV5GreenMask', DWORD),
        ('bV5BlueMask', DWORD),
        ('bV5AlphaMask', DWORD),
        ('bV5CSType', DWORD),
        ('bV5Endpoints', CIEXYZTRIPLE),
        ('bV5GammaRed', DWORD),
        ('bV5GammaGreen', DWORD),
        ('bV5GammaBlue', DWORD),
        ('bV5Intent', DWORD),
        ('bV5ProfileData', DWORD),
        ('bV5ProfileSize', DWORD),
        ('bV5Reserved', DWORD),
    ]

class BITMAPINFO(Structure):
    _fields_ = [
        ('bmiHeader', BITMAPINFOHEADER),
        ('bmiColors', RGBQUAD * 1)
    ]
    __slots__ = [f[0] for f in _fields_]

class LOGFONT(Structure):
    _fields_ = [
        ('lfHeight', LONG),
        ('lfWidth', LONG),
        ('lfEscapement', LONG),
        ('lfOrientation', LONG),
        ('lfWeight', LONG),
        ('lfItalic', BYTE),
        ('lfUnderline', BYTE),
        ('lfStrikeOut', BYTE),
        ('lfCharSet', BYTE),
        ('lfOutPrecision', BYTE),
        ('lfClipPrecision', BYTE),
        ('lfQuality', BYTE),
        ('lfPitchAndFamily', BYTE),
        ('lfFaceName', (c_char * LF_FACESIZE))  # Use ASCII
    ]

class TRACKMOUSEEVENT(Structure):
    _fields_ = [
        ('cbSize', DWORD),
        ('dwFlags', DWORD),
        ('hwndTrack', HWND),
        ('dwHoverTime', DWORD)
    ]
    __slots__ = [f[0] for f in _fields_]

class MINMAXINFO(Structure):
    _fields_ = [
        ('ptReserved', POINT),
        ('ptMaxSize', POINT),
        ('ptMaxPosition', POINT),
        ('ptMinTrackSize', POINT),
        ('ptMaxTrackSize', POINT)
    ]
    __slots__ = [f[0] for f in _fields_]

class ABC(Structure):
    _fields_ = [
        ('abcA', c_int),
        ('abcB', c_uint),
        ('abcC', c_int)
    ]
    __slots__ = [f[0] for f in _fields_]

class TEXTMETRIC(Structure):
    _fields_ = [
        ('tmHeight', c_long),
        ('tmAscent', c_long),
        ('tmDescent', c_long),
        ('tmInternalLeading', c_long),
        ('tmExternalLeading', c_long),
        ('tmAveCharWidth', c_long),
        ('tmMaxCharWidth', c_long),
        ('tmWeight', c_long),
        ('tmOverhang', c_long),
        ('tmDigitizedAspectX', c_long),
        ('tmDigitizedAspectY', c_long),
        ('tmFirstChar', c_char),  # Use ASCII
        ('tmLastChar', c_char),
        ('tmDefaultChar', c_char),
        ('tmBreakChar', c_char),
        ('tmItalic', c_byte),
        ('tmUnderlined', c_byte),
        ('tmStruckOut', c_byte),
        ('tmPitchAndFamily', c_byte),
        ('tmCharSet', c_byte)
    ]
    __slots__ = [f[0] for f in _fields_]

class MONITORINFOEX(Structure):
    _fields_ = [
        ('cbSize', DWORD),
        ('rcMonitor', RECT),
        ('rcWork', RECT),
        ('dwFlags', DWORD),
        ('szDevice', WCHAR * CCHDEVICENAME)
    ]
    __slots__ = [f[0] for f in _fields_]

class DEVMODE(Structure):
    _fields_ = [
        ('dmDeviceName', BCHAR * CCHDEVICENAME),
        ('dmSpecVersion', WORD),
        ('dmDriverVersion', WORD),
        ('dmSize', WORD),
        ('dmDriverExtra', WORD),
        ('dmFields', DWORD),
        # Just using largest union member here
        ('dmOrientation', c_short),
        ('dmPaperSize', c_short),
        ('dmPaperLength', c_short),
        ('dmPaperWidth', c_short),
        ('dmScale', c_short),
        ('dmCopies', c_short),
        ('dmDefaultSource', c_short),
        ('dmPrintQuality', c_short),
        # End union
        ('dmColor', c_short),
        ('dmDuplex', c_short),
        ('dmYResolution', c_short),
        ('dmTTOption', c_short),
        ('dmCollate', c_short),
        ('dmFormName', BCHAR * CCHFORMNAME),
        ('dmLogPixels', WORD),
        ('dmBitsPerPel', DWORD),
        ('dmPelsWidth', DWORD),
        ('dmPelsHeight', DWORD),
        ('dmDisplayFlags', DWORD), # union with dmNup
        ('dmDisplayFrequency', DWORD),
        ('dmICMMethod', DWORD),
        ('dmICMIntent', DWORD),
        ('dmDitherType', DWORD),
        ('dmReserved1', DWORD),
        ('dmReserved2', DWORD),
        ('dmPanningWidth', DWORD),
        ('dmPanningHeight', DWORD),
    ]

class ICONINFO(Structure):
    _fields_ = [
        ('fIcon', BOOL),
        ('xHotspot', DWORD),
        ('yHotspot', DWORD),
        ('hbmMask', HBITMAP),
        ('hbmColor', HBITMAP)
    ]
    __slots__ = [f[0] for f in _fields_]
