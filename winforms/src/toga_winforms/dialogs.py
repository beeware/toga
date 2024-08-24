import asyncio
import os
from pathlib import Path

import comtypes
import comtypes.client

from comtypes import COMMETHOD, GUID
from comtypes.hresult import S_OK

from ctypes import HRESULT, POINTER, Structure, byref, c_int, c_uint, c_ulong, c_void_p, c_wchar_p, windll
from ctypes import cast as cast_with_ctypes
from ctypes.wintypes import BOOL, DWORD, HWND, LPCWSTR, LPWSTR
from enum import IntFlag
from typing import Callable, List, Optional, Tuple, Union

import System.Windows.Forms as WinForms
from System.Drawing import (
    ContentAlignment,
    Font as WinFont,
    FontFamily,
    FontStyle,
    SystemFonts,
)
from System.Windows.Forms import DialogResult, MessageBoxButtons, MessageBoxIcon

from .libs.wrapper import WeakrefCallable


class COMDLG_FILTERSPEC(Structure):  # noqa: N801
    _fields_ = [
        ("pszName", LPCWSTR),
        ("pszSpec", LPCWSTR)
    ]


class FileOpenOptions(IntFlag):
    FOS_OVERWRITEPROMPT = 0x00000002
    FOS_STRICTFILETYPES = 0x00000004
    FOS_NOCHANGEDIR = 0x00000008
    FOS_PICKFOLDERS = 0x00000020
    FOS_FORCEFILESYSTEM = 0x00000040
    FOS_ALLNONSTORAGEITEMS = 0x00000080
    FOS_NOVALIDATE = 0x00000100
    FOS_ALLOWMULTISELECT = 0x00000200
    FOS_PATHMUSTEXIST = 0x00000800
    FOS_FILEMUSTEXIST = 0x00001000
    FOS_CREATEPROMPT = 0x00002000
    FOS_SHAREAWARE = 0x00004000
    FOS_NOREADONLYRETURN = 0x00008000
    FOS_NOTESTFILECREATE = 0x00010000
    FOS_HIDEMRUPLACES = 0x00020000
    FOS_HIDEPINNEDPLACES = 0x00040000
    FOS_NODEREFERENCELINKS = 0x00100000
    FOS_DONTADDTORECENT = 0x02000000
    FOS_FORCESHOWHIDDEN = 0x10000000
    FOS_DEFAULTNOMINIMODE = 0x20000000
    FOS_FORCEPREVIEWPANEON = 0x40000000


IID_IShellItem = GUID("{43826D1E-E718-42EE-BC55-A1E261C37BFE}")
IID_IShellItemArray = GUID("{B63EA76D-1F85-456F-A19C-48159EFA858B}")
IID_IShellItemFilter = GUID("{2659B475-EEB8-48B7-8F07-B378810F48CF}")
IID_IModalWindow = GUID("{B4DB1657-70D7-485E-8E3E-6FCB5A5C1802}")
IID_IFileDialog = GUID("{42F85136-DB7E-439C-85F1-E4075D135FC8}")
IID_IFileOpenDialog = GUID("{D57C7288-D4AD-4768-BE02-9D969532D960}")
IID_IFileSaveDialog = GUID("{84BCCD23-5FDE-4CDB-AEA4-AF64B83D78AB}")
CLSID_FileOpenDialog = GUID("{DC1C5A9C-E88A-4dde-A5A1-60F82A20AEF7}")
CLSID_FileSaveDialog = GUID("{C0B4E2F3-BA21-4773-8DBA-335EC946EB8B}")


