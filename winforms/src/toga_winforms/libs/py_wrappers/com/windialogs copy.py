from __future__ import annotations

import errno
import json
import os
import random
from ctypes import (
    HRESULT,
    POINTER,
    Structure,
    WinError,
    byref,
    c_int,
    c_uint,
    c_ulong,
    c_void_p,
    c_wchar_p,
    windll,
)
from ctypes import cast as cast_with_ctypes
from ctypes.wintypes import BOOL, DWORD, HWND, LPCWSTR, LPWSTR
from enum import IntFlag
from pathlib import WindowsPath
from typing import TYPE_CHECKING, Callable, ClassVar, Sequence

import comtypes  # pyright: ignore[reportMissingTypeStubs]
import comtypes.client  # pyright: ignore[reportMissingTypeStubs]
from comtypes import COMMETHOD, GUID
from comtypes.hresult import S_OK

if TYPE_CHECKING:
    from ctypes import Array, _CData, _Pointer
    from ctypes.wintypes import ULONG

    from comtypes._memberspec import _ComMemberSpec


class COMDLG_FILTERSPEC(Structure):  # noqa: N801
    _fields_: Sequence[tuple[str, type[_CData]] | tuple[str, type[_CData], int]] = [
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
    _methods_: ClassVar[list[_ComMemberSpec]] = [
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
    AddRef: Callable[[], ULONG]
    Release: Callable[[], ULONG]
    BindToHandler: Callable[[comtypes.IUnknown, GUID, GUID, _Pointer[c_void_p]], int]
    GetParent: Callable[[], comtypes.IUnknown]
    GetDisplayName: Callable[[c_ulong | int], str]
    GetAttributes: Callable[[c_ulong | int], int]
    Compare: Callable[[comtypes.IUnknown, c_ulong, c_int], int]


SHCreateItemFromParsingName = windll.shell32.SHCreateItemFromParsingName
SHCreateItemFromParsingName.argtypes = [
    c_wchar_p,                            # LPCWSTR (wide string, null-terminated)
    POINTER(comtypes.IUnknown),                    # IBindCtx* (can be NULL, hence POINTER(IUnknown))
    POINTER(GUID),                        # REFIID (pointer to the interface ID, typically GUID)
    POINTER(POINTER(IShellItem))          # void** (output pointer to the requested interface)
]
SHCreateItemFromParsingName.restype = HRESULT


class IShellItemArray(comtypes.IUnknown):
    _case_insensitive_: bool = True
    _iid_: GUID = IID_IShellItemArray
    _methods_: ClassVar[list[_ComMemberSpec]] = [
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
    AddRef: Callable[[], ULONG]
    Release: Callable[[], ULONG]
    BindToHandler: Callable[[_Pointer[comtypes.IUnknown], GUID, GUID], int]
    GetPropertyStore: Callable[[c_ulong, GUID], c_void_p]
    GetPropertyDescriptionList: Callable[[GUID, GUID], c_void_p]
    GetAttributes: Callable[[c_ulong, c_ulong], _Pointer[c_ulong]]
    GetCount: Callable[[], int]
    GetItemAt: Callable[[c_uint | int], IShellItem]
    EnumItems: Callable[[], comtypes.IUnknown]


class IModalWindow(comtypes.IUnknown):
    _case_insensitive_: bool = True
    _iid_: GUID = IID_IModalWindow
    _methods_: ClassVar[list[_ComMemberSpec]] = [
        COMMETHOD([], HRESULT, "Show",
                  (["in"], HWND, "hwndParent"))
    ]
    Show: Callable[[int | HWND], int]


class IFileDialog(IModalWindow):
    _iid_: GUID = IID_IFileDialog
    _methods_: ClassVar[list[_ComMemberSpec]] = [
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
    SetFileTypes: Callable[[c_uint | int, _Pointer[c_void_p]], int]
    SetFileTypeIndex: Callable[[c_uint], int]
    GetFileTypeIndex: Callable[[], _Pointer[c_uint]]
    Advise: Callable[[comtypes.IUnknown | comtypes.COMObject], int]
    Unadvise: Callable[[int], int]
    SetOptions: Callable[[DWORD | int], int]
    GetOptions: Callable[[], int]
    SetDefaultFolder: Callable[[_Pointer[IShellItem]], int]
    SetFolder: Callable[[_Pointer[IShellItem]], int]
    GetFolder: Callable[[], IShellItem]
    GetCurrentSelection: Callable[[], IShellItem]
    SetFileName: Callable[[str], int]
    GetFileName: Callable[[], _Pointer[LPWSTR]]
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
    _methods_: ClassVar[list[_ComMemberSpec]] = [
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
    _methods_: ClassVar[list[_ComMemberSpec]] = [
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


def show_file_dialog(
    fileDialog: IFileOpenDialog | IFileSaveDialog,  # noqa: N803
    hwndOwner: HWND,  # noqa: N803
) -> bool:
    """Shows the IFileDialog. Returns True if the user progressed to the end and found a file. False if they cancelled."""
    hr: HRESULT | int = -1
    CANCELLED_BY_USER = -2147023673

    try:
        hr = fileDialog.Show(hwndOwner)
    except OSError as e:
        if e.winerror == CANCELLED_BY_USER:
            return False
        raise
    else:
        if hr:
            raise WinError(hr, "An unexpected error occurred showing the file browser dialog")
    return True


def create_shell_item(path: str) -> _Pointer[IShellItem]:  # noqa: N803, ARG001
    shell_item = POINTER(IShellItem)()
    hr = SHCreateItemFromParsingName(path, None, IShellItem._iid_, byref(shell_item))
    if hr != S_OK:
        raise WinError(hr, f"Failed to create shell item from path: {path}")
    return shell_item


DEFAULT_FILTERS: list[COMDLG_FILTERSPEC] = [
    COMDLG_FILTERSPEC("All Files", "*.*"),
    COMDLG_FILTERSPEC("Text Files", "*.txt"),
    COMDLG_FILTERSPEC("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),
    COMDLG_FILTERSPEC("Document Files", "*.doc;*.docx;*.pdf;*.xls;*.xlsx"),
    COMDLG_FILTERSPEC("Audio Files", "*.mp3;*.wav;*.wma;*.aac"),
    COMDLG_FILTERSPEC("Video Files", "*.mp4;*.avi;*.mkv;*.mov;*.wmv"),
    COMDLG_FILTERSPEC("Archive Files", "*.zip;*.rar;*.7z;*.tar;*.gz"),
]


def configure_file_dialog(  # noqa: PLR0913, PLR0912, C901, PLR0915
    file_dialog: IFileSaveDialog | IFileOpenDialog,
    title: str | None = None,
    options: int = 0,
    default_folder: str | None = None,
    ok_button_label: str | None = None,
    file_name_label: str | None = None,
    file_types: list[tuple[str, str]] | None = None,
    default_extension: str | None = None,
    hwnd: HWND | int | None = None,
) -> list[str] | None:  # sourcery skip: low-code-quality
    hwnd = HWND(hwnd) if isinstance(hwnd, int) else hwnd
    hwnd = HWND(0) if hwnd is None else hwnd
    if default_folder:
        default_folder_path = WindowsPath(default_folder).resolve()
        if not default_folder_path.exists() or not default_folder_path.is_dir():
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), str(default_folder_path))
        shell_item = create_shell_item(str(default_folder_path))
        file_dialog.SetFolder(shell_item)
        file_dialog.SetDefaultFolder(shell_item)

    # Resolve contradictory options
    if options & FileOpenOptions.FOS_ALLNONSTORAGEITEMS:
        if options & FileOpenOptions.FOS_FORCEFILESYSTEM:
            options &= ~FileOpenOptions.FOS_FORCEFILESYSTEM
        if options & FileOpenOptions.FOS_PICKFOLDERS:
            options &= ~FileOpenOptions.FOS_PICKFOLDERS

    file_dialog.SetOptions(options)

    if not options & FileOpenOptions.FOS_PICKFOLDERS:
        filters: Array[COMDLG_FILTERSPEC]
        if file_types:
            filters = (COMDLG_FILTERSPEC * len(file_types))(
                *[
                    (c_wchar_p(name), c_wchar_p(spec))
                    for name, spec in file_types
                ]
            )
        else:
            filters = (COMDLG_FILTERSPEC * len(DEFAULT_FILTERS))(*DEFAULT_FILTERS)
        file_dialog.SetFileTypes(len(filters), cast_with_ctypes(filters, POINTER(c_void_p)))

    if title:
        file_dialog.SetTitle(title)

    if ok_button_label:
        file_dialog.SetOkButtonLabel(ok_button_label)
    elif isinstance(file_dialog, IFileSaveDialog):
        file_dialog.SetOkButtonLabel("Save")
    elif options & FileOpenOptions.FOS_PICKFOLDERS:
        file_dialog.SetOkButtonLabel("Select Folder")
    else:
        file_dialog.SetOkButtonLabel("Select File")

    if file_name_label:
        file_dialog.SetFileNameLabel(file_name_label)
    if default_extension:
        file_dialog.SetDefaultExtension(default_extension)

    if show_file_dialog(file_dialog, hwnd):
        return (
            [get_save_file_dialog_results(file_dialog)]
            if isinstance(file_dialog, IFileSaveDialog)
            else get_open_file_dialog_results(file_dialog)
        )
    return None


def open_file_dialog(  # noqa: C901, PLR0913, PLR0912
    title: str | None = "Open File",
    default_folder: str | None = None,
    file_types: list[tuple[str, str]] | None = None,
    default_extension: str | None = None,
    *,
    overwrite_prompt: bool = False,
    strict_file_types: bool = False,
    no_change_dir: bool = True,
    force_filesystem: bool = True,
    all_non_storage_items: bool = False,
    no_validate: bool = False,
    allow_multiple_selection: bool = False,
    path_must_exist: bool = True,
    file_must_exist: bool = True,
    create_prompt: bool = False,
    share_aware: bool = False,
    no_readonly_return: bool = False,
    no_test_file_create: bool = False,
    hide_mru_places: bool = False,
    hide_pinned_places: bool = False,
    no_dereference_links: bool = False,
    add_to_recent: bool = True,
    show_hidden_files: bool = False,
    default_no_minimode: bool = False,
    force_preview_pane_on: bool = False,
    ok_button_text: str | None = None,
) -> list[str] | None:  # sourcery skip: low-code-quality
    """Opens a file dialog to select files.

    Args:
        title (str | None): The title of the dialog.
        default_folder (str | None): The initial folder to open.
        file_types (list[tuple[str, str]] | None): A list of file type filters.
        default_extension (str | None): The default file extension.
        overwrite_prompt (bool): Prompts if the selected file already exists. FileOpenOptions.FOS_OVERWRITEPROMPT.
        strict_file_types (bool): Restricts selection to specified file types. FileOpenOptions.FOS_STRICTFILETYPES.
        no_change_dir (bool): Prevents changing the current working directory. FileOpenOptions.FOS_NOCHANGEDIR.
        force_filesystem (bool): Ensures only file system items are shown. FileOpenOptions.FOS_FORCEFILESYSTEM.
        all_non_storage_items (bool): Allows selection of non-file system items. FileOpenOptions.FOS_ALLNONSTORAGEITEMS.
        no_validate (bool): Disables file name validation. FileOpenOptions.FOS_NOVALIDATE.
        allow_multiple_selection (bool): Allows selecting multiple files. FileOpenOptions.FOS_ALLOWMULTISELECT.
        path_must_exist (bool): Requires the path to exist. FileOpenOptions.FOS_PATHMUSTEXIST.
        file_must_exist (bool): Requires the file to exist. FileOpenOptions.FOS_FILEMUSTEXIST.
        create_prompt (bool): Prompts to create a new file if it doesn't exist. FileOpenOptions.FOS_CREATEPROMPT.
        share_aware (bool): Ensures the dialog is aware of sharing conflicts. FileOpenOptions.FOS_SHAREAWARE.
        no_readonly_return (bool): Prevents selection of read-only items. FileOpenOptions.FOS_NOREADONLYRETURN.
        no_test_file_create (bool): Disables testing file creation ability. FileOpenOptions.FOS_NOTESTFILECREATE.
        hide_mru_places (bool): Hides most recently used places. FileOpenOptions.FOS_HIDEMRUPLACES.
        hide_pinned_places (bool): Hides pinned places. FileOpenOptions.FOS_HIDEPINNEDPLACES.
        no_dereference_links (bool): Prevents dereferencing shortcuts. FileOpenOptions.FOS_NODEREFERENCELINKS.
        add_to_recent (bool): Prevents adding the file to recent files. FileOpenOptions.FOS_DONTADDTORECENT.
        show_hidden_files (bool): Shows hidden files and folders. FileOpenOptions.FOS_FORCESHOWHIDDEN.
        default_no_minimode (bool): Uses default non-minimized mode. FileOpenOptions.FOS_DEFAULTNOMINIMODE.
        force_preview_pane_on (bool): Forces the preview pane to be visible. FileOpenOptions.FOS_FORCEPREVIEWPANEON.
        ok_button_text (str): The text for the button used to select/confirm the dialog.

    Returns:
        list[str] | None: A list of selected file paths or None if cancelled.
    """
    options = 0
    if overwrite_prompt:
        options |= FileOpenOptions.FOS_OVERWRITEPROMPT
    if strict_file_types:
        options |= FileOpenOptions.FOS_STRICTFILETYPES
    if no_change_dir:
        options |= FileOpenOptions.FOS_NOCHANGEDIR
    if force_filesystem:
        options |= FileOpenOptions.FOS_FORCEFILESYSTEM
    if all_non_storage_items:
        options |= FileOpenOptions.FOS_ALLNONSTORAGEITEMS
    if no_validate:
        options |= FileOpenOptions.FOS_NOVALIDATE
    if allow_multiple_selection:
        options |= FileOpenOptions.FOS_ALLOWMULTISELECT
    if path_must_exist:
        options |= FileOpenOptions.FOS_PATHMUSTEXIST
    if file_must_exist:
        options |= FileOpenOptions.FOS_FILEMUSTEXIST
    if create_prompt:
        options |= FileOpenOptions.FOS_CREATEPROMPT
    if share_aware:
        options |= FileOpenOptions.FOS_SHAREAWARE
    if no_readonly_return:
        options |= FileOpenOptions.FOS_NOREADONLYRETURN
    if no_test_file_create:
        options |= FileOpenOptions.FOS_NOTESTFILECREATE
    if hide_mru_places:
        options |= FileOpenOptions.FOS_HIDEMRUPLACES
    if hide_pinned_places:
        options |= FileOpenOptions.FOS_HIDEPINNEDPLACES
    if no_dereference_links:
        options |= FileOpenOptions.FOS_NODEREFERENCELINKS
    if not add_to_recent:
        options |= FileOpenOptions.FOS_DONTADDTORECENT
    if show_hidden_files:
        options |= FileOpenOptions.FOS_FORCESHOWHIDDEN
    if default_no_minimode:
        options |= FileOpenOptions.FOS_DEFAULTNOMINIMODE
    if force_preview_pane_on:
        options |= FileOpenOptions.FOS_FORCEPREVIEWPANEON
    file_dialog = comtypes.client.CreateObject(CLSID_FileOpenDialog, interface=IFileOpenDialog)
    return configure_file_dialog(file_dialog, title, options, default_folder, ok_button_text, None, file_types, default_extension)


def save_file_dialog(  # noqa: C901, PLR0913, PLR0912
    title: str | None = "Save File",
    default_folder: str | None = None,
    file_types: list[tuple[str, str]] | None = None,
    default_extension: str | None = None,
    *,
    overwrite_prompt: bool = True,
    strict_file_types: bool = False,
    no_change_dir: bool = True,
    force_filesystem: bool = True,
    all_non_storage_items: bool = False,
    no_validate: bool = False,
    path_must_exist: bool = True,
    file_must_exist: bool = False,
    create_prompt: bool = False,
    share_aware: bool = False,
    no_readonly_return: bool = False,
    no_test_file_create: bool = False,
    hide_mru_places: bool = False,
    hide_pinned_places: bool = False,
    no_dereference_links: bool = False,
    add_to_recent: bool = True,
    show_hidden_files: bool = False,
    default_no_minimode: bool = False,
    force_preview_pane_on: bool = False,
    ok_button_text: str | None = None,
) -> list[str] | None:  # sourcery skip: low-code-quality
    """Opens a file dialog to save a file.

    Args:
        title (str | None): The title of the dialog.
        default_folder (str | None): The initial folder to open.
        file_types (list[tuple[str, str]] | None): A list of file type filters.
        default_extension (str | None): The default file extension.
        overwrite_prompt (bool): Prompts if the selected file already exists. FileOpenOptions.FOS_OVERWRITEPROMPT.
        strict_file_types (bool): Restricts selection to specified file types. FileOpenOptions.FOS_STRICTFILETYPES.
        no_change_dir (bool): Prevents changing the current working directory. FileOpenOptions.FOS_NOCHANGEDIR.
        force_filesystem (bool): Ensures only file system items are shown. FileOpenOptions.FOS_FORCEFILESYSTEM.
        all_non_storage_items (bool): Allows selection of non-file system items. FileOpenOptions.FOS_ALLNONSTORAGEITEMS.
        no_validate (bool): Disables file name validation. FileOpenOptions.FOS_NOVALIDATE.
        path_must_exist (bool): Requires the path to exist. FileOpenOptions.FOS_PATHMUSTEXIST.
        file_must_exist (bool): Requires the file to exist. FileOpenOptions.FOS_FILEMUSTEXIST.
        create_prompt (bool): Prompts to create a new file if it doesn't exist. FileOpenOptions.FOS_CREATEPROMPT.
        share_aware (bool): Ensures the dialog is aware of sharing conflicts. FileOpenOptions.FOS_SHAREAWARE.
        no_readonly_return (bool): Prevents selection of read-only items. FileOpenOptions.FOS_NOREADONLYRETURN.
        no_test_file_create (bool): Disables testing file creation ability. FileOpenOptions.FOS_NOTESTFILECREATE.
        hide_mru_places (bool): Hides most recently used places. FileOpenOptions.FOS_HIDEMRUPLACES.
        hide_pinned_places (bool): Hides pinned places. FileOpenOptions.FOS_HIDEPINNEDPLACES.
        no_dereference_links (bool): Prevents dereferencing shortcuts. FileOpenOptions.FOS_NODEREFERENCELINKS.
        add_to_recent (bool): Prevents adding the file to recent files. FileOpenOptions.FOS_DONTADDTORECENT.
        show_hidden_files (bool): Shows hidden files and folders. FileOpenOptions.FOS_FORCESHOWHIDDEN.
        default_no_minimode (bool): Uses default non-minimized mode. FileOpenOptions.FOS_DEFAULTNOMINIMODE.
        force_preview_pane_on (bool): Forces the preview pane to be visible. FileOpenOptions.FOS_FORCEPREVIEWPANEON.
        ok_button_text (str): The text for the button used to select/confirm the dialog.

    Returns:
        list[str] | None: A list of selected file paths or None if cancelled.
    """
    options = 0
    if overwrite_prompt:
        options |= FileOpenOptions.FOS_OVERWRITEPROMPT
    if strict_file_types:
        options |= FileOpenOptions.FOS_STRICTFILETYPES
    if no_change_dir:
        options |= FileOpenOptions.FOS_NOCHANGEDIR
    if force_filesystem:
        options |= FileOpenOptions.FOS_FORCEFILESYSTEM
    if all_non_storage_items:
        options |= FileOpenOptions.FOS_ALLNONSTORAGEITEMS
    if no_validate:
        options |= FileOpenOptions.FOS_NOVALIDATE
    if path_must_exist:
        options |= FileOpenOptions.FOS_PATHMUSTEXIST
    if file_must_exist:
        options |= FileOpenOptions.FOS_FILEMUSTEXIST
    if create_prompt:
        options |= FileOpenOptions.FOS_CREATEPROMPT
    if share_aware:
        options |= FileOpenOptions.FOS_SHAREAWARE
    if no_readonly_return:
        options |= FileOpenOptions.FOS_NOREADONLYRETURN
    if no_test_file_create:
        options |= FileOpenOptions.FOS_NOTESTFILECREATE
    if hide_mru_places:
        options |= FileOpenOptions.FOS_HIDEMRUPLACES
    if hide_pinned_places:
        options |= FileOpenOptions.FOS_HIDEPINNEDPLACES
    if no_dereference_links:
        options |= FileOpenOptions.FOS_NODEREFERENCELINKS
    if not add_to_recent:
        options |= FileOpenOptions.FOS_DONTADDTORECENT
    if show_hidden_files:
        options |= FileOpenOptions.FOS_FORCESHOWHIDDEN
    if default_no_minimode:
        options |= FileOpenOptions.FOS_DEFAULTNOMINIMODE
    if force_preview_pane_on:
        options |= FileOpenOptions.FOS_FORCEPREVIEWPANEON
    options &= ~FileOpenOptions.FOS_PICKFOLDERS  # Required (exceptions otherwise)
    options &= ~FileOpenOptions.FOS_ALLOWMULTISELECT  # Required (exceptions otherwise)
    file_dialog = comtypes.client.CreateObject(CLSID_FileSaveDialog, interface=IFileSaveDialog)
    return configure_file_dialog(file_dialog, title, options, default_folder, ok_button_text, None, file_types, default_extension)


def open_folder_dialog(  # noqa: C901, PLR0913, PLR0912
    title: str | None = "Select Folder",
    default_folder: str | None = None,
    *,
    overwrite_prompt: bool = False,
    strict_file_types: bool = False,
    no_change_dir: bool = False,
    force_filesystem: bool = True,
    no_validate: bool = False,
    allow_multiple_selection: bool = False,
    path_must_exist: bool = True,
    file_must_exist: bool = False,
    create_prompt: bool = False,
    share_aware: bool = False,
    no_readonly_return: bool = False,
    no_test_file_create: bool = False,
    hide_mru_places: bool = False,
    hide_pinned_places: bool = False,
    no_dereference_links: bool = False,
    add_to_recent: bool = True,
    show_hidden_files: bool = False,
    default_no_minimode: bool = False,
    force_preview_pane_on: bool = False,
    ok_button_text: str | None = None,
) -> list[str] | None:  # sourcery skip: low-code-quality
    """Opens a dialog to select folders.

    Args:
        title (str | None): The title of the dialog.
        default_folder (str | None): The initial folder to open.
        overwrite_prompt (bool): Prompts if the selected file already exists. FileOpenOptions.FOS_OVERWRITEPROMPT.
        strict_file_types (bool): Restricts selection to specified file types. FileOpenOptions.FOS_STRICTFILETYPES.
        no_change_dir (bool): Prevents changing the current working directory. FileOpenOptions.FOS_NOCHANGEDIR.
        force_filesystem (bool): Ensures only file system items are shown. FileOpenOptions.FOS_FORCEFILESYSTEM.
        no_validate (bool): Disables file name validation. FileOpenOptions.FOS_NOVALIDATE.
        allow_multiple_selection (bool): Allows selecting multiple files. FileOpenOptions.FOS_ALLOWMULTISELECT.
        path_must_exist (bool): Requires the path to exist. FileOpenOptions.FOS_PATHMUSTEXIST.
        file_must_exist (bool): Requires the file to exist. FileOpenOptions.FOS_FILEMUSTEXIST.
        create_prompt (bool): Prompts to create a new file if it doesn't exist. FileOpenOptions.FOS_CREATEPROMPT.
        share_aware (bool): Ensures the dialog is aware of sharing conflicts. FileOpenOptions.FOS_SHAREAWARE.
        no_readonly_return (bool): Prevents selection of read-only items. FileOpenOptions.FOS_NOREADONLYRETURN.
        no_test_file_create (bool): Disables testing file creation ability. FileOpenOptions.FOS_NOTESTFILECREATE.
        hide_mru_places (bool): Hides most recently used places. FileOpenOptions.FOS_HIDEMRUPLACES.
        hide_pinned_places (bool): Hides pinned places. FileOpenOptions.FOS_HIDEPINNEDPLACES.
        no_dereference_links (bool): Prevents dereferencing shortcuts. FileOpenOptions.FOS_NODEREFERENCELINKS.
        add_to_recent (bool): Prevents adding the file to recent files. FileOpenOptions.FOS_DONTADDTORECENT.
        show_hidden_files (bool): Shows hidden files and folders. FileOpenOptions.FOS_FORCESHOWHIDDEN.
        default_no_minimode (bool): Uses default non-minimized mode. FileOpenOptions.FOS_DEFAULTNOMINIMODE.
        force_preview_pane_on (bool): Forces the preview pane to be visible. FileOpenOptions.FOS_FORCEPREVIEWPANEON.
        ok_button_text (str): The text for the button used to select/confirm the dialog.

    Returns:
        list[str] | None: A list of selected folder paths or None if cancelled.
    """
    options = 0
    options |= FileOpenOptions.FOS_PICKFOLDERS
    options &= ~FileOpenOptions.FOS_ALLNONSTORAGEITEMS
    if overwrite_prompt:
        options |= FileOpenOptions.FOS_OVERWRITEPROMPT
    if strict_file_types:
        options |= FileOpenOptions.FOS_STRICTFILETYPES
    if no_change_dir:
        options |= FileOpenOptions.FOS_NOCHANGEDIR
    if force_filesystem:
        options |= FileOpenOptions.FOS_FORCEFILESYSTEM
    if no_validate:
        options |= FileOpenOptions.FOS_NOVALIDATE
    if allow_multiple_selection:
        options |= FileOpenOptions.FOS_ALLOWMULTISELECT
    if path_must_exist:
        options |= FileOpenOptions.FOS_PATHMUSTEXIST
    if file_must_exist:
        options |= FileOpenOptions.FOS_FILEMUSTEXIST
    if create_prompt:
        options |= FileOpenOptions.FOS_CREATEPROMPT
    if share_aware:
        options |= FileOpenOptions.FOS_SHAREAWARE
    if no_readonly_return:
        options |= FileOpenOptions.FOS_NOREADONLYRETURN
    if no_test_file_create:
        options |= FileOpenOptions.FOS_NOTESTFILECREATE
    if hide_mru_places:
        options |= FileOpenOptions.FOS_HIDEMRUPLACES
    if hide_pinned_places:
        options |= FileOpenOptions.FOS_HIDEPINNEDPLACES
    if no_dereference_links:
        options |= FileOpenOptions.FOS_NODEREFERENCELINKS
    if not add_to_recent:
        options |= FileOpenOptions.FOS_DONTADDTORECENT
    if show_hidden_files:
        options |= FileOpenOptions.FOS_FORCESHOWHIDDEN
    if default_no_minimode:
        options |= FileOpenOptions.FOS_DEFAULTNOMINIMODE
    if force_preview_pane_on:
        options |= FileOpenOptions.FOS_FORCEPREVIEWPANEON
    file_dialog = comtypes.client.CreateObject(CLSID_FileOpenDialog, interface=IFileOpenDialog)
    return configure_file_dialog(file_dialog, title, options, default_folder, ok_button_text, None, None, None)


def get_open_file_dialog_results(
    file_open_dialog: IFileOpenDialog,
) -> list[str]:
    results: list[str] = []
    results_array: IShellItemArray = file_open_dialog.GetResults()
    item_count: int = results_array.GetCount()
    for i in range(item_count):
        shell_item: IShellItem = results_array.GetItemAt(i)
        szFilePath: str = shell_item.GetDisplayName(0x80058000)  # SIGDN_FILESYSPATH
        if szFilePath and szFilePath.strip():
            results.append(szFilePath)
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), szFilePath)
    return results


def get_save_file_dialog_results(file_save_dialog: IFileSaveDialog) -> str:
    results = ""
    resultItem: IShellItem = file_save_dialog.GetResult()
    szFilePath = resultItem.GetDisplayName(0x80058000)  # SIGDN_FILESYSPATH
    szFilePathStr = str(szFilePath)
    if szFilePathStr and szFilePathStr.strip():
        results = szFilePathStr
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), str(szFilePath))
    resultItem.Release()
    return results


# Example usage
if __name__ == "__main__":
    # Randomizing arguments for open_file_dialog
    open_file_args = {
        "title": "Open File" if random.choice([True, False]) else None,  # noqa: S311
        "default_folder": "C:\\Users" if random.choice([True, False]) else None,  # noqa: S311
        "file_types": [("Text Files", "*.txt")] if random.choice([True, False]) else None,  # noqa: S311
        "default_extension": "txt" if random.choice([True, False]) else None,  # noqa: S311
        "overwrite_prompt": random.choice([True, False]),  # noqa: S311
        "strict_file_types": random.choice([True, False]),  # noqa: S311
        "no_change_dir": random.choice([True, False]),  # noqa: S311
        "force_filesystem": random.choice([True, False]),  # noqa: S311
        "all_non_storage_items": False,  # random.choice([True, False]),  # noqa: S311
        "no_validate": random.choice([True, False]),  # noqa: S311
        "allow_multiple_selection": random.choice([True, False]),  # noqa: S311
        "path_must_exist": random.choice([True, False]),  # noqa: S311
        "file_must_exist": random.choice([True, False]),  # noqa: S311
        "create_prompt": random.choice([True, False]),  # noqa: S311
        "share_aware": random.choice([True, False]),  # noqa: S311
        "no_readonly_return": random.choice([True, False]),  # noqa: S311
        "no_test_file_create": random.choice([True, False]),  # noqa: S311
        "hide_mru_places": random.choice([True, False]),  # noqa: S311
        "hide_pinned_places": random.choice([True, False]),  # noqa: S311
        "no_dereference_links": random.choice([True, False]),  # noqa: S311
        "add_to_recent": random.choice([True, False]),  # noqa: S311
        "show_hidden_files": random.choice([True, False]),  # noqa: S311
        "default_no_minimode": random.choice([True, False]),  # noqa: S311
        "force_preview_pane_on": random.choice([True, False]),  # noqa: S311
    }
    print("\nOpen file args")
    print(json.dumps(open_file_args, indent=4, sort_keys=True))
    selected_files: list[str] | None = open_file_dialog(**open_file_args)
    print("Selected files:", selected_files)

    # Randomizing arguments for open_folder_dialog
    open_folder_args = {
        "title": "Select Folder" if random.choice([True, False]) else None,  # noqa: S311
        "default_folder": "C:\\Users" if random.choice([True, False]) else None,  # noqa: S311
        "overwrite_prompt": random.choice([True, False]),  # noqa: S311
        "strict_file_types": random.choice([True, False]),  # noqa: S311
        "no_change_dir": random.choice([True, False]),  # noqa: S311
        "force_filesystem": random.choice([True, False]),  # noqa: S311
        "no_validate": random.choice([True, False]),  # noqa: S311
        "allow_multiple_selection": random.choice([True, False]),  # noqa: S311
        "path_must_exist": random.choice([True, False]),  # noqa: S311
        "file_must_exist": random.choice([True, False]),  # noqa: S311
        "create_prompt": random.choice([True, False]),  # noqa: S311
        "share_aware": random.choice([True, False]),  # noqa: S311
        "no_readonly_return": random.choice([True, False]),  # noqa: S311
        "no_test_file_create": random.choice([True, False]),  # noqa: S311
        "hide_mru_places": random.choice([True, False]),  # noqa: S311
        "hide_pinned_places": random.choice([True, False]),  # noqa: S311
        "no_dereference_links": random.choice([True, False]),  # noqa: S311
        "add_to_recent": random.choice([True, False]),  # noqa: S311
        "show_hidden_files": random.choice([True, False]),  # noqa: S311
        "default_no_minimode": random.choice([True, False]),  # noqa: S311
        "force_preview_pane_on": random.choice([True, False]),  # noqa: S311
    }
    print("\nOpen folder args")
    print(json.dumps(open_folder_args, indent=4, sort_keys=True))
    selected_folders: list[str] | None = open_folder_dialog(**open_folder_args)
    print("Selected folders:", selected_folders)

    # Randomizing arguments for save_file_dialog
    save_file_args = {
        "title": "Save File" if random.choice([True, False]) else None,  # noqa: S311
        "default_folder": "C:\\Users" if random.choice([True, False]) else None,  # noqa: S311
        "file_types": [("Text Files", "*.txt")] if random.choice([True, False]) else None,  # noqa: S311
        "default_extension": "txt" if random.choice([True, False]) else None,  # noqa: S311
        "overwrite_prompt": random.choice([True, False]),  # noqa: S311
        "strict_file_types": random.choice([True, False]),  # noqa: S311
        "no_change_dir": random.choice([True, False]),  # noqa: S311
        "force_filesystem": random.choice([True, False]),  # noqa: S311
        "all_non_storage_items": random.choice([True, False]),  # noqa: S311
        "no_validate": random.choice([True, False]),  # noqa: S311
        "path_must_exist": random.choice([True, False]),  # noqa: S311
        "file_must_exist": random.choice([True, False]),  # noqa: S311
        "create_prompt": random.choice([True, False]),  # noqa: S311
        "share_aware": random.choice([True, False]),  # noqa: S311
        "no_readonly_return": random.choice([True, False]),  # noqa: S311
        "no_test_file_create": random.choice([True, False]),  # noqa: S311
        "hide_mru_places": random.choice([True, False]),  # noqa: S311
        "hide_pinned_places": random.choice([True, False]),  # noqa: S311
        "no_dereference_links": random.choice([True, False]),  # noqa: S311
        "add_to_recent": random.choice([True, False]),  # noqa: S311
        "show_hidden_files": random.choice([True, False]),  # noqa: S311
        "default_no_minimode": random.choice([True, False]),  # noqa: S311
        "force_preview_pane_on": random.choice([True, False]),  # noqa: S311
    }
    print("\nSave file args")
    print(json.dumps(save_file_args, indent=4, sort_keys=True))
    saved_file: list[str] | None = save_file_dialog(**save_file_args)
    print("Saved file:", saved_file)
