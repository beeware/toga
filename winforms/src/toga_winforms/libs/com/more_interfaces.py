from __future__ import annotations

from ctypes import HRESULT, POINTER as C_POINTER, c_bool, c_int, c_uint
from ctypes.wintypes import LPCWSTR, ULONG
from typing import TYPE_CHECKING, Callable, ClassVar

from comtypes import COMMETHOD, GUID, IUnknown

from toga_winforms.libs.com.identifiers import (
    IID_IFileDialogControlEvents,
    IID_IFileDialogCustomize,
    IID_IFileDialogEvents,
)
from toga_winforms.libs.com.interfaces import IFileDialog, IShellItem

if TYPE_CHECKING:

    from comtypes._memberspec import _ComMemberSpec


class IFileDialogEvents(IUnknown):
    _case_insensitive_: bool = True
    _iid_: GUID = IID_IFileDialogEvents
    _methods_: ClassVar[list[_ComMemberSpec]] = [  # noqa: SLF001
        COMMETHOD([], HRESULT, "OnFileOk", (["in"], C_POINTER(IFileDialog), "pfd")),
        COMMETHOD(
            [],
            HRESULT,
            "OnFolderChanging",
            (["in"], C_POINTER(IFileDialog), "pfd"),
            (["in"], C_POINTER(IShellItem), "psiFolder"),
        ),
        COMMETHOD(
            [], HRESULT, "OnFolderChange", (["in"], C_POINTER(IFileDialog), "pfd")
        ),
        COMMETHOD(
            [], HRESULT, "OnSelectionChange", (["in"], C_POINTER(IFileDialog), "pfd")
        ),
        COMMETHOD(
            [],
            HRESULT,
            "OnShareViolation",
            (["in"], C_POINTER(IFileDialog), "pfd"),
            (["in"], C_POINTER(IShellItem), "psi"),
            (["out"], C_POINTER(c_int), "pResponse"),
        ),
        COMMETHOD([], HRESULT, "OnTypeChange", (["in"], C_POINTER(IFileDialog), "pfd")),
        COMMETHOD(
            [],
            HRESULT,
            "OnOverwrite",
            (["in"], C_POINTER(IFileDialog), "pfd"),
            (["in"], C_POINTER(IShellItem), "psi"),
            (["out"], C_POINTER(c_int), "pResponse"),
        ),
    ]
    QueryInterface: Callable[[GUID, IUnknown], int]
    AddRef: Callable[[], ULONG]
    Release: Callable[[], ULONG]
    OnFileOk: Callable[[IFileDialog], int]
    OnFolderChanging: Callable[[IFileDialog, IShellItem], int]
    OnFolderChange: Callable[[IFileDialog], int]
    OnSelectionChange: Callable[[IFileDialog], int]
    OnShareViolation: Callable[[IFileDialog, IShellItem, c_int], int]
    OnTypeChange: Callable[[IFileDialog], int]
    OnOverwrite: Callable[[IFileDialog, IShellItem, c_int], int]


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
            (["out"], C_POINTER(c_int), "pbChecked"),
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
            (["out"], C_POINTER(LPCWSTR), "ppszText"),
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
            (["out"], C_POINTER(c_int), "pdwState"),
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
            (["out"], C_POINTER(c_uint), "pdwIDItem"),
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
            (["out"], C_POINTER(c_int), "pdwState"),
        ),
    ]
    EnableOpenDropDown: Callable[[int], int]
    AddText: Callable[[int, str], int]
    AddPushButton: Callable[[int, str], int]
    AddCheckButton: Callable[[int, str, int], int]
    AddRadioButtonList: Callable[[int], int]
    AddComboBox: Callable[[int], int]
    AddControlItem: Callable[[int, int, str], int]
    AddEditBox: Callable[[int, str], int]
    AddSeparator: Callable[[int], int]
    AddMenu: Callable[[int, str], int]
    SetControlLabel: Callable[[int, str], int]
    SetControlState: Callable[[int, int], int]
    SetCheckButtonState: Callable[[int, int], int]
    GetCheckButtonState: Callable[[int], int]
    SetEditBoxText: Callable[[int, str], int]
    GetEditBoxText: Callable[[int], LPCWSTR]
    SetControlItemText: Callable[[int, int, str], int]
    GetControlItemState: Callable[[int, int], int]
    SetControlItemState: Callable[[int, int, int], int]
    GetSelectedControlItem: Callable[[int], int]
    SetSelectedControlItem: Callable[[int, int], int]
    StartVisualGroup: Callable[[int, str], int]
    EndVisualGroup: Callable[[int], int]
    MakeProminent: Callable[[int], int]
    RemoveControlItem: Callable[[int, int], int]
    RemoveAllControlItems: Callable[[int], int]
    GetControlState: Callable[[int], int]


class IFileDialogControlEvents(IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IFileDialogControlEvents
    _methods_: ClassVar[list[_ComMemberSpec]] = [
        COMMETHOD(
            [],
            HRESULT,
            "OnItemSelected",
            (["in"], C_POINTER(IFileDialogCustomize), "pfdc"),
            (["in"], c_int, "dwIDCtl"),
            (["in"], c_int, "dwIDItem"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "OnButtonClicked",
            (["in"], C_POINTER(IFileDialogCustomize), "pfdc"),
            (["in"], c_int, "dwIDCtl"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "OnCheckButtonToggled",
            (["in"], C_POINTER(IFileDialogCustomize), "pfdc"),
            (["in"], c_int, "dwIDCtl"),
            (["in"], c_bool, "bChecked"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "OnControlActivating",
            (["in"], C_POINTER(IFileDialogCustomize), "pfdc"),
            (["in"], c_int, "dwIDCtl"),
        ),
    ]
    OnButtonClicked: Callable[[IFileDialogCustomize, c_uint], int]
    OnCheckButtonToggled: Callable[[IFileDialogCustomize, c_uint, c_int], int]
    OnControlActivating: Callable[[IFileDialogCustomize, c_uint], int]
    OnItemSelected: Callable[[IFileDialogCustomize, c_uint, c_uint], int]
