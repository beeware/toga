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
    _WINDOW_CLASS = "Window"

    def __init__(
        self,
        id: str | None = None,
        title: str | None = None,
        position: tuple[int, int] = (100, 100),
        size: tuple[int, int] = (640, 480),
        resizable: bool = True,
        closable: bool = True,
        minimizable: bool = True,
        on_close: OnCloseHandler | None = None,
        resizeable=None,  # DEPRECATED
        closeable=None,  # DEPRECATED
    ) -> None:
        """Create a new Window.

        :param id: The ID of the window.
        :param title: Title for the window. Defaults to "Toga".
        :param position: Position of the window, as a tuple of ``(x, y)`` coordinates.
        :param size: Size of the window, as a tuple of ``(width, height)``, in :ref:`CSS
            pixels <css-units>`.
        :param resizable: Can the window be manually resized by the user?
        :param closable: Should the window provide the option to be manually closed?
        :param minimizable: Can the window be minimized by the user?
        :param on_close: The initial ``on_close`` handler.
        :param resizeable: **DEPRECATED** - Use ``resizable``.
        :param closeable: **DEPRECATED** - Use ``closable``.
        """
        ######################################################################
        # 2023-08: Backwards compatibility
        ######################################################################
        if resizeable is not None:
            warnings.warn(
                "Window.resizeable has been renamed Window.resizable",
                DeprecationWarning,
            )
            resizable = resizeable

        if closeable is not None:
            warnings.warn(
                "Window.closeable has been renamed Window.closable",
                DeprecationWarning,
            )
            closable = closeable
        ######################################################################
        # End backwards compatibility
        ######################################################################

        self.widgets = WidgetRegistry()

        self._id = str(id if id else identifier(self))
        self._impl = None
        self._app = None
        self._content = None
        self._is_full_screen = False

        self._resizable = resizable
        self._closable = closable
        self._minimizable = minimizable

        self.factory = get_platform_factory()
        self._impl = getattr(self.factory, self._WINDOW_CLASS)(
            interface=self,
            title=title if title else self._default_title,
            position=position,
            size=size,
        )

        self._toolbar = CommandSet(widget=self, on_change=self._impl.create_toolbar)

        self.on_close = on_close

    @property
    def id(self) -> str:
        """The DOM identifier for the window."""
        return self._id

    @property
    def app(self) -> App | None:
        """Instance of the :class:`toga.App` that this window belongs to.

        :raises ValueError: If a window is already assigned to an app, and an attempt is made
            to assign the window to a new app."""
        return self._app

    @app.setter
    def app(self, app: App) -> None:
        if self._app:
            raise ValueError("Window is already associated with an App")

        self._app = app
        self._impl.set_app(app._impl)

        if self.content:
            self.content.app = app

    @property
    def _default_title(self) -> str:
        return "Toga"

    @property
    def title(self) -> str:
        """Title of the window. If no title is provided, the title will default to ``"Toga"``."""
        return self._impl.get_title()

    @title.setter
    def title(self, title: str) -> None:
        if not title:
            title = self._default_title

        self._impl.set_title(str(title).split("\n")[0])

    @property
    def resizable(self) -> bool:
        """Is the window resizable?"""
        return self._resizable

    @property
    def closable(self) -> bool:
        """Can the window be closed by a user action?"""
        return self._closable

    @property
    def minimizable(self) -> bool:
        """Can the window be minimized?"""
        return self._minimizable

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
        """Size of the window, as (width, height) in :ref:`CSS pixels <css-units>`."""
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
        """Show the window, if hidden."""

        if self.app is None:
            # Needs to be a late import to avoid circular dependencies.
            from toga import App

            App.app.windows += self

        self._impl.show()

    def hide(self) -> None:
        """Hide window, if shown."""
        if self.app is None:
            # Needs to be a late import to avoid circular dependencies.
            from toga import App

            App.app.windows += self

        self._impl.hide()

    @property
    def full_screen(self) -> bool:
        """Is the window in full screen mode?

        .. note::
            Full screen mode is *not* the same as "maximized". A full screen window
            has no title bar, tool bar or window control widgets; some or all of these
            controls may be visible on a maximized app. A good example of "full screen"
            mode is a slideshow app in presentation mode - the only visible content is
            the slide.
        """
        return self._is_full_screen

    @full_screen.setter
    def full_screen(self, is_full_screen: bool) -> None:
        self._is_full_screen = is_full_screen
        self._impl.set_full_screen(is_full_screen)

    @property
    def visible(self) -> bool:
        "Is the window visible?"
        return self._impl.get_visible()

    @visible.setter
    def visible(self, visible: bool) -> None:
        if visible:
            self.show()
        else:
            self.hide()

    @property
    def on_close(self) -> OnCloseHandler:
        """The handler to invoke before the window is closed in response to a user
        action.

        If the handler returns ``False``, the request to close the window will be
        cancelled.
        """
        return self._on_close

    @on_close.setter
    def on_close(self, handler: OnCloseHandler | None) -> None:
        def cleanup(window: Window, should_close: bool) -> None:
            if should_close or handler is None:
                window.close()

        self._on_close = wrapped_handler(self, handler, cleanup=cleanup)

    def close(self) -> None:
        """Close the window.

        This *does not* invoke the ``on_close`` handler; the window will be immediately
        and unconditionally closed.
        """
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

        Presents as a dialog with a single "OK" button to close the dialog.

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

        Presents as a dialog with "Yes" and "No" buttons.

        :param title: The title of the dialog window.
        :param message: The question to be answered.
        :param on_result: A callback that will be invoked when the user
            selects an option on the dialog.
        :returns: An awaitable Dialog object. The Dialog object returns
            ``True`` when the "Yes" button was pressed, ``False`` when
            the "No" button was pressed.
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

        Presents as a dialog with "Cancel" and "OK" buttons (or whatever labels
        are appropriate on the current platform).

        :param title: The title of the dialog window.
        :param message: A message describing the action to be confirmed.
        :param on_result: A callback that will be invoked when the user
            selects an option on the dialog.
        :returns: An awaitable Dialog object. The Dialog object returns
            ``True`` when the "OK" button was pressed, ``False`` when
            the "CANCEL" button was pressed.
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

        Presents as an error dialog with a "OK" button to close the dialog.

        :param title: The title of the dialog window.
        :param message: The error message to display.
        :param on_result: A callback that will be invoked when the user
            selects an option on the dialog.
        :returns: An awaitable Dialog object. The Dialog object returns
            ``None`` after the user pressed the "OK" button.
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
            message=message,
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

        This opens a native dialog where the user can select a place to save a file. It
        is possible to suggest a filename, and constrain the list of allowed file
        extensions.

        :param title: The title of the dialog window
        :param suggested_filename: A default filename
        :param file_types: A list of strings with the allowed file extensions.
        :param on_result: A callback that will be invoked when the user selects an
            option on the dialog.
        :returns: An awaitable Dialog object. The Dialog object returns a path object
            for the selected file location, or ``None`` if the user cancelled the save
            operation.
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
        multiple_select: Literal[False] = False,
        on_result: DialogResultHandler[Path | None] | None = None,
        multiselect=None,  # DEPRECATED
    ) -> Dialog:
        ...

    @overload
    def open_file_dialog(
        self,
        title: str,
        initial_directory: Path | str | None = None,
        file_types: list[str] | None = None,
        multiple_select: Literal[True] = True,
        on_result: DialogResultHandler[list[Path] | None] | None = None,
        multiselect=None,  # DEPRECATED
    ) -> Dialog:
        ...

    @overload
    def open_file_dialog(
        self,
        title: str,
        initial_directory: Path | str | None = None,
        file_types: list[str] | None = None,
        multiple_select: bool = False,
        on_result: DialogResultHandler[list[Path] | Path | None] | None = None,
        multiselect=None,  # DEPRECATED
    ) -> Dialog:
        ...

    def open_file_dialog(
        self,
        title: str,
        initial_directory: Path | str | None = None,
        file_types: list[str] | None = None,
        multiple_select: bool = False,
        on_result: DialogResultHandler[list[Path] | Path | None] | None = None,
        multiselect=None,  # DEPRECATED
    ) -> Dialog:
        """Ask the user to select a file (or files) to open.

        Presents the user a system-native "Open file" dialog.

        :param title: The title of the dialog window
        :param initial_directory: The initial folder in which to open the dialog.
            If ``None``, use the default location provided by the operating system
            (which will often be the last used location)
        :param file_types: A list of strings with the allowed file extensions.
        :param multiple_select: If True, the user will be able to select multiple
            files; if False, the selection will be restricted to a single file.
        :param on_result: A callback that will be invoked when the user
            selects an option on the dialog.
        :param multiselect: **DEPRECATED** Use ``multiple_select``.
        :returns: An awaitable Dialog object. The Dialog object returns
            a list of ``Path`` objects if ``multiple_select`` is ``True``, or a single
            ``Path`` otherwise. Returns ``None`` if the open operation is
            cancelled by the user.
        """
        ######################################################################
        # 2023-08: Backwards compatibility
        ######################################################################
        if multiselect is not None:
            warnings.warn(
                "open_file_dialog(multiselect) has been renamed multiple_select",
                DeprecationWarning,
            )
            multiple_select = multiselect
        ######################################################################
        # End Backwards compatibility
        ######################################################################

        dialog = Dialog(self)
        self.factory.dialogs.OpenFileDialog(
            dialog,
            title,
            initial_directory=Path(initial_directory) if initial_directory else None,
            file_types=file_types,
            multiple_select=multiple_select,
            on_result=wrapped_handler(self, on_result),
        )
        return dialog

    @overload
    def select_folder_dialog(
        self,
        title: str,
        initial_directory: Path | str | None = None,
        multiple_select: Literal[False] = False,
        on_result: DialogResultHandler[Path | None] | None = None,
        multiselect=None,  # DEPRECATED
    ) -> Dialog:
        ...

    @overload
    def select_folder_dialog(
        self,
        title: str,
        initial_directory: Path | str | None = None,
        multiple_select: Literal[True] = True,
        on_result: DialogResultHandler[list[Path] | None] | None = None,
        multiselect=None,  # DEPRECATED
    ) -> Dialog:
        ...

    @overload
    def select_folder_dialog(
        self,
        title: str,
        initial_directory: Path | str | None = None,
        multiple_select: bool = False,
        on_result: DialogResultHandler[list[Path] | Path | None] | None = None,
        multiselect=None,  # DEPRECATED
    ) -> Dialog:
        ...

    def select_folder_dialog(
        self,
        title: str,
        initial_directory: Path | str | None = None,
        multiple_select: bool = False,
        on_result: DialogResultHandler[list[Path] | Path | None] | None = None,
        multiselect=None,  # DEPRECATED
    ) -> Dialog:
        """Ask the user to select a directory/folder (or folders) to open.

        Presents the user a system-native "Open folder" dialog.

        :param title: The title of the dialog window
        :param initial_directory: The initial folder in which to open the dialog.
            If ``None``, use the default location provided by the operating system
            (which will often be "last used location")
        :param multiple_select: If True, the user will be able to select multiple
            files; if False, the selection will be restricted to a single file/
        :param on_result: A callback that will be invoked when the user
            selects an option on the dialog.
        :param multiselect: **DEPRECATED** Use ``multiple_select``.
        :returns: An awaitable Dialog object. The Dialog object returns
            a list of ``Path`` objects if ``multiple_select`` is ``True``, or a single
            ``Path`` otherwise. Returns ``None`` if the open operation is
            cancelled by the user.
        """
        ######################################################################
        # 2023-08: Backwards compatibility
        ######################################################################
        if multiselect is not None:
            warnings.warn(
                "select_folder_dialog(multiselect) has been renamed multiple_select",
                DeprecationWarning,
            )
            multiple_select = multiselect
        ######################################################################
        # End Backwards compatibility
        ######################################################################

        dialog = Dialog(self)
        self.factory.dialogs.SelectFolderDialog(
            dialog,
            title,
            initial_directory=Path(initial_directory) if initial_directory else None,
            multiple_select=multiple_select,
            on_result=wrapped_handler(self, on_result),
        )
        return dialog

    ######################################################################
    # 2023-08: Backwards compatibility
    ######################################################################

    @property
    def resizeable(self) -> bool:
        """**DEPRECATED** Use :attr:`resizable`"""
        warnings.warn(
            "Window.resizeable has been renamed Window.resizable",
            DeprecationWarning,
        )
        return self._resizable

    @property
    def closeable(self) -> bool:
        """**DEPRECATED** Use :attr:`closable`"""
        warnings.warn(
            "Window.closeable has been renamed Window.closable",
            DeprecationWarning,
        )
        return self._closable
