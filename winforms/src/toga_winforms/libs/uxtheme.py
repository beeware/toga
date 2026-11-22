from ctypes import HRESULT, windll
from ctypes.wintypes import HWND, INT, LPCWSTR

uxtheme = windll.uxtheme


# https://learn.microsoft.com/en-us/windows/win32/api/uxtheme/nf-uxtheme-setwindowtheme
SetWindowTheme = uxtheme.SetWindowTheme
SetWindowTheme.restype = HRESULT
SetWindowTheme.argtypes = [HWND, LPCWSTR, LPCWSTR]


# Undocumented UxTheme APIs for Win32 dark mode context menus
# Ordinal 135: SetPreferredAppMode
# https://github.com/microsoft/terminal/blob/main/src/interactivity/win32/DarkMode.cpp
SetPreferredAppMode = uxtheme[135]
SetPreferredAppMode.restype = INT
SetPreferredAppMode.argtypes = [INT]


# Ordinal 136: FlushMenuThemes
FlushMenuThemes = uxtheme[136]
FlushMenuThemes.restype = None
FlushMenuThemes.argtypes = []
