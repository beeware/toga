from __future__ import annotations

import asyncio
from ctypes import (
    HRESULT,
    POINTER,
    byref,
    c_int,
    c_void_p,
    c_wchar_p,
    sizeof,
    windll,
)
from ctypes import cast as cast_with_ctypes
from ctypes.wintypes import HWND, LPCWSTR
from pathlib import Path
from typing import TYPE_CHECKING

import comtypes
import comtypes.client
from comtypes import GUID
from comtypes.hresult import S_OK

from toga_winforms.libs.win_wrappers.com.interfaces import (
    COMDLG_FILTERSPEC,
    CLSID_FileOpenDialog,
    CLSID_FileSaveDialog,
    FileOpenOptions,
    IFileOpenDialog,
    IFileSaveDialog,
    IShellItem,
    IShellItemArray,
)
from toga_winforms.libs.win_wrappers.hwnd import (
    ES_AUTOVSCROLL,
    ES_MULTILINE,
    ES_READONLY,
    IDCANCEL,
    IDOK,
    IDYES,
    MB_ICONASTERISK,
    MB_ICONEXCLAMATION,
    MB_ICONHAND,
    MB_ICONQUESTION,
    MB_OK,
    MB_OKCANCEL,
    MB_YESNO,
    SW_SHOW,
    WM_COMMAND,
    WM_DESTROY,
    WNDPROC,
    WS_CHILD,
    WS_EX_DLGMODALFRAME,
    WS_OVERLAPPEDWINDOW,
    WS_VISIBLE,
    WS_VSCROLL,
    CursorType,
    MessageBoxW,
    ctypesWNDCLASS,
)

if TYPE_CHECKING:
    import os


class BaseDialog:
    def show(self, host_window, future):
        self.future = future

        # Don't differentiate between app and window modal dialogs
        # Show the dialog using an inner loop.
        asyncio.get_event_loop().start_inner_loop(self._show)


class MessageDialog(BaseDialog):
    def __init__(self, title, message, buttons, icon, success_result=None):
        super().__init__()
        self.message = message
        self.title = title
        self.buttons = buttons
        self.icon = icon
        self.success_result = success_result

    def _show(self):
        style = self.buttons | self.icon
        return_value = MessageBoxW(0, self.message, self.title, style)
        if self.success_result:
            self.future.set_result(return_value == self.success_result)
        else:
            self.future.set_result(None)


class InfoDialog(MessageDialog):
    def __init__(self, title, message):
        super().__init__(title, message, MB_OK, MB_ICONASTERISK)


class QuestionDialog(MessageDialog):
    def __init__(self, title, message):
        super().__init__(title, message, MB_YESNO, MB_ICONQUESTION, success_result=IDYES)


class ConfirmDialog(MessageDialog):
    def __init__(self, title, message):
        super().__init__(title, message, MB_OKCANCEL, MB_ICONEXCLAMATION, success_result=IDOK)


class ErrorDialog(MessageDialog):
    def __init__(self, title, message=None):
        super().__init__(title, message, MB_OK, MB_ICONHAND)


