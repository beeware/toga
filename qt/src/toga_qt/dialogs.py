import os.path
from pathlib import Path
from warnings import warn

from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox


class MessageDialog:
    def __init__(self, title, message, icon, buttons=QMessageBox.Ok, detail=None):
        self.title, self.message, self.icon, self.buttons, self.detail = (
            title,
            message,
            icon,
            buttons,
            detail,
        )
        # Note: The parent of the dialog must be passed in at creation time.
        # Therefore, the native must be initially None.
        self.native = None

    def show(self, parent, future):
        self.future = future
        if parent is not None:
            self.native = QMessageBox(parent._impl.native)
        else:
            self.native = QMessageBox()
        self.native.setIcon(self.icon)
        self.native.setWindowTitle(self.title)
        self.native.setText(self.message)
        if self.detail is not None:
            self.native.setDetailedText(self.detail)
        self.native.setStandardButtons(self.buttons)
        self.native.finished.connect(self.qt_finished)
        self.native.open()

    def qt_finished(self, result):
        self.future.set_result(self._get_result(result))
        self.native.deleteLater()
        self.native = None

    def _get_result(self, result):
        return None


class InfoDialog(MessageDialog):
    def __init__(self, title, message):
        super().__init__(
            title=title,
            message=message,
            icon=QMessageBox.Icon.Information,
        )


class QuestionDialog(MessageDialog):
    def __init__(self, title, message):
        super().__init__(
            title=title,
            message=message,
            icon=QMessageBox.Icon.Question,
            buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

    def _get_result(self, result):
        return result == QMessageBox.StandardButton.Yes


class ConfirmDialog(MessageDialog):
    def __init__(self, title, message):
        super().__init__(
            title=title,
            message=message,
            icon=QMessageBox.Icon.Question,
            buttons=QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
        )

    def _get_result(self, result):
        return result == QMessageBox.StandardButton.Ok


class ErrorDialog(MessageDialog):
    def __init__(self, title, message):
        super().__init__(
            title=title,
            message=message,
            icon=QMessageBox.Icon.Critical,
        )


class StackTraceDialog(MessageDialog):
    def __init__(self, title, message, content, retry=False):
        if retry:
            buttons = (
                QMessageBox.StandardButton.Retry | QMessageBox.StandardButton.Cancel
            )
        else:
            buttons = QMessageBox.StandardButton.Ok
        super().__init__(
            title=title,
            message=message,
            icon=QMessageBox.Icon.Critical,
            buttons=buttons,
        )
        self.retry = retry

    def _get_result(self, result):
        if self.retry:
            return result == QMessageBox.StandardButton.Retry
        else:
            return None


class FileDialog:
    def __init__(
        self,
        title: str,
        filename: str | None = None,
        initial_directory: Path | None = None,
        file_types: list[str] | None = None,
        accept_mode=QFileDialog.AcceptMode.AcceptOpen,
        file_mode=QFileDialog.FileMode.AnyFile,
    ) -> None:
        self.title = title
        self.filename = filename
        self.initial_directory = initial_directory
        self.file_types = file_types
        self.multiple_select = file_types
        self.file_mode = file_mode
        self.accept_mode = accept_mode

    def show(self, parent, future):
        self.future = future
        if parent is not None:
            self.native = QFileDialog(parent._impl.native)
        else:
            self.native = QFileDialog()
        self.native.setWindowTitle(self.title)
        if self.initial_directory is not None:
            self.native.setDirectory(str(self.initial_directory))
        if self.filename:
            self.native.selectFile(self.filename)
            self.native.setDefaultSuffix(os.path.splitext(self.filename)[1])
        if self.file_types:
            self.native.setNameFilter(
                " ".join(f"*.{file_type}" for file_type in self.file_types)
            )
            if not self.filename:
                self.native.setDefaultSuffix(self.file_types[0])
        self.native.setAcceptMode(self.accept_mode)
        self.native.setFileMode(self.file_mode)
        self.native.finished.connect(self.qt_finished)
        self.native.open()

    def qt_finished(self, result):
        self.future.set_result(self._get_result(result))
        self.native.deleteLater()
        self.native = None

    def _get_result(self, result):
        if result == QDialog.DialogCode.Accepted:
            if self.native.fileMode() == QFileDialog.FileMode.ExistingFiles:
                return [Path(file) for file in self.native.selectedFiles()]
            elif self.native.selectedFiles():
                return Path(self.native.selectedFiles()[0])

        return None


class SaveFileDialog(FileDialog):
    def __init__(
        self,
        title: str,
        filename: str,
        initial_directory: Path | None,
        file_types: list[str] | None = None,
    ) -> None:
        super().__init__(
            title=title,
            filename=filename,
            initial_directory=initial_directory,
            file_types=file_types,
            accept_mode=QFileDialog.AcceptMode.AcceptSave,
            file_mode=QFileDialog.FileMode.AnyFile,
        )


class OpenFileDialog(FileDialog):
    def __init__(
        self,
        title: str,
        initial_directory: Path | None,
        file_types: list[str] | None = None,
        multiple_select: bool = False,
    ) -> None:
        file_mode = (
            QFileDialog.FileMode.ExistingFiles
            if multiple_select
            else QFileDialog.FileMode.ExistingFile
        )
        super().__init__(
            title=title,
            initial_directory=initial_directory,
            file_types=file_types,
            accept_mode=QFileDialog.AcceptMode.AcceptOpen,
            file_mode=file_mode,
        )


class SelectFolderDialog(FileDialog):
    def __init__(
        self,
        title: str,
        initial_directory: Path | None,
        file_types: list[str] | None = None,
        multiple_select: bool = False,
    ) -> None:
        if multiple_select:
            warn(
                "Qt backend does not support multiple_selection of folders",
                RuntimeWarning,
                stacklevel=2,
            )
        super().__init__(
            title=title,
            initial_directory=initial_directory,
            file_types=file_types,
            accept_mode=QFileDialog.AcceptMode.AcceptOpen,
            file_mode=QFileDialog.FileMode.Directory,
        )
