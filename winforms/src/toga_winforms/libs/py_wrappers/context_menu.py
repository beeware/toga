from __future__ import annotations

import ctypes
import errno
from contextlib import ExitStack
from ctypes import byref, windll
from pathlib import WindowsPath
from typing import TYPE_CHECKING, Iterable, Protocol, cast, runtime_checkable

import comtypes  # pyright: ignore[reportMissingTypeStubs]
import comtypes.client  # pyright: ignore[reportMissingTypeStubs]

from toga_winforms.libs.win_wrappers.hwnd import SimplePyHWND

if TYPE_CHECKING:
    import os
    from typing import Any, Callable, Sequence

    from typing_extensions import Literal
    from win32com.client.dynamic import CDispatch


def safe_isfile(path: WindowsPath) -> bool | None:
    try:
        result: bool = path.is_file()
    except (OSError, ValueError):
        return None
    else:
        return result


def safe_isdir(path: WindowsPath) -> bool | None:
    try:
        result: bool = path.is_dir()
    except (OSError, ValueError):
        return None
    else:
        return result


def create_dispatch_shell() -> CDispatch | ShellNamespace:
    try:
        import win32com.client
    except ImportError:
        return comtypes.client.CreateObject("Shell.Application")
    else:
        return win32com.client.Dispatch("Shell.Application")


def get_context_menu_functions() -> tuple[bool, Callable[..., Any], Callable[..., Any], Callable[..., Any], Callable[..., Any], int, int, int]:
    try:
        import win32con
        import win32gui
    except ImportError:
        return (False, windll.user32.AppendMenuW, windll.user32.CreatePopupMenu, windll.user32.GetCursorPos, windll.user32.TrackPopupMenu,
                0x0000, 0x0000, 0x0100)
    else:
        return (True, win32gui.AppendMenu, win32gui.CreatePopupMenu, win32gui.GetCursorPos, win32gui.TrackPopupMenu,
            win32con.MF_STRING, win32con.TPM_LEFTALIGN, win32con.TPM_RETURNCMD)


class _Vector2:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y


class _POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]  # noqa: RUF012


@runtime_checkable
class ShellNamespace(Protocol):
    def NameSpace(self, folder: str | Literal[0]) -> ShellFolder:
        ...


@runtime_checkable
class ShellFolder(Protocol):
    def ParseName(self, name: str) -> ShellFolderItem:
        ...


@runtime_checkable
class ShellFolderItem(Protocol):
    def Verbs(self) -> ShellFolderItemVerbs:
        ...


@runtime_checkable
class ShellFolderItemVerbs(Protocol):
    def Item(self, index: int) -> ShellFolderItemVerb:
        ...
    def __getitem__(self, index: int) -> ShellFolderItemVerb:
        ...
    def __len__(self) -> int:
        ...


@runtime_checkable
class ShellFolderItemVerb(Protocol):
    def DoIt(self) -> None:
        ...
    @property
    def Name(self) -> str:
        ...


def get_cursor_pos(c_getcursorpos: Callable, *, use_pywin32: bool) -> _Vector2:
    if use_pywin32:
        return _Vector2(*c_getcursorpos())
    pt = _POINT()
    c_getcursorpos(byref(pt))
    return cast(_Vector2, pt)


def show_context_menu(context_menu: CDispatch | ShellFolderItemVerbs, hwnd: int | None):
    # assert isinstance(context_menu, Iterable)  # this fails!
    assert hasattr(context_menu, "__iter__")  # this also fails!
    if not hasattr(context_menu, "__getitem__"):
        raise TypeError(f"Expected arg1 to be Iterable or something similar: {context_menu} ({context_menu.__class__.__name__})")

    pywin32_available, AppendMenu, CreatePopupMenu, GetCursorPos, TrackPopupMenu, MF_STRING, TPM_LEFTALIGN, TPM_RETURNCMD = get_context_menu_functions()
    hmenu = CreatePopupMenu()
    for i, verb in enumerate(context_menu):  # pyright: ignore[reportArgumentType]
        if verb.Name:
            AppendMenu(hmenu, MF_STRING, i + 1, verb.Name)
    pt: _Vector2 = get_cursor_pos(GetCursorPos, use_pywin32=pywin32_available)
    with ExitStack() as stack:
        hwnd = stack.enter_context(SimplePyHWND()) if hwnd is None else hwnd
        cmd = TrackPopupMenu(hmenu, TPM_LEFTALIGN | TPM_RETURNCMD,
                             pt.x, pt.y, 0, hwnd, None)
    if not isinstance(cmd, int):
        raise RuntimeError("Unable to open the context manager, reason unknown")  # noqa: TRY004
    verb = context_menu.Item(cmd - 1)
    if verb:
        verb.DoIt()


def windows_context_menu_file(
    file_path: os.PathLike | str,
    hwnd: int | None = None,
) -> None:
    parsed_filepath: WindowsPath = WindowsPath(file_path).resolve()
    shell = create_dispatch_shell()
    folder_object = shell.NameSpace(str(parsed_filepath.parent))
    folder_item = folder_object.ParseName(parsed_filepath.name)
    show_context_menu(folder_item.Verbs(), hwnd)


def windows_context_menu_multiple(
    paths: Sequence[os.PathLike | str],
    hwnd: int | None = None,
):
    parsed_paths: list[WindowsPath] = [WindowsPath(path).resolve() for path in paths]
    folder_items = []
    shell = create_dispatch_shell()
    for path in parsed_paths:
        folder_object = shell.NameSpace(str(path.parent if safe_isfile(path) else path))
        item = folder_object.ParseName(path.name)  # Following happens when path doesn't exist: `AttributeError: 'NoneType' object has no attribute 'ParseName'`
        folder_items.append(item)
    show_context_menu(folder_items[0].Verbs(), hwnd)


def windows_context_menu_folder(
    folder_path: os.PathLike | str,
    hwnd: int | None = None,
) -> None:
    parsed_folderpath: WindowsPath = WindowsPath(folder_path).resolve()
    shell = create_dispatch_shell()
    desktop_object = shell.NameSpace(0)
    folder_item = desktop_object.ParseName(str(parsed_folderpath))
    context_menu = folder_item.Verbs()
    show_context_menu(context_menu, hwnd)


def windows_context_menu(path: os.PathLike | str | Iterable[os.PathLike | str], hwnd: int | None = None):
    if isinstance(path, Iterable):
        paths = list(path)
        if not paths:
            return
        if len(paths) > 1:
            windows_context_menu_multiple(paths, hwnd)
            return
        parsed_path: WindowsPath = WindowsPath(paths[0])
    else:
        parsed_path = WindowsPath(path)

    if safe_isfile(parsed_path):
        windows_context_menu_file(parsed_path, hwnd)
    elif safe_isdir(parsed_path):
        windows_context_menu_folder(parsed_path, hwnd)
    else:
        msg = f"Path is neither file nor folder: '{path}'"
        raise FileNotFoundError(errno.ENOENT, msg, str(path))


# Example usage
if __name__ == "__main__":
    windows_context_menu(r"C:\Users\Wizard\test_folder\City.sol")

    multiple_files = [
        r"C:\Users\Wizard\test_folder\RestoreBackup.ps1",
        r"C:\Users\Wizard\test_folder\City.sol",
    ]
    windows_context_menu_multiple(multiple_files)

    folderpath = r"C:\Users\Wizard\test_folder"
    windows_context_menu_folder(folderpath)
