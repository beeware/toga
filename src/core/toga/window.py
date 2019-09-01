from builtins import id as identifier

from toga.command import CommandSet
from toga.platform import get_platform_factory


class Window:
    """The top level container of a application.

    Args:
        id (str): The ID of the window (optional).
        title (str): Title for the window (optional).
        position (``tuple`` of (int, int)): Position of the window, as x,y coordinates.
        size (``tuple`` of (int, int)):  Size of the window, as (width, height) sizes, in pixels.
        toolbar (``list`` of :class:`toga.Widget`): A list of widgets to add to a toolbar
        resizeable (bool): Toggle if the window is resizable by the user, defaults to `True`.
        closeable (bool): Toggle if the window is closable by the user, defaults to `True`.
        minimizable (bool): Toggle if the window is minimizable by the user, defaults to `True`.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional; normally not needed)
    """
    _WINDOW_CLASS = 'Window'

    def __init__(self, id=None, title=None,
                 position=(100, 100), size=(640, 480),
                 toolbar=None, resizeable=True,
                 closeable=True, minimizable=True, factory=None):

        self._id = id if id else identifier(self)
        self._impl = None
        self._app = None
        self._content = None
        self._position = position
        self._size = size
        self._is_full_screen = False

        self.resizeable = resizeable
        self.closeable = closeable
        self.minimizable = minimizable

        self.factory = get_platform_factory(factory)
        self._impl = getattr(self.factory, self._WINDOW_CLASS)(interface=self)

        self._toolbar = CommandSet(
            factory=self.factory,
            widget=self,
            on_change=self._impl.create_toolbar
        )

        self.position = position
        self.size = size
        self.title = title

    @property
    def id(self):
        """ The DOM identifier for the window.
        This id can be used to target CSS directives

        Returns:
            The identifier as a ``str``.
        """
        return self._id

    @property
    def app(self):
        """ Instance of the :class:`toga.App` that this window belongs to.

        Returns:
            The app that it belongs to :class:`toga.App`.

        Raises:
            Exception: If the window already is associated with another app.
        """
        return self._app

    @app.setter
    def app(self, app):
        if self._app:
            raise Exception("Window is already associated with an App")

        self._app = app
        self._impl.set_app(app._impl)

    @property
    def title(self):
        """ Title of the window. If no title is given it defaults to "Toga".

        Returns:
            The current title of the window as a ``str``.
        """
        return self._title

    @title.setter
    def title(self, title):
        if not title:
            title = "Toga"

        self._title = title
        self._impl.set_title(title)

    @property
    def toolbar(self):
        """ Toolbar for the window.

        Returns:
            A ``list`` of :class:`toga.Widget`
        """
        return self._toolbar

    @property
    def content(self):
        """ Content of the window.
        On setting, the content is added to the same app as the window and to the same app.

        Returns:
            A :class:`toga.Widget`
        """
        return self._content

    @content.setter
    def content(self, widget):
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
    def size(self):
        """ Size of the window, as width, height.

        Returns:
            A ``tuple`` of (``int``, ``int``) where the first value is
            the width and the second it the height of the window.
        """
        return self._size

    @size.setter
    def size(self, size):
        self._size = size
        self._impl.set_size(size)
        if self.content:
            self.content.refresh()

    @property
    def position(self):
        """ Position of the window, as x, y

        Returns:
            A ``tuple`` of (``int``, ``int``) int the from (x, y).
        """
        return self._position

    @position.setter
    def position(self, position):
        self._position = position
        self._impl.set_position(position)

    def show(self):
        """ Show window, if hidden """
        self._impl.show()

    @property
    def full_screen(self):
        return self._is_full_screen

    @full_screen.setter
    def full_screen(self, is_full_screen):
        self._is_full_screen = is_full_screen
        self._impl.set_full_screen(is_full_screen)

    def close(self):
        self._impl.close()

    def on_close(self):
        self._impl.on_close()

    ############################################################
    # Dialogs
    ############################################################

    def info_dialog(self, title, message):
        """ Opens a info dialog with a 'OK' button to close the dialog.

        Args:
            title (str): The title of the dialog window.
            message (str): The dialog message to display.

        Returns:
            Returns `None` after the user pressed the 'OK' button.
        """
        return self._impl.info_dialog(title, message)

    def question_dialog(self, title, message):
        """ Opens a dialog with a 'YES' and 'NO' button.

        Args:
            title (str): The title of the dialog window.
            message (str): The dialog message to display.

        Returns:
            Returns `True` when the 'YES' button was pressed, `False` when the 'NO' button was pressed.
        """
        return self._impl.question_dialog(title, message)

    def confirm_dialog(self, title, message):
        """ Opens a dialog with a 'Cancel' and 'OK' button.

        Args:
            title (str): The title of the dialog window.
            message (str): The dialog message to display.

        Returns:
            Returns `True` when the 'OK' button was pressed, `False` when the 'CANCEL' button was pressed.
        """
        return self._impl.confirm_dialog(title, message)

    def error_dialog(self, title, message):
        """ Opens a error dialog with a 'OK' button to close the dialog.

        Args:
            title (str): The title of the dialog window.
            message (str): The dialog message to display.

        Returns:
            Returns `None` after the user pressed the 'OK' button.
        """
        return self._impl.error_dialog(title, message)

    def stack_trace_dialog(self, title, message, content, retry=False):
        """ Calling this function opens a dialog that allows to display a
        large text body in a scrollable fashion.

        Args:
            title (str): The title of the dialog window.
            message (str): The dialog message to display.
            content (str):
            retry (bool):

        Returns:
            Returns `None` after the user pressed the 'OK' button.
        """
        return self._impl.stack_trace_dialog(title, message, content, retry)

    def save_file_dialog(self, title, suggested_filename, file_types=None):
        """ This opens a native dialog where the user can select a place to save a file.
        It is possible to suggest a filename and force the user to use a specific file extension.
        If no path is returned (eg. dialog is canceled), a ValueError is raised.

        Args:
            title (str): The title of the dialog window.
            suggested_filename(str): The automatically filled in filename.
            file_types: A list of strings with the allowed file extensions.

        Returns:
            The absolute path(str) to the selected location.
        """
        return self._impl.save_file_dialog(title, suggested_filename, file_types)

    def open_file_dialog(self, title, initial_directory=None, file_types=None, multiselect=False):
        """ This opens a native dialog where the user can select the file to open.
        It is possible to set the initial folder and only show files with specified file extensions.
        If no path is returned (eg. dialog is canceled), a ValueError is raised.
        Args:
            title (str): The title of the dialog window.
            initial_directory(str): Initial folder displayed in the dialog.
            file_types: A list of strings with the allowed file extensions.
            multiselect: Value showing whether a user can select multiple files.

        Returns:
            The absolute path(str) to the selected file or a list(str) if multiselect
        """
        return self._impl.open_file_dialog(title, initial_directory, file_types, multiselect)

    def select_folder_dialog(self, title, initial_directory=None, multiselect=False):
        """ This opens a native dialog where the user can select a folder.
        It is possible to set the initial folder.
        If no path is returned (eg. dialog is canceled), a ValueError is raised.
        Args:
            title (str): The title of the dialog window.
            initial_directory(str): Initial folder displayed in the dialog.
            multiselect (bool): Value showing whether a user can select multiple files.

        Returns:
            The absolute path(str) to the selected file or None.
        """
        return self._impl.select_folder_dialog(title, initial_directory, multiselect)
