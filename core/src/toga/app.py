import signal
import sys
import warnings
import webbrowser
from builtins import id as identifier
from collections.abc import MutableSet
from email.message import Message

from toga.command import CommandSet
from toga.handlers import wrapped_handler
from toga.icons import Icon
from toga.platform import get_platform_factory
from toga.widgets.base import WidgetRegistry
from toga.window import Window

try:
    from importlib import metadata as importlib_metadata
except ImportError:
    # Backwards compatibility - importlib.metadata was added in Python 3.8
    import importlib_metadata


# Make sure deprecation warnings are shown by default
warnings.filterwarnings("default", category=DeprecationWarning)


class WindowSet(MutableSet):
    """This class represents windows of a toga app.

    A window can be added to app by using
    `app.windows.add(toga.Window(...))` or `app.windows +=
    toga.Window(...)` notations. Adding a window to app automatically
    sets `window.app` property to the app.
    """

    def __init__(self, app, iterable=None):
        self.app = app
        self.elements = set() if iterable is None else set(iterable)

    def add(self, window: Window) -> None:
        if not isinstance(window, Window):
            raise TypeError("Toga app.windows can only add objects of toga.Window type")
        # Silently not add if duplicate
        if window not in self.elements:
            self.elements.add(window)
            window.app = self.app

    def discard(self, window: Window) -> None:
        if not isinstance(window, Window):
            raise TypeError(
                "Toga app.windows can only discard an object of a toga.Window type"
            )
        if window not in self.elements:
            raise AttributeError(
                "The window you are trying to remove is not associated with this app"
            )
        self.elements.remove(window)

    def __iadd__(self, window):
        self.add(window)
        return self

    def __isub__(self, other):
        self.discard(other)
        return self

    def __iter__(self):
        return iter(self.elements)

    def __contains__(self, value):
        return value in self.elements

    def __len__(self):
        return len(self.elements)


class MainWindow(Window):
    _WINDOW_CLASS = "MainWindow"

    def __init__(
        self,
        id=None,
        title=None,
        position=(100, 100),
        size=(640, 480),
        toolbar=None,
        resizeable=True,
        minimizable=True,
        factory=None,  # DEPRECATED !
        on_close=None,
    ):
        ######################################################################
        # 2022-09: Backwards compatibility
        ######################################################################
        # factory no longer used
        if factory:
            warnings.warn("The factory argument is no longer used.", DeprecationWarning)
        ######################################################################
        # End backwards compatibility.
        ######################################################################
        super().__init__(
            id=id,
            title=title,
            position=position,
            size=size,
            toolbar=toolbar,
            resizeable=resizeable,
            closeable=True,
            minimizable=minimizable,
            on_close=on_close,
        )

    @Window.on_close.setter
    def on_close(self, handler):
        """Raise an exception: on_exit for the app should be used instead of
        on_close on main window.

        Args:
            handler (:obj:`callable`): The handler passed.
        """
        if handler:
            raise AttributeError(
                "Cannot set on_close handler for the main window. Use the app on_exit handler instead"
            )


