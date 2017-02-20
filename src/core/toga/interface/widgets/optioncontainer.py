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
        if widget._impl is None:
            container = self._CONTAINER_CLASS()
            container.content = widget
        else:
            container = widget

        self._containers.append((label, container, widget))

        widget.window = self.window
        widget.app = self.app

        self._add_content(label, container, widget)

    def _update_child_layout(self):
        for label, container, widget in self._containers:
            container._update_layout()
