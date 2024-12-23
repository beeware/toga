from __future__ import annotations

import warnings
from builtins import id as identifier
from collections.abc import Mapping, MutableSet
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    ItemsView,
    Iterator,
    KeysView,
    Literal,
    Protocol,
    TypeVar,
    ValuesView,
    overload,
)

from toga.command import Command, CommandSet
from toga.handlers import AsyncResult, wrapped_handler
from toga.images import Image
from toga.platform import get_platform_factory

if TYPE_CHECKING:
    from toga.app import App
    from toga.images import ImageT
    from toga.widgets.base import Widget


class FilteredWidgetRegistry:
    # A class that exposes a mapping lookup interface, filtered to widgets from a single
    # window. The underlying data store is on the app.

    def __init__(self, window):
        self._window = window

    def __len__(self) -> int:
        return len(list(self.items()))

    def __getitem__(self, key: str) -> Widget:
        item = self._window.app.widgets[key]
        if item.window != self._window:
            raise KeyError(key)
        return item

    def __contains__(self, key: str) -> bool:
        try:
            item = self._window.app.widgets[key]
            return item.window == self._window
        except KeyError:
            return False

    def __iter__(self) -> Iterator[Widget]:
        return iter(self.values())

    def __repr__(self) -> str:
        return "{" + ", ".join(f"{k!r}: {v!r}" for k, v in sorted(self.items())) + "}"

    def items(self) -> ItemsView:
        for item in self._window.app.widgets.items():
            if item[1].window == self._window:
                yield item

    def keys(self) -> KeysView:
        for item in self._window.app.widgets.items():
            if item[1].window == self._window:
                yield item[0]

    def values(self) -> ValuesView:
        for item in self._window.app.widgets.items():
            if item[1].window == self._window:
                yield item[1]


class OnCloseHandler(Protocol):
    def __call__(self, window: Window, **kwargs: Any) -> bool:
        """A handler to invoke when a window is about to close.

        The return value of this callback controls whether the window is allowed to close.
        This can be used to prevent a window closing with unsaved changes, etc.

        :param window: The window instance that is closing.
        :param kwargs: Ensures compatibility with additional arguments introduced in
            future versions.
        :returns: ``True`` if the window is allowed to close; ``False`` if the window is not
            allowed to close.
        """
        ...


T = TypeVar("T")


class DialogResultHandler(Protocol[T]):
    def __call__(self, window: Window, result: T, **kwargs: Any) -> None:
        """A handler to invoke when a dialog is closed.

        :param window: The window that opened the dialog.
        :param result: The result returned by the dialog.
        :param kwargs: Ensures compatibility with additional arguments introduced in
            future versions.
        """
        ...


