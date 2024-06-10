from __future__ import annotations

import asyncio
import importlib.metadata
import signal
import sys
import warnings
import webbrowser
from collections.abc import Iterator
from email.message import Message
from pathlib import Path
from typing import TYPE_CHECKING, Any, MutableSet, Protocol
from warnings import warn
from weakref import WeakValueDictionary

from toga.command import CommandSet
from toga.documents import Document
from toga.handlers import wrapped_handler
from toga.hardware.camera import Camera
from toga.hardware.location import Location
from toga.icons import Icon
from toga.paths import Paths
from toga.platform import get_platform_factory
from toga.screens import Screen
from toga.types import Position, Size
from toga.widgets.base import Widget
from toga.window import OnCloseHandler, Window

if TYPE_CHECKING:
    from toga.icons import IconContentT
    from toga.types import PositionT, SizeT

# Make sure deprecation warnings are shown by default
warnings.filterwarnings("default", category=DeprecationWarning)


class AppStartupMethod(Protocol):
    def __call__(self, app: App, /, **kwargs: Any) -> Widget:
        """The startup method of the app.

        Called during app startup to set the initial main window content.

        :param app: The app instance that is starting.
        :param kwargs: Ensures compatibility with additional arguments introduced in
            future versions.
        :returns: The widget to use as the main window content.
        """


class OnExitHandler(Protocol):
    def __call__(self, app: App, /, **kwargs: Any) -> bool:
        """A handler to invoke when the app is about to exit.

        The return value of this callback controls whether the app is allowed to exit.
        This can be used to prevent the app exiting with unsaved changes, etc.

        :param app: The app instance that is exiting.
        :param kwargs: Ensures compatibility with additional arguments introduced in
            future versions.
        :returns: ``True`` if the app is allowed to exit; ``False`` if the app is not
            allowed to exit.
        """


class BackgroundTask(Protocol):
    def __call__(self, app: App, /, **kwargs: Any) -> object:
        """Code that should be executed as a background task.

        :param app: The app that is handling the background task.
        :param kwargs: Ensures compatibility with additional arguments introduced in
            future versions.
        """


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

    ######################################################################
    # 2023-10: Backwards compatibility
    ######################################################################

    def __iadd__(self, window: Window) -> WindowSet:
        # The standard set type does not have a += operator.
        warn(
            "Windows are automatically associated with the app; += is not required",
            DeprecationWarning,
            stacklevel=2,
        )
        return self

    def __isub__(self, other: Window) -> WindowSet:
        # The standard set type does have a -= operator, but it takes sets rather than
        # individual items.
        warn(
            "Windows are automatically removed from the app; -= is not required",
            DeprecationWarning,
            stacklevel=2,
        )
        return self

    ######################################################################
    # End backwards compatibility
    ######################################################################

    def __iter__(self) -> Iterator[Window]:
        return iter(self.elements)

    def __contains__(self, value: object) -> bool:
        return value in self.elements

    def __len__(self) -> int:
        return len(self.elements)


class WidgetRegistry:
    # WidgetRegistry is implemented as a wrapper around a WeakValueDictionary, because
    # it provides a mapping from ID to widget. The mapping is weak so the registry
    # doesn't retain a strong reference to the widget, preventing memory cleanup.
    #
    # The lookup methods (__getitem__(), __iter__(), __len()__, keys(), items(), and
    # values()) are all proxied to underlying data store. Private methods exist for
    # internal use, but those methods shouldn't be used by end-users.

    def __init__(self, *args: Any, **kwargs: Any):
        self._registry = WeakValueDictionary(*args, **kwargs)

    def __len__(self) -> int:
        return len(self._registry)

    def __getitem__(self, key: str) -> Widget:
        return self._registry[key]

    def __contains__(self, key: str) -> bool:
        return key in self._registry

    def __iter__(self) -> Iterator[Widget]:
        return self.values()

    def __repr__(self) -> str:
        return f"{{{', '.join(f'{k!r}: {v!r}' for k, v in sorted(self._registry.items()))}}}"

    def items(self) -> Iterator[tuple[str, Widget]]:
        return self._registry.items()

    def keys(self) -> Iterator[str]:
        return self._registry.keys()

    def values(self) -> Iterator[Widget]:
        return self._registry.values()

    # Private methods for internal use
    def _update(self, widgets: list[Widget]) -> None:
        for widget in widgets:
            self._add(widget)

    def _add(self, widget: Widget) -> None:
        if widget.id in self._registry:
            # Prevent adding the same widget twice or adding 2 widgets with the same id
            raise KeyError(f"There is already a widget with the id {widget.id!r}")
        self._registry[widget.id] = widget

    def _remove(self, id: str) -> None:
        del self._registry[id]