class StackTraceDialog(BaseDialog):
    def __init__(self, title, message, content, retry):
        super().__init__()
        self.title = title
        self.message = message
        self.content = content
        self.retry = retry
        self.hwnd = None
        self.hInstance = windll.kernel32.GetModuleHandleW(None)
        self._register_class()

    def _register_class(self):
        wnd_class = ctypesWNDCLASS()
        wnd_class.cbSize = sizeof(ctypesWNDCLASS)
        wnd_class.style = 0
        wnd_class.lpfnWndProc = WNDPROC(self._wnd_proc)
        wnd_class.cbClsExtra = 0
        wnd_class.cbWndExtra = 0
        wnd_class.hInstance = self.hInstance
        wnd_class.hIcon = windll.user32.LoadIconW(None, c_wchar_p(CursorType.ARROW.value))  # IDI_APPLICATION
        wnd_class.hCursor = windll.user32.LoadCursorW(None, c_wchar_p(CursorType.ARROW.value))  # IDC_ARROW
        wnd_class.hbrBackground = windll.gdi32.GetStockObject(15)  # WHITE_BRUSH
        wnd_class.lpszClassName = "StackTraceDialogClass"
        wnd_class.hIconSm = windll.user32.LoadIconW(None, c_wchar_p(CursorType.ARROW.value))  # IDI_APPLICATION

        self.class_atom = LPCWSTR(windll.user32.RegisterClassExW(byref(wnd_class)))

    def _create_dialog(self):
        self.hwnd = windll.user32.CreateWindowExW(
            WS_EX_DLGMODALFRAME,
            self.class_atom,
            self.title,
            WS_OVERLAPPEDWINDOW | WS_VISIBLE,
            100, 100, 540, 320,
            None, None, self.hInstance, None
        )
        # SetWindowTextW is used to set the window title
        windll.user32.SetWindowTextW(self.hwnd, self.title)

        # Create controls
        self._create_controls()

        windll.user32.ShowWindow(self.hwnd, SW_SHOW)
        windll.user32.UpdateWindow(self.hwnd)

    def _create_controls(self):
        # Create the label
        hLabel = windll.user32.CreateWindowExW(
            0, "STATIC", self.message,
            WS_CHILD | WS_VISIBLE,
            10, 10, 520, 20,
            self.hwnd, None, self.hInstance, None
        )

        # Create the multiline text box for the stack trace
        hEdit = windll.user32.CreateWindowExW(
            0, "EDIT", self.content,
            WS_CHILD | WS_VISIBLE | ES_MULTILINE | ES_AUTOVSCROLL | ES_READONLY | WS_VSCROLL,
            10, 30, 504, 210,
            self.hwnd, None, self.hInstance, None
        )

        # Create buttons based on whether retry is needed
        if self.retry:
            hRetry = windll.user32.CreateWindowExW(
                0, "BUTTON", "&Retry",
                WS_CHILD | WS_VISIBLE,
                290, 250, 100, 30,
                self.hwnd, IDOK, self.hInstance, None
            )
            hQuit = windll.user32.CreateWindowExW(
                0, "BUTTON", "&Quit",
                WS_CHILD | WS_VISIBLE,
                400, 250, 100, 30,
                self.hwnd, IDCANCEL, self.hInstance, None
            )
        else:
            hOk = windll.user32.CreateWindowExW(
                0, "BUTTON", "&OK",
                WS_CHILD | WS_VISIBLE,
                400, 250, 100, 30,
                self.hwnd, IDOK, self.hInstance, None
            )

    def _wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == WM_COMMAND:
            control_id = wparam & 0xFFFF
            if control_id == IDOK:
                self._handle_ok()
            elif control_id == IDCANCEL:
                self._handle_cancel()
            windll.user32.DestroyWindow(hwnd)
        elif msg == WM_DESTROY:
            windll.user32.DestroyWindow(hwnd)
        return windll.user32.DefWindowProcW(hwnd, msg, wparam, lparam)

    def _show(self):
        self._create_dialog()
        # MessageBox to show dialog (optional)
        windll.user32.MessageBoxW(self.hwnd, self.message, self.title, MB_OK)
        if self.retry:
            self.future.set_result(True)
        else:
            self.future.set_result(None)

    def _handle_ok(self):
        self.future.set_result(True)
        windll.user32.DestroyWindow(self.hwnd)

    def _handle_cancel(self):
        self.future.set_result(False)
        windll.user32.DestroyWindow(self.hwnd)


class FileDialog(BaseDialog):
    def __init__(
        self,
        native: IFileOpenDialog | IFileSaveDialog,
        title: str,
        initial_directory: os.PathLike | str,
        *,
        filename: str | None = None,
        file_types: list[str] | None = None,
    ):
        super().__init__()
        self.native: IFileOpenDialog | IFileSaveDialog = native

        self._set_title(title)
        if filename is not None:
            self.native.SetFileName(filename)

        if initial_directory is not None:
            self._set_initial_directory(str(initial_directory))

        if file_types is not None:
            filters: list[tuple[str, str]] = [
                (f"{ext.upper()} files", f"*.{ext}")
                for ext in file_types
            ]
            filterspec = (COMDLG_FILTERSPEC * len(file_types))(
                *[
                    (c_wchar_p(name), c_wchar_p(spec))
                    for name, spec in filters
                ]
            )
            self.native.SetFileTypes(len(filterspec), cast_with_ctypes(filterspec, POINTER(c_void_p)))

    def _show(self):
        hwnd = HWND(0)
        hr: int = self.native.Show(hwnd)
        if hr == S_OK:
            assert isinstance(self, (SaveFileDialog, OpenFileDialog, SelectFolderDialog))
            self.future.set_result(self._get_filenames())
        else:
            self.future.set_result(None)

    def _set_title(self, title: str):
        self.native.SetTitle(title)

    def _set_initial_directory(self, initial_directory: os.PathLike | str | None):
        if initial_directory is None:
            return
        folder_path: Path = Path(initial_directory).resolve()
        if folder_path.is_dir():  # sourcery skip: extract-method
            SHCreateItemFromParsingName = windll.shell32.SHCreateItemFromParsingName
            SHCreateItemFromParsingName.argtypes = [
                c_wchar_p,                            # LPCWSTR (wide string, null-terminated)
                POINTER(comtypes.IUnknown),           # IBindCtx* (can be NULL, hence POINTER(IUnknown))
                POINTER(GUID),                        # REFIID (pointer to the interface ID, typically GUID)
                POINTER(POINTER(IShellItem))          # void** (output pointer to the requested interface)
            ]
            SHCreateItemFromParsingName.restype = HRESULT
            shell_item = POINTER(IShellItem)()
            hr = SHCreateItemFromParsingName(str(folder_path), None, IShellItem._iid_, byref(shell_item))
            if hr == S_OK:
                self.native.SetFolder(shell_item)


