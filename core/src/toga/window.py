from __future__ import annotations

import warnings
from builtins import id as identifier
from collections.abc import Iterator, MutableSet
from pathlib import Path
from typing import TYPE_CHECKING, Any, Protocol, TypeVar

import toga
from toga import dialogs
from toga.command import CommandSet
from toga.constants import WindowState
from toga.handlers import AsyncResult, wrapped_handler
from toga.images import Image
from toga.platform import get_platform_factory
from toga.types import Position, Size

if TYPE_CHECKING:
    from toga.app import App
    from toga.images import ImageT
    from toga.screens import Screen
    from toga.types import PositionT, SizeT
    from toga.widgets.base import Widget


_window_count = -1


def _initial_position() -> Position:
    """Compute a cascading initial position for platforms that don't have a native
    implementation.

    This is a stateful method; each time it is invoked, it will yield a new initial
    position.

    :returns: The position for the new window.
    """
    # Each new window created without an explicit position is positioned
    # 50px down and to the right from the previous window, with the first
    # window positioned at (100, 100). Every 15 windows, move back to a
    # y coordinate of 100, and start from 50 pixels further right.
    global _window_count
    _window_count += 1

    pos = 100 + (_window_count % 15) * 50
    return Position(pos + (_window_count // 15 * 50), pos)


class FilteredWidgetRegistry:
    # A class that exposes a mapping lookup interface, filtered to widgets from a single
    # window. The underlying data store is on the app.

    def __init__(self, window: Window) -> None:
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

    def items(self) -> Iterator[tuple[str, Widget]]:
        for item in self._window.app.widgets.items():
            if item[1].window == self._window:
                yield item

    def keys(self) -> Iterator[str]:
        for item in self._window.app.widgets.items():
            if item[1].window == self._window:
                yield item[0]

    def values(self) -> Iterator[Widget]:
        for item in self._window.app.widgets.items():
            if item[1].window == self._window:
                yield item[1]


class OnCloseHandler(Protocol):
    def __call__(self, window: Window, **kwargs: Any) -> bool:
        """A handler to invoke when a window is about to close.

        The return value of this callback controls whether the window
        is allowed to close.
        This can be used to prevent a window closing with unsaved changes, etc.

        :param window: The window instance that is closing.
        :param kwargs: Ensures compatibility with arguments added in future versions.
        :returns: ``True`` if the window is allowed to close; ``False`` if the window
            is not allowed to close.
        """
        ...


class OnGainFocusHandler(Protocol):
    def __call__(self, window: Window, **kwargs: Any) -> None:
        """A handler to invoke when a window gains input focus.

        :param window: The window instance that gains input focus.
        :param kwargs: Ensures compatibility with additional arguments introduced in
            future versions.
        """
        ...


class OnLoseFocusHandler(Protocol):
    def __call__(self, window: Window, **kwargs: Any) -> None:
        """A handler to invoke when a window loses input focus.

        :param window: The window instance that loses input focus.
        :param kwargs: Ensures compatibility with additional arguments introduced in
            future ver
        """
        ...


class OnShowHandler(Protocol):
    def __call__(self, window: Window, **kwargs: Any) -> None:
        """A handler to invoke when a window becomes visible.

        This event will be triggered when a window is first displayed, and when the
        window is restored from a minimized or hidden state. On mobile platforms, it is
        also triggered when an app is made the currently active app.

        :param window: The window instance that becomes visible.
        :param kwargs: Ensures compatibility with additional arguments introduced in
            future ver
        """
        ...


class OnHideHandler(Protocol):
    def __call__(self, window: Window, **kwargs: Any) -> None:
        """A handler to invoke when a window stops being visible.

        This event will be triggered when a window moves to a minimized or hidden state.
        On mobile platforms, it is also triggered when an app is moved to the background
        and is no longer the currently active app.

        :param window: The window instance that becomes not visible to the user.
        :param kwargs: Ensures compatibility with additional arguments introduced in
            future ver
        """
        ...


_DialogResultT = TypeVar("_DialogResultT", contravariant=True)


class DialogResultHandler(Protocol[_DialogResultT]):
    def __call__(self, window: Window, result: _DialogResultT, **kwargs: Any) -> object:
        """A handler to invoke when a dialog is closed.

        :param window: The window that opened the dialog.
        :param kwargs: Ensures compatibility with arguments added in future versions.
        :param result: The result returned by the dialog.
        """


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
        position: PositionT | None = None,
        size: SizeT = (640, 480),
        resizable: bool = True,
        closable: bool = True,
        minimizable: bool = True,
        on_close: OnCloseHandler | None = None,
        on_gain_focus: OnGainFocusHandler | None = None,
        on_lose_focus: OnLoseFocusHandler | None = None,
        on_show: OnShowHandler | None = None,
        on_hide: OnHideHandler | None = None,
        content: Widget | None = None,
    ) -> None:
        """Create a new Window.

        :param id: A unique identifier for the window. If not provided, one will be
            automatically generated.
        :param title: Title for the window. Defaults to the formal name of the app.
        :param position: Position of the window, as a :any:`toga.Position` or tuple of
            ``(x, y)`` coordinates, in :ref:`CSS pixels <css-units>`.
        :param size: Size of the window, as a :any:`toga.Size` or tuple of ``(width,
            height)``, in :ref:`CSS pixels <css-units>`.
        :param resizable: Can the window be resized by the user?
        :param closable: Can the window be closed by the user?
        :param minimizable: Can the window be minimized by the user?
        :param on_close: The initial :any:`on_close` handler.
        :param content: The initial content for the window.
        """
        # Needs to be a late import to avoid circular dependencies.
        from toga import App

        self._id = str(id if id else identifier(self))
        self._impl: Any = None
        self._content: Widget | None = None
        self._closed = False

        self._resizable = resizable
        self._closable = closable
        self._minimizable = minimizable

        # The app needs to exist before windows are created. _app will only be None
        # until the window is added to the app below.
        self._app: App = None
        if App.app is None:
            raise RuntimeError("Cannot create a Window before creating an App")

        self.factory = get_platform_factory()
        self._impl = getattr(self.factory, self._WINDOW_CLASS)(
            interface=self,
            title=title if title else self._default_title,
            position=None if position is None else Position(*position),
            size=Size(*size),
        )

        # Add the window to the app
        App.app.windows.add(self)

        # If content has been provided, set it
        if content:
            self.content = content

        self.on_close = on_close

        self.on_gain_focus = on_gain_focus
        self.on_lose_focus = on_lose_focus
        self.on_show = on_show
        self.on_hide = on_hide

    def __lt__(self, other: Window) -> bool:
        return self.id < other.id

    ######################################################################
    # Window properties
    ######################################################################

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
    def closable(self) -> bool:
        """Can the window be closed by the user?"""
        return self._closable

    @property
    def id(self) -> str:
        """A unique identifier for the window (read-only)."""
        return self._id

    @property
    def minimizable(self) -> bool:
        """Can the window be minimized by the user?"""
        return self._minimizable

    @property
    def resizable(self) -> bool:
        """Can the window be resized by the user?"""
        return self._resizable

    @property
    def _default_title(self) -> str:
        return toga.App.app.formal_name

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

    ######################################################################
    # Window lifecycle
    ######################################################################

    def close(self) -> None:
        """Close the window.

        This *does not* invoke the ``on_close`` handler. If the window being closed
        is the app's main window, it will trigger ``on_exit`` handling; otherwise, the
        window will be immediately and unconditionally closed.

        Once a window has been closed, it *cannot* be reused. The behavior of any method
        or property on a :class:`~toga.Window` instance after it has been closed is
        undefined, except for :attr:`closed` which can be used to check if the window
        was closed.

        :returns: True if the window was actually closed; False if closing the window
            triggered ``on_exit`` handling.
        """
        close_window = True
        if self.app.main_window == self:
            # Closing the window marked as the main window is a request to exit.
            self.app.request_exit()
            close_window = False
        elif self.app.main_window is None:
            # If this is an app without a main window, the app is running, this
            # is the last window in the app, and the platform exits on last
            # window close, request an exit.
            if (
                len(self.app.windows) == 1
                and self.app._impl.CLOSE_ON_LAST_WINDOW
                and self.app.loop.is_running()
            ):
                self.app.request_exit()
                close_window = False

        if close_window:
            self._close()

        # Return whether the window was actually closed
        return close_window

    def _close(self):
        # The actual logic for closing a window. This is abstracted so that the testbed
        # can monkeypatch this method, recording the close request without actually
        # closing the app.
        if self.content:
            self.content.window = None
        self.app.windows.discard(self)
        self._impl.close()
        self._closed = True

    @property
    def closed(self) -> bool:
        """Whether the window was closed."""
        return self._closed

    def show(self) -> None:
        """Show the window. If the window is already visible, this method has no
        effect.

        :raises ValueError: If the window is currently in a minimized, full screen or
            presentation state.
        """
        if not self.visible:
            if self.state in {
                WindowState.MINIMIZED,
                WindowState.FULLSCREEN,
                WindowState.PRESENTATION,
            }:
                raise ValueError(f"A window in {self.state} state cannot be shown.")
            else:
                self._impl.show()

    ######################################################################
    # Window content and resources
    ######################################################################

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
    def widgets(self) -> FilteredWidgetRegistry:
        """The widgets contained in the window.

        Can be used to look up widgets by ID (e.g., ``window.widgets["my_id"]``).
        """
        return FilteredWidgetRegistry(self)

    ######################################################################
    # Window size
    ######################################################################

    @property
    def size(self) -> Size:
        """Size of the window, in :ref:`CSS pixels <css-units>`.

        :raises RuntimeError: If resize is requested while in
            :any:`WindowState.FULLSCREEN` or :any:`WindowState.PRESENTATION`.
        """
        return self._impl.get_size()

    @size.setter
    def size(self, size: SizeT) -> None:
        if self.state in {WindowState.FULLSCREEN, WindowState.PRESENTATION}:
            raise RuntimeError(f"Cannot resize window while in {self.state}")
        elif self.size != size:
            self._impl.set_size(size)
            if self.content:
                self.content.refresh()

    ######################################################################
    # Window position
    ######################################################################

    @property
    def position(self) -> Position:
        """Absolute position of the window, in :ref:`CSS pixels <css-units>`.

        The origin is the top left corner of the primary screen.

        :raises RuntimeError: If position change is requested while in
            :any:`WindowState.FULLSCREEN` or :any:`WindowState.PRESENTATION`.
        """
        absolute_origin = self._app.screens[0].origin
        absolute_window_position = self._impl.get_position()
        window_position = absolute_window_position - absolute_origin

        return window_position

    @position.setter
    def position(self, position: PositionT) -> None:
        if self.state in {WindowState.FULLSCREEN, WindowState.PRESENTATION}:
            raise RuntimeError(f"Cannot change window position while in {self.state}")
        absolute_origin = self._app.screens[0].origin
        absolute_new_position = Position(*position) + absolute_origin
        self._impl.set_position(absolute_new_position)

    @property
    def screen(self) -> Screen:
        """Instance of the :class:`toga.Screen` on which this window is present."""
        return self._impl.get_current_screen().interface

    @screen.setter
    def screen(self, app_screen: Screen) -> None:
        original_window_location = self.position
        original_origin = self.screen.origin
        new_origin = app_screen.origin
        self._impl.set_position(original_window_location - original_origin + new_origin)

    @property
    def screen_position(self) -> Position:
        """Position of the window with respect to current screen, in
        :ref:`CSS pixels <css-units>`.

        :raises RuntimeError: If position change is requested while in
            :any:`WindowState.FULLSCREEN` or :any:`WindowState.PRESENTATION`.
        """
        return self.position - self.screen.origin

    @screen_position.setter
    def screen_position(self, position: PositionT) -> None:
        if self.state in {WindowState.FULLSCREEN, WindowState.PRESENTATION}:
            raise RuntimeError(f"Cannot change window position while in {self.state}")
        new_relative_position = Position(*position) + self.screen.origin
        self._impl.set_position(new_relative_position)

    ######################################################################
    # Window visibility
    ######################################################################

    def hide(self) -> None:
        """Hide the window. If the window is already hidden, this method has no
        effect.

        :raises ValueError: If the window is currently in a minimized, full screen or
            presentation state.
        """
        if self.visible:
            if self.state in {
                WindowState.MINIMIZED,
                WindowState.FULLSCREEN,
                WindowState.PRESENTATION,
            }:
                raise ValueError(f"A window in {self.state} state cannot be hidden.")
            else:
                self._impl.hide()

    @property
    def visible(self) -> bool:
        """Is the window visible?"""
        return self._impl.get_visible()

    @visible.setter
    def visible(self, visible: bool) -> None:
        if visible:
            self.show()
        else:
            self.hide()

    ######################################################################
    # Window state
    ######################################################################

    @property
    def state(self) -> WindowState:
        """The current state of the window.

        When the window is in transition, then this will return the state it
        is transitioning towards, instead of the actual instantaneous state.

        :raises RuntimeError: If state change is requested while the window is
            hidden.

        :raises ValueError: If any state other than :any:`WindowState.MINIMIZED`
            or :any:`WindowState.NORMAL` is requested on a non-resizable window.
        """
        # There are 2 types of window states that we can get from the backend:
        # * The instantaneous state -- Used internally on implementation side
        # * The in-progress state -- Used for same state checking on the core
        #                            and for the public API.
        return self._impl.get_window_state(in_progress_state=True)

    @state.setter
    def state(self, state: WindowState) -> None:
        if not self.visible:
            raise RuntimeError("Window state of a hidden window cannot be changed.")
        elif not self.resizable and state in {
            WindowState.MAXIMIZED,
            WindowState.FULLSCREEN,
            WindowState.PRESENTATION,
        }:
            raise ValueError(
                f"A non-resizable window cannot be set to a state of {state}."
            )
        else:
            if self.state != state:
                self._impl.set_window_state(state)

    ######################################################################
    # Window capabilities
    ######################################################################

    def as_image(self, format: type[ImageT] = Image) -> ImageT:
        """Render the current contents of the window as an image.

        :param format: Format to provide. Defaults to :class:`~toga.images.Image`; also
            supports :any:`PIL.Image.Image` if Pillow is installed, as well as any image
            types defined by installed :doc:`image format plugins
            </reference/plugins/image_formats>`.
        :returns: An image containing the window content, in the format requested.
        """
        return Image(self._impl.get_image_data()).as_format(format)

    async def dialog(
        self, dialog: dialogs.Dialog[dialogs.DialogResultT]
    ) -> dialogs.DialogResultT:
        """Display a dialog to the user, modal to this window.

        :param: The :doc:`dialog <resources/dialogs>` to display to the user.
        :returns: The result of the dialog.
        """
        return await dialog._show(self)

    ######################################################################
    # Window events
    ######################################################################

    @property
    def on_close(self) -> OnCloseHandler | None:
        """The handler to invoke if the user attempts to close the window."""
        return self._on_close

    @on_close.setter
    def on_close(self, handler: OnCloseHandler | None) -> None:
        def cleanup(window: Window, should_close: bool) -> None:
            if should_close or handler is None:
                window.close()

        self._on_close = wrapped_handler(self, handler, cleanup=cleanup)

    @property
    def on_gain_focus(self) -> callable:
        """The handler to invoke if the window gains input focus."""
        return self._on_gain_focus

    @on_gain_focus.setter
    def on_gain_focus(self, handler):
        self._on_gain_focus = wrapped_handler(self, handler)

    @property
    def on_lose_focus(self) -> callable:
        """The handler to invoke if the window loses input focus."""
        return self._on_lose_focus

    @on_lose_focus.setter
    def on_lose_focus(self, handler):
        self._on_lose_focus = wrapped_handler(self, handler)

    @property
    def on_show(self) -> callable:
        """The handler to invoke if the window is shown from a hidden state."""
        return self._on_show

    @on_show.setter
    def on_show(self, handler):
        self._on_show = wrapped_handler(self, handler)

    @property
    def on_hide(self) -> callable:
        """The handler to invoke if the window is hidden from a visible state."""
        return self._on_hide

    @on_hide.setter
    def on_hide(self, handler):
        self._on_hide = wrapped_handler(self, handler)

    ######################################################################
    # 2024-06: Backwards compatibility for <= 0.4.5
    ######################################################################

    def info_dialog(
        self,
        title: str,
        message: str,
        on_result: DialogResultHandler[None] | None = None,
    ) -> Dialog:
        """**DEPRECATED** - await :meth:`dialog` with an :any:`InfoDialog`"""
        warnings.warn(
            "info_dialog(...) has been deprecated; use dialog(toga.InfoDialog(...))",
            DeprecationWarning,
            stacklevel=2,
        )

        result = Dialog(
            self,
            on_result=wrapped_handler(self, on_result) if on_result else None,
        )
        result.dialog = dialogs.InfoDialog(title, message)
        result.dialog._impl.show(self, result)
        return result

    def question_dialog(
        self,
        title: str,
        message: str,
        on_result: DialogResultHandler[bool] | None = None,
    ) -> Dialog:
        """**DEPRECATED** - await :meth:`dialog` with a :any:`QuestionDialog`"""
        warnings.warn(
            (
                "question_dialog(...) has been deprecated; "
                "use dialog(toga.QuestionDialog(...))"
            ),
            DeprecationWarning,
            stacklevel=2,
        )

        result = Dialog(
            self,
            on_result=wrapped_handler(self, on_result) if on_result else None,
        )
        result.dialog = dialogs.QuestionDialog(title, message)
        result.dialog._impl.show(self, result)
        return result

    def confirm_dialog(
        self,
        title: str,
        message: str,
        on_result: DialogResultHandler[bool] | None = None,
    ) -> Dialog:
        """**DEPRECATED** - await :meth:`dialog` with a :any:`ConfirmDialog`"""
        warnings.warn(
            (
                "confirm_dialog(...) has been deprecated; "
                "use dialog(toga.ConfirmDialog(...))"
            ),
            DeprecationWarning,
            stacklevel=2,
        )

        result = Dialog(
            self,
            on_result=wrapped_handler(self, on_result) if on_result else None,
        )
        result.dialog = dialogs.ConfirmDialog(title, message)
        result.dialog._impl.show(self, result)
        return result

    def error_dialog(
        self,
        title: str,
        message: str,
        on_result: DialogResultHandler[None] | None = None,
    ) -> Dialog:
        """**DEPRECATED** - await :meth:`dialog` with an :any:`ErrorDialog`"""
        warnings.warn(
            "error_dialog(...) has been deprecated; use dialog(toga.ErrorDialog(...))",
            DeprecationWarning,
            stacklevel=2,
        )

        result = Dialog(
            self,
            on_result=wrapped_handler(self, on_result) if on_result else None,
        )
        result.dialog = dialogs.ErrorDialog(title, message)
        result.dialog._impl.show(self, result)
        return result

    def stack_trace_dialog(
        self,
        title: str,
        message: str,
        content: str,
        retry: bool = False,
        on_result: DialogResultHandler[bool] | DialogResultHandler[None] | None = None,
    ) -> Dialog:
        """**DEPRECATED** - await :meth:`dialog` with a :any:`StackTraceDialog`"""
        warnings.warn(
            (
                "stack_trace_dialog(...) has been deprecated; "
                "use dialog(toga.StackTraceDialog(...))"
            ),
            DeprecationWarning,
            stacklevel=2,
        )

        result = Dialog(
            self,
            on_result=wrapped_handler(self, on_result) if on_result else None,
        )
        result.dialog = dialogs.StackTraceDialog(
            title,
            message=message,
            content=content,
            retry=retry,
        )
        result.dialog._impl.show(self, result)
        return result

    def save_file_dialog(
        self,
        title: str,
        suggested_filename: Path | str,
        file_types: list[str] | None = None,
        on_result: DialogResultHandler[Path | None] | None = None,
    ) -> Dialog:
        """**DEPRECATED** - await :meth:`dialog` with a :any:`SaveFileDialog`"""
        warnings.warn(
            (
                "save_file_dialog(...) has been deprecated; "
                "use dialog(toga.SaveFileDialog(...))"
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        result = Dialog(
            self,
            on_result=wrapped_handler(self, on_result) if on_result else None,
        )
        result.dialog = dialogs.SaveFileDialog(
            title,
            suggested_filename=suggested_filename,
            file_types=file_types,
        )
        result.dialog._impl.show(self, result)
        return result

    def open_file_dialog(
        self,
        title: str,
        initial_directory: Path | str | None = None,
        file_types: list[str] | None = None,
        multiple_select: bool = False,
        on_result: (
            DialogResultHandler[list[Path]]
            | DialogResultHandler[Path]
            | DialogResultHandler[None]
            | None
        ) = None,
    ) -> Dialog:
        """**DEPRECATED** - await :meth:`dialog` with an :any:`OpenFileDialog`"""
        warnings.warn(
            (
                "open_file_dialog(...) has been deprecated; "
                "use dialog(toga.OpenFileDialog(...))"
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        result = Dialog(
            self,
            on_result=wrapped_handler(self, on_result) if on_result else None,
        )
        result.dialog = dialogs.OpenFileDialog(
            title,
            initial_directory=initial_directory,
            file_types=file_types,
            multiple_select=multiple_select,
        )
        result.dialog._impl.show(self, result)
        return result

    def select_folder_dialog(
        self,
        title: str,
        initial_directory: Path | str | None = None,
        multiple_select: bool = False,
        on_result: (
            DialogResultHandler[list[Path]]
            | DialogResultHandler[Path]
            | DialogResultHandler[None]
            | None
        ) = None,
    ) -> Dialog:
        """**DEPRECATED** - await :meth:`dialog` with a :any:`SelectFolderDialog`"""
        warnings.warn(
            (
                "select_folder_dialog(...) has been deprecated; "
                "use dialog(toga.SelectFolderDialog(...))"
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        result = Dialog(
            self,
            on_result=wrapped_handler(self, on_result) if on_result else None,
        )
        result.dialog = dialogs.SelectFolderDialog(
            title,
            initial_directory=initial_directory,
            multiple_select=multiple_select,
        )
        result.dialog._impl.show(self, result)
        return result

    ######################################################################
    # End backwards compatibility
    ######################################################################

    ######################################################################
    # 2024-10: Backwards compatibility for < 0.5.0
    ######################################################################
    @property
    def full_screen(self) -> bool:
        """**DEPRECATED** – Use :any:`Window.state`."""
        warnings.warn(
            "`Window.full_screen` is deprecated. Use `Window.state` instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return bool(self.state == WindowState.FULLSCREEN)

    @full_screen.setter
    def full_screen(self, is_full_screen: bool) -> None:
        warnings.warn(
            "`Window.full_screen` is deprecated. Use `Window.state` instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        target_state = WindowState.FULLSCREEN if is_full_screen else WindowState.NORMAL
        if self.state != target_state:
            self._impl.set_window_state(target_state)

    ######################################################################
    # End Backwards compatibility
    ######################################################################


class MainWindow(Window):
    _WINDOW_CLASS = "MainWindow"

    def __init__(self, *args, **kwargs):
        """Create a new Main Window.

        Accepts the same arguments as :class:`~toga.Window`.
        """
        super().__init__(*args, **kwargs)

        # Create a toolbar that is linked to the app.
        self._toolbar = CommandSet(app=self.app)

        # If the window has been created during startup(), we don't want to
        # install a change listener yet, as the startup process may install
        # additional commands - we want to wait until startup is complete,
        # create the initial state of the menus and toolbars, and then add a
        # change listener. However, if startup *has* completed, we can install a
        # change listener immediately, and trigger the creation of menus and
        # toolbars.
        if self.app.commands.on_change:
            self._toolbar.on_change = self._impl.create_toolbar

            self._impl.create_menus()
            self._impl.create_toolbar()

    @property
    def toolbar(self) -> CommandSet:
        """Toolbar for the window."""
        return self._toolbar


class WindowSet(MutableSet[Window]):
    def __init__(self, app: App):
        """A collection of windows managed by an app.

        A window is automatically added to the app when it is created, and removed when
        it is closed. Adding a window to an App's window set automatically sets the
        :attr:`~toga.Window.app` property of the Window.
        """
        self.app = app
        self.elements: set[Window] = set()

    def add(self, window: Window) -> None:
        if not isinstance(window, Window):
            raise TypeError("Can only add objects of type toga.Window")
        # Silently not add if duplicate
        if window not in self.elements:
            self.elements.add(window)
            window.app = self.app

    def discard(self, window: Window) -> None:
        if not isinstance(window, Window):
            raise TypeError("Can only discard objects of type toga.Window")
        if window not in self.elements:
            raise ValueError(f"{window!r} is not part of this app")
        self.elements.remove(window)

    def __iter__(self) -> Iterator[Window]:
        return iter(self.elements)

    def __contains__(self, value: object) -> bool:
        return value in self.elements

    def __len__(self) -> int:
        return len(self.elements)
