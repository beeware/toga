from ctypes import Structure as c_Structure, windll
from ctypes.wintypes import DWORD, HMODULE, LANGID, LPCWSTR, ULONG, USHORT

kernel32 = windll.kernel32


# https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-actctxw
class ACTCTXW(c_Structure):
    _fields_ = [
        ("cbSize", ULONG),
        ("dwFlags", DWORD),
        ("lpSource", LPCWSTR),
        ("wProcessorArchitecture", USHORT),
        ("wLangId", LANGID),
        ("lpAssemblyDirectory", LPCWSTR),
        ("lpResourceName", LPCWSTR),
        ("lpApplicationName", LPCWSTR),
        ("hModule", HMODULE),
    ]