class App:
    """The App is the top level of any GUI program. It is the manager of all
    the other bits of the GUI app: the main window and events that window
    generates like user input.

    When you create an App you need to provide it a name, an id for uniqueness
    (by convention, the identifier is a reversed domain name.) and an
    optional startup function which should run once the App has initialized.
    The startup function typically constructs some initial user interface.

    If the name and app_id are *not* provided, the application will attempt
    to find application metadata. This process will determine the module in
    which the App class is defined, and look for a ``.dist-info`` file
    matching that name.

    Once the app is created you should invoke the main_loop() method, which
    will hand over execution of your program to Toga to make the App interface
    do its thing.

    The absolute minimum App would be::

        >>> app = toga.App(formal_name='Empty App', app_id='org.beeware.empty')
        >>> app.main_loop()

    :param formal_name: The formal name of the application. Will be derived from
        packaging metadata if not provided.
    :param app_id: The unique application identifier. This will usually be a
        reversed domain name, e.g. ``org.beeware.myapp``. Will be derived from
        packaging metadata if not provided.
    :param app_name: The name of the Python module containing the app.
        Will be derived from the module defining the instance of the App class
        if not provided.
    :param id: The DOM identifier for the app (optional)
    :param icon: Identifier for the application's icon.
    :param author: The person or organization to be credited as the author
        of the application. Will be derived from application metadata if not
        provided.
    :param version: The version number of the app. Will be derived from
        packaging metadata if not provided.
    :param home_page: A URL for a home page for the app. Used in auto-generated
        help menu items. Will be derived from packaging metadata if not
        provided.
    :param description: A brief (one line) description of the app. Will be
        derived from packaging metadata if not provided.
    :param startup: The callback method before starting the app, typically to
        add the components. Must be a ``callable`` that expects a single
        argument of :class:`~toga.app.App`.
    :param windows: An iterable with objects of :class:`~toga.window.Window`
        that will be the app's secondary windows.
    """

    app = None

    def __init__(
        self,
        formal_name=None,
        app_id=None,
        app_name=None,
        id=None,
        icon=None,
        author=None,
        version=None,
        home_page=None,
        description=None,
        startup=None,
        windows=None,
        on_exit=None,
        factory=None,  # DEPRECATED !
    ):
        ######################################################################
        # 2022-09: Backwards compatibility
        ######################################################################
        # factory no longer used
        if factory:
            warnings.warn("The factory argument is no longer used.", DeprecationWarning)
        ######################################################################
        # End backwards compatibility.
        ######################################################################

        # Initialize empty widgets registry
        self._widgets = WidgetRegistry()

        # Keep an accessible copy of the app instance
        App.app = self

        # We need a module name to load app metadata. If an app_name has been
        # provided, we can set the app name now, and derive the module name
        # from there.
        if app_name:
            self._app_name = app_name
        else:
            # If the code is contained in appname.py, and you start the app
            # using `python -m appname`, the main module package will report
            # as ''. Set the initial app name as None.
            # If the code is contained in appname.py, and you start the app
            # using `python appname.py`, the main module will report as None.
            # If the code is contained in a folder, and you start the app
            # using `python -m appname`, the main module will report as the
            # name of the folder.
            try:
                main_module_pkg = sys.modules["__main__"].__package__
                if main_module_pkg == "":
                    self._app_name = None
                else:
                    self._app_name = main_module_pkg
            except KeyError:
                # We use the existence of a __main__ module as a proxy for
                # being in test conditions. This isn't *great*, but the __main__
                # module isn't meaningful during tests, and removing it allows
                # us to avoid having explicit "if under test conditions" checks.
                # If there's no __main__ module, we're in a test, and we can't
                # imply an app name from that module name.
                self._app_name = None

            # Try deconstructing the app name from the app ID
            if self._app_name is None and app_id:
                self._app_name = app_id.split(".")[-1]

        # Load the app metadata (if it is available)
        # Apps packaged with Briefcase will have this metadata.
        try:
            self.metadata = importlib_metadata.metadata(self.module_name)
        except importlib_metadata.PackageNotFoundError:
            self.metadata = Message()

        # Now that we have metadata, we can fix the app name (in the case
        # where the app name and the module name differ - e.g., an app name
        # of ``hello-world`` will have a module name of ``hello_world``).
        # We use the PEP566-compliant key ``Name```, rather than the internally
        # consistent key ``App-Name```.
        if self.metadata["Name"] is not None:
            self._app_name = self.metadata["Name"]

        # Whatever app name has been given, speculatively attempt to import
        # the app module. Single-file apps won't have an app folder; apps with
        # misleading or misconfigured app names haven't given us enough
        # metadata to determine the app folder. In those cases, fall back to
        # an app name that *will* exist (``toga```)
        try:
            sys.modules[self.module_name]
        except KeyError:
            # Well that didn't work...
            self._app_name = "toga"

        # If a name has been provided, use it; otherwise, look to
        # the module metadata. However, a name *must* be provided.
        if formal_name:
            self._formal_name = formal_name
        else:
            self._formal_name = self.metadata["Formal-Name"]

        if self._formal_name is None:
            raise RuntimeError("Toga application must have a formal name")

        # If an app_id has been provided, use it; otherwise, look to
        # the module metadata. However, an app_id *must* be provided
        if app_id:
            self._app_id = app_id
        else:
            self._app_id = self.metadata.get("App-ID", None)

        if self._app_id is None:
            raise RuntimeError("Toga application must have an App ID")

        # If an author has been provided, use it; otherwise, look to
        # the module metadata.
        if author:
            self._author = author
        else:
            self._author = self.metadata.get("Author", None)

        # If a version has been provided, use it; otherwise, look to
        # the module metadata.
        if version:
            self._version = version
        else:
            self._version = self.metadata.get("Version", None)

        # If a home_page has been provided, use it; otherwise, look to
        # the module metadata.
        if home_page:
            self._home_page = home_page
        else:
            self._home_page = self.metadata.get("Home-page", None)

        # If a description has been provided, use it; otherwise, look to
        # the module metadata.
        if description:
            self._description = description
        else:
            self._description = self.metadata.get("Summary", None)

        # Set the application DOM ID; create an ID if one hasn't been provided.
        self._id = id if id else identifier(self)

        # Get a platform factory, and a paths instance from the factory.
        self.factory = get_platform_factory()
        self.paths = self.factory.paths

        # If an icon (or icon name) has been explicitly provided, use it;
        # otherwise, the icon will be based on the app name.
        if icon:
            self.icon = icon
        else:
            self.icon = f"resources/{self.app_name}"

        self.commands = CommandSet()

        self._startup_method = startup

        self._main_window = None
        # In this world, TogaApp.windows would be a set-like object
        # that has add/remove methods (including support for
        # the + and += operators); adding a window to TogaApp.windows
        # would assign the window to the app.
        self.windows = WindowSet(self, windows)

        self._full_screen_windows = None

        self._impl = self._create_impl()
        self.on_exit = on_exit

    def _create_impl(self):
        return self.factory.App(interface=self)

    @property
    def name(self):
        """The formal name of the app.

        :returns: The formal name of the app, as a ``str``.
        """
        return self._formal_name

    @property
    def formal_name(self):
        """The formal name of the app.

        :returns: The formal name of the app, as a ``str``.
        """
        return self._formal_name

    @property
    def app_name(self):
        """The machine-readable, PEP508-compliant name of the app.

        :returns: The machine-readable app name, as a ``str``.
        """
        return self._app_name

    @property
    def module_name(self):
        """The module name for the app.

        :returns: The module name for the app, as a ``str``.
        """
        try:
            return self._app_name.replace("-", "_")
        except AttributeError:
            # If the app was created from an interactive prompt,
            # there won't be a module name.
            return None

    @property
    def app_id(self):
        """The identifier for the app.

        This is a reversed domain name, often used for targeting resources,
        etc.

        :returns: The identifier as a ``str``.
        """
        return self._app_id

    @property
    def author(self):
        """The author of the app. This may be an organization name.

        :returns: The author of the app, as a ``str``.
        """
        return self._author

    @property
    def version(self):
        """The version number of the app.

        :returns: The version number of the app, as a ``str``.
        """
        return self._version

    @property
    def home_page(self):
        """The URL of a web page for the app.

        :returns: The URL of the app's home page, as a ``str``.
        """
        return self._home_page

    @property
    def description(self):
        """A brief description of the app.

        :returns: A brief description of the app, as a ``str``.
        """
        return self._description

    @property
    def id(self):
        """The DOM identifier for the app.

        This id can be used to target CSS directives.

        :returns: A DOM identifier for the app.
        """
        return self._id

    @property
    def icon(self):
        """The Icon for the app.

        :returns: A ``toga.Icon`` instance for the app's icon.
        """
        return self._icon

    @icon.setter
    def icon(self, icon_or_name):
        if isinstance(icon_or_name, Icon):
            self._icon = icon_or_name
        else:
            self._icon = Icon(icon_or_name)

    @property
    def widgets(self):
        """The widgets collection of the entire app.

        Can be used to lookup widgets over the entire app through widget
        id or manually iterating through it.
        Example: ``app.widgets["my_id"]``

        :returns: The reference to the widgets collection of the entire app.
        """
        return self._widgets

    @property
    def main_window(self):
        """The main window for the app.

        :returns: The main Window of the app.
        """
        return self._main_window

    @main_window.setter
    def main_window(self, window):
        self._main_window = window
        self.windows += window
        self._impl.set_main_window(window)

    @property
    def current_window(self):
        """Return the currently active content window."""
        return self._impl.current_window().interface

    @property
    def is_full_screen(self):
        """Is the app currently in full screen mode?"""
        return self._full_screen_windows is not None

    def set_full_screen(self, *windows):
        """Make one or more windows full screen.

        Full screen is not the same as "maximized"; full screen mode
        is when all window borders and other chrome is no longer
        visible.

        Args:
            windows: The list of windows to go full screen,
                in order of allocation to screens. If the number of
                windows exceeds the number of available displays,
                those windows will not be visible. If no windows
                are specified, the app will exit full screen mode.
        """
        if not windows:
            self.exit_full_screen()
        else:
            self._impl.enter_full_screen(windows)
            self._full_screen_windows = windows

    def exit_full_screen(self):
        """Exit full screen mode."""
        if self.is_full_screen:
            self._impl.exit_full_screen(self._full_screen_windows)
            self._full_screen_windows = None

    def show_cursor(self):
        """Show cursor."""
        self._impl.show_cursor()

    def hide_cursor(self):
        """Hide cursor from view."""
        self._impl.hide_cursor()

    def startup(self):
        """Create and show the main window for the application."""
        self.main_window = MainWindow(title=self.formal_name)

        if self._startup_method:
            self.main_window.content = self._startup_method(self)

        self.main_window.show()

    def about(self):
        """Display the About dialog for the app.

        Default implementation shows a platform-appropriate about dialog
        using app metadata. Override if you want to display a custom
        About dialog.
        """
        self._impl.show_about_dialog()

    def visit_homepage(self):
        """Open the application's homepage in the default browser.

        If the application metadata doesn't define a homepage, this is a
        no-op.
        """
        if self.home_page is not None:
            webbrowser.open(self.home_page)

    def main_loop(self):
        """Invoke the application to handle user input.

        This method typically only returns once the application is
        exiting.
        """
        # Modify signal handlers to make sure Ctrl-C is caught and handled.
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        self._impl.main_loop()

    def exit(self):
        """Quit the application gracefully."""
        self.on_exit(None)

    @property
    def on_exit(self):
        """The handler to invoke before the application exits.

        Returns:
            The function ``callable`` that is called on application exit.
        """
        return self._on_exit

    @on_exit.setter
    def on_exit(self, handler):
        """Set the handler to invoke before the app exits.

        Args:
            handler (:obj:`callable`): The handler to invoke before the app exits.
        """
        if handler is None:

            def handler(app, *args, **kwargs):
                app._impl.exit()

        def cleanup(app, should_exit):
            if should_exit:
                app._impl.exit()

        self._on_exit = wrapped_handler(self, handler, cleanup=cleanup)

    def add_background_task(self, handler):
        """Schedule a task to run in the background.

        Schedules a coroutine or a generator to run in the background. Control
        will be returned to the event loop during await or yield statements,
        respectively. Use this to run background tasks without blocking the
        GUI. If a regular callable is passed, it will be called as is and will
        block the GUI until the call returns.

        :param handler: A coroutine, generator or callable.
        """
        self._impl.loop.call_soon_threadsafe(wrapped_handler(self, handler), None)