class IShellItem(comtypes.IUnknown):
    _case_insensitive_: bool = True
    _iid_: GUID = IID_IShellItem
    _methods_ = [
        COMMETHOD([], HRESULT, "BindToHandler",
                  (["in"], POINTER(comtypes.IUnknown), "pbc"),
                  (["in"], POINTER(GUID), "bhid"),
                  (["in"], POINTER(GUID), "riid"),
                  (["out"], POINTER(c_void_p), "ppv")),
        COMMETHOD([], HRESULT, "GetParent",
                  (["out"], POINTER(POINTER(comtypes.IUnknown)), "ppsi")),
        COMMETHOD([], HRESULT, "GetDisplayName",
                  (["in"], c_ulong, "sigdnName"),
                  (["out"], POINTER(LPWSTR), "ppszName")),
        COMMETHOD([], HRESULT, "GetAttributes",
                  (["in"], c_ulong, "sfgaoMask"),
                  (["out"], POINTER(c_ulong), "psfgaoAttribs")),
        COMMETHOD([], HRESULT, "Compare",
                  (["in"], POINTER(comtypes.IUnknown), "psi"),
                  (["in"], c_ulong, "hint"),
                  (["out"], POINTER(c_int), "piOrder"))
    ]
    QueryInterface: Callable[[GUID, comtypes.IUnknown], int]
    AddRef: Callable[[], int]
    Release: Callable[[], int]
    BindToHandler: Callable[[comtypes.IUnknown, GUID, GUID, c_void_p], int]
    GetParent: Callable[[], comtypes.IUnknown]
    GetDisplayName: Callable[[Union[c_ulong, int]], str]
    GetAttributes: Callable[[Union[c_ulong, int]], int]
    Compare: Callable[[comtypes.IUnknown, c_ulong, c_int], int]


class IShellItemArray(comtypes.IUnknown):
    _case_insensitive_: bool = True
    _iid_: GUID = IID_IShellItemArray
    _methods_ = [
        COMMETHOD([], HRESULT, "BindToHandler",
                  (["in"], POINTER(comtypes.IUnknown), "pbc"),
                  (["in"], POINTER(GUID), "bhid"),
                  (["in"], POINTER(GUID), "riid"),
                  (["out"], POINTER(c_void_p), "ppv")),
        COMMETHOD([], HRESULT, "GetPropertyStore",
                  (["in"], c_ulong, "flags"),
                  (["in"], POINTER(GUID), "riid"),
                  (["out"], POINTER(c_void_p), "ppv")),
        COMMETHOD([], HRESULT, "GetPropertyDescriptionList",
                  (["in"], POINTER(GUID), "keyType"),
                  (["in"], POINTER(GUID), "riid"),
                  (["out"], POINTER(c_void_p), "ppv")),
        COMMETHOD([], HRESULT, "GetAttributes",
                  (["in"], c_ulong, "attribFlags"),
                  (["in"], c_ulong, "sfgaoMask"),
                  (["out"], POINTER(c_ulong), "psfgaoAttribs")),
        COMMETHOD([], HRESULT, "GetCount",
                  (["out"], POINTER(c_uint), "pdwNumItems")),
        COMMETHOD([], HRESULT, "GetItemAt",
                  (["in"], c_uint, "dwIndex"),
                  (["out"], POINTER(POINTER(IShellItem)), "ppsi")),
        COMMETHOD([], HRESULT, "EnumItems",
                  (["out"], POINTER(POINTER(comtypes.IUnknown)), "ppenumShellItems"))
    ]
    QueryInterface: Callable[[GUID, comtypes.IUnknown], int]
    AddRef: Callable[[], int]
    Release: Callable[[], int]
    BindToHandler: Callable[[comtypes.IUnknown, GUID, GUID], int]
    GetPropertyStore: Callable[[int, GUID], c_void_p]
    GetPropertyDescriptionList: Callable[[GUID, GUID], c_void_p]
    GetAttributes: Callable[[int, int], int]
    GetCount: Callable[[], int]
    GetItemAt: Callable[[Union[int, int]], IShellItem]
    EnumItems: Callable[[], comtypes.IUnknown]


class IModalWindow(comtypes.IUnknown):
    _case_insensitive_: bool = True
    _iid_: GUID = IID_IModalWindow
    _methods_ = [
        COMMETHOD([], HRESULT, "Show",
                  (["in"], HWND, "hwndParent"))
    ]
    Show: Callable[[Union[int, HWND]], int]


