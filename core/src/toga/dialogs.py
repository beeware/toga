from __future__ import annotations

import asyncio
from pathlib import Path
from typing import TYPE_CHECKING

from toga.platform import get_platform_factory

if TYPE_CHECKING:
    from toga.window import Window


__all__ = [
    "InfoDialog",
    "QuestionDialog",
    "ConfirmDialog",
    "ErrorDialog",
    "StackTraceDialog",
    "SaveFileDialog",
    "OpenFileDialog",
    "SelectFolderDialog",
]


class Dialog:
    """A base class for dialogs.

    These classes are not displayed directly. To use them, pass a
    :class:`~toga.dialogs.Dialog` instance to :meth:`~toga.Window.dialog()` (for a
    window-modal dialog), or :meth:`~toga.App.dialog()` for an app-level dialog.
    """

    def _show(self, window: Window | None) -> asyncio.Future:
        """Display the dialog and return the user's response.

        :param window: The window for which the dialog should be modal; or ``None`` for
            an app-level dialog.
        :returns: A future capturing the user's response to the dialog
        """
        future = asyncio.Future()
        self._impl.show(window, future)
        return future


class InfoDialog(Dialog):
    def __init__(self, title: str, message: str):
        """Ask the user to acknowledge some information.

        Presents as a dialog with a single "OK" button to close the dialog.

        Returns a response of ``None``.

        :param title: The title of the dialog window.
        :param message: The message to display.
        """
        self.factory = get_platform_factory()
        self._impl = self.factory.dialogs.InfoDialog(title=title, message=message)


class QuestionDialog(Dialog):
    def __init__(self, title: str, message: str):
        """Ask the user a yes/no question.

        Presents as a dialog with "Yes" and "No" buttons.

        Returns a response of ``True`` when the "Yes" button is pressed, ``False`` when
        the "No" button is pressed.

        :param title: The title of the dialog window.
        :param message: The question to be answered.
        """
        self.factory = get_platform_factory()
        self._impl = self.factory.dialogs.QuestionDialog(title=title, message=message)


class ConfirmDialog(Dialog):
    def __init__(self, title: str, message: str):
        """Ask the user to confirm if they wish to proceed with an action.

        Presents as a dialog with "Cancel" and "OK" buttons (or whatever labels are
        appropriate on the current platform).

        Returns a response of ``True`` when the "OK" button is pressed, ``False`` when
        the "Cancel" button is pressed.

        :param title: The title of the dialog window.
        :param message: A message describing the action to be confirmed.
        """
        self.factory = get_platform_factory()
        self._impl = self.factory.dialogs.ConfirmDialog(title=title, message=message)


class ErrorDialog(Dialog):
    def __init__(self, title: str, message: str):
        """Ask the user to acknowledge an error state.

        Presents as an error dialog with an "OK" button to close the dialog.

        Returns a response of ``None``.

        :param title: The title of the dialog window.
        :param message: The error message to display.
        """
        self.factory = get_platform_factory()
        self._impl = self.factory.dialogs.ErrorDialog(title=title, message=message)


class StackTraceDialog(Dialog):
    def __init__(self, title: str, message: str, content: str, retry: bool = False):
        """Open a dialog to display a large block of text, such as a stack trace.

        If ``retry`` is true, returns a response of ``True`` when the user selects
        "Retry", and ``False`` when they select "Quit".

        If ``retry`` is ``False``, returns a response of ``None``.

        :param title: The title of the dialog window.
        :param message: Contextual information about the source of the stack trace.
        :param content: The stack trace, pre-formatted as a multi-line string.
        :param retry: If true, the user will be given options to "Retry" or "Quit"; if
            false, a single option to acknowledge the error will be displayed.
        """
        self.factory = get_platform_factory()
        self._impl = self.factory.dialogs.StackTraceDialog(
            title=title,
            message=message,
            content=content,
            retry=retry,
        )


class SaveFileDialog(Dialog):
    def __init__(
        self,
        title: str,
        suggested_filename: Path | str,
        file_types: list[str] | None = None,
    ):
        """Prompt the user for a location to save a file.

        This dialog is not currently supported on Android or iOS.

        Returns a path object for the selected file location, or ``None`` if the user
        cancelled the save operation.

        If the filename already exists, the user will be prompted to confirm they want
        to overwrite the existing file.

        :param title: The title of the dialog window
        :param suggested_filename: The initial suggested filename
        :param file_types: The allowed filename extensions, without leading dots. If not
            provided, any extension will be allowed.
        """
        # Convert suggested filename to a path (if it isn't already),
        # and break it into a filename and a directory
        suggested_path = Path(suggested_filename)
        initial_directory: Path | None = suggested_path.parent
        if initial_directory == Path("."):
            initial_directory = None
        filename = suggested_path.name

        self.factory = get_platform_factory()
        self._impl = self.factory.dialogs.SaveFileDialog(
            title=title,
            filename=filename,
            initial_directory=initial_directory,
            file_types=file_types,
        )


class OpenFileDialog(Dialog):
    def __init__(
        self,
        title: str,
        initial_directory: Path | str | None = None,
        file_types: list[str] | None = None,
        multiple_select: bool = False,
    ):
        """Prompt the user to select a file (or files) to open.

        This dialog is not currently supported on Android or iOS.

        If ``multiple_select`` is ``True``, returns a list of ``Path`` objects.

        If ``multiple_select`` is ``False``, returns a single ``Path``.

        Returns ``None`` if the open operation is cancelled by the user.

        :param title: The title of the dialog window
        :param initial_directory: The initial folder in which to open the dialog. If
            ``None``, use the default location provided by the operating system (which
            will often be the last used location)
        :param file_types: The allowed filename extensions, without leading dots. If not
            provided, all files will be shown.
        :param multiple_select: If True, the user will be able to select multiple files;
            if False, the selection will be restricted to a single file.
        """
        self.factory = get_platform_factory()
        self._impl = self.factory.dialogs.OpenFileDialog(
            title=title,
            initial_directory=Path(initial_directory) if initial_directory else None,
            file_types=file_types,
            multiple_select=multiple_select,
        )


class SelectFolderDialog(Dialog):
    def __init__(
        self,
        title: str,
        initial_directory: Path | str | None = None,
        multiple_select: bool = False,
    ):
        """Prompt the user to select a directory (or directories).

        This dialog is not currently supported on Android or iOS.

        If ``multiple_select`` is ``True``, returns a list of ``Path`` objects.

        If ``multiple_select`` is ``False``, returns a single ``Path``.

        Returns ``None`` if the select operation is cancelled by the user.

        :param title: The title of the dialog window
        :param initial_directory: The initial folder in which to open the dialog. If
            ``None``, use the default location provided by the operating system (which
            will often be "last used location")
        :param multiple_select: If True, the user will be able to select multiple
            directories; if False, the selection will be restricted to a single
            directory. This option is not supported on WinForms.
        """
        self.factory = get_platform_factory()
        self._impl = self.factory.dialogs.SelectFolderDialog(
            title=title,
            initial_directory=Path(initial_directory) if initial_directory else None,
            multiple_select=multiple_select,
        )