class MainWindow(Window):
    _WINDOW_CLASS = "MainWindow"

    def __init__(
        self,
        id: str | None = None,
        title: str | None = None,
        position: PositionT = Position(100, 100),
        size: SizeT = Size(640, 480),
        resizable: bool = True,
        minimizable: bool = True,
        content: Widget | None = None,
        resizeable: None = None,  # DEPRECATED
        closeable: None = None,  # DEPRECATED
    ):
        """Create a new main window.

        :param id: A unique identifier for the window. If not provided, one will be
            automatically generated.
        :param title: Title for the window. Defaults to the formal name of the app.
        :param position: Position of the window, as a :any:`toga.Position` or tuple of
            ``(x, y)`` coordinates, in :ref:`CSS pixels <css-units>`.
        :param size: Size of the window, as a :any:`toga.Size` or tuple of ``(width,
            height)``, in :ref:`CSS pixels <css-units>`.
        :param resizable: Can the window be resized by the user?
        :param minimizable: Can the window be minimized by the user?
        :param content: The initial content for the window.
        :param resizeable: **DEPRECATED** - Use ``resizable``.
        :param closeable: **DEPRECATED** - Use ``closable``.
        """
        super().__init__(
            id=id,
            title=title,
            position=position,
            size=size,
            resizable=resizable,
            closable=True,
            minimizable=minimizable,
            content=content,
            # Deprecated arguments
            resizeable=resizeable,
            closeable=closeable,
        )

    @property
    def _default_title(self) -> str:
        return App.app.formal_name

    @property
    def on_close(self) -> None:
        """The handler to invoke before the window is closed in response to a user
        action.

        Always returns ``None``. Main windows should use :meth:`toga.App.on_exit`,
        rather than ``on_close``.

        :raises ValueError: if an attempt is made to set the ``on_close`` handler.
        """
        return None

    @on_close.setter
    def on_close(self, handler: OnCloseHandler | None) -> None:
        if handler:
            raise ValueError(
                "Cannot set on_close handler for the main window. "
                "Use the app on_exit handler instead."
            )


class DocumentMainWindow(Window):
    def __init__(
        self,
        doc: Document,
        id: str | None = None,
        title: str | None = None,
        position: PositionT = Position(100, 100),
        size: SizeT = Size(640, 480),
        resizable: bool = True,
        minimizable: bool = True,
    ):
        """Create a new document Main Window.

        This installs a default on_close handler that honors platform-specific document
        closing behavior. If you want to control whether a document is allowed to close
        (e.g., due to having unsaved change), override
        :meth:`toga.Document.can_close()`, rather than implementing an on_close handler.

        :param doc: The document being managed by this window
        :param id: The ID of the window.
        :param title: Title for the window. Defaults to the formal name of the app.
        :param position: Position of the window, as a :any:`toga.Position` or tuple of
            ``(x, y)`` coordinates.
        :param size: Size of the window, as a :any:`toga.Size` or tuple of
            ``(width, height)``, in pixels.
        :param resizable: Can the window be manually resized by the user?
        :param minimizable: Can the window be minimized by the user?
        """
        self.doc = doc
        super().__init__(
            id=id,
            title=title,
            position=position,
            size=size,
            resizable=resizable,
            closable=True,
            minimizable=minimizable,
            on_close=doc.handle_close,
        )

    @property
    def _default_title(self) -> str:
        return self.doc.path.name


