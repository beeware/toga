from ctypes import HRESULT, windll
from ctypes.wintypes import HWND, LPCWSTR

uxtheme = windll.uxtheme


# https://learn.microsoft.com/en-us/windows/win32/api/uxtheme/nf-uxtheme-setwindowtheme
SetWindowTheme = uxtheme.SetWindowTheme
SetWindowTheme.restype = HRESULT
SetWindowTheme.argtypes = [HWND, LPCWSTR, LPCWSTR]
