from ctypes import c_void_p, windll, wintypes

from System import Environment

user32 = windll.user32


# https://learn.microsoft.com/en-us/windows/win32/hidpi/dpi-awareness-context
DPI_AWARENESS_CONTEXT_UNAWARE = -1
DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2 = -4

# https://www.lifewire.com/windows-version-numbers-2625171
win_version = Environment.OSVersion.Version
if (win_version.Major, win_version.Minor, win_version.Build) >= (10, 0, 15063):
    SetProcessDpiAwarenessContext = user32.SetProcessDpiAwarenessContext
    SetProcessDpiAwarenessContext.restype = wintypes.BOOL
    SetProcessDpiAwarenessContext.argtypes = [c_void_p]

    SetThreadDpiAwarenessContext = user32.SetThreadDpiAwarenessContext
    SetThreadDpiAwarenessContext.restype = c_void_p
    SetThreadDpiAwarenessContext.argtypes = [c_void_p]

else:  # pragma: no cover
    print(
        "WARNING: Your Windows version doesn't support DPI Awareness setting. "
        "We recommend you upgrade to at least Windows 10 version 1703."
    )
    SetProcessDpiAwarenessContext = SetThreadDpiAwarenessContext = None


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-monitorfromrect
MONITOR_DEFAULTTONEAREST = 2

MonitorFromRect = user32.MonitorFromRect
MonitorFromRect.restype = wintypes.HMONITOR
MonitorFromRect.argtypes = [wintypes.LPRECT, wintypes.DWORD]
