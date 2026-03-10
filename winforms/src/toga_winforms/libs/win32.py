from ctypes import POINTER, c_size_t
from ctypes.wintypes import HWND, LPARAM, RECT

LRESULT = LPARAM  # LPARAM is essentially equivalent to LRESULT
UINT_PTR = c_size_t
DWORD_PTR = c_size_t
PUINT = c_size_t
INT_PTR = c_size_t
RECT_PTR = POINTER(RECT)
HBRUSH = HWND
HIMAGELIST = HWND