class Dialog(AsyncResult):
    RESULT_TYPE = "dialog"

    def __init__(self, window: Window, on_result: DialogResultHandler[Any]):
        super().__init__(on_result=on_result)
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

        :param id: A unique identifier for the window. If not provided, one will be
            automatically generated.
        :param title: Title for the window. Defaults to "Toga".
        :param position: Position of the window, as a tuple of ``(x, y)`` coordinates,
            in :ref:`CSS pixels <css-units>`.
        :param size: Size of the window, as a tuple of ``(width, height)``, in :ref:`CSS
            pixels <css-units>`.
        :param resizable: Can the window be resized by the user?
        :param closable: Can the window be closed by the user?
        :param minimizable: Can the window be minimized by the user?
        :param on_close: The initial :any:`on_close` handler.
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

        # Needs to be a late import to avoid circular dependencies.
        from toga import App

        self._id = str(id if id else identifier(self))
        self._impl = None
        self._content = None
        self._is_full_screen = False
        self._closed = False

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

        # Add the window to the app
        self._app = None
        if App.app is None:
            raise RuntimeError("Cannot create a Window before creating an App")
        App.app.windows.add(self)

        # Create a toolbar that is linked to the app
        self._toolbar = CommandSet(on_change=self._impl.create_toolbar, app=self._app)

        self.on_close = on_close

    @property
    def id(self) -> str:
        """A unique identifier for the window."""
        return self._id

    def __lt__(self, other) -> bool:
        return self.id < other.id

    @property
    def app(self) -> App:
        """The :any:`App` that this window belongs to (read-only).

        New windows are automatically associated with the currently active app."""
        return self._app

    @app.setter
    def app(self, app: App) -> None:
        if self._app:
            raise ValueError("Window is already associated with an App")

        self._app = app
        self._impl.set_app(app._impl)

    @property
    def closed(self) -> bool:
        """Whether the window was closed."""
        return self._closed

    @property
    def _default_title(self) -> str:
        return "Toga"

    @property
    def title(self) -> str:
        """Title of the window. If no title is provided, the title will default to
        "Toga"."""
        return self._impl.get_title()

    @title.setter
    def title(self, title: str) -> None:
        if not title:
            title = self._default_title

        self._impl.set_title(str(title).split("\n")[0])

    @property
    def resizable(self) -> bool:
        """Can the window be resized by the user?"""
        return self._resizable

    @property
    def closable(self) -> bool:
        """Can the window be closed by the user?"""
        return self._closable

    @property
    def minimizable(self) -> bool:
        """Can the window be minimized by the user?"""
        return self._minimizable

    @property
    def toolbar(self) -> MutableSet[Command]:
        """Toolbar for the window."""
        return self._toolbar

    @property
    def content(self) -> Widget | None:
        """Content of the window. On setting, the content is added to the same app as
        the window."""
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
    def widgets(self) -> Mapping[str, Widget]:
        """The widgets contained in the window.

        Can be used to look up widgets by ID (e.g., ``window.widgets["my_id"]``).
        """
        return FilteredWidgetRegistry(self)

    @property
    def size(self) -> tuple[int, int]:
        """Size of the window, as a tuple of ``(width, height)``, in
        :ref:`CSS pixels <css-units>`."""
        return self._impl.get_size()

    @size.setter
    def size(self, size: tuple[int, int]) -> None:
        self._impl.set_size(size)
        if self.content:
            self.content.refresh()

    @property
    def position(self) -> tuple[int, int]:
        """Position of the window, as a tuple of ``(x, y)`` coordinates, in
        :ref:`CSS pixels <css-units>`."""
        return self._impl.get_position()

    @position.setter
    def position(self, position: tuple[int, int]) -> None:
        self._impl.set_position(position)

    def show(self) -> None:
        """Show the window. If the window is already visible, this method has no
        effect."""
        self._impl.show()

    def hide(self) -> None:
        """Hide the window. If the window is already hidden, this method has no
        effect."""
        self._impl.hide()

    @property
    def full_screen(self) -> bool:
        """Is the window in full screen mode?

        Full screen mode is *not* the same as "maximized". A full screen window
        has no title bar, toolbar or window controls; some or all of these
        items may be visible on a maximized window. A good example of "full screen"
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
        """The handler to invoke if the user attempts to close the window."""
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

        Once a window has been closed, it *cannot* be reused. The behavior of any method
        or property on a :class:`~toga.Window` instance after it has been closed is
        undefined, except for :attr:`closed` which can be used to check if the window
        was closed.
        """
        self.app.windows.discard(self)
        self._impl.close()
        self._closed = True

    def as_image(self, format: type[ImageT] = Image) -> ImageT:
        """Render the current contents of the window as an image.

        :param format: Format to provide. Defaults to :class:`~toga.images.Image`; also
            supports :any:`PIL.Image.Image` if Pillow is installed
        :returns: An image containing the window content, in the format requested.
        """
        return Image(self._impl.get_image_data()).as_format(format)

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

        **This is an asynchronous method**. If you invoke this method in synchronous
        context, it will show the dialog, but will return *immediately*. The object
        returned by this method can be awaited to obtain the result of the dialog.

        :param title: The title of the dialog window.
        :param message: The message to display.
        :param on_result: **DEPRECATED** ``await`` the return value of this method.
        :returns: An awaitable Dialog object. The Dialog object returns ``None`` when
            the user presses the 'OK' button.
        """
        dialog = Dialog(
            self,
            on_result=wrapped_handler(self, on_result) if on_result else None,
        )
        self.factory.dialogs.InfoDialog(dialog, title, message)
        return dialog

    def question_dialog(
        self,
        title: str,
        message: str,
        on_result: DialogResultHandler[bool] | None = None,
    ) -> Dialog:
        """Ask the user a yes/no question.

        Presents as a dialog with "Yes" and "No" buttons.

        **This is an asynchronous method**. If you invoke this method in synchronous
        context, it will show the dialog, but will return *immediately*. The object
        returned by this method can be awaited to obtain the result of the dialog.

        :param title: The title of the dialog window.
        :param message: The question to be answered.
        :param on_result: **DEPRECATED** ``await`` the return value of this method.
        :returns: An awaitable Dialog object. The Dialog object returns ``True`` when
            the "Yes" button is pressed, ``False`` when the "No" button is pressed.
        """
        dialog = Dialog(
            self,
            on_result=wrapped_handler(self, on_result) if on_result else None,
        )
        self.factory.dialogs.QuestionDialog(dialog, title, message)
        return dialog

    def confirm_dialog(
        self,
        title: str,
        message: str,
        on_result: DialogResultHandler[bool] | None = None,
    ) -> Dialog:
        """Ask the user to confirm if they wish to proceed with an action.

        Presents as a dialog with "Cancel" and "OK" buttons (or whatever labels are
        appropriate on the current platform).

        **This is an asynchronous method**. If you invoke this method in synchronous
        context, it will show the dialog, but will return *immediately*. The object
        returned by this method can be awaited to obtain the result of the dialog.

        :param title: The title of the dialog window.
        :param message: A message describing the action to be confirmed.
        :param on_result: **DEPRECATED** ``await`` the return value of this method.
        :returns: An awaitable Dialog object. The Dialog object returns ``True`` when
            the "OK" button is pressed, ``False`` when the "Cancel" button is pressed.
        """
        dialog = Dialog(
            self,
            on_result=wrapped_handler(self, on_result) if on_result else None,
        )
        self.factory.dialogs.ConfirmDialog(dialog, title, message)
        return dialog

    def error_dialog(
        self,
        title: str,
        message: str,
        on_result: DialogResultHandler[None] | None = None,
    ) -> Dialog:
        """Ask the user to acknowledge an error state.

        Presents as an error dialog with a "OK" button to close the dialog.

        **This is an asynchronous method**. If you invoke this method in synchronous
        context, it will show the dialog, but will return *immediately*. The object
        returned by this method can be awaited to obtain the result of the dialog.

        :param title: The title of the dialog window.
        :param message: The error message to display.
        :param on_result: **DEPRECATED** ``await`` the return value of this method.
        :returns: An awaitable Dialog object. The Dialog object returns ``None`` when
            the user presses the "OK" button.
        """
        dialog = Dialog(
            self,
            on_result=wrapped_handler(self, on_result) if on_result else None,
        )
        self.factory.dialogs.ErrorDialog(dialog, title, message)
        return dialog

    @overload
    def stack_trace_dialog(
        self,
        title: str,
        message: str,
        content: str,
        retry: Literal[False] = False,
        on_result: DialogResultHandler[None] | None = None,
    ) -> Dialog: ...

    @overload
    def stack_trace_dialog(
        self,
        title: str,
        message: str,
        content: str,
        retry: Literal[True] = False,
        on_result: DialogResultHandler[bool] | None = None,
    ) -> Dialog: ...

    @overload
    def stack_trace_dialog(
        self,
        title: str,
        message: str,
        content: str,
        retry: bool = False,
        on_result: DialogResultHandler[bool | None] | None = None,
    ) -> Dialog: ...

    def stack_trace_dialog(
        self,
        title: str,
        message: str,
        content: str,
        retry: bool = False,
        on_result: DialogResultHandler[bool | None] | None = None,
    ) -> Dialog:
        """Open a dialog to display a large block of text, such as a stack trace.

        **This is an asynchronous method**. If you invoke this method in synchronous
        context, it will show the dialog, but will return *immediately*. The object
        returned by this method can be awaited to obtain the result of the dialog.

        :param title: The title of the dialog window.
        :param message: Contextual information about the source of the stack trace.
        :param content: The stack trace, pre-formatted as a multi-line string.
        :param retry: If true, the user will be given options to "Retry" or "Quit"; if
            false, a single option to acknowledge the error will be displayed.
        :param on_result: **DEPRECATED** ``await`` the return value of this method.
        :returns: An awaitable Dialog object. If ``retry`` is true, the Dialog object
            returns ``True`` when the user selects "Retry", and ``False`` when they
            select "Quit". If ``retry`` is false, the Dialog object returns ``None``.
        """
        dialog = Dialog(
            self,
            on_result=wrapped_handler(self, on_result) if on_result else None,
        )
        self.factory.dialogs.StackTraceDialog(
            dialog,
            title,
            message=message,
            content=content,
            retry=retry,
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

        This dialog is not currently supported on Android or iOS.

        **This is an asynchronous method**. If you invoke this method in synchronous
        context, it will show the dialog, but will return *immediately*. The object
        returned by this method can be awaited to obtain the result of the dialog.

        :param title: The title of the dialog window
        :param suggested_filename: A default filename
        :param file_types: The allowed filename extensions, without leading dots. If not
            provided, any extension will be allowed.
        :param on_result: **DEPRECATED** ``await`` the return value of this method.
        :returns: An awaitable Dialog object. The Dialog object returns a path object
            for the selected file location, or ``None`` if the user cancelled the save
            operation.
        """
        dialog = Dialog(
            self,
            on_result=wrapped_handler(self, on_result) if on_result else None,
        )
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
    ) -> Dialog: ...

    @overload
    def open_file_dialog(
        self,
        title: str,
        initial_directory: Path | str | None = None,
        file_types: list[str] | None = None,
        multiple_select: Literal[True] = True,
        on_result: DialogResultHandler[list[Path] | None] | None = None,
        multiselect=None,  # DEPRECATED
    ) -> Dialog: ...

    @overload
    def open_file_dialog(
        self,
        title: str,
        initial_directory: Path | str | None = None,
        file_types: list[str] | None = None,
        multiple_select: bool = False,
        on_result: DialogResultHandler[list[Path] | Path | None] | None = None,
        multiselect=None,  # DEPRECATED
    ) -> Dialog: ...

    def open_file_dialog(
        self,
        title: str,
        initial_directory: Path | str | None = None,
        file_types: list[str] | None = None,
        multiple_select: bool = False,
        on_result: DialogResultHandler[list[Path] | Path | None] | None = None,
        multiselect=None,  # DEPRECATED
    ) -> Dialog:
        """Prompt the user to select a file (or files) to open.

        This dialog is not currently supported on Android or iOS.

        **This is an asynchronous method**. If you invoke this method in synchronous
        context, it will show the dialog, but will return *immediately*. The object
        returned by this method can be awaited to obtain the result of the dialog.

        :param title: The title of the dialog window
        :param initial_directory: The initial folder in which to open the dialog. If
            ``None``, use the default location provided by the operating system (which
            will often be the last used location)
        :param file_types: The allowed filename extensions, without leading dots. If not
            provided, all files will be shown.
        :param multiple_select: If True, the user will be able to select multiple files;
            if False, the selection will be restricted to a single file.
        :param on_result: **DEPRECATED** ``await`` the return value of this method.
        :param multiselect: **DEPRECATED** Use ``multiple_select``.
        :returns: An awaitable Dialog object. The Dialog object returns a list of
            ``Path`` objects if ``multiple_select`` is ``True``, or a single ``Path``
            otherwise. Returns ``None`` if the open operation is cancelled by the user.
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

        dialog = Dialog(
            self,
            on_result=wrapped_handler(self, on_result) if on_result else None,
        )
        self.factory.dialogs.OpenFileDialog(
            dialog,
            title,
            initial_directory=Path(initial_directory) if initial_directory else None,
            file_types=file_types,
            multiple_select=multiple_select,
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
    ) -> Dialog: ...

    @overload
    def select_folder_dialog(
        self,
        title: str,
        initial_directory: Path | str | None = None,
        multiple_select: Literal[True] = True,
        on_result: DialogResultHandler[list[Path] | None] | None = None,
        multiselect=None,  # DEPRECATED
    ) -> Dialog: ...

    @overload
    def select_folder_dialog(
        self,
        title: str,
        initial_directory: Path | str | None = None,
        multiple_select: bool = False,
        on_result: DialogResultHandler[list[Path] | Path | None] | None = None,
        multiselect=None,  # DEPRECATED
    ) -> Dialog: ...

    def select_folder_dialog(
        self,
        title: str,
        initial_directory: Path | str | None = None,
        multiple_select: bool = False,
        on_result: DialogResultHandler[list[Path] | Path | None] | None = None,
        multiselect=None,  # DEPRECATED
    ) -> Dialog:
        """Prompt the user to select a directory (or directories).

        This dialog is not currently supported on Android or iOS.

        **This is an asynchronous method**. If you invoke this method in synchronous
        context, it will show the dialog, but will return *immediately*. The object
        returned by this method can be awaited to obtain the result of the dialog.

        :param title: The title of the dialog window
        :param initial_directory: The initial folder in which to open the dialog. If
            ``None``, use the default location provided by the operating system (which
            will often be "last used location")
        :param multiple_select: If True, the user will be able to select multiple
            directories; if False, the selection will be restricted to a single
            directory. This option is not supported on WinForms.
        :param on_result: **DEPRECATED** ``await`` the return value of this method.
        :param multiselect: **DEPRECATED** Use ``multiple_select``.
        :returns: An awaitable Dialog object. The Dialog object returns a list of
            ``Path`` objects if ``multiple_select`` is ``True``, or a single ``Path``
            otherwise. Returns ``None`` if the open operation is cancelled by the user.
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

        dialog = Dialog(
            self,
            on_result=wrapped_handler(self, on_result) if on_result else None,
        )
        self.factory.dialogs.SelectFolderDialog(
            dialog,
            title,
            initial_directory=Path(initial_directory) if initial_directory else None,
            multiple_select=multiple_select,
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
