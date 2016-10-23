from __future__ import print_function, absolute_import, division

import struct

from .debug import DebugLibrary
from .types import *


IS64 = struct.calcsize("P") == 8

user32 = DebugLibrary(windll.user32)

user32.AdjustWindowRectEx.restype = BOOL
user32.AdjustWindowRectEx.argtypes = [LPRECT, DWORD, BOOL, DWORD]
user32.ChangeDisplaySettingsExW.restype = LONG
user32.ChangeDisplaySettingsExW.argtypes = [c_wchar_p, POINTER(DEVMODE), HWND, DWORD, LPVOID]
user32.ClientToScreen.restype = BOOL
user32.ClientToScreen.argtypes = [HWND, LPPOINT]
user32.ClipCursor.restype = BOOL
user32.ClipCursor.argtypes = [LPRECT]
user32.CreateIconIndirect.restype = HICON
user32.CreateIconIndirect.argtypes = [POINTER(ICONINFO)]
user32.CreateWindowExW.restype = HWND
user32.CreateWindowExW.argtypes = [DWORD, c_wchar_p, c_wchar_p, DWORD, c_int, c_int, c_int, c_int, HWND, HMENU, HINSTANCE, LPVOID]
user32.DefWindowProcW.restype = LRESULT
user32.DefWindowProcW.argtypes = [HWND, UINT, WPARAM, LPARAM]
user32.DestroyWindow.restype = BOOL
user32.DestroyWindow.argtypes = [HWND]
user32.DispatchMessageW.restype = LRESULT
user32.DispatchMessageW.argtypes = [LPMSG]
user32.EnumDisplayMonitors.restype = BOOL
user32.EnumDisplayMonitors.argtypes = [HDC, LPRECT, MONITORENUMPROC, LPARAM]
user32.EnumDisplaySettingsW.restype = BOOL
user32.EnumDisplaySettingsW.argtypes = [c_wchar_p, DWORD, POINTER(DEVMODE)]
user32.FillRect.restype = c_int
user32.FillRect.argtypes = [HDC, LPRECT, HBRUSH]
user32.GetClientRect.restype = BOOL
user32.GetClientRect.argtypes = [HWND, LPRECT]
user32.GetCursorPos.restype = BOOL
user32.GetCursorPos.argtypes = [LPPOINT]
user32.GetDC.restype = HDC
user32.GetDC.argtypes = [HWND]
user32.GetDesktopWindow.restype = HWND
user32.GetDesktopWindow.argtypes = []
user32.GetKeyState.restype = c_short
user32.GetKeyState.argtypes = [c_int]
user32.GetMessageW.restype = BOOL
user32.GetMessageW.argtypes = [LPMSG, HWND, UINT, UINT]
user32.GetMonitorInfoW.restype = BOOL
user32.GetMonitorInfoW.argtypes = [HMONITOR, POINTER(MONITORINFOEX)]
user32.GetQueueStatus.restype = DWORD
user32.GetQueueStatus.argtypes = [UINT]
user32.GetSystemMetrics.restype = c_int
user32.GetSystemMetrics.argtypes = [c_int]
user32.GetSysColorBrush.restype = HGDIOBJ
user32.GetSysColorBrush.argtypes = [INT]
user32.LoadCursorW.restype = HCURSOR
user32.LoadCursorW.argtypes = [HINSTANCE, c_wchar_p]
user32.LoadIconW.restype = HICON
user32.LoadIconW.argtypes = [HINSTANCE, c_wchar_p]
user32.MapVirtualKeyW.restype = UINT
user32.MapVirtualKeyW.argtypes = [UINT, UINT]
user32.MapWindowPoints.restype = c_int
user32.MapWindowPoints.argtypes = [HWND, HWND, c_void_p, UINT]  # HWND, HWND, LPPOINT, UINT
user32.MsgWaitForMultipleObjects.restype = DWORD
user32.MsgWaitForMultipleObjects.argtypes = [DWORD, POINTER(HANDLE), BOOL, DWORD, DWORD]
user32.PeekMessageW.restype = BOOL
user32.PeekMessageW.argtypes = [LPMSG, HWND, UINT, UINT, UINT]
user32.PostQuitMessage.restype = BOOL
user32.PostQuitMessage.argtypes = [INT]
user32.PostThreadMessageW.restype = BOOL
user32.PostThreadMessageW.argtypes = [DWORD, UINT, WPARAM, LPARAM]
user32.RegisterClassW.restype = ATOM
user32.RegisterClassW.argtypes = [POINTER(WNDCLASS)]
user32.RegisterHotKey.restype = BOOL
user32.RegisterHotKey.argtypes = [HWND, c_int, UINT, UINT]
user32.ReleaseCapture.restype = BOOL
user32.ReleaseCapture.argtypes = []
user32.ReleaseDC.restype = c_int
user32.ReleaseDC.argtypes = [HWND, HDC]
user32.ScreenToClient.restype = BOOL
user32.ScreenToClient.argtypes = [HWND, LPPOINT]
user32.SetCapture.restype = HWND
user32.SetCapture.argtypes = [HWND]
user32.SetClassLongW.restype = DWORD
user32.SetClassLongW.argtypes = [HWND, c_int, LONG]
if IS64:
    user32.SetClassLongPtrW.restype = ULONG
    user32.SetClassLongPtrW.argtypes = [HWND, c_int, LONG_PTR]
else:
    user32.SetClassLongPtrW = user32.SetClassLongW
user32.SetCursor.restype = HCURSOR
user32.SetCursor.argtypes = [HCURSOR]
user32.SetCursorPos.restype = BOOL
user32.SetCursorPos.argtypes = [c_int, c_int]
user32.SetFocus.restype = HWND
user32.SetFocus.argtypes = [HWND]
user32.SetForegroundWindow.restype = BOOL
user32.SetForegroundWindow.argtypes = [HWND]
user32.SetTimer.restype = UINT_PTR
user32.SetTimer.argtypes = [HWND, UINT_PTR, UINT, TIMERPROC]
user32.SetWindowLongW.restype = LONG
user32.SetWindowLongW.argtypes = [HWND, c_int, LONG]
user32.SetWindowPos.restype = BOOL
user32.SetWindowPos.argtypes = [HWND, HWND, c_int, c_int, c_int, c_int, UINT]
user32.SetWindowTextW.restype = BOOL
user32.SetWindowTextW.argtypes = [HWND, c_wchar_p]
user32.ShowCursor.restype = c_int
user32.ShowCursor.argtypes = [BOOL]
user32.ShowWindow.restype = BOOL
user32.ShowWindow.argtypes = [HWND, c_int]
user32.TrackMouseEvent.restype = BOOL
user32.TrackMouseEvent.argtypes = [POINTER(TRACKMOUSEEVENT)]
user32.TranslateMessage.restype = BOOL
user32.TranslateMessage.argtypes = [LPMSG]
user32.UnregisterClassW.restype = BOOL
user32.UnregisterClassW.argtypes = [c_wchar_p, HINSTANCE]
user32.UnregisterHotKey.restype = BOOL
user32.UnregisterHotKey.argtypes = [HWND, c_int]
