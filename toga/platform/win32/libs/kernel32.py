from __future__ import print_function, absolute_import, division

from .debug import DebugLibrary
from .types import *

kernel32 = DebugLibrary(windll.kernel32)

kernel32.CloseHandle.restype = BOOL
kernel32.CloseHandle.argtypes = [HANDLE]
kernel32.CreateEventW.restype = HANDLE
kernel32.CreateEventW.argtypes = [POINTER(SECURITY_ATTRIBUTES), BOOL, BOOL, c_wchar_p]
kernel32.CreateWaitableTimerA.restype = HANDLE
kernel32.CreateWaitableTimerA.argtypes = [POINTER(SECURITY_ATTRIBUTES), BOOL, c_char_p]
kernel32.GetCurrentThreadId.restype = DWORD
kernel32.GetCurrentThreadId.argtypes = []
kernel32.GetModuleHandleW.restype = HMODULE
kernel32.GetModuleHandleW.argtypes = [c_wchar_p]
kernel32.GlobalAlloc.restype = HGLOBAL
kernel32.GlobalAlloc.argtypes = [UINT, c_size_t]
kernel32.GlobalLock.restype = LPVOID
kernel32.GlobalLock.argtypes = [HGLOBAL]
kernel32.GlobalUnlock.restype = BOOL
kernel32.GlobalUnlock.argtypes = [HGLOBAL]
kernel32.SetLastError.restype = DWORD
kernel32.SetLastError.argtypes = []
kernel32.SetWaitableTimer.restype = BOOL
kernel32.SetWaitableTimer.argtypes = [HANDLE, POINTER(LARGE_INTEGER), LONG, LPVOID, LPVOID, BOOL]  # TIMERAPCPROC
kernel32.WaitForSingleObject.restype = DWORD
kernel32.WaitForSingleObject.argtypes = [HANDLE, DWORD]
