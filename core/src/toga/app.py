from __future__ import annotations

import asyncio
import importlib.metadata
import signal
import sys
import warnings
import webbrowser
from collections.abc import (
    Collection,
    ItemsView,
    Iterator,
    KeysView,
    Mapping,
    MutableSet,
    ValuesView,
)
from email.message import Message
from pathlib import Path
from typing import TYPE_CHECKING, Any, Protocol
from warnings import warn
from weakref import WeakValueDictionary

from toga.command import Command, CommandSet
from toga.documents import Document
from toga.handlers import wrapped_handler
from toga.hardware.camera import Camera
from toga.icons import Icon
from toga.paths import Paths
from toga.platform import get_platform_factory
from toga.screens import Screen
from toga.widgets.base import Widget
from toga.window import MainWindow, Window

if TYPE_CHECKING:
    from toga.icons import IconContent

# Make sure deprecation warnings are shown by default
warnings.filterwarnings("default", category=DeprecationWarning)


class AppStartupMethod(Protocol):
    def __call__(self, app: App, **kwargs: Any) -> Widget:
        """The startup method of the app.

        Called during app startup to set the initial main window content.

        :param app: The app instance that is starting.
        :param kwargs: Ensures compatibility with additional arguments introduced in
            future versions.
        :returns: The widget to use as the main window content.
        """
        ...


class OnExitHandler(Protocol):
    def __call__(self, app: App, **kwargs: Any) -> bool:
        """A handler to invoke when the app is about to exit.

        The return value of this callback controls whether the app is allowed to exit.
        This can be used to prevent the app exiting with unsaved changes, etc.

        :param app: The app instance that is exiting.
        :param kwargs: Ensures compatibility with additional arguments introduced in
            future versions.
        :returns: ``True`` if the app is allowed to exit; ``False`` if the app is not
            allowed to exit.
        """
        ...


class BackgroundTask(Protocol):
    def __call__(self, app: App, **kwargs: Any) -> None:
        """Code that should be executed as a background task.

        :param app: The app that is handling the background task.
        :param kwargs: Ensures compatibility with additional arguments introduced in
            future versions.
        """
        ...


class WindowSet(MutableSet):
    def __init__(self, app: App):
        """A collection of windows managed by an app.

        A window is automatically added to the app when it is created, and removed when
        it is closed. Adding a window to an App's window set automatically sets the
        :attr:`~toga.Window.app` property of the Window.
        """
        self.app = app
        self.elements = set()

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

    def __iadd__(self, window: Window) -> None:
        # The standard set type does not have a += operator.
        warn(
            "Windows are automatically associated with the app; += is not required",
            DeprecationWarning,
            stacklevel=2,
        )
        return self

    def __isub__(self, other: Window) -> None:
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

    def __iter__(self) -> Iterator:
        return iter(self.elements)

    def __contains__(self, value: Window) -> bool:
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

    def __init__(self, *args, **kwargs):
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
        return (
            "{"
            + ", ".join(f"{k!r}: {v!r}" for k, v in sorted(self._registry.items()))
            + "}"
        )

    def items(self) -> ItemsView:
        return self._registry.items()

    def keys(self) -> KeysView:
        return self._registry.keys()

    def values(self) -> ValuesView:
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