class IFileDialog(IModalWindow):
    _iid_: GUID = IID_IFileDialog
    _methods_ = [
        COMMETHOD([], HRESULT, "SetFileTypes",
                  (["in"], c_uint, "cFileTypes"),
                  (["in"], POINTER(c_void_p), "rgFilterSpec")),
        COMMETHOD([], HRESULT, "SetFileTypeIndex",
                  (["in"], c_uint, "iFileType")),
        COMMETHOD([], HRESULT, "GetFileTypeIndex",
                  (["out"], POINTER(c_uint), "piFileType")),
        COMMETHOD([], HRESULT, "Advise",
                  (["in"], POINTER(comtypes.IUnknown), "pfde"),
                  (["out"], POINTER(DWORD), "pdwCookie")),
        COMMETHOD([], HRESULT, "Unadvise",
                  (["in"], DWORD, "dwCookie")),
        COMMETHOD([], HRESULT, "SetOptions",
                  (["in"], c_uint, "fos")),
        COMMETHOD([], HRESULT, "GetOptions",
                  (["out"], POINTER(DWORD), "pfos")),
        COMMETHOD([], HRESULT, "SetDefaultFolder",
                  (["in"], POINTER(IShellItem), "psi")),
        COMMETHOD([], HRESULT, "SetFolder",
                  (["in"], POINTER(IShellItem), "psi")),
        COMMETHOD([], HRESULT, "GetFolder",
                  (["out"], POINTER(POINTER(IShellItem)), "ppsi")),
        COMMETHOD([], HRESULT, "GetCurrentSelection",
                  (["out"], POINTER(POINTER(IShellItem)), "ppsi")),
        COMMETHOD([], HRESULT, "SetFileName",
                  (["in"], LPCWSTR, "pszName")),
        COMMETHOD([], HRESULT, "GetFileName",
                  (["out"], POINTER(LPWSTR), "pszName")),
        COMMETHOD([], HRESULT, "SetTitle",
                  (["in"], LPCWSTR, "pszTitle")),
        COMMETHOD([], HRESULT, "SetOkButtonLabel",
                  (["in"], LPCWSTR, "pszText")),
        COMMETHOD([], HRESULT, "SetFileNameLabel",
                  (["in"], LPCWSTR, "pszLabel")),
        COMMETHOD([], HRESULT, "GetResult",
                  (["out"], POINTER(POINTER(IShellItem)), "ppsi")),
        COMMETHOD([], HRESULT, "AddPlace",
                  (["in"], POINTER(IShellItem), "psi"),
                  (["in"], c_int, "fdap")),
        COMMETHOD([], HRESULT, "SetDefaultExtension",
                  (["in"], LPCWSTR, "pszDefaultExtension")),
        COMMETHOD([], HRESULT, "Close",
                  (["in"], HRESULT, "hr")),
        COMMETHOD([], HRESULT, "SetClientGuid",
                  (["in"], POINTER(GUID), "guid")),
        COMMETHOD([], HRESULT, "ClearClientData"),
        COMMETHOD([], HRESULT, "SetFilter",
                  (["in"], POINTER(comtypes.IUnknown), "pFilter"))  # IShellItemFilter
    ]
    SetFileTypes: Callable[[Union[c_uint, int], c_void_p], int]
    SetFileTypeIndex: Callable[[c_uint], int]
    GetFileTypeIndex: Callable[[], int]
    Advise: Callable[[Union[comtypes.IUnknown, comtypes.COMObject]], int]
    Unadvise: Callable[[int], int]
    SetOptions: Callable[[Union[int, int]], int]
    GetOptions: Callable[[], int]
    SetDefaultFolder: Callable[[IShellItem], int]
    SetFolder: Callable[[IShellItem], int]
    GetFolder: Callable[[], IShellItem]
    GetCurrentSelection: Callable[[], IShellItem]
    SetFileName: Callable[[str], int]
    GetFileName: Callable[[], str]
    SetTitle: Callable[[str], int]
    SetOkButtonLabel: Callable[[str], int]
    SetFileNameLabel: Callable[[str], int]
    GetResult: Callable[[], IShellItem]
    AddPlace: Callable[[IShellItem, c_int], int]
    SetDefaultExtension: Callable[[str], int]
    Close: Callable[[HRESULT], int]
    SetClientGuid: Callable[[GUID], int]
    ClearClientData: Callable[[], int]
    SetFilter: Callable[[comtypes.IUnknown], int]


