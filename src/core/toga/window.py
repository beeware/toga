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
        self._impl = getattr(self.factory, self.__class__.__name__)(interface=self)

        self._toolbar = CommandSet(self, self._impl.create_toolbar)

        self.position = position
        self.size = size
        # self.title = title

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
        return self._impl.info(self, title, message)

    def question_dialog(self, title, message):
        return self._impl.question(self, title, message)

    def confirm_dialog(self, title, message):
        return self._impl.confirm(self, title, message)

    def error_dialog(self, title, message):
        return self._impl.error(self, title, message)

    def stack_trace_dialog(self, title, message, content, retry=False):
        return self._impl.stack_trace(self, title, message,
                                               content, retry)

    def save_file_dialog(self, title, suggested_filename, file_types):
        return self._impl.save_file(self, title, suggested_filename,
                                             file_types)
