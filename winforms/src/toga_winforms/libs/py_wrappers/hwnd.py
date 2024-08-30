from __future__ import annotations


from ctypes import POINTER, WINFUNCTYPE, Structure, c_int, c_wchar_p, windll, c_long, c_uint, c_void_p
from ctypes.wintypes import ATOM, BOOL, DWORD, HBRUSH, HICON, HINSTANCE, HMENU, HWND, LPARAM, LPCWSTR, LPVOID, UINT, WPARAM

from toga_winforms.libs.py_wrappers.common import LRESULT
from enum import IntEnum
from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from ctypes import (
        _CData,
        _FuncPointer,
    )
    from ctypes.wintypes import HMENU, LPVOID
    from types import TracebackType

    from _win32typing import PyResourceId  # pyright: ignore[reportMissingModuleSource]


WNDPROC: type[_FuncPointer] = WINFUNCTYPE(c_long, HWND, c_uint, WPARAM, LPARAM)
WM_DESTROY = 0x0002
WS_OVERLAPPEDWINDOW = (0x00CF0000)
WS_VISIBLE = 0x10000000
HCURSOR = c_void_p


class ctypesWNDCLASS(Structure):  # noqa: N801
    _fields_: Sequence[tuple[str, type[_CData]] | tuple[str, type[_CData], int]] = [
        ("style", UINT),
        ("lpfnWndProc", WNDPROC),
        ("cbClsExtra", c_int),
        ("cbWndExtra", c_int),
        ("hInstance", HINSTANCE),
        ("hIcon", HICON),
        ("hCursor", HCURSOR),
        ("hbrBackground", HBRUSH),
        ("lpszMenuName", LPCWSTR),
        ("lpszClassName", LPCWSTR)
    ]




# Constants for MessageBox
MB_OK = 0x0
MB_OKCANCEL = 0x1
MB_ABORTRETRYIGNORE = 0x2
MB_YESNOCANCEL = 0x3
MB_YESNO = 0x4
MB_RETRYCANCEL = 0x5
MB_CANCELTRYCONTINUE = 0x6

MB_ICONHAND = 0x10
MB_ICONQUESTION = 0x20
MB_ICONEXCLAMATION = 0x30
MB_ICONASTERISK = 0x40

MB_DEFBUTTON1 = 0x0
MB_DEFBUTTON2 = 0x100
MB_DEFBUTTON3 = 0x200
MB_DEFBUTTON4 = 0x300

MB_APPLMODAL = 0x0
MB_SYSTEMMODAL = 0x1000
MB_TASKMODAL = 0x2000

MB_ICONERROR = MB_ICONHAND
MB_ICONWARNING = MB_ICONEXCLAMATION
MB_ICONINFORMATION = MB_ICONASTERISK

MB_RIGHT = 0x800
MB_RTLREADING = 0x1000

IDOK = 1
IDCANCEL = 2
IDABORT = 3
IDRETRY = 4
IDIGNORE = 5
IDYES = 6
IDNO = 7
IDTRYAGAIN = 10
IDCONTINUE = 11

WS_EX_DLGMODALFRAME = 0x00000001

windll.user32.MessageBoxW.argtypes = [c_int, c_wchar_p, c_wchar_p, c_int]
windll.user32.MessageBoxW.restype = c_int

CBTProc = WINFUNCTYPE(c_int, c_int, WPARAM, LPARAM)
SetWindowsHookExW = windll.user32.SetWindowsHookExW
UnhookWindowsHookEx = windll.user32.UnhookWindowsHookEx
CallNextHookEx = windll.user32.CallNextHookEx
GetWindowRect = windll.user32.GetWindowRect
MoveWindow = windll.user32.MoveWindow

# Windows API function prototypes
MessageBoxW = windll.user32.MessageBoxW
MessageBoxW.argtypes = [HWND, LPCWSTR, LPCWSTR, UINT]
MessageBoxW.restype = c_int

CreateWindowExW = windll.user32.CreateWindowExW
CreateWindowExW.argtypes = [
    DWORD, LPCWSTR, LPCWSTR, DWORD,
    c_int, c_int, c_int, c_int,
    HWND, HMENU, HINSTANCE, LPVOID
]
CreateWindowExW.restype = HWND

DefWindowProcW = windll.user32.DefWindowProcW
DefWindowProcW.argtypes = [HWND, UINT, WPARAM, LPARAM]
DefWindowProcW.restype = LRESULT

RegisterClassExW = windll.user32.RegisterClassExW
RegisterClassExW.argtypes = [POINTER(ctypesWNDCLASS)]
RegisterClassExW.restype = ATOM

GetModuleHandleW = windll.kernel32.GetModuleHandleW
GetModuleHandleW.argtypes = [LPCWSTR]
GetModuleHandleW.restype = HINSTANCE

LoadIconW = windll.user32.LoadIconW
LoadIconW.argtypes = [HINSTANCE, LPCWSTR]
LoadIconW.restype = HICON

LoadCursorW = windll.user32.LoadCursorW
LoadCursorW.argtypes = [HINSTANCE, LPCWSTR]
LoadCursorW.restype = HCURSOR

ShowWindow = windll.user32.ShowWindow
ShowWindow.argtypes = [HWND, c_int]
ShowWindow.restype = BOOL

UpdateWindow = windll.user32.UpdateWindow
UpdateWindow.argtypes = [HWND]
UpdateWindow.restype = BOOL

SetWindowTextW = windll.user32.SetWindowTextW
SetWindowTextW.argtypes = [HWND, LPCWSTR]
SetWindowTextW.restype = BOOL

CreateDialogParamW = windll.user32.CreateDialogParamW
CreateDialogParamW.argtypes = [HINSTANCE, LPCWSTR, HWND, LPVOID, LPARAM]
CreateDialogParamW.restype = HWND