class App:
    #: The currently running :class:`~toga.App`. Since there can only be one running
    #: Toga app in a process, this is available as a class property via ``toga.App.app``.
    app: App
    _impl: Any
    _camera: Camera
    _location: Location

    def __init__(
        self,
        formal_name: str | None = None,
        app_id: str | None = None,
        app_name: str | None = None,
        *,
        icon: IconContentT | None = None,
        author: str | None = None,
        version: str | None = None,
        home_page: str | None = None,
        description: str | None = None,
        startup: AppStartupMethod | None = None,
        on_exit: OnExitHandler | None = None,
        id: None = None,  # DEPRECATED
        windows: None = None,  # DEPRECATED
    ):
        """Create a new App instance.

        Once the app has been created, you should invoke the
        :meth:`~toga.App.main_loop()` method, which will start the event loop of your
        App.

        :param formal_name: The human-readable name of the app. If not provided, the
            metadata key ``Formal-Name`` must be present.
        :param app_id: The unique application identifier. This will usually be a
            reversed domain name, e.g. ``org.beeware.myapp``. If not provided, the
            metadata key ``App-ID`` must be present.
        :param app_name: The name of the distribution used to load metadata with
            :any:`importlib.metadata`. If not provided, the following will be tried in
            order:

            #. If the ``__main__`` module is contained in a package, that package's name
               will be used.
            #. If the ``app_id`` argument was provided, its last segment will be used.
               For example, an ``app_id`` of ``com.example.my-app`` would yield a
               distribution name of ``my-app``.
            #. As a last resort, the name ``toga``.
        :param icon: The :any:`icon <IconContentT>` for the app. Defaults to
            :attr:`toga.Icon.APP_ICON`.
        :param author: The person or organization to be credited as the author of the
            app. If not provided, the metadata key ``Author`` will be used.
        :param version: The version number of the app.  If not provided, the metadata
            key ``Version`` will be used.
        :param home_page: The URL of a web page for the app. Used in auto-generated help
            menu items. If not provided, the metadata key ``Home-page`` will be used.
        :param description: A brief (one line) description of the app. If not provided,
            the metadata key ``Summary`` will be used.
        :param startup: A callable to run before starting the app.
        :param on_exit: The initial :any:`on_exit` handler.
        :param id: **DEPRECATED** - This argument will be ignored. If you need a
            machine-friendly identifier, use ``app_id``.
        :param windows: **DEPRECATED** – Windows are now automatically added to the
            current app. Passing this argument will cause an exception.
        """
        ######################################################################
        # 2023-10: Backwards compatibility
        ######################################################################
        if id is not None:
            warn(
                "App.id is deprecated and will be ignored. Use app_id instead",
                DeprecationWarning,
                stacklevel=2,
            )

        if windows is not None:
            raise ValueError(
                "The `windows` constructor argument of toga.App has been removed. "
                "Windows are now automatically added to the current app."
            )
        ######################################################################
        # End backwards compatibility
        ######################################################################

        # Initialize empty widgets registry
        self._widgets = WidgetRegistry()

        # Keep an accessible copy of the app singleton instance
        App.app = self

        # We need a distribution name to load app metadata.
        if app_name is None:
            # If the code is contained in appname.py, and you start the app using
            # `python -m appname`, then __main__.__package__ will be an empty string.
            #
            # If the code is contained in appname.py, and you start the app using
            # `python appname.py`, then __main__.__package__ will be None.
            #
            # If the code is contained in appname/__main__.py, and you start the app
            # using `python -m appname`, then __main__.__package__ will be "appname".
            try:
                main_module_pkg = sys.modules["__main__"].__package__
                if main_module_pkg:
                    app_name = main_module_pkg
            except KeyError:
                # If there's no __main__ module, we're probably in a test.
                pass

        # Try deconstructing the distribution name from the app ID
        if (app_name is None) and app_id:
            app_name = app_id.split(".")[-1]

        # If we still don't have a distribution name, fall back to ``toga`` as a
        # last resort.
        if app_name is None:
            app_name = "toga"

        # Try to load the app metadata with our best guess of the distribution name.
        self._app_name = app_name
        try:
            self.metadata = importlib.metadata.metadata(app_name)
        except importlib.metadata.PackageNotFoundError:
            self.metadata = Message()

        # If a formal name has been provided, use it; otherwise, look to
        # the metadata. However, a formal name *must* be provided.
        if formal_name:
            self._formal_name = formal_name
        else:
            self._formal_name = self.metadata.get("Formal-Name")
        if self._formal_name is None:
            raise RuntimeError("Toga application must have a formal name")

        # If an app_id has been provided, use it; otherwise, look to
        # the metadata. However, an app_id *must* be provided
        if app_id:
            self._app_id = app_id
        else:
            self._app_id = self.metadata.get("App-ID")
        if self._app_id is None:
            raise RuntimeError("Toga application must have an app ID")

        # Other metadata may be passed to the constructor, or loaded with importlib.
        if author:
            self._author = author
        else:
            self._author = self.metadata.get("Author", None)

        if version:
            self._version = version
        else:
            self._version = self.metadata.get("Version", None)

        if home_page:
            self._home_page = home_page
        else:
            self._home_page = self.metadata.get("Home-page", None)

        if description:
            self._description = description
        else:
            self._description = self.metadata.get("Summary", None)

        # Get a platform factory.
        self.factory = get_platform_factory()

        # Instantiate the paths instance for this app.
        self._paths = Paths()

        if icon is None:
            self.icon = Icon.APP_ICON
        else:
            self.icon = icon

        self.on_exit = on_exit

        # We need the command set to exist so that startup et al. can add commands;
        # but we don't have an impl yet, so we can't set the on_change handler
        self._commands = CommandSet()

        self._startup_method = startup

        self._main_window: MainWindow | None = None
        self._windows = WindowSet(self)

        self._full_screen_windows: tuple[Window, ...] | None = None

        self._create_impl()

        # Now that we have an impl, set the on_change handler for commands
        self.commands.on_change = self._impl.create_menus

    def _create_impl(self) -> None:
        self.factory.App(interface=self)

    ######################################################################
    # App properties
    ######################################################################

    @property
    def app_name(self) -> str:
        """The name of the distribution used to load metadata with
        :any:`importlib.metadata` (read-only)."""
        return self._app_name

    @property
    def app_id(self) -> str:
        """The unique application identifier (read-only). This will usually be a
        reversed domain name, e.g. ``org.beeware.myapp``.
        """
        return self._app_id

    @property
    def author(self) -> str | None:
        """The person or organization to be credited as the author of the app
        (read-only)."""
        return self._author

    @property
    def description(self) -> str | None:
        """A brief (one line) description of the app (read-only)."""
        return self._description

    @property
    def formal_name(self) -> str:
        """The human-readable name of the app (read-only)."""
        return self._formal_name

    @property
    def home_page(self) -> str | None:
        """The URL of a web page for the app (read-only). Used in auto-generated help
        menu items."""
        return self._home_page

    @property
    def icon(self) -> Icon:
        """The Icon for the app.

        Can be specified as any valid :any:`icon content <IconContentT>`.
        """
        return self._icon

    @icon.setter
    def icon(self, icon_or_name: IconContentT) -> None:
        if isinstance(icon_or_name, Icon):
            self._icon = icon_or_name
        else:
            self._icon = Icon(icon_or_name)

        try:
            self._impl.set_icon(self._icon)
        except AttributeError:
            # The first time the icon is set, it is *before* the impl has been created,
            # so that the app instance can be instantiated with the correct icon.
            pass

    @property
    def id(self) -> str:
        """**DEPRECATED** – Use :any:`app_id`."""
        warn(
            "App.id is deprecated. Use app_id instead", DeprecationWarning, stacklevel=2
        )
        return self._app_id

    @property
    def version(self) -> str | None:
        """The version number of the app (read-only)."""
        return self._version

    @property
    def is_bundled(self) -> bool:
        """Has the app been bundled as a standalone binary, or is it running as a Python script?"""
        return Path(sys.executable).stem not in {
            "python",
            f"python{sys.version_info.major}",
            f"python{sys.version_info.major}.{sys.version_info.minor}",
        }

    ######################################################################
    # App lifecycle
    ######################################################################

    def add_background_task(self, handler: BackgroundTask) -> None:
        """Schedule a task to run in the background.

        Schedules a coroutine or a generator to run in the background. Control
        will be returned to the event loop during await or yield statements,
        respectively. Use this to run background tasks without blocking the
        GUI. If a regular callable is passed, it will be called as is and will
        block the GUI until the call returns.

        :param handler: A coroutine, generator or callable.
        """
        self.loop.call_soon_threadsafe(wrapped_handler(self, handler))

    def exit(self) -> None:
        """Exit the application gracefully.

        This *does not* invoke the ``on_exit`` handler; the app will be immediately
        and unconditionally closed.
        """
        self._impl.exit()

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        """The `event loop
        <https://docs.python.org/3/library/asyncio-eventloop.html>`__ of the app's main
        thread (read-only)."""
        return self._impl.loop

    def main_loop(self) -> None:
        """Start the application.

        On desktop platforms, this method will block until the application has exited.
        On mobile and web platforms, it returns immediately.
        """
        # Modify signal handlers to make sure Ctrl-C is caught and handled.
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        self._impl.main_loop()

    @property
    def main_window(self) -> MainWindow | None:
        """The main window for the app."""
        return self._main_window

    @main_window.setter
    def main_window(self, window: MainWindow | None) -> None:
        self._main_window = window
        self._impl.set_main_window(window)

    def _verify_startup(self) -> None:
        if not isinstance(self.main_window, MainWindow):
            raise ValueError(
                "Application does not have a main window. "
                "Does your startup() method assign a value to self.main_window?"
            )

    def _startup(self) -> None:
        # This is a wrapper around the user's startup method that performs any
        # post-setup validation.
        self.startup()
        self._verify_startup()

    def startup(self) -> None:
        """Create and show the main window for the application.

        Subclasses can override this method to define customized startup behavior;
        however, any override *must* ensure the :any:`main_window` has been assigned
        before it returns.
        """
        self.main_window = MainWindow(title=self.formal_name, id="main")

        if self._startup_method:
            self.main_window.content = self._startup_method(self)

        self.main_window.show()

    ######################################################################
    # App resources
    ######################################################################

    @property
    def camera(self) -> Camera:
        """A representation of the device's camera (or cameras)."""
        try:
            return self._camera
        except AttributeError:
            # Instantiate the camera instance for this app on first access
            # This will raise an exception if the platform doesn't implement
            # the Camera API.
            self._camera = Camera(self)
        return self._camera

    @property
    def commands(self) -> CommandSet:
        """The commands available in the app."""
        return self._commands

    @property
    def location(self) -> Location:
        """A representation of the device's location service."""
        try:
            return self._location
        except AttributeError:
            # Instantiate the location service for this app on first access
            # This will raise an exception if the platform doesn't implement
            # the Location API.
            self._location = Location(self)
        return self._location

    @property
    def paths(self) -> Paths:
        """Paths for platform-appropriate locations on the user's file system.

        Some platforms do not allow access to any file system location other than these
        paths. Even when arbitrary file access is allowed, there are preferred locations
        for each type of content.
        """
        return self._paths

    @property
    def screens(self) -> list[Screen]:
        """Returns a list of available screens."""
        return [screen.interface for screen in self._impl.get_screens()]

    @property
    def widgets(self) -> WidgetRegistry:
        """The widgets managed by the app, over all windows.

        Can be used to look up widgets by ID over the entire app (e.g.,
        ``app.widgets["my_id"]``).

        Only returns widgets that are currently part of a layout. A widget that has been
        created, but not assigned as part of window content will not be returned by
        widget lookup.
        """
        return self._widgets

    @property
    def windows(self) -> WindowSet:
        """The windows managed by the app. Windows are automatically added to the app
        when they are created, and removed when they are closed."""
        return self._windows

    ######################################################################
    # App capabilities
    ######################################################################

    def about(self) -> None:
        """Display the About dialog for the app.

        Default implementation shows a platform-appropriate about dialog using app
        metadata. Override if you want to display a custom About dialog.
        """
        self._impl.show_about_dialog()

    def beep(self) -> None:
        """Play the default system notification sound."""
        self._impl.beep()

    def visit_homepage(self) -> None:
        """Open the application's :any:`home_page` in the default browser.

        If the :any:`home_page` is ``None``, this is a no-op.
        """
        if self.home_page is not None:
            webbrowser.open(self.home_page)

    ######################################################################
    # Cursor control
    ######################################################################

    def hide_cursor(self) -> None:
        """Hide cursor from view."""
        self._impl.hide_cursor()

    def show_cursor(self) -> None:
        """Make the cursor visible."""
        self._impl.show_cursor()

    ######################################################################
    # Window control
    ######################################################################

    @property
    def current_window(self) -> Window | None:
        """Return the currently active window."""
        window = self._impl.get_current_window()
        if window is None:
            return None
        return window.interface

    @current_window.setter
    def current_window(self, window: Window) -> None:
        """Set a window into current active focus."""
        self._impl.set_current_window(window)

    ######################################################################
    # Full screen control
    ######################################################################

    def exit_full_screen(self) -> None:
        """Exit full screen mode."""
        if self.is_full_screen:
            self._impl.exit_full_screen(self._full_screen_windows)
            self._full_screen_windows = None

    @property
    def is_full_screen(self) -> bool:
        """Is the app currently in full screen mode?"""
        return self._full_screen_windows is not None

    def set_full_screen(self, *windows: Window) -> None:
        """Make one or more windows full screen.

        Full screen is not the same as "maximized"; full screen mode is when all window
        borders and other window decorations are no longer visible.

        :param windows: The list of windows to go full screen, in order of allocation to
            screens. If the number of windows exceeds the number of available displays,
            those windows will not be visible. If no windows are specified, the app will
            exit full screen mode.
        """
        self.exit_full_screen()
        if windows:
            self._impl.enter_full_screen(windows)
            self._full_screen_windows = windows

    ######################################################################
    # App events
    ######################################################################

    @property
    def on_exit(self) -> OnExitHandler:
        """The handler to invoke if the user attempts to exit the app."""
        return self._on_exit

    @on_exit.setter
    def on_exit(self, handler: OnExitHandler | None) -> None:
        def cleanup(app: App, should_exit: bool) -> None:
            if should_exit or handler is None:
                app.exit()

        self._on_exit = wrapped_handler(self, handler, cleanup=cleanup)

    ######################################################################
    # 2023-10: Backwards compatibility
    ######################################################################

    @property
    def name(self) -> str:
        """**DEPRECATED** – Use :any:`formal_name`."""
        warn(
            "App.name is deprecated. Use formal_name instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._formal_name

    # Support WindowSet __iadd__ and __isub__
    @windows.setter
    def windows(self, windows: WindowSet) -> None:
        if windows is not self._windows:
            raise AttributeError("can't set attribute 'windows'")

    ######################################################################
    # End backwards compatibility
    ######################################################################


class DocumentApp(App):
    def __init__(
        self,
        formal_name: str | None = None,
        app_id: str | None = None,
        app_name: str | None = None,
        *,
        icon: IconContentT | None = None,
        author: str | None = None,
        version: str | None = None,
        home_page: str | None = None,
        description: str | None = None,
        startup: AppStartupMethod | None = None,
        document_types: dict[str, type[Document]] | None = None,
        on_exit: OnExitHandler | None = None,
        id: None = None,  # DEPRECATED
    ):
        """Create a document-based application.

        A document-based application is the same as a normal application, with the
        exception that there is no main window. Instead, each document managed by the
        app will create and manage its own window (or windows).

        :param document_types: Initial :any:`document_types` mapping.
        """
        if document_types is None:
            raise ValueError("A document must manage at least one document type.")

        self._document_types = document_types
        self._documents: list[Document] = []

        super().__init__(
            formal_name=formal_name,
            app_id=app_id,
            app_name=app_name,
            icon=icon,
            author=author,
            version=version,
            home_page=home_page,
            description=description,
            startup=startup,
            on_exit=on_exit,
            id=id,
        )

    def _create_impl(self) -> None:
        self.factory.DocumentApp(interface=self)

    def _verify_startup(self) -> None:
        # No post-startup validation required for DocumentApps
        pass

    @property
    def document_types(self) -> dict[str, type[Document]]:
        """The document types this app can manage.

        A dictionary of file extensions, without leading dots, mapping to the
        :class:`toga.Document` subclass that will be created when a document with that
        extension is opened. The subclass must take exactly 2 arguments in its
        constructor: ``path`` and ``app``.
        """
        return self._document_types

    @property
    def documents(self) -> list[Document]:
        """The list of documents associated with this app."""
        return self._documents

    def startup(self) -> None:
        """No-op; a DocumentApp has no windows until a document is opened.

        Subclasses can override this method to define customized startup behavior.
        """

    def _open(self, path: Path) -> None:
        """Internal utility method; open a new document in this app, and shows the document.

        :param path: The path to the document to be opened.
        :raises ValueError: If the document is of a type that can't be opened. Backends can
            suppress this exception if necessary to preserve platform-native behavior.
        """
        try:
            DocType = self.document_types[path.suffix[1:]]
        except KeyError:
            raise ValueError(f"Don't know how to open documents of type {path.suffix}")
        else:
            document = DocType(path, app=self)
            self._documents.append(document)
            document.show()
