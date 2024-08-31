from __future__ import annotations

from ctypes import (
    HRESULT,
    POINTER,
    POINTER as C_POINTER,
    c_bool,
    c_int,
    c_uint,
    c_ulong,
    c_void_p,
    c_wchar_p,
)
from ctypes.wintypes import BOOL, DWORD, HWND, LPCWSTR, LPWSTR, ULONG
from typing import TYPE_CHECKING, Callable, ClassVar, Sequence

import comtypes
from comtypes import COMMETHOD, GUID, COMObject, IUnknown
from comtypes.hresult import S_OK

from toga_winforms.libs.com.identifiers import (
    IID_IContextMenu,
    IID_IEnumShellItems,
    IID_IFileDialog,
    IID_IFileDialogControlEvents,
    IID_IFileDialogCustomize,
    IID_IFileDialogEvents,
    IID_IFileOpenDialog,
    IID_IFileOperation,
    IID_IFileOperationProgressSink,
    IID_IFileSaveDialog,
    IID_IModalWindow,
    IID_IPropertyStore,
    IID_IShellFolder,
    IID_IShellItem,
    IID_IShellItemArray,
    IID_IShellItemFilter,
    IID_IShellLibrary,
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
    Show: Callable[[int | HWND], HRESULT]


class IShellItem(IUnknown):
    _case_insensitive_: bool = True
    _iid_: GUID = IID_IShellItem
    _methods_: ClassVar[list[_ComMemberSpec]] = [
        COMMETHOD(
            [],
            HRESULT,
            "BindToHandler",
            (["in"], POINTER(IUnknown), "pbc"),
            (["in"], POINTER(GUID), "bhid"),
            (["in"], POINTER(GUID), "riid"),
            (["out"], POINTER(c_void_p), "ppv"),
        ),
        COMMETHOD(
            [], HRESULT, "GetParent", (["out"], POINTER(POINTER(IUnknown)), "ppsi")
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetDisplayName",
            (["in"], c_ulong, "sigdnName"),
            (["out"], POINTER(LPWSTR), "ppszName"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetAttributes",
            (["in"], c_ulong, "sfgaoMask"),
            (["out"], POINTER(c_ulong), "psfgaoAttribs"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "Compare",
            (["in"], POINTER(IUnknown), "psi"),
            (["in"], c_ulong, "hint"),
            (["out"], POINTER(c_int), "piOrder"),
        ),
    ]
    QueryInterface: Callable[[GUID, _Pointer[_Pointer[IUnknown]]], HRESULT]
    AddRef: Callable[[], ULONG]
    Release: Callable[[], ULONG]
    BindToHandler: Callable[
        [_Pointer[IUnknown], GUID, GUID, _Pointer[c_void_p]], HRESULT
    ]
    GetParent: Callable[[], IUnknown]
    GetDisplayName: Callable[[c_ulong | int], str]
    GetAttributes: Callable[[c_ulong | int], int]
    Compare: Callable[[_Pointer[IUnknown], c_ulong, c_int], HRESULT]


class IContextMenu(IUnknown):
    _case_insensitive_: bool = True
    _iid_: GUID = IID_IContextMenu
    _methods_: ClassVar[list[_ComMemberSpec]] = [
        COMMETHOD(
            [],
            HRESULT,
            "QueryContextMenu",
            (["in"], c_void_p, "hmenu"),
            (["in"], c_uint, "indexMenu"),
            (["in"], c_uint, "idCmdFirst"),
            (["in"], c_uint, "idCmdLast"),
            (["in"], c_uint, "uFlags"),
        ),
        COMMETHOD([], HRESULT, "InvokeCommand", (["in"], c_void_p, "pici")),
        COMMETHOD(
            [],
            HRESULT,
            "GetCommandString",
            (["in"], c_uint, "idCmd"),
            (["in"], c_uint, "uType"),
            (["in"], c_void_p, "pReserved"),
            (["out"], c_wchar_p, "pszName"),
            (["in"], c_uint, "cchMax"),
        ),
    ]
    QueryInterface: Callable[[GUID, _Pointer[_Pointer[IUnknown]]], HRESULT]
    AddRef: Callable[[], ULONG]
    Release: Callable[[], ULONG]
    QueryContextMenu: Callable[[c_void_p, c_uint, c_uint, c_uint, c_uint], HRESULT]
    InvokeCommand: Callable[[c_void_p], HRESULT]
    GetCommandString: Callable[
        [c_uint, c_uint, c_void_p, _Pointer[c_wchar_p], c_uint], HRESULT
    ]


class IShellFolder(IUnknown):
    _case_insensitive_: bool = True
    _iid_: GUID = IID_IShellFolder
    _methods_: ClassVar[list[_ComMemberSpec]] = [
        COMMETHOD(
            [],
            HRESULT,
            "ParseDisplayName",
            (["in"], HWND, "hwnd"),
            (["in"], POINTER(IUnknown), "pbc"),
            (["in"], LPCWSTR, "pszDisplayName"),
            (["out"], POINTER(ULONG), "pchEaten"),
            (["out"], POINTER(c_void_p), "ppidl"),
            (["in"], POINTER(ULONG), "pdwAttributes"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "EnumObjects",
            (["in"], HWND, "hwnd"),
            (["in"], c_ulong, "grfFlags"),
            (["out"], POINTER(POINTER(IUnknown)), "ppenumIDList"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "BindToObject",
            (["in"], c_void_p, "pidl"),
            (["in"], POINTER(IUnknown), "pbc"),
            (["in"], POINTER(GUID), "riid"),
            (["out"], POINTER(c_void_p), "ppv"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "BindToStorage",
            (["in"], c_void_p, "pidl"),
            (["in"], POINTER(IUnknown), "pbc"),
            (["in"], POINTER(GUID), "riid"),
            (["out"], POINTER(c_void_p), "ppv"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "CompareIDs",
            (["in"], c_void_p, "lParam"),
            (["in"], c_void_p, "pidl1"),
            (["in"], c_void_p, "pidl2"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "CreateViewObject",
            (["in"], HWND, "hwndOwner"),
            (["in"], POINTER(GUID), "riid"),
            (["out"], POINTER(c_void_p), "ppv"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetAttributesOf",
            (["in"], c_uint, "cidl"),
            (["in"], C_POINTER(c_void_p), "apidl"),
            (["out"], POINTER(c_ulong), "rgfInOut"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetUIObjectOf",
            (["in"], HWND, "hwndOwner"),
            (["in"], c_uint, "cidl"),
            (["in"], C_POINTER(c_void_p), "apidl"),
            (["in"], POINTER(GUID), "riid"),
            (["in"], POINTER(c_uint), "rgfReserved"),
            (["out"], POINTER(c_void_p), "ppv"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetDisplayNameOf",
            (["in"], c_void_p, "pidl"),
            (["in"], c_ulong, "uFlags"),
            (["out"], POINTER(c_wchar_p), "pName"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetNameOf",
            (["in"], HWND, "hwnd"),
            (["in"], c_void_p, "pidl"),
            (["in"], LPCWSTR, "pszName"),
            (["in"], c_ulong, "uFlags"),
            (["out"], POINTER(c_void_p), "ppidlOut"),
        ),
    ]
    QueryInterface: Callable[[GUID, _Pointer[_Pointer[IUnknown]]], HRESULT]
    AddRef: Callable[[], ULONG]
    Release: Callable[[], ULONG]
    ParseDisplayName: Callable[
        [
            HWND,
            _Pointer[IUnknown],
            LPCWSTR,
            _Pointer[ULONG],
            _Pointer[c_void_p],
            _Pointer[ULONG],
        ],
        HRESULT,
    ]
    EnumObjects: Callable[[HWND, c_ulong, _Pointer[_Pointer[IUnknown]]], HRESULT]
    BindToObject: Callable[
        [c_void_p, _Pointer[IUnknown], GUID, _Pointer[c_void_p]], HRESULT
    ]
    BindToStorage: Callable[
        [c_void_p, _Pointer[IUnknown], GUID, _Pointer[c_void_p]], HRESULT
    ]
    CompareIDs: Callable[[c_void_p, c_void_p, c_void_p], HRESULT]
    CreateViewObject: Callable[[HWND, GUID, _Pointer[c_void_p]], HRESULT]
    GetAttributesOf: Callable[[c_uint, _Pointer[c_void_p], _Pointer[c_ulong]], HRESULT]
    GetUIObjectOf: Callable[
        [HWND, c_uint, _Pointer[c_void_p], GUID, _Pointer[c_uint], _Pointer[c_void_p]],
        HRESULT,
    ]
    GetDisplayNameOf: Callable[[c_void_p, c_ulong, _Pointer[c_wchar_p]], HRESULT]
    SetNameOf: Callable[[HWND, c_void_p, LPCWSTR, c_ulong, _Pointer[c_void_p]], HRESULT]


class IShellItemArray(IUnknown):
    _case_insensitive_: bool = True
    _iid_: GUID = IID_IShellItemArray
    _methods_: ClassVar[list[_ComMemberSpec]] = [
        COMMETHOD(
            [],
            HRESULT,
            "BindToHandler",
            (["in"], POINTER(IUnknown), "pbc"),
            (["in"], POINTER(GUID), "bhid"),
            (["in"], POINTER(GUID), "riid"),
            (["out"], POINTER(c_void_p), "ppv"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetPropertyStore",
            (["in"], c_ulong, "flags"),
            (["in"], POINTER(GUID), "riid"),
            (["out"], POINTER(c_void_p), "ppv"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetPropertyDescriptionList",
            (["in"], POINTER(GUID), "keyType"),
            (["in"], POINTER(GUID), "riid"),
            (["out"], POINTER(c_void_p), "ppv"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetAttributes",
            (["in"], c_ulong, "attribFlags"),
            (["in"], c_ulong, "sfgaoMask"),
            (["out"], POINTER(c_ulong), "psfgaoAttribs"),
        ),
        COMMETHOD([], HRESULT, "GetCount", (["out"], POINTER(c_uint), "pdwNumItems")),
        COMMETHOD(
            [],
            HRESULT,
            "GetItemAt",
            (["in"], c_uint, "dwIndex"),
            (["out"], POINTER(POINTER(IShellItem)), "ppsi"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "EnumItems",
            (["out"], POINTER(POINTER(IUnknown)), "ppenumShellItems"),
        ),
    ]
    QueryInterface: Callable[[GUID, IUnknown], HRESULT]
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
        COMMETHOD([], HRESULT, "IncludeItem", (["in"], POINTER(IShellItem), "psi")),
        COMMETHOD(
            [],
            HRESULT,
            "GetEnumFlagsForItem",
            (["in"], POINTER(IShellItem), "psi"),
            (["out"], POINTER(c_ulong), "pgrfFlags"),
        ),
    ]
    QueryInterface: Callable[[GUID, IUnknown], HRESULT]
    AddRef: Callable[[], ULONG]
    Release: Callable[[], ULONG]
    IncludeItem: Callable[[IShellItem], c_ulong]
    GetEnumFlagsForItem: Callable[[], HRESULT]


class IEnumShellItems(IUnknown):
    _case_insensitive_: bool = True
    _iid_: GUID = IID_IEnumShellItems
    _methods_: ClassVar[list[_ComMemberSpec]]
    QueryInterface: Callable[[GUID, IUnknown], HRESULT]
    AddRef: Callable[[], ULONG]
    Release: Callable[[], ULONG]
    Next: Callable[
        [_Pointer[IEnumShellItems], c_ulong, IShellItem, _Pointer[c_ulong]], HRESULT
    ]
    Skip: Callable[[_Pointer[IEnumShellItems], c_ulong], HRESULT]
    Reset: Callable[[_Pointer[IEnumShellItems]], HRESULT]
    Clone: Callable[
        [_Pointer[IEnumShellItems], _Pointer[_Pointer[IEnumShellItems]]], HRESULT
    ]


IEnumShellItems._methods_ = [  # noqa: SLF001
    COMMETHOD(
        [],
        HRESULT,
        "Next",
        (["in"], c_ulong, "celt"),
        (["out"], POINTER(POINTER(IShellItem)), "rgelt"),
        (["out"], POINTER(c_ulong), "pceltFetched"),
    ),
    COMMETHOD([], HRESULT, "Skip", (["in"], c_ulong, "celt")),
    COMMETHOD([], HRESULT, "Reset"),
    COMMETHOD(
        [], HRESULT, "Clone", (["out"], POINTER(POINTER(IEnumShellItems)), "ppenum")
    ),
]


class IPropertyStore(IUnknown):
    _case_insensitive_: bool = True
    _iid_: GUID = IID_IPropertyStore
    _methods_: ClassVar[list[_ComMemberSpec]] = [
        COMMETHOD([], HRESULT, "GetCount", (["out"], POINTER(c_ulong), "count")),
        COMMETHOD(
            [],
            HRESULT,
            "GetAt",
            (["in"], c_ulong, "index"),
            (["out"], POINTER(GUID), "key"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetValue",
            (["in"], POINTER(GUID), "key"),
            (["out"], POINTER(c_void_p), "pv"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetValue",
            (["in"], POINTER(GUID), "key"),
            (["in"], POINTER(c_void_p), "propvar"),
        ),
        COMMETHOD([], HRESULT, "Commit"),
    ]
    QueryInterface: Callable[[GUID, IUnknown], HRESULT]
    AddRef: Callable[[], ULONG]
    Release: Callable[[], ULONG]
    GetCount: Callable[[_Pointer[IPropertyStore], _Pointer[c_ulong]], HRESULT]
    GetAt: Callable[[_Pointer[IPropertyStore], c_ulong, GUID], HRESULT]
    GetValue: Callable[[_Pointer[IPropertyStore], GUID, _Pointer[c_void_p]], HRESULT]
    SetValue: Callable[[_Pointer[IPropertyStore], GUID, _Pointer[c_void_p]], HRESULT]
    Commit: Callable[[_Pointer[IPropertyStore]], HRESULT]


class IFileOperationProgressSink(IUnknown):
    _case_insensitive_: bool = True
    _iid_: GUID = IID_IFileOperationProgressSink
    _methods_: ClassVar[list[_ComMemberSpec]] = [
        COMMETHOD([], HRESULT, "StartOperations"),
        COMMETHOD([], HRESULT, "FinishOperations", (["in"], HRESULT, "hr")),
        COMMETHOD(
            [],
            HRESULT,
            "PreRenameItem",
            (["in"], c_ulong, "dwFlags"),
            (["in"], POINTER(IShellItem), "psiItem"),
            (["in"], c_wchar_p, "pszNewName"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "PostRenameItem",
            (["in"], c_ulong, "dwFlags"),
            (["in"], POINTER(IShellItem), "psiItem"),
            (["in"], c_wchar_p, "pszNewName"),
            (["in"], HRESULT, "hrRename"),
            (["in"], POINTER(IShellItem), "psiNewlyCreated"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "PreMoveItem",
            (["in"], c_ulong, "dwFlags"),
            (["in"], POINTER(IShellItem), "psiItem"),
            (["in"], POINTER(IShellItem), "psiDestinationFolder"),
            (["in"], c_wchar_p, "pszNewName"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "PostMoveItem",
            (["in"], c_ulong, "dwFlags"),
            (["in"], POINTER(IShellItem), "psiItem"),
            (["in"], POINTER(IShellItem), "psiDestinationFolder"),
            (["in"], c_wchar_p, "pszNewName"),
            (["in"], HRESULT, "hrMove"),
            (["in"], POINTER(IShellItem), "psiNewlyCreated"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "PreCopyItem",
            (["in"], c_ulong, "dwFlags"),
            (["in"], POINTER(IShellItem), "psiItem"),
            (["in"], POINTER(IShellItem), "psiDestinationFolder"),
            (["in"], c_wchar_p, "pszNewName"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "PostCopyItem",
            (["in"], c_ulong, "dwFlags"),
            (["in"], POINTER(IShellItem), "psiItem"),
            (["in"], POINTER(IShellItem), "psiDestinationFolder"),
            (["in"], c_wchar_p, "pszNewName"),
            (["in"], HRESULT, "hrCopy"),
            (["in"], POINTER(IShellItem), "psiNewlyCreated"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "PreDeleteItem",
            (["in"], c_ulong, "dwFlags"),
            (["in"], POINTER(IShellItem), "psiItem"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "PostDeleteItem",
            (["in"], c_ulong, "dwFlags"),
            (["in"], POINTER(IShellItem), "psiItem"),
            (["in"], HRESULT, "hrDelete"),
            (["in"], POINTER(IShellItem), "psiNewlyCreated"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "PreNewItem",
            (["in"], c_ulong, "dwFlags"),
            (["in"], POINTER(IShellItem), "psiDestinationFolder"),
            (["in"], c_wchar_p, "pszNewName"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "PostNewItem",
            (["in"], c_ulong, "dwFlags"),
            (["in"], POINTER(IShellItem), "psiDestinationFolder"),
            (["in"], c_wchar_p, "pszNewName"),
            (["in"], c_wchar_p, "pszTemplateName"),
            (["in"], c_ulong, "dwFileAttributes"),
            (["in"], HRESULT, "hrNew"),
            (["in"], POINTER(IShellItem), "psiNewItem"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "UpdateProgress",
            (["in"], c_ulong, "iWorkTotal"),
            (["in"], c_ulong, "iWorkSoFar"),
        ),
        COMMETHOD([], HRESULT, "ResetTimer"),
        COMMETHOD([], HRESULT, "PauseTimer"),
        COMMETHOD([], HRESULT, "ResumeTimer"),
    ]
    QueryInterface: Callable[[GUID, IUnknown], HRESULT]
    AddRef: Callable[[], ULONG]
    Release: Callable[[], ULONG]
    StartOperations: Callable[[], HRESULT]
    FinishOperations: Callable[[HRESULT], HRESULT]
    PreRenameItem: Callable[[c_ulong, IShellItem, c_wchar_p], HRESULT]
    PostRenameItem: Callable[
        [c_ulong, IShellItem, c_wchar_p, HRESULT, IShellItem], HRESULT
    ]
    PreMoveItem: Callable[[c_ulong, IShellItem, IShellItem, c_wchar_p], HRESULT]
    PostMoveItem: Callable[
        [c_ulong, IShellItem, IShellItem, c_wchar_p, HRESULT, IShellItem], HRESULT
    ]
    PreCopyItem: Callable[[c_ulong, IShellItem, IShellItem, c_wchar_p], HRESULT]
    PostCopyItem: Callable[
        [c_ulong, IShellItem, IShellItem, c_wchar_p, HRESULT, IShellItem], HRESULT
    ]
    PreDeleteItem: Callable[[c_ulong, IShellItem], HRESULT]
    PostDeleteItem: Callable[[c_ulong, IShellItem, HRESULT, IShellItem], HRESULT]
    PreNewItem: Callable[[c_ulong, IShellItem, c_wchar_p], HRESULT]
    PostNewItem: Callable[
        [c_ulong, IShellItem, c_wchar_p, c_wchar_p, c_ulong, HRESULT, IShellItem],
        HRESULT,
    ]
    UpdateProgress: Callable[[c_ulong, c_ulong], HRESULT]
    ResetTimer: Callable[[], HRESULT]
    PauseTimer: Callable[[], HRESULT]
    ResumeTimer: Callable[[], HRESULT]


class FileOperationProgressSink(COMObject):
    _com_interfaces_: Sequence[type[IUnknown]] = [IFileOperationProgressSink]

    def StartOperations(self) -> HRESULT:
        return S_OK

    def FinishOperations(self, hr: HRESULT) -> HRESULT:
        return S_OK

    def PreRenameItem(
        self, dwFlags: c_ulong | int, psiItem: IShellItem, pszNewName: LPCWSTR | str
    ) -> HRESULT:  # noqa: N803
        return S_OK

    def PostRenameItem(
        self,
        dwFlags: c_ulong | int,
        psiItem: IShellItem,
        pszNewName: LPCWSTR | str,
        hrRename: HRESULT,
        psiNewlyCreated: IShellItem,
    ) -> HRESULT:  # noqa: N803
        return S_OK

    def PreMoveItem(
        self,
        dwFlags: c_ulong | int,
        psiItem: IShellItem,
        psiDestinationFolder: IShellItem,
        pszNewName: LPCWSTR | str,
    ) -> HRESULT:  # noqa: N803
        return S_OK

    def PostMoveItem(
        self,
        dwFlags: c_ulong | int,
        psiItem: IShellItem,
        psiDestinationFolder: IShellItem,
        pszNewName: LPCWSTR | str,
        hrMove: HRESULT,
        psiNewlyCreated: IShellItem,
    ) -> HRESULT:  # noqa: N803, E501
        return S_OK

    def PreCopyItem(
        self,
        dwFlags: c_ulong | int,
        psiItem: IShellItem,
        psiDestinationFolder: IShellItem,
        pszNewName: LPCWSTR | str,
    ) -> HRESULT:  # noqa: N803
        return S_OK

    def PostCopyItem(
        self,
        dwFlags: c_ulong | int,
        psiItem: IShellItem,
        psiDestinationFolder: IShellItem,
        pszNewName: LPCWSTR | str,
        hrCopy: HRESULT,
        psiNewlyCreated: IShellItem,
    ) -> HRESULT:  # noqa: N803, E501
        return S_OK

    def PreDeleteItem(self, dwFlags: c_ulong | int, psiItem: IShellItem) -> HRESULT:
        return S_OK

    def PostDeleteItem(
        self,
        dwFlags: c_ulong | int,
        psiItem: IShellItem,
        hrDelete: HRESULT,
        psiNewlyCreated: IShellItem,
    ) -> HRESULT:
        return S_OK

    def PreNewItem(
        self,
        dwFlags: c_ulong | int,
        psiDestinationFolder: IShellItem,
        pszNewName: LPCWSTR | str,
    ) -> HRESULT:
        return S_OK

    def PostNewItem(
        self,
        dwFlags: c_ulong | int,
        psiDestinationFolder: IShellItem,
        pszNewName: LPCWSTR | str,
        pszTemplateName: LPCWSTR | str,
        dwFileAttributes: c_ulong | int,
        hrNew: HRESULT,
        psiNewItem: IShellItem,
    ) -> HRESULT:  # noqa: N803, E501
        return S_OK

    def UpdateProgress(
        self, iWorkTotal: c_ulong | int, iWorkSoFar: c_ulong | int
    ) -> HRESULT:  # noqa: N803
        return S_OK

    def ResetTimer(self) -> HRESULT:
        return S_OK

    def PauseTimer(self) -> HRESULT:
        return S_OK

    def ResumeTimer(self) -> HRESULT:
        return S_OK


class IFileOperation(IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IFileOperation
    _idlflags_ = []

    _methods_: ClassVar[list[_ComMemberSpec]] = [
        # Advise methods
        comtypes.COMMETHOD(
            [],
            HRESULT,
            "Advise",
            (["in"], POINTER(IFileOperationProgressSink), "pfops"),
            (["out"], POINTER(c_ulong), "pdwCookie"),
        ),
        comtypes.COMMETHOD([], HRESULT, "Unadvise", (["in"], c_ulong, "dwCookie")),
        # Operation control methods
        comtypes.COMMETHOD(
            [], HRESULT, "SetOperationFlags", (["in"], c_ulong, "dwOperationFlags")
        ),
        comtypes.COMMETHOD(
            [], HRESULT, "SetProgressMessage", (["in"], c_wchar_p, "pszMessage")
        ),
        comtypes.COMMETHOD(
            [],
            HRESULT,
            "SetProgressDialog",
            (["in"], POINTER(IUnknown), "popd"),
        ),
        # Item methods
        comtypes.COMMETHOD(
            [],
            HRESULT,
            "SetProperties",
            (["in"], POINTER(IUnknown), "pproparray"),
        ),
        comtypes.COMMETHOD(
            [], HRESULT, "SetOwnerWindow", (["in"], c_ulong, "hwndOwner")
        ),
        comtypes.COMMETHOD(
            [],
            HRESULT,
            "ApplyPropertiesToItem",
            (["in"], POINTER(IShellItem), "psiItem"),
        ),
        comtypes.COMMETHOD(
            [],
            HRESULT,
            "ApplyPropertiesToItems",
            (["in"], POINTER(IUnknown), "punkItems"),
        ),
        # Operation methods
        comtypes.COMMETHOD(
            [],
            HRESULT,
            "RenameItem",
            (["in"], POINTER(IShellItem), "psiItem"),
            (["in"], c_wchar_p, "pszNewName"),
            (["in"], POINTER(IFileOperationProgressSink), "pfopsItem"),
        ),
        comtypes.COMMETHOD(
            [],
            HRESULT,
            "RenameItems",
            (["in"], POINTER(IUnknown), "pUnkItems"),
            (["in"], c_wchar_p, "pszNewName"),
        ),
        comtypes.COMMETHOD(
            [],
            HRESULT,
            "MoveItem",
            (["in"], POINTER(IShellItem), "psiItem"),
            (["in"], POINTER(IShellItem), "psiDestinationFolder"),
            (["in"], c_wchar_p, "pszNewName"),
            (["in"], POINTER(IFileOperationProgressSink), "pfopsItem"),
        ),
        comtypes.COMMETHOD(
            [],
            HRESULT,
            "MoveItems",
            (["in"], POINTER(IUnknown), "punkItems"),
            (["in"], POINTER(IShellItem), "psiDestinationFolder"),
        ),
        comtypes.COMMETHOD(
            [],
            HRESULT,
            "CopyItem",
            (["in"], POINTER(IShellItem), "psiItem"),
            (["in"], POINTER(IShellItem), "psiDestinationFolder"),
            (["in"], c_wchar_p, "pszNewName"),
            (["in"], POINTER(IFileOperationProgressSink), "pfopsItem"),
        ),
        comtypes.COMMETHOD(
            [],
            HRESULT,
            "CopyItems",
            (["in"], POINTER(IUnknown), "punkItems"),
            (["in"], POINTER(IShellItem), "psiDestinationFolder"),
        ),
        comtypes.COMMETHOD(
            [],
            HRESULT,
            "DeleteItem",
            (["in"], POINTER(IShellItem), "psiItem"),
            (["in"], POINTER(IFileOperationProgressSink), "pfopsItem"),
        ),
        comtypes.COMMETHOD(
            [],
            HRESULT,
            "DeleteItems",
            (["in"], POINTER(IUnknown), "punkItems"),
        ),
        comtypes.COMMETHOD(
            [],
            HRESULT,
            "NewItem",
            (["in"], POINTER(IShellItem), "psiDestinationFolder"),
            (["in"], c_ulong, "dwFileAttributes"),
            (["in"], c_wchar_p, "pszName"),
            (["in"], c_wchar_p, "pszTemplateName"),
            (["in"], POINTER(IFileOperationProgressSink), "pfopsItem"),
        ),
        # Execution methods
        comtypes.COMMETHOD([], HRESULT, "PerformOperations"),
        comtypes.COMMETHOD(
            [],
            HRESULT,
            "GetAnyOperationsAborted",
            (["out"], POINTER(c_int), "pfAnyOperationsAborted"),
        ),
    ]


class IFileDialogEvents(IUnknown):
    _case_insensitive_: bool = True
    _iid_: GUID = IID_IFileDialogEvents
    _methods_: ClassVar[list[_ComMemberSpec]]
    QueryInterface: Callable[[GUID, IUnknown], HRESULT]
    AddRef: Callable[[], ULONG]
    Release: Callable[[], ULONG]
    OnFileOk: Callable[[IFileDialog], HRESULT]
    OnFolderChanging: Callable[[IFileDialog, IShellItem], HRESULT]
    OnFolderChange: Callable[[IFileDialog], HRESULT]
    OnSelectionChange: Callable[[IFileDialog], HRESULT]
    OnShareViolation: Callable[[IFileDialog, IShellItem, c_int], HRESULT]
    OnTypeChange: Callable[[IFileDialog], HRESULT]
    OnOverwrite: Callable[[IFileDialog, IShellItem, c_int], HRESULT]


class IFileDialog(IModalWindow):
    _iid_: GUID = IID_IFileDialog
    _methods_: ClassVar[list[_ComMemberSpec]] = [
        COMMETHOD(
            [],
            HRESULT,
            "SetFileTypes",
            (["in"], c_uint, "cFileTypes"),
            (["in"], POINTER(c_void_p), "rgFilterSpec"),
        ),
        COMMETHOD([], HRESULT, "SetFileTypeIndex", (["in"], c_uint, "iFileType")),
        COMMETHOD(
            [], HRESULT, "GetFileTypeIndex", (["out"], POINTER(c_uint), "piFileType")
        ),
        COMMETHOD(
            [],
            HRESULT,
            "Advise",
            (["in"], POINTER(IUnknown), "pfde"),
            (["out"], POINTER(DWORD), "pdwCookie"),
        ),
        COMMETHOD([], HRESULT, "Unadvise", (["in"], DWORD, "dwCookie")),
        COMMETHOD([], HRESULT, "SetOptions", (["in"], c_uint, "fos")),
        COMMETHOD([], HRESULT, "GetOptions", (["out"], POINTER(DWORD), "pfos")),
        COMMETHOD(
            [], HRESULT, "SetDefaultFolder", (["in"], POINTER(IShellItem), "psi")
        ),
        COMMETHOD([], HRESULT, "SetFolder", (["in"], POINTER(IShellItem), "psi")),
        COMMETHOD(
            [], HRESULT, "GetFolder", (["out"], POINTER(POINTER(IShellItem)), "ppsi")
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetCurrentSelection",
            (["out"], POINTER(POINTER(IShellItem)), "ppsi"),
        ),
        COMMETHOD([], HRESULT, "SetFileName", (["in"], LPCWSTR, "pszName")),
        COMMETHOD([], HRESULT, "GetFileName", (["out"], POINTER(LPWSTR), "pszName")),
        COMMETHOD([], HRESULT, "SetTitle", (["in"], LPCWSTR, "pszTitle")),
        COMMETHOD([], HRESULT, "SetOkButtonLabel", (["in"], LPCWSTR, "pszText")),
        COMMETHOD([], HRESULT, "SetFileNameLabel", (["in"], LPCWSTR, "pszLabel")),
        COMMETHOD(
            [], HRESULT, "GetResult", (["out"], POINTER(POINTER(IShellItem)), "ppsi")
        ),
        COMMETHOD(
            [],
            HRESULT,
            "AddPlace",
            (["in"], POINTER(IShellItem), "psi"),
            (["in"], c_int, "fdap"),
        ),
        COMMETHOD(
            [], HRESULT, "SetDefaultExtension", (["in"], LPCWSTR, "pszDefaultExtension")
        ),
        COMMETHOD([], HRESULT, "Close", (["in"], HRESULT, "hr")),
        COMMETHOD([], HRESULT, "SetClientGuid", (["in"], POINTER(GUID), "guid")),
        COMMETHOD([], HRESULT, "ClearClientData"),
        COMMETHOD(
            [], HRESULT, "SetFilter", (["in"], POINTER(IShellItemFilter), "pFilter")
        ),
    ]
    SetFileTypes: Callable[[c_uint | int, _Pointer[c_void_p]], HRESULT]
    SetFileTypeIndex: Callable[[c_uint], HRESULT]
    GetFileTypeIndex: Callable[[], _Pointer[c_uint]]
    Advise: Callable[[IUnknown | COMObject], int]
    Unadvise: Callable[[int], HRESULT]
    SetOptions: Callable[[DWORD | int], HRESULT]
    GetOptions: Callable[[], int]
    SetDefaultFolder: Callable[[_Pointer[IShellItem]], HRESULT]
    SetFolder: Callable[[_Pointer[IShellItem]], HRESULT]
    GetFolder: Callable[[], IShellItem]
    GetCurrentSelection: Callable[[], IShellItem]
    SetFileName: Callable[[str], HRESULT]
    GetFileName: Callable[[], _Pointer[LPWSTR]]
    SetTitle: Callable[[str], HRESULT]
    SetOkButtonLabel: Callable[[str], HRESULT]
    SetFileNameLabel: Callable[[str], HRESULT]
    GetResult: Callable[[], IShellItem]
    AddPlace: Callable[[IShellItem, c_int], HRESULT]
    SetDefaultExtension: Callable[[str], HRESULT]
    Close: Callable[[HRESULT], HRESULT]
    SetClientGuid: Callable[[GUID], HRESULT]
    ClearClientData: Callable[[], HRESULT]
    SetFilter: Callable[[IShellItemFilter], HRESULT]


IFileDialogEvents._methods_ = [  # noqa: SLF001
    COMMETHOD([], HRESULT, "OnFileOk", (["in"], POINTER(IFileDialog), "pfd")),
    COMMETHOD(
        [],
        HRESULT,
        "OnFolderChanging",
        (["in"], POINTER(IFileDialog), "pfd"),
        (["in"], POINTER(IShellItem), "psiFolder"),
    ),
    COMMETHOD([], HRESULT, "OnFolderChange", (["in"], POINTER(IFileDialog), "pfd")),
    COMMETHOD([], HRESULT, "OnSelectionChange", (["in"], POINTER(IFileDialog), "pfd")),
    COMMETHOD(
        [],
        HRESULT,
        "OnShareViolation",
        (["in"], POINTER(IFileDialog), "pfd"),
        (["in"], POINTER(IShellItem), "psi"),
        (["out"], POINTER(c_int), "pResponse"),
    ),
    COMMETHOD([], HRESULT, "OnTypeChange", (["in"], POINTER(IFileDialog), "pfd")),
    COMMETHOD(
        [],
        HRESULT,
        "OnOverwrite",
        (["in"], POINTER(IFileDialog), "pfd"),
        (["in"], POINTER(IShellItem), "psi"),
        (["out"], POINTER(c_int), "pResponse"),
    ),
]


class IShellLibrary(IUnknown):
    _case_insensitive_: bool = True
    _iid_: GUID = IID_IShellLibrary
    _methods_: ClassVar[list[_ComMemberSpec]] = [
        COMMETHOD(
            [],
            HRESULT,
            "LoadLibraryFromItem",
            (["in"], POINTER(IShellItem), "psi"),
            (["in"], c_ulong, "grfMode"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "LoadLibraryFromKnownFolder",
            (["in"], POINTER(GUID), "kfidLibrary"),
            (["in"], c_ulong, "grfMode"),
        ),
        COMMETHOD([], HRESULT, "AddFolder", (["in"], POINTER(IShellItem), "psi")),
        COMMETHOD([], HRESULT, "RemoveFolder", (["in"], POINTER(IShellItem), "psi")),
        COMMETHOD(
            [],
            HRESULT,
            "GetFolders",
            (["in"], c_int, "lff"),
            (["in"], POINTER(GUID), "riid"),
            (["out"], POINTER(POINTER(c_void_p)), "ppv"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "ResolveFolder",
            (["in"], POINTER(IShellItem), "psi"),
            (["in"], c_ulong, "grfMode"),
            (["in"], POINTER(GUID), "riid"),
            (["out"], POINTER(POINTER(c_void_p)), "ppv"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetDefaultSaveFolder",
            (["in"], c_int, "dsft"),
            (["in"], POINTER(GUID), "riid"),
            (["out"], POINTER(POINTER(c_void_p)), "ppv"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetDefaultSaveFolder",
            (["in"], c_int, "dsft"),
            (["in"], POINTER(IShellItem), "psi"),
        ),
        COMMETHOD([], HRESULT, "GetOptions", (["out"], POINTER(c_uint), "pOptions")),
        COMMETHOD(
            [],
            HRESULT,
            "SetOptions",
            (["in"], c_ulong, "stfOptions"),
            (["in"], c_ulong, "stfMask"),
        ),
        COMMETHOD([], HRESULT, "GetFolderType", (["out"], POINTER(GUID), "pftid")),
        COMMETHOD([], HRESULT, "SetFolderType", (["in"], POINTER(GUID), "ftid")),
        COMMETHOD([], HRESULT, "GetIcon", (["out"], POINTER(LPWSTR), "ppszIcon")),
        COMMETHOD([], HRESULT, "SetIcon", (["in"], LPCWSTR, "pszIcon")),
        COMMETHOD([], HRESULT, "Commit"),
        COMMETHOD(
            [],
            HRESULT,
            "Save",
            (["in"], POINTER(IShellItem), "psiFolderToSaveIn"),
            (["in"], LPCWSTR, "pszLibraryName"),
            (["in"], c_ulong, "lrf"),
            (["out"], POINTER(POINTER(IShellItem)), "ppsiNewItem"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SaveInKnownFolder",
            (["in"], POINTER(GUID), "kfid"),
            (["in"], LPCWSTR, "pszLibraryName"),
            (["in"], c_ulong, "lrf"),
            (["out"], POINTER(POINTER(IShellItem)), "ppsiNewItem"),
        ),
    ]
    QueryInterface: Callable[[GUID, IUnknown], HRESULT]
    AddRef: Callable[[], ULONG]
    Release: Callable[[], ULONG]
    LoadLibraryFromItem: Callable[
        [_Pointer[IShellLibrary], IShellItem, c_ulong], HRESULT
    ]
    LoadLibraryFromKnownFolder: Callable[
        [_Pointer[IShellLibrary], GUID, c_ulong], HRESULT
    ]
    AddFolder: Callable[[_Pointer[IShellLibrary], IShellItem], HRESULT]
    RemoveFolder: Callable[[_Pointer[IShellLibrary], IShellItem], HRESULT]
    GetFolders: Callable[
        [_Pointer[IShellLibrary], c_int, GUID, _Pointer[_Pointer[c_void_p]]], HRESULT
    ]
    ResolveFolder: Callable[
        [
            _Pointer[IShellLibrary],
            IShellItem,
            c_ulong,
            GUID,
            _Pointer[_Pointer[c_void_p]],
        ],
        HRESULT,
    ]
    GetDefaultSaveFolder: Callable[
        [_Pointer[IShellLibrary], c_int, GUID, _Pointer[_Pointer[c_void_p]]], HRESULT
    ]
    SetDefaultSaveFolder: Callable[
        [_Pointer[IShellLibrary], c_int, IShellItem], HRESULT
    ]
    GetOptions: Callable[[_Pointer[IShellLibrary], _Pointer[c_uint]], HRESULT]
    SetOptions: Callable[[_Pointer[IShellLibrary], c_ulong, c_ulong], HRESULT]
    GetFolderType: Callable[[_Pointer[IShellLibrary], GUID], HRESULT]
    SetFolderType: Callable[[_Pointer[IShellLibrary], GUID], HRESULT]
    GetIcon: Callable[[_Pointer[IShellLibrary], _Pointer[LPWSTR]], HRESULT]
    SetIcon: Callable[[_Pointer[IShellLibrary], LPCWSTR], HRESULT]
    Commit: Callable[[_Pointer[IShellLibrary]], HRESULT]
    Save: Callable[
        [_Pointer[IShellLibrary], IShellItem, LPCWSTR, c_ulong, IShellItem], HRESULT
    ]
    SaveInKnownFolder: Callable[
        [_Pointer[IShellLibrary], GUID, LPCWSTR, c_ulong, IShellItem], HRESULT
    ]


class IFileOpenDialog(IFileDialog):
    _case_insensitive_: bool = True
    _iid_: GUID = IID_IFileOpenDialog
    _methods_: ClassVar[list[_ComMemberSpec]] = [
        COMMETHOD(
            [],
            HRESULT,
            "GetResults",
            (["out"], POINTER(POINTER(IShellItemArray)), "ppenum"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetSelectedItems",
            (["out"], POINTER(POINTER(IShellItemArray)), "ppsai"),
        ),
    ]
    GetResults: Callable[[], IShellItemArray]
    GetSelectedItems: Callable[[], IShellItemArray]


class IFileSaveDialog(IFileDialog):
    _case_insensitive_: bool = True
    _iid_: GUID = IID_IFileSaveDialog
    _methods_: ClassVar[list[_ComMemberSpec]] = [
        COMMETHOD([], HRESULT, "SetSaveAsItem", (["in"], POINTER(IShellItem), "psi")),
        COMMETHOD([], HRESULT, "SetProperties", (["in"], POINTER(IUnknown), "pStore")),
        COMMETHOD(
            [],
            HRESULT,
            "SetCollectedProperties",
            (["in"], POINTER(IUnknown), "pList"),
            (["in"], BOOL, "fAppendDefault"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetProperties",
            (["out"], POINTER(POINTER(IUnknown)), "ppStore"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "ApplyProperties",
            (["in"], POINTER(IShellItem), "psi"),
            (["in"], POINTER(IUnknown), "pStore"),
            (["in"], HWND, "hwnd"),
            (["in"], POINTER(IUnknown), "pSink"),
        ),
    ]
    SetSaveAsItem: Callable[[IShellItem], HRESULT]
    SetProperties: Callable[[_Pointer[IUnknown]], HRESULT]
    SetCollectedProperties: Callable[[_Pointer[IUnknown], BOOL], HRESULT]
    GetProperties: Callable[[_Pointer[_Pointer[IUnknown]]], HRESULT]
    ApplyProperties: Callable[
        [IShellItem, _Pointer[IUnknown], HWND, _Pointer[IUnknown]], HRESULT
    ]


class IFileDialogCustomize(IUnknown):
    _case_insensitive_ = True
    _iid_: GUID = IID_IFileDialogCustomize
    _methods_: ClassVar[list[_ComMemberSpec]] = [
        COMMETHOD([], HRESULT, "EnableOpenDropDown", (["in"], c_uint, "dwIDCtl")),
        COMMETHOD(
            [],
            HRESULT,
            "AddText",
            (["in"], c_uint, "dwIDCtl"),
            (["in"], LPCWSTR, "pszText"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "AddPushButton",
            (["in"], c_uint, "dwIDCtl"),
            (["in"], LPCWSTR, "pszLabel"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "AddCheckButton",
            (["in"], c_uint, "dwIDCtl"),
            (["in"], LPCWSTR, "pszLabel"),
            (["in"], c_int, "bChecked"),
        ),
        COMMETHOD([], HRESULT, "AddRadioButtonList", (["in"], c_uint, "dwIDCtl")),
        COMMETHOD([], HRESULT, "AddComboBox", (["in"], c_uint, "dwIDCtl")),
        COMMETHOD(
            [],
            HRESULT,
            "AddControlItem",
            (["in"], c_uint, "dwIDCtl"),
            (["in"], c_uint, "dwIDItem"),
            (["in"], LPCWSTR, "pszLabel"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "AddEditBox",
            (["in"], c_uint, "dwIDCtl"),
            (["in"], LPCWSTR, "pszText"),
        ),
        COMMETHOD([], HRESULT, "AddSeparator", (["in"], c_uint, "dwIDCtl")),
        COMMETHOD(
            [],
            HRESULT,
            "AddMenu",
            (["in"], c_uint, "dwIDCtl"),
            (["in"], LPCWSTR, "pszLabel"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetControlLabel",
            (["in"], c_uint, "dwIDCtl"),
            (["in"], LPCWSTR, "pszLabel"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetControlState",
            (["in"], c_uint, "dwIDCtl"),
            (["in"], c_int, "dwState"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetCheckButtonState",
            (["in"], c_uint, "dwIDCtl"),
            (["in"], c_int, "bChecked"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetCheckButtonState",
            (["in"], c_uint, "dwIDCtl"),
            (["out"], POINTER(c_int), "pbChecked"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetEditBoxText",
            (["in"], c_uint, "dwIDCtl"),
            (["in"], LPCWSTR, "pszText"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetEditBoxText",
            (["in"], c_uint, "dwIDCtl"),
            (["out"], POINTER(LPCWSTR), "ppszText"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetControlItemText",
            (["in"], c_uint, "dwIDCtl"),
            (["in"], c_uint, "dwIDItem"),
            (["in"], LPCWSTR, "pszLabel"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetControlItemState",
            (["in"], c_uint, "dwIDCtl"),
            (["in"], c_uint, "dwIDItem"),
            (["out"], POINTER(c_int), "pdwState"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetControlItemState",
            (["in"], c_uint, "dwIDCtl"),
            (["in"], c_uint, "dwIDItem"),
            (["in"], c_int, "dwState"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetSelectedControlItem",
            (["in"], c_uint, "dwIDCtl"),
            (["out"], POINTER(c_uint), "pdwIDItem"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetSelectedControlItem",
            (["in"], c_uint, "dwIDCtl"),
            (["in"], c_uint, "dwIDItem"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "StartVisualGroup",
            (["in"], c_uint, "dwIDCtl"),
            (["in"], LPCWSTR, "pszLabel"),
        ),
        COMMETHOD([], HRESULT, "EndVisualGroup", (["in"], c_uint, "dwIDCtl")),
        COMMETHOD([], HRESULT, "MakeProminent", (["in"], c_uint, "dwIDCtl")),
        COMMETHOD(
            [],
            HRESULT,
            "RemoveControlItem",
            (["in"], c_uint, "dwIDCtl"),
            (["in"], c_uint, "dwIDItem"),
        ),
        COMMETHOD([], HRESULT, "RemoveAllControlItems", (["in"], c_uint, "dwIDCtl")),
        COMMETHOD(
            [],
            HRESULT,
            "GetControlState",
            (["in"], c_uint, "dwIDCtl"),
            (["out"], POINTER(c_int), "pdwState"),
        ),
    ]
    EnableOpenDropDown: Callable[[int], HRESULT]
    AddText: Callable[[int, str], HRESULT]
    AddPushButton: Callable[[int, str], HRESULT]
    AddCheckButton: Callable[[int, str, int], HRESULT]
    AddRadioButtonList: Callable[[int], HRESULT]
    AddComboBox: Callable[[int], HRESULT]
    AddControlItem: Callable[[int, int, str], HRESULT]
    AddEditBox: Callable[[int, str], HRESULT]
    AddSeparator: Callable[[int], HRESULT]
    AddMenu: Callable[[int, str], HRESULT]
    SetControlLabel: Callable[[int, str], HRESULT]
    SetControlState: Callable[[int, int], HRESULT]
    SetCheckButtonState: Callable[[int, int], HRESULT]
    GetCheckButtonState: Callable[[int], int]
    SetEditBoxText: Callable[[int, str], HRESULT]
    GetEditBoxText: Callable[[int], LPCWSTR]
    SetControlItemText: Callable[[int, int, str], HRESULT]
    GetControlItemState: Callable[[int, int], int]
    SetControlItemState: Callable[[int, int, int], HRESULT]
    GetSelectedControlItem: Callable[[int], int]
    SetSelectedControlItem: Callable[[int, int], HRESULT]
    StartVisualGroup: Callable[[int, str], HRESULT]
    EndVisualGroup: Callable[[int], HRESULT]
    MakeProminent: Callable[[int], HRESULT]
    RemoveControlItem: Callable[[int, int], HRESULT]
    RemoveAllControlItems: Callable[[int], HRESULT]
    GetControlState: Callable[[int], int]


class IFileDialogControlEvents(IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IFileDialogControlEvents
    _methods_: ClassVar[list[_ComMemberSpec]] = [
        COMMETHOD(
            [],
            HRESULT,
            "OnItemSelected",
            (["in"], comtypes.POINTER(IFileDialogCustomize), "pfdc"),
            (["in"], c_int, "dwIDCtl"),
            (["in"], c_int, "dwIDItem"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "OnButtonClicked",
            (["in"], comtypes.POINTER(IFileDialogCustomize), "pfdc"),
            (["in"], c_int, "dwIDCtl"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "OnCheckButtonToggled",
            (["in"], comtypes.POINTER(IFileDialogCustomize), "pfdc"),
            (["in"], c_int, "dwIDCtl"),
            (["in"], c_bool, "bChecked"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "OnControlActivating",
            (["in"], comtypes.POINTER(IFileDialogCustomize), "pfdc"),
            (["in"], c_int, "dwIDCtl"),
        ),
    ]
    OnButtonClicked: Callable[[IFileDialogCustomize, c_uint], HRESULT]
    OnCheckButtonToggled: Callable[[IFileDialogCustomize, c_uint, c_int], HRESULT]
    OnControlActivating: Callable[[IFileDialogCustomize, c_uint], HRESULT]
    OnItemSelected: Callable[[IFileDialogCustomize, c_uint, c_uint], HRESULT]