DestroyWindow = windll.user32.DestroyWindow
DestroyWindow.argtypes = [HWND]
DestroyWindow.restype = BOOL

# Constants for Window Styles
WS_OVERLAPPEDWINDOW = 0x00CF0000
WS_VISIBLE = 0x10000000
WS_CHILD = 0x40000000

SW_SHOW = 5
# Constants for window creation and message handling
WM_COMMAND = 0x0111
WM_DESTROY = 0x0002
WS_OVERLAPPEDWINDOW = 0x00CF0000
WS_VISIBLE = 0x10000000
WS_CHILD = 0x40000000
SW_SHOW = 5
SW_HIDE = 0
ES_MULTILINE = 0x0004
ES_AUTOVSCROLL = 0x0040
ES_READONLY = 0x0800
WS_VSCROLL = 0x00200000
WS_EX_DLGMODALFRAME = 0x00000001
IDOK = 1
IDCANCEL = 2


def wnd_proc(
    hwnd: HWND,
    message: c_uint,
    wparam: WPARAM,
    lparam: LPARAM,
) -> c_long:
    if message == WM_DESTROY:
        windll.user32.PostQuitMessage(0)
        return c_long(0)
    print(f"wnd_proc(hwnd={hwnd}, message={message}, wparam={wparam}, lparam={lparam})")
    result = windll.user32.DefWindowProcW(hwnd, message, wparam, lparam)
    if isinstance(result, int):
        return c_long(result)
    print(result, "result is unexpectedly class:", result.__class__.__name__)
    return result


class CursorType(IntEnum):
    ARROW = 32512
    IBEAM = 32513
    WAIT = 32514
    CROSS = 32515
    UPARROW = 32516
    SIZE = 32640
    ICON = 32641
    SIZENWSE = 32642
    SIZENESW = 32643
    SIZEWE = 32644
    SIZENS = 32645
    SIZEALL = 32646
    NO = 32648
    HAND = 32649
    APPSTARTING = 32650
    HELP = 32651


class SimplePyHWND:
    """Context manager for creating and destroying a simple custom window."""
    CLASS_NAME: str = "SimplePyHWND"
    DISPLAY_NAME: str = "Python Simple Window"

    def __init__(
        self,
        *,
        visible: bool = False,
        dwExStyle: int = 0,  # noqa: N803
        lpClassName: PyResourceId | str | None = None,  # noqa: N803
        lpWindowName: str | None = None,  # noqa: N803
        dwStyle: int | None = None,  # noqa: N803
        x: int = 0,
        y: int = 0,
        nWidth: int = 1280,  # noqa: N803
        nHeight: int = 720,  # noqa: N803
        hWndParent: HWND | None = None,  # noqa: N803
        hMenu: HMENU | None = None,  # noqa: N803
        hInstance: HINSTANCE | None = None,  # noqa: N803
        lpParam: LPVOID | None = None,  # noqa: N803
    ):
        self.hwnd: int | None = None
        self.visible: bool = visible
        self.dwExStyle: int = dwExStyle
        self.lpClassName: PyResourceId | str | None = lpClassName or self.CLASS_NAME
        self.lpWindowName: str | None = lpWindowName or self.DISPLAY_NAME
        self.dwStyle: int | None = WS_OVERLAPPEDWINDOW | WS_VISIBLE if visible else (dwStyle or 0)
        self.x: int = x
        self.y: int = y
        self.nWidth: int = nWidth
        self.nHeight: int = nHeight
        self.hWndParent: HWND | None = hWndParent
        self.hMenu: HMENU | None = hMenu
        self.hInstance: HINSTANCE | None = hInstance
        self.lpParam: LPVOID | None = lpParam

    def __enter__(self) -> int:
        self.register_class()
        self.hwnd = self.create_window()
        self._class_atom: PyResourceId | None = None
        return self.hwnd

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ):
        if self.hwnd is not None:
            windll.user32.DestroyWindow(self.hwnd)
        self.unregister_class()

    def register_class(self):
        """Register the window class."""
        import win32gui
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = WNDPROC(wnd_proc)  # pyright: ignore[reportAttributeAccessIssue]
        wc.lpszClassName = self.CLASS_NAME  # pyright: ignore[reportAttributeAccessIssue]
        self.hinst = wc.hInstance = win32gui.GetModuleHandle(None)  # pyright: ignore[reportAttributeAccessIssue]
        wc.hCursor = windll.user32.LoadCursorW(None, CursorType.ARROW.value)  # pyright: ignore[reportAttributeAccessIssue]
        try:
            self._class_atom = win32gui.RegisterClass(wc)
        except Exception as e:  # pywintypes.error
            if getattr(e, "winerror", None) != 1410:  # class already registered
                raise
            print(f"{e} (Class already registered)")

    def unregister_class(self):
        """Unregister the window class."""
        if self._class_atom is not None:
            import win32gui
            win32gui.UnregisterClass(self._class_atom, windll.kernel32.GetModuleHandleW(None))

    def create_window(self) -> int:
        """Create the window."""
        return windll.user32.CreateWindowExW(
            self.dwExStyle, self.lpClassName, self.lpWindowName, self.dwStyle,
            self.x, self.y, self.nWidth, self.nHeight,
            self.hWndParent, self.hMenu,
            windll.kernel32.GetModuleHandleW(None) if self.hInstance is None else self.hInstance,
            self.lpParam)


if __name__ == "__main__":
    import time

    with SimplePyHWND(visible=True) as hwnd:
        print(f"Created SimplePyHWND with handle: {hwnd}")
        time.sleep(3)
    print("SimplePyHWND has been destroyed.")
