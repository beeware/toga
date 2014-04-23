from .types import *

_kernel32 = DebugLibrary(windll.kernel32)

_kernel32.CloseHandle.restype = BOOL
_kernel32.CloseHandle.argtypes = [HANDLE]
_kernel32.CreateEventW.restype = HANDLE
_kernel32.CreateEventW.argtypes = [POINTER(SECURITY_ATTRIBUTES), BOOL, BOOL, c_wchar_p]
_kernel32.CreateWaitableTimerA.restype = HANDLE
_kernel32.CreateWaitableTimerA.argtypes = [POINTER(SECURITY_ATTRIBUTES), BOOL, c_char_p]
_kernel32.GetCurrentThreadId.restype = DWORD
_kernel32.GetCurrentThreadId.argtypes = []
_kernel32.GetModuleHandleW.restype = HMODULE
_kernel32.GetModuleHandleW.argtypes = [c_wchar_p]
_kernel32.GlobalAlloc.restype = HGLOBAL
_kernel32.GlobalAlloc.argtypes = [UINT, c_size_t]
_kernel32.GlobalLock.restype = LPVOID
_kernel32.GlobalLock.argtypes = [HGLOBAL]
_kernel32.GlobalUnlock.restype = BOOL
_kernel32.GlobalUnlock.argtypes = [HGLOBAL]
_kernel32.SetLastError.restype = DWORD
_kernel32.SetLastError.argtypes = []
_kernel32.SetWaitableTimer.restype = BOOL
_kernel32.SetWaitableTimer.argtypes = [HANDLE, POINTER(LARGE_INTEGER), LONG, LPVOID, LPVOID, BOOL]  # TIMERAPCPROC
_kernel32.WaitForSingleObject.restype = DWORD
_kernel32.WaitForSingleObject.argtypes = [HANDLE, DWORD]

