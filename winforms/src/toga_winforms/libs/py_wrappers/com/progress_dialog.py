from __future__ import annotations

import errno
import os
from pathlib import WindowsPath
from typing import TYPE_CHECKING

import comtypes
from comtypes.client import CreateObject
from comtypes.gen import Shell32
from utility.logger_util import RobustRootLogger

from toga_winforms.libs.win_wrappers.com.interfaces import (
    CLSID_FileOperation,
    IFileOperationProgressSink,
)
from toga_winforms.libs.win_wrappers.hresult import S_OK

if TYPE_CHECKING:
    from typing_extensions import Literal


class FileOperationProgressSinkImpl(IFileOperationProgressSink):
    def StartOperations(self):
        print("Operation started")
        return S_OK

    def FinishOperations(self, hr):
        print("Operation finished with hr:", hr)
        return S_OK

    def PreRenameItem(self, dwFlags, psiItem, pszNewName):
        print(f"Preparing to rename item {psiItem.GetDisplayName()} to {pszNewName}")
        return S_OK

    def PostRenameItem(self, dwFlags, psiItem, pszNewName, hrRename, psiNewlyCreated):
        print(f"Renamed item {psiItem.GetDisplayName()} to {pszNewName}")
        return S_OK

    def PreMoveItem(self, dwFlags, psiItem, psiDestinationFolder, pszNewName):
        print(f"Preparing to move item {psiItem.GetDisplayName()} to {pszNewName}")
        return S_OK

    def PostMoveItem(self, dwFlags, psiItem, psiDestinationFolder, pszNewName, hrMove, psiNewlyCreated):
        print(f"Moved item {psiItem.GetDisplayName()} to {pszNewName}")
        return S_OK

    def PreCopyItem(self, dwFlags, psiItem, psiDestinationFolder, pszNewName):
        print(f"Preparing to copy item {psiItem.GetDisplayName()} to {pszNewName}")
        return S_OK

    def PostCopyItem(self, dwFlags, psiItem, psiDestinationFolder, pszNewName, hrCopy, psiNewlyCreated):
        print(f"Copied item {psiItem.GetDisplayName()} to {pszNewName}")
        return S_OK

    def PreDeleteItem(self, dwFlags, psiItem):
        print(f"Preparing to delete item {psiItem.GetDisplayName()}")
        return S_OK

    def PostDeleteItem(self, dwFlags, psiItem, hrDelete, psiNewlyCreated):
        print(f"Deleted item {psiItem.GetDisplayName()}")
        return S_OK

    def PreNewItem(self, dwFlags, psiDestinationFolder, pszNewName):
        print(f"Preparing to create new item {pszNewName}")
        return S_OK

    def PostNewItem(self, dwFlags, psiDestinationFolder, pszNewName, pszTemplateName, dwFileAttributes, hrNew, psiNewItem):
        print(f"Created new item {pszNewName}")
        return S_OK

    def UpdateProgress(self, iWorkTotal, iWorkSoFar):
        print(f"Progress: {iWorkSoFar}/{iWorkTotal}")
        return S_OK

    def ResetTimer(self):
        print("Timer reset")
        return S_OK

    def PauseTimer(self):
        print("Timer paused")
        return S_OK

    def ResumeTimer(self):
        print("Timer resumed")
        return S_OK

def initialize_com():
    comtypes.CoInitialize()

def uninitialize_com():
    comtypes.CoUninitialize()

def create_shell_item(path_obj):
    path = WindowsPath(path_obj).resolve()
    if not path.exists():
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), str(path))
    shell = CreateObject(Shell32.Shell, interface=Shell32.IShellDispatch4)
    folder = shell.NameSpace(str(path.parent))
    item = folder.ParseName(path.name)
    return item.QueryInterface(Shell32.IShellItem)

def perform_file_operation(
    source: os.PathLike | str,
    destination: os.PathLike | str,
    operation: Literal["copy", "move"] = "copy",
):
    initialize_com()
    source_path = source
    destination_path = destination

    try:
        file_operation = CreateObject(CLSID_FileOperation, interface=Shell32.IFileOperation)

        source_item = create_shell_item(source_path)
        dest_item = create_shell_item(destination_path)

        progress_sink = FileOperationProgressSinkImpl()
        file_operation.Advise(progress_sink, None)

        file_operation.SetOperationFlags(Shell32.FOF_NOCONFIRMATION | Shell32.FOF_SILENT)

        if operation == "copy":
            file_operation.CopyItem(source_item, dest_item, None, None)
        elif operation == "move":
            file_operation.MoveItem(source_item, dest_item, None, None)
        elif operation == "delete":
            file_operation.DeleteItem(source_item, None)
        else:
            raise ValueError(f"Unsupported operation: {operation}")  # noqa: TRY301

        result = file_operation.PerformOperations()
        if result != 0:
            raise comtypes.COMError(result, "Error performing file operation", None)  # noqa: TRY301

        print(f"File operation {operation} from {source_path} to {destination_path} completed")

    except Exception as e:  # noqa: BLE001
        RobustRootLogger().exception(f"General error while attempting to perform file operations with the com objects: {e.__class__.__name__}: {e}")

    finally:
        uninitialize_com()

# Example usage
if __name__ == "__main__":
    source_path = r"C:\path\to\source\file.txt"
    destination_path = r"C:\path\to\destination\folder"

    perform_file_operation(source_path, destination_path, operation="copy")
