import os
import signal
import sys
from builtins import id as identifier

from toga.command import CommandSet
from toga.platform import get_platform_factory
from toga.widgets.icon import Icon
from toga.window import Window


class MainWindow(Window):
    _WINDOW_CLASS = 'MainWindow'

    def __init__(self, id=None, title=None, position=(100, 100), size=(640, 480), factory=None):
        super(MainWindow, self).__init__(id=id, title=title, position=position, size=size, factory=factory)


class App:
    """ The App is the top level of any GUI program. It is the manager of all
    the other bits of the GUI app: the main window and events that window
    generates like user input.

    When you create an App you need to provide it a name, an id for uniqueness
    (by convention, the identifier is a "reversed domain name".) and an
    optional startup function which should run once the App has initialised.
    The startup function typically constructs some initial user interface.

    Once the app is created you should invoke the main_loop() method, which
    will hand over execution of your program to Toga to make the App interface
    do its thing.

    Args:
        name (str): Is the name of the application.
        app_id (str): The unique application identifier, the reversed domain name, e.g. 'org.pybee.me'
        icon (str): Path to the icon for the application.
        id (str): The DOM identifier for the app (optional)
        startup(``callable``): The callback method before starting the app, typically to add the components.
            Must be a ``callable`` that expects a single argument of :class:`toga.App`.
        document_types (:obj:`list` of :obj:`str`): Document types.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)

    Examples:
        >>> # Here is the absolute minimum App::
        >>> app = toga.App('Empty App', 'org.pybee.empty')
        >>> app.main_loop()
    """
    app = None

    def __init__(self, name, app_id,
                 id=None, icon=None, startup=None, document_types=None, factory=None):

        self.factory = get_platform_factory(factory)

        # Keep an accessible copy of the app instance
        App.app = self
        App.app_module = self.__module__.split('.')[0]
        App.app_dir = os.path.dirname(sys.modules[App.app_module].__file__)

        self.name = name
        self._app_id = app_id
        self._id = id if id else identifier(self)

        self.commands = CommandSet(None)

        self.document_types = document_types
        self._documents = []

        self._startup_method = startup

        self.default_icon = Icon('tiberius', system=True)
        self.icon = icon
        self._main_window = None

        self._impl = self.factory.App(interface=self)

    @property
    def app_id(self):
        """ The identifier for the app.
        This is the reversed domain name, often used for targetting resources, etc.

        Returns:
            The identifier as a ``str``.
        """
        return self._app_id

    @property
    def id(self):
        """ The DOM identifier for the app. This id can be used to target CSS directives.

        Returns:
            The identifier for the app as a ``str``.
        """
        return self._id

    @property
    def icon(self):
        """ The Icon for the app. On setting, the icon is loaded automatically.

        Returns:
            The icon of the app ``toga.Icon``.
        """
        return self._icon

    @icon.setter
    def icon(self, name):
        self._icon = Icon.load(name, default=self.default_icon)

    @property
    def main_window(self):
        """The main Windows for the app.

        Returns:
            The main Window of the app.
        """
        return self._main_window

    @main_window.setter
    def main_window(self, window):
        self._main_window = window
        window.app = self

    @property
    def documents(self):
        """ Return the list of documents associated with this app.

        Returns:
            A ``list`` of ``str``.
        """
        return self._documents

    def add_document(self, doc):
        """ Add a new document to this app.

        Args:
            doc (str): The document to add.
        """
        doc.app = self
        self._documents.append(doc)

    def open_document(self, fileURL):
        """ Add a new document to this app.

        Args:
            fileURL (str): The URL/path to the file to add as a document.
        """
        raise NotImplementedError('Application class must define open_document()')

    def startup(self):
        """ Create and show the main window for the application
        """
        self.main_window = MainWindow(title=self.name, factory=self.factory)

        if self._startup_method:
            self.main_window.content = self._startup_method(self)

        self.main_window.show()

    def main_loop(self):
        """ Invoke the application to handle user input.
        This method typically only returns once the application is exiting.
        """
        # Modify signal handlers to make sure Ctrl-C is caught and handled.
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        self._impl.main_loop()

    def exit(self):
        """ Quit the application gracefully.
        """
        self._impl.exit()
