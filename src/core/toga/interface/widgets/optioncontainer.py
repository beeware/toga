from .base import Widget


class OptionContainer(Widget):
    _CONTAINER_CLASS = None

    def __init__(self, id=None, style=None, content=None):
        '''
        Instantiate a new instance of the option container widget

        :param id:          An identifier for this widget.
        :type  id:          ``str``

        :param style:       an optional style object. If no style is provided then a
                            new one will be created for the widget.
        :type style:        :class:`colosseum.CSSNode`

        :param content:     List of components to choose from.
        :type  content:     ``list`` of ``tuple`` (``str``, :class:`toga.Widget`)
        '''

        super().__init__(id=id, style=style, content=content)
        self._containers = []
        self._selected = None

    def _configure(self, content):
        if content:
            for label, widget in content:
                self.add(label, widget)

    def add(self, label, widget):
        '''
        Add a widget to the option container

        :param label: The label for the option
        :type  label: ``str``

        :param widget: The widget to add
        :type  widget: :class:`toga.Widget`
        '''
        widget._update_layout()
        widget.app = self.app
        widget.window = self.window

        if widget._impl is None:
            container = self._CONTAINER_CLASS()
            container.content = widget
        else:
            container = widget

        self._containers.append((label, container, widget))

        self._add_content(label, container, widget)

    @property
    def selected(self):
        """
        The current id and label of the tab view selected

        :rtype: ``dict``
        """
        return self._selected

    @selected.setter
    def selected(self, view_id, view_label):
        self._selected = {'id':view_id, 'label':view_label}

    def _update_child_layout(self):
        for label, container, widget in self._containers:
            container._update_layout()