class IFileOpenDialog(IFileDialog):
    _case_insensitive_: bool = True
    _iid_: GUID = IID_IFileOpenDialog
    _methods_ = [
        COMMETHOD([], HRESULT, "GetResults",
                  (["out"], POINTER(POINTER(IShellItemArray)), "ppenum")),
        COMMETHOD([], HRESULT, "GetSelectedItems",
                  (["out"], POINTER(POINTER(IShellItemArray)), "ppsai"))
    ]
    GetResults: Callable[[], IShellItemArray]
    GetSelectedItems: Callable[[], IShellItemArray]


class IFileSaveDialog(IFileDialog):
    _case_insensitive_: bool = True
    _iid_: GUID = IID_IFileSaveDialog
    _methods_ = [
        COMMETHOD([], HRESULT, "SetSaveAsItem",
                  (["in"], POINTER(IShellItem), "psi")),
        COMMETHOD([], HRESULT, "SetProperties",
                  (["in"], POINTER(comtypes.IUnknown), "pStore")),
        COMMETHOD([], HRESULT, "SetCollectedProperties",
                  (["in"], POINTER(comtypes.IUnknown), "pList"),
                  (["in"], BOOL, "fAppendDefault")),
        COMMETHOD([], HRESULT, "GetProperties",
                  (["out"], POINTER(POINTER(comtypes.IUnknown)), "ppStore")),
        COMMETHOD([], HRESULT, "ApplyProperties",
                  (["in"], POINTER(IShellItem), "psi"),
                  (["in"], POINTER(comtypes.IUnknown), "pStore"),
                  (["in"], HWND, "hwnd"),
                  (["in"], POINTER(comtypes.IUnknown), "pSink"))
    ]
    SetSaveAsItem: Callable[[IShellItem], int]
    SetProperties: Callable[[comtypes.IUnknown], int]
    SetCollectedProperties: Callable[[comtypes.IUnknown, BOOL], int]
    GetProperties: Callable[[comtypes.IUnknown], int]
    ApplyProperties: Callable[[IShellItem, comtypes.IUnknown, HWND, comtypes.IUnknown], int]


class BaseDialog:
    def show(self, host_window, future):
        self.future = future

        # Don't differentiate between app and window modal dialogs
        # Show the dialog using an inner loop.
        asyncio.get_event_loop().start_inner_loop(self._show)


class MessageDialog(BaseDialog):
    def __init__(
        self,
        title,
        message,
        buttons,
        icon,
        success_result=None,
    ):
        super().__init__()
        self.message = message
        self.title = title
        self.buttons = buttons
        self.icon = icon
        self.success_result = success_result

    def _show(self):
        return_value = WinForms.MessageBox.Show(
            self.message,
            self.title,
            self.buttons,
            self.icon,
        )
        if self.success_result:
            self.future.set_result(return_value == self.success_result)
        else:
            self.future.set_result(None)


class InfoDialog(MessageDialog):
    def __init__(self, title, message):
        super().__init__(
            title,
            message,
            MessageBoxButtons.OK,
            MessageBoxIcon.Information,
        )


class QuestionDialog(MessageDialog):
    def __init__(self, title, message):
        super().__init__(
            title,
            message,
            MessageBoxButtons.YesNo,
            MessageBoxIcon.Information,
            success_result=DialogResult.Yes,
        )


class ConfirmDialog(MessageDialog):
    def __init__(self, title, message):
        super().__init__(
            title,
            message,
            MessageBoxButtons.OKCancel,
            MessageBoxIcon.Warning,
            success_result=DialogResult.OK,
        )


class ErrorDialog(MessageDialog):
    def __init__(self, title, message=None):
        super().__init__(
            title,
            message,
            WinForms.MessageBoxButtons.OK,
            WinForms.MessageBoxIcon.Error,
        )


