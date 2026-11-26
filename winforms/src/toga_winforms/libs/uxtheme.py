import sys
from ctypes import HRESULT, windll
from ctypes.wintypes import HWND, INT, LPCWSTR

uxtheme = windll.uxtheme


# https://learn.microsoft.com/en-us/windows/win32/api/uxtheme/nf-uxtheme-setwindowtheme
SetWindowTheme = uxtheme.SetWindowTheme
SetWindowTheme.restype = HRESULT
SetWindowTheme.argtypes = [HWND, LPCWSTR, LPCWSTR]


# Undocumented UxTheme APIs for Win32 dark mode context menus and dialogs.
# Reference: https://github.com/ysc3839/win32-darkmode
#
# FlushMenuThemes (ordinal 136) was introduced in Windows 10 1809 (Build 17763), and
# SetPreferredAppMode (ordinal 135) was introduced in Windows 10 1903 (Build 18362),
# replacing AllowDarkModeForApp from Build 17763. Guard on >= 18362 so earlier builds
# do not hit missing ordinals or incompatible signatures.
if sys.getwindowsversion().build >= 18362:
    # Ordinal 135: SetPreferredAppMode
    # Configures the preferred dark mode behavior for the current process
    # (e.g., APPMODE_DEFAULT = 0, APPMODE_FORCEDARK = 2). Enabling this allows Win32
    # popup menus and standard controls/dialogs to participate in dark mode.
    SetPreferredAppMode = uxtheme[135]
    SetPreferredAppMode.restype = INT
    SetPreferredAppMode.argtypes = [INT]

    # Ordinal 136: FlushMenuThemes
    # Flushes the cached menu theme data so subsequent Win32 popup menus immediately
    # reflect the active preferred app mode.
    FlushMenuThemes = uxtheme[136]
    FlushMenuThemes.restype = None
    FlushMenuThemes.argtypes = []
else:  # pragma: no cover
    SetPreferredAppMode = None
    FlushMenuThemes = None
