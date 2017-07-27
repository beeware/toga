from builtins import id as identifier

from .command import CommandSet

from .platform import get_platform_factory


class Window:
    """
    Window
    """
    _CONTAINER_CLASS = None
    _DIALOG_MODULE = None

    def __init__(self, id=None, title=None,
                 position=(100, 100), size=(640, 480),
                 toolbar=None, resizeable=True,
                 closeable=True, minimizable=True, factory=None):
        """
        Instantiates a window

        :param id: The ID of the window (optional)
        :type  id: ``str``

        :param title: Title for the window (optional)
        :type  title: ``str``

        :param position: Position of the window, as x,y coordinates
        :type  position: ``tuple`` of (``int``, ``int``)

        :param size: Size of the window, as (width, height) sizes, in pixels
        :type  size: ``tuple`` of (``int``, ``int``)

        :param toolbar: An list of widgets to add to a toolbar
        :type  toolbar: ``list`` of :class:`toga.Widget`

        :param resizable: Toggle if the window is resizable by the user, defaults
            to `True`.
        :type  resizable: ``bool``

        :param closable: Toggle if the window is closable by the user, defaults
            to `True`.
        :type  closable: ``bool``

        :param minimizable: Toggle if the window is minimizable by the user, defaults
            to `True`.
        :type  minimizable: ``bool``
        """
        # if self._CONTAINER_CLASS is None:
        #     raise NotImplementedError('Window class must define show()')

        self._id = id if id else identifier(self)
        self._impl = None
        self._app = None
        self._content = None
        self._position = position
        self._size = size

        self.resizeable = resizeable
        self.closeable = closeable
        self.minimizable = minimizable

        self.factory = get_platform_factory(factory)
        self._impl = self.factory.Window(interface=self)

        self._toolbar = CommandSet(self, self._impl.create_toolbar)

        self.position = position
        self.size = size
        self.title = title

    @property
    def id(self):
        """
        The DOM identifier for the window.

        This id can be used to target CSS directives

        :rtype: ``str``
        """
        return self._id

    @property
    def app(self):
        """
        Instance of the :class:`toga.App` that this window belongs to

        :rtype: :class:`toga.App`
        """
        return self._app

    @app.setter
    def app(self, app):
        if self._app:
            raise Exception("Window is already associated with an App")

        self._app = app
        self._impl.set_app(app)

    @property
    def title(self):
        """
        Title of the window

        :rtype: ``str``
        """
        return self._title

    @title.setter
    def title(self, title):
        if not title:
            title = "Toga"

        self._impl.set_title(title)
        self._title = title

    @property
    def toolbar(self):
        """
        Toolbar for the window

        :rtype: ``list`` of :class:`toga.Widget`
        """
        return self._toolbar

    @property
    def content(self):
        """
        Content of the window

        :rtype: :class:`toga.Widget`
        """
        return self._content

    @content.setter
    def content(self, widget):
        # Save the content widget.
        widget._update_layout()

        # Assign the widget to the same app as the window.
        widget.app = self.app

        # Assign the widget to window.
        widget.window = self

        # Track our new content
        self._content = widget

        # Manifest the widget
        self._impl.set_content(widget._impl)

    @property
    def size(self):
        """
        Size of the window, as width, height

        :rtype: ``tuple`` of (``int``, ``int``)
        """
        return self._size

    @size.setter
    def size(self, size):
        self._size = size
        self._impl.set_size(size)

    @property
    def position(self):
        """
        Position of the window, as x, y

        :rtype: ``tuple`` of (``int``, ``int``)
        """
        return self._position

    @position.setter
    def position(self, position):
        self._position = position
        self._impl.set_position(position)

    def _set_position(self, position):
        pass

    def show(self):
        # '''
        # Show window, if hidden
        # '''
        self._impl.show()

    def on_close(self):
        self._impl.on_close()

    def info_dialog(self, title, message):
        """ Opens a info dialog with a 'OK' button to close the dialog.

        Args:
            title (str): The title of the dialog window.
            message (str):

        Returns:
            Returns `None after the user pressed the 'OK' button.
        """
        return self._impl.info_dialog(title, message)

    def question_dialog(self, title, message):
        """ Opens a dialog with a 'YES' and 'NO' button.

        Args:
            title (str): The title of the dialog window.
            message (str):

        Returns:
            Returns `True` when the 'YES' button was pressed, `False` when the 'NO' button was pressed.
        """
        return self._impl.question_dialog(title, message)

    def confirm_dialog(self, title, message):
        """ Opens a dialog with a 'Cancel' and 'OK' button.

        Args:
            title (str): The title of the dialog window.
            message (str):

        Returns:
            Returns `True` when the 'OK' button was pressed, `False` when the 'CANCEL' button was pressed.
        """
        return self._impl.confirm_dialog(title, message)

    def error_dialog(self, title, message):
        """ Opens a error dialog with a 'OK' button to close the dialog.

        Args:
            title (str): The title of the dialog window.
            message (str):

        Returns:
            Returns `None` after the user pressed the 'OK' button.
        """
        return self._impl.error_dialog(title, message)

    def stack_trace_dialog(self, title, message, content, retry=False):
        """ Calling this function opens a dialog that allows to display a
        large text body in a scrollable fashion.

        Args:
            title (str): The title of the dialog window.
            message (str):
            content (str):
            retry (bool):

        Returns:
            Returns `None` after the user pressed the 'OK' button.
        """
        return self._impl.stack_trace_dialog(title, message, content, retry)

    def save_file_dialog(self, title, suggested_filename, file_types=None):
        """ This opens a native dialog where the user can select a place to save a file.
        It is possible to suggest a filename and force the user to use a specific file extension.

        Args:
            title (str): The title of the dialog window.
            suggested_filename(str): The automatically filled in filename.
            file_types: A list of strings with the allowed file extensions.

        Returns:
            The absolute path(str) to the selected location.
        """
        return self._impl.save_file_dialog(title, suggested_filename, file_types)