class StackTraceDialog(BaseDialog):
    def __init__(self, title, message, content, retry):
        super().__init__()

        self.native = WinForms.Form()
        self.native.MinimizeBox = False
        self.native.FormBorderStyle = self.native.FormBorderStyle.FixedSingle
        self.native.MaximizeBox = False
        self.native.FormClosing += WeakrefCallable(self.winforms_FormClosing)
        self.native.Width = 540
        self.native.Height = 320
        self.native.Text = title

        # The top-of-page introductory message
        textLabel = WinForms.Label()
        textLabel.Left = 10
        textLabel.Top = 10
        textLabel.Width = 520
        textLabel.Alignment = ContentAlignment.MiddleCenter
        textLabel.Text = message

        self.native.Controls.Add(textLabel)

        # A scrolling text box for the stack trace.
        trace = WinForms.RichTextBox()
        trace.Left = 10
        trace.Top = 30
        trace.Width = 504
        trace.Height = 210
        trace.Multiline = True
        trace.ReadOnly = True
        trace.Font = WinFont(
            FontFamily.GenericMonospace,
            float(SystemFonts.DefaultFont.Size),
            FontStyle.Regular,
        )
        trace.Text = content

        self.native.Controls.Add(trace)

        # Add acceptance/close buttons
        if retry:
            retry = WinForms.Button()
            retry.Left = 290
            retry.Top = 250
            retry.Width = 100
            retry.Text = "&Retry"
            retry.Click += WeakrefCallable(self.winforms_Click_retry)

            self.native.Controls.Add(retry)

            quit = WinForms.Button()
            quit.Left = 400
            quit.Top = 250
            quit.Width = 100
            quit.Text = "&Quit"
            quit.Click += WeakrefCallable(self.winforms_Click_quit)

            self.native.Controls.Add(quit)
        else:
            accept = WinForms.Button()
            accept.Left = 400
            accept.Top = 250
            accept.Width = 100
            accept.Text = "&OK"
            accept.Click += WeakrefCallable(self.winforms_Click_accept)

            self.native.Controls.Add(accept)

    def _show(self):
        self.native.ShowDialog()

    def winforms_FormClosing(self, sender, event):
        # If the close button is pressed, the future won't be done.
        # We cancel this event to prevent the dialog from closing.
        # If a button is pressed, the future will be set, and a close
        # event will be triggered.
        if not self.future.done():
            event.Cancel = True  # pragma: no cover

    def winforms_Click_quit(self, sender, event):
        self.future.set_result(False)
        self.native.Close()

    def winforms_Click_retry(self, sender, event):
        self.future.set_result(True)
        self.native.Close()

    def winforms_Click_accept(self, sender, event):
        self.future.set_result(None)
        self.native.Close()


class FileDialog(BaseDialog):
    def __init__(
        self,
        native: Union[IFileOpenDialog, IFileSaveDialog],
        title: str,
        initial_directory: Union[os.PathLike, str],
        *,
        filename: Optional[str] = None,
        file_types: Optional[List[str]] = None,
    ):
        super().__init__()
        self.native: Union[IFileOpenDialog, IFileSaveDialog] = native

        self._set_title(title)
        if filename is not None:
            self.native.SetFileName(filename)

        if initial_directory is not None:
            self._set_initial_directory(str(initial_directory))

        if file_types is not None:
            filters: List[Tuple[str, str]] = [
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


class SaveFileDialog(FileDialog):
    def __init__(
        self,
        title: str,
        filename: str,
        initial_directory: Union[os.PathLike, str],
        file_types: List[str],
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
        initial_directory: Union[os.PathLike, str],
        file_types: List[str],
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

    def _get_filenames(self) -> List[Path]:
        assert isinstance(self.native, IFileOpenDialog)
        results: List[Path] = []
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
        initial_directory: Union[os.PathLike, str],
        multiple_select: bool,
    ):
        super().__init__(
            comtypes.client.CreateObject(CLSID_FileOpenDialog, interface=IFileOpenDialog),
            title,
            initial_directory,
        )
        self.native.SetOptions(FileOpenOptions.FOS_PICKFOLDERS)
        self.multiple_select = multiple_select

    def _get_filenames(self) -> Union[List[Path], Path]:
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