class DocumentApp(App):
    """A document-based application.

    Definition and arguments are the same as a base App, plus the following:

    Args:
        document_types (:obj:`list` of :obj:`str`): Document types.
    """

    def __init__(
        self,
        formal_name=None,
        app_id=None,
        app_name=None,
        id=None,
        icon=None,
        author=None,
        version=None,
        home_page=None,
        description=None,
        startup=None,
        document_types=None,
        on_exit=None,
        factory=None,  # DEPRECATED !
    ):
        ######################################################################
        # 2022-09: Backwards compatibility
        ######################################################################
        # factory no longer used
        if factory:
            warnings.warn("The factory argument is no longer used.", DeprecationWarning)
        ######################################################################
        # End backwards compatibility.
        ######################################################################

        self.document_types = document_types
        self._documents = []

        super().__init__(
            formal_name=formal_name,
            app_id=app_id,
            app_name=app_name,
            id=id,
            icon=icon,
            author=author,
            version=version,
            home_page=home_page,
            description=description,
            startup=startup,
            on_exit=on_exit,
        )

    def _create_impl(self):
        return self.factory.DocumentApp(interface=self)

    @property
    def documents(self):
        """Return the list of documents associated with this app.

        Returns:
            A ``list`` of ``str``.
        """
        return self._documents
