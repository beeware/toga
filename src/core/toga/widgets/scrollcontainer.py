from .base import Widget


class ScrollContainer(Widget):
    '''
    A scrollable container
    '''
    _CONTAINER_CLASS = None

    def __init__(self, id=None, style=None, horizontal=True,
                 vertical=True, content=None):
        '''
        Instantiate a new instance of the scrollable container widget

        :param id:          An identifier for this widget.
        :type  id:          ``str``

        :param style:       an optional style object. If no style is provided then a
                            new one will be created for the widget.
        :type style:        :class:`colosseum.CSSNode`

        :param horizontal: Enable horizontal scroll bar
        :type  horizontal: ``bool``

        :param vertical: Enable vertical scroll bar
        :type  vertical: ``bool``

        :param content: The content of the scroll window
        :type  content: :class:`toga.Widget`
        '''
        super().__init__(id=id, style=style, horizontal=horizontal, vertical=vertical, content=content)

    def _configure(self, horizontal, vertical, content):
        self.horizontal = horizontal
        self.vertical = vertical
        self.content = content

    @property
    def content(self):
        '''
        Content of the scroll window

        :rtype: :class:`toga.Widget`
        '''
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget
        if widget:
            widget._update_layout()
            self._content.app = self.app
            self._content.window = self.window

            if widget._impl is None:
                self._inner_container = self._CONTAINER_CLASS()
                self._inner_container.root_content = widget
            else:
                self._inner_container = widget

            self._set_content(self._inner_container, widget)

    @property
    def vertical(self):
        '''
        Enable vertical scaling

        :rtype: ``bool``
        '''
        return self._vertical

    @vertical.setter
    def vertical(self, value):
        self._vertical = value
        self._set_vertical(value)

    @property
    def horizontal(self):
        '''
        Enable horizontal scaling

        :rtype: ``bool``
        '''
        return self._horizontal

    @horizontal.setter
    def horizontal(self, value):
        self._horizontal = value
        self._set_horizontal(value)

    def _set_vertical(self, value):
        raise NotImplementedError('ScrollContainer must define _set_vertical()')

    def _set_horizontal(self, value):
        raise NotImplementedError('ScrollContainer must define _set_horizontal()')
