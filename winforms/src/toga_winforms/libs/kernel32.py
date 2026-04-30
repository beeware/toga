from ctypes import POINTER, windll
from ctypes.wintypes import DWORD, HANDLE

from .win32structures import ACTCTXW, ULONG_PTR

kernel32 = windll.kernel32


# https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-activateactctx
ActivateActCtx = kernel32.ActivateActCtx
ActivateActCtx.argtypes = [HANDLE, POINTER(ULONG_PTR)]


# https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createactctxw
CreateActCtxW = kernel32.CreateActCtxW
CreateActCtxW.restype = HANDLE
CreateActCtxW.argtypes = [POINTER(ACTCTXW)]


# https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-deactivateactctx
DeactivateActCtx = kernel32.DeactivateActCtx
DeactivateActCtx.argtypes = [DWORD, ULONG_PTR]


# https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-releaseactctx
ReleaseActCtx = kernel32.ReleaseActCtx
ReleaseActCtx.restype = None
ReleaseActCtx.argtypes = [HANDLE]
