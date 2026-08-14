from ctypes import HRESULT, POINTER, byref, c_char_p, c_wchar_p, windll, wintypes
from uuid import UUID

# https://learn.microsoft.com/en-us/windows/win32/shell/knownfolderid
FOLDERID_Downloads = UUID("{374DE290-123F-4565-9164-39C4925E467B}")

SHGetKnownFolderPath = windll.shell32.SHGetKnownFolderPath
SHGetKnownFolderPath.restype = HRESULT
SHGetKnownFolderPath.argtypes = [
    c_char_p,  # REFKNOWNFOLDERID rfid (pointer to 16 byte GUID data)
    wintypes.DWORD,  # DWORD dwFlags
    wintypes.HANDLE,  # HANDLE hToken
    POINTER(c_wchar_p),  # PWSTR *ppszPath
]

CoTaskMemFree = windll.ole32.CoTaskMemFree
CoTaskMemFree.restype = None
CoTaskMemFree.argtypes = [c_wchar_p]


def get_known_folder_path(folder_id):
    """Return the current path of a Windows known folder as a string.

    :param folder_id: The :any:`uuid.UUID` of the known folder.
    """
    path_ptr = c_wchar_p()
    # The HRESULT restype raises OSError if the call fails.
    SHGetKnownFolderPath(folder_id.bytes_le, 0, None, byref(path_ptr))
    try:
        return path_ptr.value
    finally:
        CoTaskMemFree(path_ptr)
