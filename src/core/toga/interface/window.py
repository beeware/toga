class Window:
    '''
    Window
    '''
    _CONTAINER_CLASS = None
    _DIALOG_MODULE = None

    def __init__(self, id_=None, title=None,
                 position=(100, 100), size=(640, 480),
                 toolbar=None, resizeable=True,
                 closeable=True, minimizable=True):
        '''
        Instantiates a window

        :param id_: The ID of the window (optional)
        :type  id_: ``str``

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
        '''
        if self._CONTAINER_CLASS is None:
            raise NotImplementedError('Window class must define show()')

        self._id = id_ if id_ else id(self)
        self._impl = None
        self._app = None
        self._container = None
        self._content = None

        self.position = position
        self.size = size

        self.resizeable = resizeable
        self.closeable = closeable
        self.minimizable = minimizable

        self._config = {
            'title': title,
            'position': position,
            'size': size,
            'toolbar': toolbar,
            'resizeable': resizeable,
            'closeable': closeable,
            'minimizable': minimizable,
        }

    def _create(self):
        self.create()
        self._configure(**self._config)

    def _configure(self, title, position, size, toolbar, resizeable, closeable, minimizable):
        self.title = title
        self.toolbar = toolbar

    @property
    def app(self):
        '''
        Instance of the :class:`toga.App` that this window belongs to

        :rtype: :class:`toga.App`
        '''
        return self._app

    @app.setter
    def app(self, app):
        if self._app:
            raise Exception("Window is already associated with an App")

        self._app = app
        self._set_app(app)

    def _set_app(self, app):
        pass

    @property
    def title(self):
        '''
        Title of the window

        :rtype: ``str``
        '''
        return self._title

    @title.setter
    def title(self, title):
        if not title:
            title = "Toga"

        self._set_title(title)
        self._title = title

    @property
    def toolbar(self):
        '''
        Toolbar for the window

        :rtype: ``list`` of :class:`toga.Widget`
        '''
        return self._toolbar

    @toolbar.setter
    def toolbar(self, items):
        # If there are toolbar items defined, add a toolbar to the window
        self._toolbar = items
        if self._toolbar:
            self._set_toolbar(items)

    def _set_toolbar(self, items):
        pass

    @property
    def content(self):
        '''
        Content of the window

        :rtype: :class:`toga.Widget`
        '''
        return self._content

    @content.setter
    def content(self, widget):
        # Save the content widget.
        widget._update_layout()

        # Assign the widget to the same app as the window.
        widget.app = self.app

        # Assign the widget to window.
        widget.window = self

        if widget._impl is None:
            self._container = self._CONTAINER_CLASS()
            self._container.content = widget
        else:
            self._container = widget

        self._content = widget

        self._set_content(widget)

    def _set_content(self, widget):
        pass

    @property
    def size(self):
        '''
        Size of the window, as width, height

        :rtype: ``tuple`` of (``int``, ``int``)
        '''
        return self._size

    @size.setter
    def size(self, size):
        self._size = size
        self._set_size(size)

    def _set_size(self, size):
        pass

    @property
    def position(self):
        '''
        Position of the window, as x, y

        :rtype: ``tuple`` of (``int``, ``int``)
        '''
        return self._position

    @position.setter
    def position(self, position):
        self._position = position
        self._set_position(position)

    def _set_position(self, position):
        pass

    def show(self):
        '''
        Show window, if hidden
        '''
        raise NotImplementedError('Window class must define show()')

    def on_close(self):
        pass

    def info_dialog(self, title, message):
        return self._DIALOG_MODULE.info(self, title, message)

    def question_dialog(self, title, message):
        return self._DIALOG_MODULE.question(self, title, message)

    def confirm_dialog(self, title, message):
        return self._DIALOG_MODULE.confirm(self, title, message)

    def error_dialog(self, title, message):
        return self._DIALOG_MODULE.error(self, title, message)

    def stack_trace_dialog(self, title, message):
        return self._DIALOG_MODULE.stack_trace(self, title, message)

    def save_file_dialog(self, title, suggested_filename, file_types):
        return self._DIALOG_MODULE.save_file(self, title, suggested_filename,
                                             file_types)