class SaveFileDialog(FileDialog):
    def __init__(
        self,
        title: str,
        filename: str,
        initial_directory: os.PathLike | str,
        file_types: list[str],
    ):
        super().__init__(
            comtypes.client.CreateObject(CLSID_FileSaveDialog, interface=IFileSaveDialog),
            title,
            initial_directory,
            filename=filename,
            file_types=file_types,
        )

    def _get_filenames(self):
        shell_item: IShellItem = self.native.GetResult()
        display_name: str = shell_item.GetDisplayName(0x80058000)  # SIGDN_FILESYSPATH
        return Path(display_name)


class OpenFileDialog(FileDialog):
    def __init__(
        self,
        title: str,
        initial_directory: os.PathLike | str,
        file_types: list[str],
        multiple_select: bool,
    ):
        super().__init__(
            comtypes.client.CreateObject(CLSID_FileOpenDialog, interface=IFileOpenDialog),
            title,
            initial_directory,
            file_types=file_types,
        )
        if multiple_select:
            self.native.SetOptions(FileOpenOptions.FOS_ALLOWMULTISELECT)

    def selected_paths(self):
        # This is a stub method; we provide functionality using the COM API
        return self._get_filenames()

    def _get_filenames(self) -> list[Path]:
        assert isinstance(self.native, IFileOpenDialog)
        results: list[Path] = []
        shell_item_array: IShellItemArray = self.native.GetResults()
        item_count: int = shell_item_array.GetCount()
        for i in range(item_count):
            shell_item: IShellItem = shell_item_array.GetItemAt(i)
            szFilePath: str = str(shell_item.GetDisplayName(0x80058000))  # SIGDN_FILESYSPATH
            results.append(Path(szFilePath))
        return results


class SelectFolderDialog(FileDialog):
    def __init__(
        self,
        title: str,
        initial_directory: os.PathLike | str,
        multiple_select: bool,
    ):
        super().__init__(
            comtypes.client.CreateObject(CLSID_FileOpenDialog, interface=IFileOpenDialog),
            title,
            initial_directory,
        )
        self.native.SetOptions(FileOpenOptions.FOS_PICKFOLDERS)
        self.multiple_select: bool = multiple_select

    def _get_filenames(self) -> list[Path] | Path:
        shell_item: IShellItem = self.native.GetResult()
        display_name: str = shell_item.GetDisplayName(0x80058000)  # SIGDN_FILESYSPATH
        return [Path(display_name)] if self.multiple_select else Path(display_name)

    def _set_title(self, title):
        self.native.SetTitle(title)

    def _set_initial_directory(self, initial_directory):
        if initial_directory is None:
            return
        folder_path: Path = Path(initial_directory).resolve()
        if folder_path.is_dir():  # sourcery skip: extract-method
            SHCreateItemFromParsingName = windll.shell32.SHCreateItemFromParsingName
            SHCreateItemFromParsingName.argtypes = [
                c_wchar_p,                            # LPCWSTR (wide string, null-terminated)
                POINTER(comtypes.IUnknown),           # IBindCtx* (can be NULL, hence POINTER(IUnknown))
                POINTER(GUID),                        # REFIID (pointer to the interface ID, typically GUID)
                POINTER(POINTER(IShellItem))          # void** (output pointer to the requested interface)
            ]
            SHCreateItemFromParsingName.restype = HRESULT
            shell_item = POINTER(IShellItem)()
            hr = SHCreateItemFromParsingName(str(folder_path), None, IShellItem._iid_, byref(shell_item))
            if hr == S_OK:
                self.native.SetFolder(shell_item)
