from __future__ import annotations

from ctypes import Structure, c_char_p, c_int, c_ssize_t, c_ulong, c_void_p, windll
from ctypes.wintypes import BOOL, DWORD, HANDLE, HINSTANCE, HKEY
from typing import Any

# context menu properties
SEE_MASK_NOCLOSEPROCESS = 0x00000040
SEE_MASK_INVOKEIDLIST = 0x0000000C

LRESULT = c_ssize_t


class SHELLEXECUTEINFO(Structure):
    _fields_ = (
        ("cbSize", DWORD),
        ("fMask", c_ulong),
        ("hwnd", HANDLE),
        ("lpVerb", c_char_p),
        ("lpFile", c_char_p),
        ("lpParameters", c_char_p),
        ("lpDirectory", c_char_p),
        ("nShow", c_int),
        ("hInstApp", HINSTANCE),
        ("lpIDList", c_void_p),
        ("lpClass", c_char_p),
        ("hKeyClass", HKEY),
        ("dwHotKey", DWORD),
        ("hIconOrMonitor", HANDLE),
        ("hProcess", HANDLE),
    )
    cbSize: int
    fMask: int
    hwnd: int
    lpVerb: bytes
    lpFile: bytes
    lpParameters: bytes
    lpDirectory: bytes
    nShow: int
    hInstApp: Any | c_void_p
    lpIDList: Any | c_void_p
    lpClass: bytes
    hKeyClass: Any | c_void_p
    dwHotKey: int
    hIconOrMonitor: int
    hProcess: int


ShellExecuteEx = windll.shell32.ShellExecuteEx
ShellExecuteEx.restype = BOOL
