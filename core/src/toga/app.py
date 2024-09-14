from __future__ import annotations

import asyncio
import importlib.metadata
import signal
import sys
import warnings
import webbrowser
from collections.abc import Coroutine, Iterator
from email.message import Message
from pathlib import Path
from typing import TYPE_CHECKING, Any, Protocol
from weakref import WeakValueDictionary

from toga.command import Command, CommandSet
from toga.documents import Document, DocumentSet
from toga.handlers import simple_handler, wrapped_handler
from toga.hardware.camera import Camera
from toga.hardware.location import Location
from toga.icons import Icon
from toga.paths import Paths
from toga.platform import get_platform_factory
from toga.screens import Screen
from toga.statusicons import StatusIconSet
from toga.widgets.base import Widget
from toga.window import MainWindow, Window, WindowSet

if TYPE_CHECKING:
    from toga.dialogs import Dialog
    from toga.icons import IconContentT

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


class OnRunningHandler(Protocol):
    def __call__(self, app: App, /, **kwargs: Any) -> None:
        """A handler to invoke when the app event loop is running.

        :param app: The app instance that is running.
        :param kwargs: Ensures compatibility with additional arguments introduced in
            future versions.
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


class App:
    #: The currently running :class:`~toga.App`. Since there can only be one running
    #: Toga app in a process, this is available as a class property via ``toga.App.app``.
    app: App
    _impl: Any
    _camera: Camera
    _location: Location
    _main_window: Window | str | None
    _running_tasks: set[asyncio.Task] = set()

    #: A constant that can be used as the main window to indicate that an app will
    #: run in the background without a main window.
    BACKGROUND: str = "background app"

    _UNDEFINED: str = "<main window not assigned>"

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
        document_types: list[type[Document]] | None = None,
        on_running: OnRunningHandler | None = None,
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
        :param on_running: The initial :any:`on_running` handler.
        :param on_exit: The initial :any:`on_exit` handler.
        :param document_types: A list of :any:`Document` classes that this app
            can manage.
        :param id: **DEPRECATED** - This argument will be ignored. If you need a
            machine-friendly identifier, use ``app_id``.
        :param windows: **DEPRECATED** – Windows are now automatically added to the
            current app. Passing this argument will cause an exception.
        """
        ######################################################################
        # 2023-10: Backwards compatibility
        ######################################################################
        if id is not None:
            warnings.warn(
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

        # Set up the document types and collection of documents being managed.
        self._documents = DocumentSet(
            self,
            types=[] if document_types is None else document_types,
        )

        # Install the lifecycle handlers. If passed in as an argument, or assigned using
        # `app.on_event = my_handler`, the event handler will take the app as the first
        # argument. If we're using the default value, or we're subclassing app, the app
        # can be safely implied; so we wrap the method as a simple handler.
        if on_running:
            self.on_running = on_running
        else:
            self.on_running = simple_handler(self.on_running)

        if on_exit:
            self.on_exit = on_exit
        else:
            self.on_exit = simple_handler(self.on_exit)

        # We need the command set to exist so that startup et al. can add commands;
        # but we don't have an impl yet, so we can't set the on_change handler
        self._commands = CommandSet()
        self._status_icons = StatusIconSet()

        self._startup_method = startup

        self._main_window = App._UNDEFINED
        self._windows = WindowSet(self)

        self._full_screen_windows: tuple[Window, ...] | None = None

        # Create the implementation. This will trigger any startup logic.
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
        warnings.warn(
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

    def request_exit(self):
        """Request an exit from the application.

        This method will call the :meth:`~toga.App.on_exit` handler to confirm if the
        app should be allowed to exit; if that handler confirms the action, the app will
        exit.
        """

        def cleanup(app, should_exit):
            if should_exit:
                app.exit()

        # Wrap on_exit to ensure that an async handler is turned into a task,
        # then immediately invoke.
        wrapped_handler(self, self.on_exit, cleanup=cleanup)()

    def exit(self) -> None:
        """Unconditionally exit the application.

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

    def _install_task_factory_wrapper(self):
        """Wrap task creation to track pending and running tasks.

        When tasks are created, asyncio only maintains a weak reference to the task.
        This allows for the possibility that the garbage collector destroys the task
        in the midst of its execution. To avoid this, a strong reference is stored on
        the app and a task callback removes the reference after the task completes.
        Upstream issue tracked at python/cpython#91887.
        """
        platform_task_factory = self.loop.get_task_factory()

        def factory(loop, coro, context=None):
            if platform_task_factory is not None:
                if sys.version_info < (3, 11):
                    task = platform_task_factory(loop, coro)
                else:
                    task = platform_task_factory(loop, coro, context=context)
            else:
                if sys.version_info < (3, 11):
                    task = asyncio.Task(coro, loop=loop)
                else:
                    task = asyncio.Task(coro, loop=loop, context=context)

            self._running_tasks.add(task)
            task.add_done_callback(self._running_tasks.discard)
            return task

        self.loop.set_task_factory(factory)

    @property
    def main_window(self) -> Window | str | None:
        """The main window for the app.

        See :ref:`the documentation on assigning a main window <assigning-main-window>`
        for values that can be used for this attribute.
        """
        if self._main_window is App._UNDEFINED:
            raise ValueError("Application has not set a main window.")

        return self._main_window

    @main_window.setter
    def main_window(self, window: MainWindow | str | None) -> None:
        if window is None or window is App.BACKGROUND or isinstance(window, Window):
            # The main window must be closable
            if isinstance(window, Window) and not window.closable:
                raise ValueError("The window used as the main window must be closable.")

            old_window = self._main_window
            self._main_window = window
            try:
                self._impl.set_main_window(window)
            except Exception as e:
                # If the main window could not be changed, revert to the previous value
                # then reraise the exception
                if old_window is not App._UNDEFINED:
                    self._main_window = old_window
                raise e
        else:
            raise ValueError(f"Don't know how to use {window!r} as a main window.")

    def _open_initial_document(self, filename: Path | str) -> bool:
        """Internal utility method for opening a document provided at the command line.

        This is abstracted so that backends that have their own management of command
        line arguments can share the same error handling.

        :param filename: The filename passed as an argument, as a string.
        :returns: ``True`` if a document was successfully loaded; ``False`` otherwise.
        """
        try:
            self.documents.open(filename)
            return True
        except FileNotFoundError:
            print(f"Document {filename} not found")
            return False
        except Exception as e:
            print(f"{filename}: {e}")
            return False

    def _create_standard_commands(self):
        """Internal utility method to create the standard commands for the app."""
        for cmd_id in [
            Command.ABOUT,
            Command.EXIT,
            Command.VISIT_HOMEPAGE,
        ]:
            self.commands.add(Command.standard(self, cmd_id))

        if self.documents.types:
            default_document_type = self.documents.types[0]
            command = Command.standard(
                self,
                Command.NEW,
                action=simple_handler(self.documents.new, default_document_type),
            )
            if command:
                if len(self.documents.types) == 1:
                    # There's only 1 document type. The new command can be used as is.
                    self.commands.add(command)
                else:
                    # There's more than one document type. Create a new command for each
                    # document type, updating the title of the command to disambiguate,
                    # and modifying the shortcut, order and ID of the document types 2+
                    for i, document_class in enumerate(self.documents.types):
                        command = Command.standard(
                            self,
                            Command.NEW,
                            action=simple_handler(self.documents.new, document_class),
                        )
                        command.text = command.text + f" {document_class.description}"
                        if i > 0:
                            command.shortcut = None
                            command._id = f"{command.id}:{document_class.extensions[0]}"
                            command.order = command.order + i

                        self.commands.add(command)

            for cmd_id in [
                Command.OPEN,
                Command.SAVE,
                Command.SAVE_AS,
                Command.SAVE_ALL,
            ]:
                self.commands.add(Command.standard(self, cmd_id))

    def _create_initial_windows(self):
        """Internal utility method for creating initial windows based on command line
        arguments. This method is used when the platform doesn't provide its own
        command-line handling interface.

        If document types are defined, try to open every argument on the command line as
        a document (unless the backend manages the command line arguments).
        """
        # If the backend handles the command line, don't do any command line processing.
        if self._impl.HANDLES_COMMAND_LINE:
            return
        doc_count = len(self.windows)
        if self.documents.types:
            for filename in sys.argv[1:]:
                if self._open_initial_document(filename):
                    doc_count += 1

        # Safety check: Do we have at least one document?
        if self.main_window is None and doc_count == 0:
            try:
                # Pass in the first document type as the default
                default_doc_type = self.documents.types[0]
                self.documents.new(default_doc_type)
            except IndexError:
                # No document types defined.
                raise RuntimeError(
                    "App didn't create any windows, or register any document types."
                )

    def _startup(self) -> None:
        # Wrap the platform's event loop's task factory for task tracking
        self._install_task_factory_wrapper()

        # Install the standard commands. This is done *before* startup so the user's
        # code has the opportunity to remove/change the default commands.
        self._create_standard_commands()
        self._impl.create_standard_commands()

        # Install the standard status icon commands. Again, this is done *before* startup
        # so that the user's code can remove/change the defaults.
        self.status_icons._create_standard_commands()

        # Invoke the user's startup method (or the default implementation)
        self.startup()

        # Validate that the startup requirements have been met.
        # Accessing the main window attribute will raise an exception if the app hasn't
        # defined a main window.
        _ = self.main_window

        # Create any initial windows
        self._create_initial_windows()

        # Manifest the initial state of the menus. This will cascade down to all
        # open windows if the platform has window-based menus. Then install the
        # on-change handler for menus to respond to any future changes.
        self._impl.create_menus()
        self.commands.on_change = self._impl.create_menus

        # Manifest the initial state of the status icons, then install an on-change
        # handler so that any future changes will be reflected in the GUI.
        self.status_icons._impl.create()
        self.status_icons.commands.on_change = self.status_icons._impl.create

        # Manifest the initial state of toolbars (on the windows that have
        # them), then install a change listener so that any future changes to
        # the toolbar cause a change in toolbar items.
        for window in self.windows:
            if hasattr(window, "toolbar"):
                window._impl.create_toolbar()
                window.toolbar.on_change = window._impl.create_toolbar

        # Queue a task to run as soon as the event loop starts.
        self.loop.call_soon_threadsafe(wrapped_handler(self, self.on_running))

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
    def documents(self) -> DocumentSet:
        """The list of documents associated with this app."""
        return self._documents

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
    def status_icons(self) -> StatusIconSet:
        """The status icons displayed by the app."""
        return self._status_icons

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

    async def dialog(self, dialog: Dialog) -> Coroutine[None, None, Any]:
        """Display a dialog to the user in the app context.

        :param: The :doc:`dialog <resources/dialogs>` to display to the user.
        :returns: The result of the dialog.
        """
        return await dialog._show(None)

    def visit_homepage(self) -> None:
        """Open the application's :any:`home_page` in the default browser.

        This method is invoked as a handler by the "Visit homepage" default menu item.
        If the :any:`home_page` is ``None``, this is a no-op, and the default menu item
        will be disabled.
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

    def on_exit(self) -> bool:
        """The event handler that will be invoked when the app is about to exit.

        The return value of this method controls whether the app is allowed to exit.
        This can be used to prevent the app exiting with unsaved changes, etc.

        If necessary, the overridden method can be defined as an ``async`` coroutine.

        :returns: ``True`` if the app is allowed to exit; ``False`` if the app is not
            allowed to exit.
        """
        # Always allow exit
        return True

    def on_running(self) -> None:
        """The event handler that will be invoked when the app's event loop starts running.

        If necessary, the overridden method can be defined as an ``async`` coroutine.
        """

    ######################################################################
    # 2023-10: Backwards compatibility
    ######################################################################

    @property
    def name(self) -> str:
        """**DEPRECATED** – Use :any:`formal_name`."""
        warnings.warn(
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
    # 2024-06: Backwards compatibility
    ######################################################################

    def add_background_task(self, handler: BackgroundTask) -> None:
        """**DEPRECATED** – Use :any:`asyncio.create_task`, or override/assign
        :meth:`~toga.App.on_running`."""
        warnings.warn(
            "App.add_background_task is deprecated. Use asyncio.create_task(), "
            "or set an App.on_running() handler",
            DeprecationWarning,
            stacklevel=2,
        )

        self.loop.call_soon_threadsafe(wrapped_handler(self, handler))

    ######################################################################
    # End backwards compatibility
    ######################################################################


######################################################################
# 2024-08: Backwards compatibility
######################################################################


class DocumentApp(App):
    def __init__(self, *args, **kwargs):
        """**DEPRECATED** - :any:`toga.DocumentApp` can be replaced with
        :any:`toga.App`.
        """
        warnings.warn(
            "toga.DocumentApp is no longer required. Use toga.App instead",
            DeprecationWarning,
            stacklevel=2,
        )
        # Convert document types from dictionary format to list format.
        # The old API guaranteed that document_types was provided
        kwargs["document_types"] = list(kwargs["document_types"].values())

        super().__init__(*args, **kwargs)

    @property
    def document_types(self) -> dict[str, type[Document]]:
        """**DEPRECATED** - Use ``documents.types``; extensions can be
        obtained from the individual document classes itself.
        """
        warnings.warn(
            "App.document_types is deprecated. Use App.documents.types",
            DeprecationWarning,
            stacklevel=2,
        )
        return {
            extension: doc_type
            for doc_type in self.documents.types
            for extension in doc_type.extensions
        }
