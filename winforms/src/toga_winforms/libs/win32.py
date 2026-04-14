from ctypes import c_size_t
from ctypes.wintypes import HWND, LPARAM


# https://learn.microsoft.com/en-us/windows/win32/winmsg/loword
def loword(lparam: int) -> int:
    """Keeps the lower 16 bits of a value with at least 16 bits."""
    return lparam & 0b1111111111111111


# https://learn.microsoft.com/en-us/windows/win32/winmsg/hiword
def hiword(lparam: int) -> int:
    """Keeps the upper 16 bits of value with at least 32 bits."""
    return (lparam >> 16) & 0b1111111111111111


def is_submessage(message: int, submessage: int) -> bool:
    """Tests if a message is a bit-wise sub-message of a given message."""
    return (message & submessage) != 0


LRESULT = LPARAM  # LPARAM is essentially equivalent to LRESULT
UINT_PTR = c_size_t
ULONG_PTR = c_size_t
DWORD_PTR = c_size_t
PUINT = c_size_t
INT_PTR = c_size_t
HIMAGELIST = HWND
