from __future__ import annotations

from contextlib import contextmanager
from ctypes import POINTER, PyDLL, byref, c_void_p, py_object
from ctypes.wintypes import BOOL
from typing import TYPE_CHECKING

from comtypes import COMObject

from toga_winforms.libs.py_wrappers.hresult import HRESULT

if TYPE_CHECKING:
    from ctypes import _NamedFuncPointer

    from _win32typing import (  # pyright: ignore[reportMissingModuleSource]
        PyIBindCtx,
        PyIUnknown,
    )
    from comtypes import IUnknown


@contextmanager
def HandleCOMCall(action_desc: str = "Unspecified COM function"):
    """
    Context manager for handling COM function calls.

    This function facilitates the execution of COM calls by providing a mechanism to manage errors effectively.
    It yields a callable that checks the result of the COM operation and raises exceptions if the result
    indicates an error.

    Args:
        action_desc (str): A description of the COM function being called. Defaults to "Unspecified COM function".

    Returns:
        Callable: A function that takes an HRESULT value and raises an exception if the value indicates an error.

    Raises:
        HRESULT: If an error occurs during the COM call, an HRESULT exception is raised with a descriptive message.

    Examples:
        with HandleCOMCall("My COM Function") as check_hr:
            hr = some_com_function()
            check_hr(hr)
    """

    print(f"Attempt to call COM func {action_desc}")
    try:
        from comtypes import (
            COMError,  # pyright: ignore[reportMissingTypeStubs, reportMissingModuleSource]
        )
    except ImportError:
        COMError = OSError
    future_error_msg = f"An error has occurred in win32 COM function '{action_desc}'"
    try:  # sourcery skip: raise-from-previous-error
        # Yield back a callable function that will raise if hr is nonzero.
        yield lambda hr: HRESULT(hr).raise_for_status(hr, future_error_msg) and hr or hr
    except (COMError, OSError) as e:
        errcode = getattr(e, "winerror", getattr(e, "hresult", None))
        if errcode is None:
            raise
        raise HRESULT(errcode).exception(future_error_msg)  # noqa: B904  # pyright: ignore[reportAttributeAccessIssue]


def comtypes2pywin(
    ptr: COMObject,
    interface: type[IUnknown] | None = None,
) -> PyIUnknown:
    """Convert a comtypes pointer 'ptr' into a pythoncom
    PyI<interface> object.

    'interface' specifies the interface we want; it must be a comtypes
    interface class.  The interface must be implemented by the object;
    and the interface must be known to pythoncom.

    If 'interface' is specified, comtypes.IUnknown is used.
    """
    import comtypes  # pyright: ignore[reportMissingTypeStubs, reportMissingModuleSource]
    import pythoncom
    if interface is None:
        interface = comtypes.IUnknown
    # ripped from
    # https://github.com/enthought/comtypes/blob/main/comtypes/test/test_win32com_interop.py
    # We use the PyCom_PyObjectFromIUnknown function in pythoncomxxx.dll to
    # convert a comtypes COM pointer into a pythoncom COM pointer.
    # This is the C prototype; we must pass 'True' as third argument:
    # PyObject *PyCom_PyObjectFromIUnknown(IUnknown *punk, REFIID riid, BOOL bAddRef)
    _PyCom_PyObjectFromIUnknown: _NamedFuncPointer = PyDLL(pythoncom.__file__).PyCom_PyObjectFromIUnknown
    _PyCom_PyObjectFromIUnknown.restype = py_object
    _PyCom_PyObjectFromIUnknown.argtypes = (POINTER(comtypes.IUnknown), c_void_p, BOOL)
    return _PyCom_PyObjectFromIUnknown(ptr, byref(interface._iid_), True)  # noqa: FBT003, SLF001


def register_idispatch_object(
    com_object: COMObject,
    name: str,
    interface: type[IUnknown] | None = None,
) -> PyIBindCtx:
    import pythoncom
    ctx: PyIBindCtx = pythoncom.CreateBindCtx()
    py_data: PyIUnknown = comtypes2pywin(com_object, interface)
    ctx.RegisterObjectParam(name, py_data)
    return ctx


if __name__ == "__main__":
    # Small test.
    from ctypes.wintypes import WIN32_FIND_DATAW
    from typing import TYPE_CHECKING, ClassVar, Sequence

    import comtypes
    from comtypes import GUID

    from toga_winforms.libs.py_wrappers.com.interfaces import SIGDN
    from toga_winforms.libs.py_wrappers.hresult import S_OK
    try:
        from win32com.shell import shell  # pyright: ignore[reportMissingModuleSource]
    except ModuleNotFoundError:
        raise RuntimeError("Small test requires `pip install pipwin32`")

    if TYPE_CHECKING:
        from ctypes import _CArgObject, _Pointer

        from _win32typing import (
            PyIShellItem,  # pyright: ignore[reportMissingModuleSource]
        )
        from comtypes._memberspec import (
            _ComMemberSpec,  # pyright: ignore[reportMissingTypeStubs]
        )
        from typing_extensions import Self
    IID_IFileSystemBindData = GUID("{01e18d10-4d8b-11d2-855d-006008059367}")

    class IFileSystemBindData(comtypes.IUnknown):
        """The IFileSystemBindData interface
        https://learn.microsoft.com/en-us/windows/win32/api/shobjidl_core/nn-shobjidl_core-ifilesystembinddata.
        """
        _iid_ = IID_IFileSystemBindData
        _methods_: ClassVar[list[_ComMemberSpec]] = [
            comtypes.COMMETHOD([], HRESULT, "SetFindData",
                    (["in"], POINTER(WIN32_FIND_DATAW), "pfd")),
            comtypes.COMMETHOD([], HRESULT, "GetFindData",
                    (["out"], POINTER(WIN32_FIND_DATAW), "pfd"))
        ]

    class FileSystemBindData(comtypes.COMObject):
        """Implements the IFileSystemBindData interface:
        https://learn.microsoft.com/en-us/windows/win32/api/shobjidl_core/nn-shobjidl_core-ifilesystembinddata.
        """
        _com_interfaces_: Sequence[type[comtypes.IUnknown]] = [IFileSystemBindData]

        def IFileSystemBindData_SetFindData(self: Self, this: Self, pfd: _Pointer | _CArgObject) -> HRESULT:
            self.pfd: _Pointer = pfd  # pyright: ignore[reportAttributeAccessIssue]
            return S_OK

        def IFileSystemBindData_GetFindData(self: Self, this: Self, pfd: _Pointer | _CArgObject) -> HRESULT:
            return S_OK
    find_data = WIN32_FIND_DATAW()  # from wintypes
    bind_data: FileSystemBindData = FileSystemBindData()  # pyright: ignore[reportAssignmentType]
    bind_data.IFileSystemBindData_SetFindData(bind_data, byref(find_data))
    ctx: PyIBindCtx = register_idispatch_object(bind_data, "File System Bind Data")

    item: PyIShellItem = shell.SHCreateItemFromParsingName(
        r"Z:\blah\blah", ctx, shell.IID_IShellItem2)
    print(item.GetDisplayName(SIGDN.SIGDN_DESKTOPABSOLUTEPARSING))  # prints Z:\blah\blah
