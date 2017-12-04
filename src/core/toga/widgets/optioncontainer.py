from toga.handlers import wrapped_handler

from .base import Widget


class OptionContainer(Widget):
    """ The option container widget.

    Args:
        id (str):   An identifier for this widget.
        style (:class:`colosseum.CSSNode`): an optional style object.
            If no style is provided then a new one will be created for the widget.
        content (``list`` of ``tuple`` (``str``, :class:`toga.Widget`)):
            Each tuple in the list is composed of a title for the option and
            the widget tree that is displayed in the option.
    """

    def __init__(self, id=None, style=None, content=None, on_select=None, factory=None):
        super().__init__(id=id, style=style, factory=factory)
        self._impl = self.factory.OptionContainer(interface=self)
        self.on_select = on_select

        if content:
            for label, widget in content:
                self.add(label, widget)

    def add(self, label, widget):
        """ Add a new option to the option container.

        Args:
            label (str): The label for the option.
            widget (:class:`toga.Widget`): The widget to add to the option.
        """
        widget._update_layout()
        widget.app = self.app
        widget.window = self.window

        self._impl.add_content(label, widget._impl)

    def _update_child_layout(self):
        """ Updates all of the option containers. """
        for label, container, widget in self._impl.options.values():
            if hasattr(container, 'interface'):
                container.interface._update_layout()
            else:
                container.update_layout()

    @property
    def on_select(self):
        """ The callback function that is invoked when one of the options is selected.

        Returns:
            (``callable``) The callback function.
        """
        return self._on_select

    @on_select.setter
    def on_select(self, handler):
        """
        Set the function to be executed on option selection

        :param handler:     callback function
        :type handler:      ``callable``
        """
        self._on_select = wrapped_handler(self, handler)
        self._impl.set_on_select(self._on_select)