class App:
    #: The currently running :class:`~toga.App`. Since there can only be one running
    #: Toga app in a process, this is available as a class property via ``toga.App.app``.
    app: App = None

    #: A constant that can be used as the main window to indicate that an app will
    #: run in the background without a main window.
    BACKGROUND = object()

    def __init__(
        self,
        formal_name: str | None = None,
        app_id: str | None = None,
        app_name: str | None = None,
        *,
        icon: IconContent | None = None,
        author: str | None = None,
        version: str | None = None,
        home_page: str | None = None,
        description: str | None = None,
        startup: AppStartupMethod | None = None,
        on_exit: OnExitHandler | None = None,
        document_types: dict[str, type[Document]] = None,
        id=None,  # DEPRECATED
        windows=None,  # DEPRECATED
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
        :param icon: The :any:`icon <IconContent>` for the app. If not provided, Toga
            will attempt to load an icon from ``resources/app_name``, where ``app_name``
            is defined above. If no resource matching this name can be found, a warning
            will be printed, and the app will fall back to a default icon.
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
        :param document_types: A mapping of document types managed by this app, to
            the :any:`Document` class managing that document type.
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
            self._app_id = self.metadata.get("App-ID", None)
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

        # If an icon (or icon name) has been explicitly provided, use it;
        # otherwise, the icon will be based on the distribution name.
        if icon:
            self.icon = icon
        else:
            self.icon = f"resources/{app_name}"

        self.on_exit = on_exit

        # Set up the document types and list of documents being managed.
        self._document_types = document_types
        self._documents = []

        # We need the command set to exist so that startup et al can add commands;
        # but we don't have an impl yet, so we can't set the on_change handler
        self._commands = CommandSet()

        self._startup_method = startup

        self._windows = WindowSet(self)

        self._full_screen_windows = None

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

        Can be specified as any valid :any:`icon content <IconContent>`.

        When setting the icon, you can provide either an :any:`Icon` instance, or a
        path that will be passed to the ``Icon`` constructor.
        """
        return self._icon

    @icon.setter
    def icon(self, icon_or_name: IconContent | None) -> None:
        if isinstance(icon_or_name, Icon):
            self._icon = icon_or_name
        else:
            self._icon = Icon(icon_or_name)

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
    def main_window(self) -> MainWindow:
        """The main window for the app."""
        try:
            return self._main_window
        except AttributeError:
            raise ValueError("Application has not set a main window.")

    @main_window.setter
    def main_window(self, window: MainWindow) -> None:
        if window is None or window == App.BACKGROUND or isinstance(window, Window):
            # If the app has a main window, it must be closable
            if isinstance(window, Window) and not window.closable:
                raise ValueError("The window used as the main window must be closable.")

            self._main_window = window
            self._impl.set_main_window(window)
        else:
            raise ValueError(f"Don't know how to use {window} as a main window")

    def _startup(self):
        # Invoke the user's startup method (or the default implementation...
        self.startup()

        # ... then validate that startup requirements have been met.
        # Accessing the main window attribute will raise an exception if the app hasn't
        # defined a main window
        _ = self.main_window

        # The App's impl is created when the app is constructed; however, on some
        # platforms, (GTK, Windows), there are some activities that can't happen until
        # the app manifests in some way (usually as a result of the app loop starting).
        # Call the impl to allow for this finalization activity.
        self._impl.finalize()

        # Now that we have a finalized impl, set the on_change handler for commands
        self.commands.on_change = self._impl.create_menus

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
    def commands(self) -> MutableSet[Command]:
        """The commands available in the app."""
        return self._commands

    @property
    def document_types(self) -> dict[str, type[Document]]:
        """The document types this app can manage.

        A dictionary of file extensions, without leading dots, mapping to the
        :class:`toga.Document` subclass that will be created when a document with that
        extension is opened.
        """
        return self._document_types

    @property
    def documents(self) -> list[Document]:
        """The list of documents associated with this app."""
        return self._documents

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
    def widgets(self) -> Mapping[str, Widget]:
        """The widgets managed by the app, over all windows.

        Can be used to look up widgets by ID over the entire app (e.g.,
        ``app.widgets["my_id"]``).

        Only returns widgets that are currently part of a layout. A widget that has been
        created, but not assigned as part of window content will not be returned by
        widget lookup.
        """
        return self._widgets

    @property
    def windows(self) -> Collection[Window]:
        """The windows managed by the app. Windows are automatically added to the app
        when they are created, and removed when they are closed."""
        return self._windows

    ######################################################################
    # App capabilities
    ######################################################################

    def _new(self, document_type: type[Document]) -> Document:
        """Create a new document, and show the document window.

        Users can define a ``new()`` method to override this method.

        :param document_type: The document type to create.
        :returns: The newly created document
        """
        document = document_type(app=self)
        self._documents.append(document)
        document.show()

        return document

    def _open(self, path: Path) -> Document:
        """Open a document in this app, and show the document window.

        :param path: The path to the document to be opened.
        :returns: The document that has been opened
        :raises ValueError: If the document is of a type that can't be opened. Backends can
            suppress this exception if necessary to presere platform-native behavior.
        """
        try:
            DocType = self.document_types[path.suffix[1:]]
        except KeyError:
            raise ValueError(f"Don't know how to open documents of type {path.suffix}")
        else:
            document = DocType(app=self)
            document.open(path)

            self._documents.append(document)
            document.show()

        return document

    def about(self) -> None:
        """Display the About dialog for the app.

        Default implementation shows a platform-appropriate about dialog using app
        metadata. Override if you want to display a custom About dialog.
        """
        self._impl.show_about_dialog()

    def beep(self) -> None:
        """Play the default system notification sound."""
        self._impl.beep()

    def _can_save(self) -> bool:
        return self.current_window is not None and hasattr(self.current_window, "doc")

    def can_save(self) -> bool:
        """Can the application currently save?

        This controls the activation status of the Save menu items, if present.

        By default, save is enabled if the current window has a ``doc`` attribute. The
        object stored at this attribute must have a ``save()`` method. Apps can override
        this method if they wish; this is strongly advised if the app provides a custom
        ``save()`` method.
        """
        return self._can_save()

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
    def current_window(self, window: Window):
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
        def cleanup(app, should_exit):
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
    def windows(self, windows):
        if windows is not self._windows:
            raise AttributeError("can't set attribute 'windows'")

    ######################################################################
    # End backwards compatibility
    ######################################################################


class DocumentApp(App):
    def __init__(self, *args, **kwargs):
        """**DEPRECATED** - :any:`toga.DocumentApp` can be replaced with
        :any:`toga.App`."""
        warn(
            "toga.DocumentApp is no longer required. Use toga.App instead",
            DeprecationWarning,
            stacklevel=2,
        )

        super().__init__(*args, **kwargs)
