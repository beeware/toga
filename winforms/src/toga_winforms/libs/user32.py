from ctypes import POINTER, c_void_p, windll
from ctypes.wintypes import (
    BOOL,
    DWORD,
    HBRUSH,
    HDC,
    HINSTANCE,
    HMENU,
    HMONITOR,
    HWND,
    INT,
    LPCWSTR,
    LPPOINT,
    LPRECT,
    LPVOID,
    RECT,
    UINT,
    WPARAM,
)

from System import Environment

from .win32misc import activation_context
from .win32structures import LPARAM_OBJECT, LRESULT, UINT_PTR

user32 = windll.user32


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-appendmenuw
AppendMenuW = user32.AppendMenuW
AppendMenuW.restype = BOOL
AppendMenuW.argtypes = [HMENU, UINT, UINT_PTR, LPCWSTR]


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-clienttoscreen
ClientToScreen = user32.ClientToScreen
ClientToScreen.restype = BOOL
ClientToScreen.argtypes = [HWND, LPPOINT]


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-createpopupmenu
CreatePopupMenu = user32.CreatePopupMenu
CreatePopupMenu.restype = HMENU
CreatePopupMenu.argtypes = []


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-createwindowexw
CreateWindowExW_raw = user32.CreateWindowExW
CreateWindowExW_raw.restype = HWND
CreateWindowExW_raw.argtypes = [
    DWORD,
    LPCWSTR,
    LPCWSTR,
    DWORD,
    INT,
    INT,
    INT,
    INT,
    HWND,
    HMENU,
    HINSTANCE,
    LPVOID,
]


# To create a window with up-to-date theme, Common Control v6 must be used. Hence,
# CreateWindowExW is called within the appropriate activation context. For more details
# see Raymond Chen's blog:
# https://devblogs.microsoft.com/oldnewthing/20140508-00/?p=1043
def CreateWindowExW(*args):
    with activation_context:
        return CreateWindowExW_raw(*args)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-destroymenu
DestroyMenu = user32.DestroyMenu
DestroyMenu.restype = BOOL
DestroyMenu.argtypes = [HMENU]


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-drawtextw
DrawTextW = user32.DrawTextW
DrawTextW.restype = INT
DrawTextW.argtypes = [HDC, LPCWSTR, INT, LPRECT, UINT]


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-fillrect
FillRect = user32.FillRect
FillRect.restype = INT
FillRect.argtypes = [HDC, POINTER(RECT), HBRUSH]


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getfocus
GetFocus = user32.GetFocus
GetFocus.restype = HWND
GetFocus.argtypes = []


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getsyscolor
GetSysColor = user32.GetSysColor
GetSysColor.restype = DWORD
GetSysColor.argtypes = [INT]


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getsystemmetrics
GetSystemMetrics = user32.GetSystemMetrics
GetSystemMetrics.restype = INT
GetSystemMetrics.argtypes = [INT]


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-invalidaterect
InvalidateRect = user32.InvalidateRect
InvalidateRect.restype = BOOL
InvalidateRect.argtypes = [HWND, POINTER(RECT), BOOL]


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-monitorfromrect
MonitorFromRect = user32.MonitorFromRect
MonitorFromRect.restype = HMONITOR
MonitorFromRect.argtypes = [LPRECT, DWORD]


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-postmessagew
# See the comment above SendMessageW for an explanation of LPARAM_OBJECT.
PostMessageW = user32.PostMessageW
PostMessageW.restype = LRESULT
PostMessageW.argtypes = [HWND, UINT, WPARAM, LPARAM_OBJECT]


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-screentoclient
ScreenToClient = user32.ScreenToClient
ScreenToClient.restype = BOOL
ScreenToClient.argtypes = [HWND, LPPOINT]


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendmessagew
# According to the documentation, the final argument type should be LPARAM. However,
# LPARAM is often used as a pointer (memory address). To use this argument type in
# Python would require the procedure: 1. Create point object, 2. Obtain memory address
# of the object, 3. Pass memory address as an integer to the function.
#
# In ctypes, the more simple and efficient method for using a pointer as a function
# argument is byref. LPARAM_OBJECT is used in place of LPARAM to allow the use of byref.
SendMessageW = user32.SendMessageW
SendMessageW.restype = LRESULT
SendMessageW.argtypes = [HWND, UINT, WPARAM, LPARAM_OBJECT]


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setprocessdpiawarenesscontext
# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setthreaddpiawarenesscontext
# https://www.lifewire.com/windows-version-numbers-2625171
win_version = Environment.OSVersion.Version
if (win_version.Major, win_version.Minor, win_version.Build) >= (10, 0, 15063):
    SetProcessDpiAwarenessContext = user32.SetProcessDpiAwarenessContext
    SetProcessDpiAwarenessContext.restype = BOOL
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


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setfocus
SetFocus = user32.SetFocus
SetFocus.restype = HWND
SetFocus.argtypes = [HWND]


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-SetForegroundWindow
SetForegroundWindow = user32.SetForegroundWindow
SetForegroundWindow.restype = BOOL
SetForegroundWindow.argtypes = [HWND]


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowpos
SetWindowPos = user32.SetWindowPos
SetWindowPos.restype = BOOL
SetWindowPos.argtypes = [HWND, HWND, INT, INT, INT, INT, UINT]


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-trackpopupmenuex
TrackPopupMenuEx = user32.TrackPopupMenuEx
TrackPopupMenuEx.restype = BOOL
TrackPopupMenuEx.argtypes = [HMENU, UINT, INT, INT, HWND, c_void_p]


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-updatewindow
UpdateWindow = user32.UpdateWindow
UpdateWindow.restype = BOOL
UpdateWindow.argtypes = [HWND]
