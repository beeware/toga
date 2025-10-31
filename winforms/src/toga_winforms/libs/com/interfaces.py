from __future__ import annotations

from ctypes import HRESULT, POINTER as C_POINTER, c_int, c_uint, c_ulong, c_void_p
from ctypes.wintypes import BOOL, DWORD, HWND, LPCWSTR, LPWSTR, ULONG
from typing import TYPE_CHECKING, Callable, ClassVar

from comtypes import COMMETHOD, GUID, COMObject, IUnknown

from toga_winforms.libs.com.identifiers import (
    IID_IFileDialog,
    IID_IFileOpenDialog,
    IID_IFileSaveDialog,
    IID_IModalWindow,
    IID_IShellItem,
    IID_IShellItemArray,
    IID_IShellItemFilter,
)

if TYPE_CHECKING:
    from ctypes import _Pointer

    from comtypes._memberspec import _ComMemberSpec


class IModalWindow(IUnknown):
    _case_insensitive_: bool = True
    _iid_: GUID = IID_IModalWindow
    _methods_: ClassVar[list[_ComMemberSpec]] = [
        COMMETHOD([], HRESULT, "Show", (["in"], HWND, "hwndParent"))
    ]
    Show: Callable[[int | HWND], int]


class IShellItem(IUnknown):
    _case_insensitive_: bool = True
    _iid_: GUID = IID_IShellItem
    _methods_: ClassVar[list[_ComMemberSpec]] = [
        COMMETHOD(
            [],
            HRESULT,
            "BindToHandler",
            (["in"], C_POINTER(IUnknown), "pbc"),
            (["in"], C_POINTER(GUID), "bhid"),
            (["in"], C_POINTER(GUID), "riid"),
            (["out"], C_POINTER(c_void_p), "ppv"),
        ),
        COMMETHOD(
            [], HRESULT, "GetParent", (["out"], C_POINTER(C_POINTER(IUnknown)), "ppsi")
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetDisplayName",
            (["in"], c_ulong, "sigdnName"),
            (["out"], C_POINTER(LPWSTR), "ppszName"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetAttributes",
            (["in"], c_ulong, "sfgaoMask"),
            (["out"], C_POINTER(c_ulong), "psfgaoAttribs"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "Compare",
            (["in"], C_POINTER(IUnknown), "psi"),
            (["in"], c_ulong, "hint"),
            (["out"], C_POINTER(c_int), "piOrder"),
        ),
    ]
    QueryInterface: Callable[[GUID, _Pointer[_Pointer[IUnknown]]], int]
    AddRef: Callable[[], ULONG]
    Release: Callable[[], ULONG]
    BindToHandler: Callable[[_Pointer[IUnknown], GUID, GUID, _Pointer[c_void_p]], int]
    GetParent: Callable[[], IUnknown]
    GetDisplayName: Callable[[c_ulong | int], str]
    GetAttributes: Callable[[c_ulong | int], int]
    Compare: Callable[[_Pointer[IUnknown], c_ulong, c_int], int]


class IShellItemArray(IUnknown):
    _case_insensitive_: bool = True
    _iid_: GUID = IID_IShellItemArray
    _methods_: ClassVar[list[_ComMemberSpec]] = [
        COMMETHOD(
            [],
            HRESULT,
            "BindToHandler",
            (["in"], C_POINTER(IUnknown), "pbc"),
            (["in"], C_POINTER(GUID), "bhid"),
            (["in"], C_POINTER(GUID), "riid"),
            (["out"], C_POINTER(c_void_p), "ppv"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetPropertyStore",
            (["in"], c_ulong, "flags"),
            (["in"], C_POINTER(GUID), "riid"),
            (["out"], C_POINTER(c_void_p), "ppv"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetPropertyDescriptionList",
            (["in"], C_POINTER(GUID), "keyType"),
            (["in"], C_POINTER(GUID), "riid"),
            (["out"], C_POINTER(c_void_p), "ppv"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetAttributes",
            (["in"], c_ulong, "attribFlags"),
            (["in"], c_ulong, "sfgaoMask"),
            (["out"], C_POINTER(c_ulong), "psfgaoAttribs"),
        ),
        COMMETHOD([], HRESULT, "GetCount", (["out"], C_POINTER(c_uint), "pdwNumItems")),
        COMMETHOD(
            [],
            HRESULT,
            "GetItemAt",
            (["in"], c_uint, "dwIndex"),
            (["out"], C_POINTER(C_POINTER(IShellItem)), "ppsi"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "EnumItems",
            (["out"], C_POINTER(C_POINTER(IUnknown)), "ppenumShellItems"),
        ),
    ]
    QueryInterface: Callable[[GUID, IUnknown], int]
    AddRef: Callable[[], ULONG]
    Release: Callable[[], ULONG]
    BindToHandler: Callable[[_Pointer[IUnknown], GUID, GUID], int]
    GetPropertyStore: Callable[[c_ulong, GUID], c_void_p]
    GetPropertyDescriptionList: Callable[[GUID, GUID], c_void_p]
    GetAttributes: Callable[[c_ulong, c_ulong], _Pointer[c_ulong]]
    GetCount: Callable[[], int]
    GetItemAt: Callable[[c_uint | int], IShellItem]
    EnumItems: Callable[[], IUnknown]


class IShellItemFilter(IUnknown):
    _case_insensitive_: bool = True
    _iid_: GUID = IID_IShellItemFilter
    _methods_: ClassVar[list[_ComMemberSpec]] = [
        COMMETHOD([], HRESULT, "IncludeItem", (["in"], C_POINTER(IShellItem), "psi")),
        COMMETHOD(
            [],
            HRESULT,
            "GetEnumFlagsForItem",
            (["in"], C_POINTER(IShellItem), "psi"),
            (["out"], C_POINTER(c_ulong), "pgrfFlags"),
        ),
    ]
    QueryInterface: Callable[[GUID, IUnknown], int]
    AddRef: Callable[[], ULONG]
    Release: Callable[[], ULONG]
    IncludeItem: Callable[[IShellItem], c_ulong]
    GetEnumFlagsForItem: Callable[[], int]


class IFileDialog(IModalWindow):
    _iid_: GUID = IID_IFileDialog
    _methods_: ClassVar[list[_ComMemberSpec]] = [
        COMMETHOD(
            [],
            HRESULT,
            "SetFileTypes",
            (["in"], c_uint, "cFileTypes"),
            (["in"], C_POINTER(c_void_p), "rgFilterSpec"),
        ),
        COMMETHOD([], HRESULT, "SetFileTypeIndex", (["in"], c_uint, "iFileType")),
        COMMETHOD(
            [], HRESULT, "GetFileTypeIndex", (["out"], C_POINTER(c_uint), "piFileType")
        ),
        COMMETHOD(
            [],
            HRESULT,
            "Advise",
            (["in"], C_POINTER(IUnknown), "pfde"),
            (["out"], C_POINTER(DWORD), "pdwCookie"),
        ),
        COMMETHOD([], HRESULT, "Unadvise", (["in"], DWORD, "dwCookie")),
        COMMETHOD([], HRESULT, "SetOptions", (["in"], c_uint, "fos")),
        COMMETHOD([], HRESULT, "GetOptions", (["out"], C_POINTER(DWORD), "pfos")),
        COMMETHOD(
            [], HRESULT, "SetDefaultFolder", (["in"], C_POINTER(IShellItem), "psi")
        ),
        COMMETHOD([], HRESULT, "SetFolder", (["in"], C_POINTER(IShellItem), "psi")),
        COMMETHOD(
            [],
            HRESULT,
            "GetFolder",
            (["out"], C_POINTER(C_POINTER(IShellItem)), "ppsi"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetCurrentSelection",
            (["out"], C_POINTER(C_POINTER(IShellItem)), "ppsi"),
        ),
        COMMETHOD([], HRESULT, "SetFileName", (["in"], LPCWSTR, "pszName")),
        COMMETHOD([], HRESULT, "GetFileName", (["out"], C_POINTER(LPWSTR), "pszName")),
        COMMETHOD([], HRESULT, "SetTitle", (["in"], LPCWSTR, "pszTitle")),
        COMMETHOD([], HRESULT, "SetOkButtonLabel", (["in"], LPCWSTR, "pszText")),
        COMMETHOD([], HRESULT, "SetFileNameLabel", (["in"], LPCWSTR, "pszLabel")),
        COMMETHOD(
            [],
            HRESULT,
            "GetResult",
            (["out"], C_POINTER(C_POINTER(IShellItem)), "ppsi"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "AddPlace",
            (["in"], C_POINTER(IShellItem), "psi"),
            (["in"], c_int, "fdap"),
        ),
        COMMETHOD(
            [], HRESULT, "SetDefaultExtension", (["in"], LPCWSTR, "pszDefaultExtension")
        ),
        COMMETHOD([], HRESULT, "Close", (["in"], HRESULT, "hr")),
        COMMETHOD([], HRESULT, "SetClientGuid", (["in"], C_POINTER(GUID), "guid")),
        COMMETHOD([], HRESULT, "ClearClientData"),
        COMMETHOD(
            [], HRESULT, "SetFilter", (["in"], C_POINTER(IShellItemFilter), "pFilter")
        ),
    ]
    SetFileTypes: Callable[[c_uint | int, _Pointer[c_void_p]], int]
    SetFileTypeIndex: Callable[[c_uint], int]
    GetFileTypeIndex: Callable[[], _Pointer[c_uint]]
    Advise: Callable[[IUnknown | COMObject], int]
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
    SetFilter: Callable[[IShellItemFilter], int]


class IFileOpenDialog(IFileDialog):
    _case_insensitive_: bool = True
    _iid_: GUID = IID_IFileOpenDialog
    _methods_: ClassVar[list[_ComMemberSpec]] = [
        COMMETHOD(
            [],
            HRESULT,
            "GetResults",
            (["out"], C_POINTER(C_POINTER(IShellItemArray)), "ppenum"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetSelectedItems",
            (["out"], C_POINTER(C_POINTER(IShellItemArray)), "ppsai"),
        ),
    ]
    GetResults: Callable[[], IShellItemArray]
    GetSelectedItems: Callable[[], IShellItemArray]


class IFileSaveDialog(IFileDialog):
    _case_insensitive_: bool = True
    _iid_: GUID = IID_IFileSaveDialog
    _methods_: ClassVar[list[_ComMemberSpec]] = [
        COMMETHOD([], HRESULT, "SetSaveAsItem", (["in"], C_POINTER(IShellItem), "psi")),
        COMMETHOD(
            [], HRESULT, "SetProperties", (["in"], C_POINTER(IUnknown), "pStore")
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetCollectedProperties",
            (["in"], C_POINTER(IUnknown), "pList"),
            (["in"], BOOL, "fAppendDefault"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetProperties",
            (["out"], C_POINTER(C_POINTER(IUnknown)), "ppStore"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "ApplyProperties",
            (["in"], C_POINTER(IShellItem), "psi"),
            (["in"], C_POINTER(IUnknown), "pStore"),
            (["in"], HWND, "hwnd"),
            (["in"], C_POINTER(IUnknown), "pSink"),
        ),
    ]
    SetSaveAsItem: Callable[[IShellItem], int]
    SetProperties: Callable[[_Pointer[IUnknown]], int]
    SetCollectedProperties: Callable[[_Pointer[IUnknown], int], int]
    GetProperties: Callable[[_Pointer[_Pointer[IUnknown]]], int]
    ApplyProperties: Callable[
        [IShellItem, _Pointer[IUnknown], HWND, _Pointer[IUnknown]], int
    ]
