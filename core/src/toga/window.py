from __future__ import annotations

import warnings
from builtins import id as identifier
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, Protocol, TypeVar, overload

from toga.command import CommandSet
from toga.handlers import AsyncResult, wrapped_handler
from toga.platform import get_platform_factory
from toga.widgets.base import WidgetRegistry

if TYPE_CHECKING:
    from toga.app import App
    from toga.widgets.base import Widget


class OnCloseHandler(Protocol):
    def __call__(self, window: Window, **kwargs: Any) -> bool:
        """A handler to invoke when a window is about to close.

        The return value of this callback controls whether the window is allowed to close.
        This can be used to prevent a window closing with unsaved changes, etc.

        .. note::
            ``**kwargs`` ensures compatibility with additional arguments
            introduced in future versions.

        :param window: The window instance that is closing.
        :returns: ``True`` if the window is allowed to close; ``False`` if the window is not
            allowed to close.
        """
        ...


T = TypeVar("T")


class DialogResultHandler(Protocol[T]):
    def __call__(self, window: Window, result: T, **kwargs: Any) -> None:
        """A handler to invoke when a dialog is closed.

        .. note::
            ``**kwargs`` ensures compatibility with additional arguments
            introduced in future versions.

        :param window: The window that opened the dialog.
        :param result: The result returned by the dialog.
        """
        ...


class Dialog(AsyncResult):
    RESULT_TYPE = "dialog"

    def __init__(self, window: Window):
        super().__init__()
        self.window = window
        self.app = window.app


