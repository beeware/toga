from .base import Widget


class OptionContainer(Widget):
    def __init__(self, id=None, style=None, content=None, factory=None):
        """ Instantiate a new instance of the option container widget

        Args:
            id (str):   An identifier for this widget.
            style (:class:`colosseum.CSSNode`): an optional style object.
                If no style is provided then a new one will be created for the widget.
            content (``list`` of ``tuple`` (``str``, :class:`toga.Widget`)):
                Each tuple in the list is composed of a title for the option and
                the widget tree that is displayed in the option.
        """
        super().__init__(id=id, style=style, factory=factory)
        self._impl = self.factory.OptionContainer(interface=self)

        if content:
            for label, widget in content:
                self.add(label, widget)

    def add(self, label, widget):
        """ Add a widget to the option container

        :param label: The label for the option
        :type  label: ``str``

        :param widget: The widget to add
        :type  widget: :class:`toga.Widget`
        """
        widget._update_layout()
        widget.app = self.app
        widget.window = self.window

        self._impl.add_content(label, widget._impl)

    def _update_child_layout(self):
        """ Updates all of the option containers. """
        for label, container, widget in self._impl.containers:
            if hasattr(container, 'interface'):
                container.interface._update_layout()
            else:
                container.update_layout()
