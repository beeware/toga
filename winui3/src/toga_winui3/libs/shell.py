import ctypes.wintypes as wt
from ctypes import POINTER, windll

from . import win32structures as ws

shell32 = windll.shell32


# learn.microsoft.com/windows/win32/api/shellapi/nf-shellapi-shell_notifyicongetrect
Shell_NotifyIconGetRect = shell32.Shell_NotifyIconGetRect
Shell_NotifyIconGetRect.restype = wt.HANDLE
Shell_NotifyIconGetRect.argtypes = [POINTER(ws.NOTIFYICONIDENTIFIER), POINTER(wt.RECT)]


# learn.microsoft.com/windows/win32/api/shellapi/nf-shellapi-shell_notifyiconw
Shell_NotifyIconW = shell32.Shell_NotifyIconW
Shell_NotifyIconW.restype = wt.BOOL
Shell_NotifyIconW.argtypes = [wt.DWORD, POINTER(ws.NOTIFYICONDATAW)]