class Window:
    """The top level container of an application.

    Args:
        id: The ID of the window.
        title: Title for the window.
        position: Position of the window, as x,y coordinates.
        size:  Size of the window, as (width, height) sizes, in pixels.
        toolbar: (Deprecated, will have no effect)
        resizeable: Toggle if the window is resizable by the user.
        closeable: Toggle if the window is closable by the user.
        minimizable: Toggle if the window is minimizable by the user.
        on_close: A callback to invoke when the user makes a request to close the window.
    """

    _WINDOW_CLASS = "Window"

    def __init__(
        self,
        id: str | None = None,
        title: str | None = None,
        position: tuple[int, int] = (100, 100),
        size: tuple[int, int] = (640, 480),
        toolbar: list[Widget | None] = None,
        resizeable: bool = True,
        closeable: bool = True,
        minimizable: bool = True,
        factory: None = None,  # DEPRECATED !
        on_close: OnCloseHandler | None = None,
    ) -> None:
        ######################################################################
        # 2022-09: Backwards compatibility
        ######################################################################
        # factory no longer used
        if factory:
            warnings.warn("The factory argument is no longer used.", DeprecationWarning)
        ######################################################################
        # End backwards compatibility.
        ######################################################################

        self.widgets = WidgetRegistry()

        self._id = str(id if id else identifier(self))
        self._impl = None
        self._app = None
        self._content = None
        self._is_full_screen = False

        self.resizeable = resizeable
        self.closeable = closeable
        self.minimizable = minimizable

        self.factory = get_platform_factory()
        self._impl = getattr(self.factory, self._WINDOW_CLASS)(
            interface=self,
            title="Toga" if title is None else title,
            position=position,
            size=size,
        )

        self._toolbar = CommandSet(widget=self, on_change=self._impl.create_toolbar)

        self.on_close = on_close

    @property
    def id(self) -> str:
        """The DOM identifier for the window.

        This id can be used to target CSS directives.
        """
        return self._id

    @property
    def app(self) -> App | None:
        """Instance of the :class:`toga.App` that this window belongs to.

        Returns:
            The app that it belongs to :class:`toga.App`.

        Raises:
            Exception: If the window already is associated with another app.
        """
        return self._app

    @app.setter
    def app(self, app: App) -> None:
        if self._app:
            raise Exception("Window is already associated with an App")

        self._app = app
        self._impl.set_app(app._impl)

        if self.content:
            self.content.app = app

    @property
    def title(self) -> str:
        """Title of the window. If no title is given it defaults to ``"Toga"``."""
        return self._impl.get_title()

    @title.setter
    def title(self, title: str) -> None:
        if not title:
            title = "Toga"

        self._impl.set_title(title)

    @property
    def toolbar(self) -> CommandSet:
        """Toolbar for the window."""
        return self._toolbar

    @property
    def content(self) -> Widget | None:
        """Content of the window. On setting, the content is added to the same app as
        the window and to the same app."""
        return self._content

    @content.setter
    def content(self, widget: Widget) -> None:
        # Set window of old content to None
        if self._content:
            self._content.window = None

        # Manifest the widget
        self._impl.clear_content()

        # Assign the content widget to the same app as the window.
        widget.app = self.app

        # Assign the content widget to the window.
        widget.window = self

        # Track our new content
        self._content = widget

        # Manifest the widget
        self._impl.set_content(widget._impl)

        # Update the geometry of the widget
        widget.refresh()

    @property
    def size(self) -> tuple[int, int]:
        """Size of the window, as a ``(width, height)`` tuple."""
        return self._impl.get_size()

    @size.setter
    def size(self, size: tuple[int, int]) -> None:
        self._impl.set_size(size)
        if self.content:
            self.content.refresh()

    @property
    def position(self) -> tuple[int, int]:
        """Position of the window, as an ``(x, y)`` tuple."""
        return self._impl.get_position()

    @position.setter
    def position(self, position: tuple[int, int]) -> None:
        self._impl.set_position(position)

    def show(self) -> None:
        """Show window, if hidden."""
        if self.app is None:
            raise AttributeError(
                "Can't show a window that doesn't have an associated app"
            )
        self._impl.show()

    def hide(self) -> None:
        """Hide window, if shown."""
        if self.app is None:
            raise AttributeError(
                "Can't hide a window that doesn't have an associated app"
            )
        self._impl.hide()

    @property
    def full_screen(self) -> bool:
        return self._is_full_screen

    @full_screen.setter
    def full_screen(self, is_full_screen: bool) -> None:
        self._is_full_screen = is_full_screen
        self._impl.set_full_screen(is_full_screen)

    @property
    def visible(self) -> bool:
        return self._impl.get_visible()

    @visible.setter
    def visible(self, visible: bool) -> None:
        if visible:
            self.show()
        else:
            self.hide()

    @property
    def on_close(self) -> OnCloseHandler:
        """The handler to invoke before the window is closed."""
        return self._on_close

    @on_close.setter
    def on_close(self, handler: OnCloseHandler | None) -> None:
        def cleanup(window: Window, should_close: bool) -> None:
            if should_close:
                window.close()

        self._on_close = wrapped_handler(self, handler, cleanup=cleanup)

    def close(self) -> None:
        self.app.windows -= self
        self._impl.close()

    ############################################################
    # Dialogs
    ############################################################

    def info_dialog(
        self,
        title: str,
        message: str,
        on_result: DialogResultHandler[None] | None = None,
    ) -> Dialog:
        """Ask the user to acknowledge some information.

        Presents as a dialog with a single 'OK' button to close the dialog.

        :param title: The title of the dialog window.
        :param message: The message to display.
        :param on_result: A callback that will be invoked when the user
            selects an option on the dialog.
        :returns: An awaitable Dialog object. The Dialog object returns
            ``None`` after the user pressed the 'OK' button.
        """
        dialog = Dialog(self)
        self.factory.dialogs.InfoDialog(
            dialog, title, message, on_result=wrapped_handler(self, on_result)
        )
        return dialog

    def question_dialog(
        self,
        title: str,
        message: str,
        on_result: DialogResultHandler[bool] | None = None,
    ) -> Dialog:
        """Ask the user a yes/no question.

        Presents as a dialog with a 'YES' and 'NO' button.

        :param title: The title of the dialog window.
        :param message: The question to be answered.
        :param on_result: A callback that will be invoked when the user
            selects an option on the dialog.
        :returns: An awaitable Dialog object. The Dialog object returns
            ``True`` when the 'YES' button was pressed, ``False`` when
            the 'NO' button was pressed.
        """
        dialog = Dialog(self)
        self.factory.dialogs.QuestionDialog(
            dialog, title, message, on_result=wrapped_handler(self, on_result)
        )
        return dialog

    def confirm_dialog(
        self,
        title: str,
        message: str,
        on_result: DialogResultHandler[bool] | None = None,
    ) -> Dialog:
        """Ask the user to confirm if they wish to proceed with an action.

        Presents as a dialog with 'Cancel' and 'OK' buttons (or whatever labels
        are appropriate on the current platform)

        :param title: The title of the dialog window.
        :param message: A message describing the action to be confirmed.
        :param on_result: A callback that will be invoked when the user
            selects an option on the dialog.
        :returns: An awaitable Dialog object. The Dialog object returns
            ``True`` when the 'OK' button was pressed, ``False`` when
            the 'CANCEL' button was pressed.
        """
        dialog = Dialog(self)
        self.factory.dialogs.ConfirmDialog(
            dialog, title, message, on_result=wrapped_handler(self, on_result)
        )
        return dialog

    def error_dialog(
        self,
        title: str,
        message: str,
        on_result: DialogResultHandler[None] | None = None,
    ) -> Dialog:
        """Ask the user to acknowledge an error state.

        Presents as an error dialog with a 'OK' button to close the dialog.

        :param title: The title of the dialog window.
        :param message: The error message to display.
        :param on_result: A callback that will be invoked when the user
            selects an option on the dialog.
        :returns: An awaitable Dialog object. The Dialog object returns
            ``None`` after the user pressed the 'OK' button.
        """
        dialog = Dialog(self)
        self.factory.dialogs.ErrorDialog(
            dialog, title, message, on_result=wrapped_handler(self, on_result)
        )
        return dialog

    @overload
    def stack_trace_dialog(
        self,
        title: str,
        message: str,
        content: str,
        retry: Literal[False] = False,
        on_result: DialogResultHandler[None] | None = None,
    ) -> Dialog:
        ...

    @overload
    def stack_trace_dialog(
        self,
        title: str,
        message: str,
        content: str,
        retry: Literal[True] = False,
        on_result: DialogResultHandler[bool] | None = None,
    ) -> Dialog:
        ...

    @overload
    def stack_trace_dialog(
        self,
        title: str,
        message: str,
        content: str,
        retry: bool = False,
        on_result: DialogResultHandler[bool | None] | None = None,
    ) -> Dialog:
        ...

    def stack_trace_dialog(
        self,
        title: str,
        message: str,
        content: str,
        retry: bool = False,
        on_result: DialogResultHandler[bool | None] | None = None,
    ) -> Dialog:
        """Open a dialog that allows to display a large text body, such as a stack
        trace.

        :param title: The title of the dialog window.
        :param message: Contextual information about the source of the stack trace.
        :param content: The stack trace, pre-formatted as a multi-line string.
        :param retry: A Boolean; if True, the user will be given a "Retry" and
            "Quit" option; if False, a single option to acknowledge the error will
            be displayed.
        :param on_result: A callback that will be invoked when the user
            selects an option on the dialog.
        :returns: An awaitable Dialog object. If retry is enabled, the Dialog object
            returns ``True`` if the user selected retry, and ``False`` otherwise;
            if retry is not enabled, the dialog object returns ``None``.
        """
        dialog = Dialog(self)
        self.factory.dialogs.StackTraceDialog(
            dialog,
            title,
            message,
            content=content,
            retry=retry,
            on_result=wrapped_handler(self, on_result),
        )
        return dialog

    def save_file_dialog(
        self,
        title: str,
        suggested_filename: Path | str,
        file_types: list[str] | None = None,
        on_result: DialogResultHandler[Path | None] | None = None,
    ) -> Dialog:
        """Prompt the user for a location to save a file.

        Presents the user a system-native "Save file" dialog.

        This opens a native dialog where the user can select a place to save a file.
        It is possible to suggest a filename and force the user to use a specific file extension.
        If no path is returned (e.g. dialog is canceled), a ValueError is raised.

        :param title: The title of the dialog window
        :param suggested_filename: A default filename
        :param file_types: A list of strings with the allowed file extensions.
        :param on_result: A callback that will be invoked when the user
            selects an option on the dialog.
        :returns: An awaitable Dialog object. The Dialog object returns
            a path object for the selected file location, or ``None`` if
            the user cancelled the save operation.
        """
        dialog = Dialog(self)
        # Convert suggested filename to a path (if it isn't already),
        # and break it into a filename and a directory
        suggested_path = Path(suggested_filename)
        initial_directory = suggested_path.parent
        if initial_directory == Path("."):
            initial_directory = None
        filename = suggested_path.name

        self.factory.dialogs.SaveFileDialog(
            dialog,
            title,
            filename=filename,
            initial_directory=initial_directory,
            file_types=file_types,
            on_result=wrapped_handler(self, on_result),
        )
        return dialog

    @overload
    def open_file_dialog(
        self,
        title: str,
        initial_directory: Path | str | None = None,
        file_types: list[str] | None = None,
        multiselect: Literal[False] = False,
        on_result: DialogResultHandler[Path | None] | None = None,
    ) -> Dialog:
        ...

    @overload
    def open_file_dialog(
        self,
        title: str,
        initial_directory: Path | str | None = None,
        file_types: list[str] | None = None,
        multiselect: Literal[True] = True,
        on_result: DialogResultHandler[list[Path] | None] | None = None,
    ) -> Dialog:
        ...

    @overload
    def open_file_dialog(
        self,
        title: str,
        initial_directory: Path | str | None = None,
        file_types: list[str] | None = None,
        multiselect: bool = False,
        on_result: DialogResultHandler[list[Path] | Path | None] | None = None,
    ) -> Dialog:
        ...

    def open_file_dialog(
        self,
        title: str,
        initial_directory: Path | str | None = None,
        file_types: list[str] | None = None,
        multiselect: bool = False,
        on_result: DialogResultHandler[list[Path] | Path | None] | None = None,
    ) -> Dialog:
        """Ask the user to select a file (or files) to open.

        Presents the user a system-native "Open file" dialog.

        :param title: The title of the dialog window
        :param initial_directory: The initial folder in which to open the dialog.
            If ``None``, use the default location provided by the operating system
            (which will often be "last used location")
        :param file_types: A list of strings with the allowed file extensions.
        :param multiselect: If True, the user will be able to select multiple
            files; if False, the selection will be restricted to a single file/
        :param on_result: A callback that will be invoked when the user
            selects an option on the dialog.
        :returns: An awaitable Dialog object. The Dialog object returns
            a list of ``Path`` objects if ``multiselect`` is ``True``, or a single
            ``Path`` otherwise. Returns ``None`` if the open operation is
            cancelled by the user.
        """
        dialog = Dialog(self)
        self.factory.dialogs.OpenFileDialog(
            dialog,
            title,
            initial_directory=Path(initial_directory) if initial_directory else None,
            file_types=file_types,
            multiselect=multiselect,
            on_result=wrapped_handler(self, on_result),
        )
        return dialog

    @overload
    def select_folder_dialog(
        self,
        title: str,
        initial_directory: Path | str | None = None,
        multiselect: Literal[False] = False,
        on_result: DialogResultHandler[Path | None] | None = None,
    ) -> Dialog:
        ...

    @overload
    def select_folder_dialog(
        self,
        title: str,
        initial_directory: Path | str | None = None,
        multiselect: Literal[True] = True,
        on_result: DialogResultHandler[list[Path] | None] | None = None,
    ) -> Dialog:
        ...

    @overload
    def select_folder_dialog(
        self,
        title: str,
        initial_directory: Path | str | None = None,
        multiselect: bool = False,
        on_result: DialogResultHandler[list[Path] | Path | None] | None = None,
    ) -> Dialog:
        ...

    def select_folder_dialog(
        self,
        title: str,
        initial_directory: Path | str | None = None,
        multiselect: bool = False,
        on_result: DialogResultHandler[list[Path] | Path | None] | None = None,
    ) -> Dialog:
        """Ask the user to select a directory/folder (or folders) to open.

        Presents the user a system-native "Open folder" dialog.

        :param title: The title of the dialog window
        :param initial_directory: The initial folder in which to open the dialog.
            If ``None``, use the default location provided by the operating system
            (which will often be "last used location")
        :param multiselect: If True, the user will be able to select multiple
            files; if False, the selection will be restricted to a single file/
        :param on_result: A callback that will be invoked when the user
            selects an option on the dialog.
        :returns: An awaitable Dialog object. The Dialog object returns
            a list of ``Path`` objects if ``multiselect`` is ``True``, or a single
            ``Path`` otherwise. Returns ``None`` if the open operation is
            cancelled by the user.
        """
        dialog = Dialog(self)
        self.factory.dialogs.SelectFolderDialog(
            dialog,
            title,
            initial_directory=Path(initial_directory) if initial_directory else None,
            multiselect=multiselect,
            on_result=wrapped_handler(self, on_result),
        )
        return dialog
