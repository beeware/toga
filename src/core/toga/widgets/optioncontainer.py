from toga.handlers import wrapped_handler

from .base import Widget


class OptionContainer(Widget):
    """ The option container widget.

    Args:
        id (str):   An identifier for this widget.
        style (:obj:`Style`): an optional style object.
            If no style is provided then a new one will be created for the widget.
        content (``list`` of ``tuple`` (``str``, :class:`toga.Widget`)):
            Each tuple in the list is composed of a title for the option and
            the widget tree that is displayed in the option.
    """

    def __init__(self, id=None, style=None, content=None, on_select=None, factory=None):
        super().__init__(id=id, style=style, factory=factory)
        self._on_select = None
        self._impl = self.factory.OptionContainer(interface=self)

        self.on_select = on_select
        self._content = []
        if content:
            for label, widget in content:
                self.add(label, widget)

        self.on_select = on_select

    @property
    def content(self):
        """ The sub layouts of the `SplitContainer`.

        Returns:
            A ``list`` of :class:`toga.Widget`. Each element of the list
            is a sub layout of the `SplitContainer`

        Raises:
            ValueError: If the list is less than two elements long.
        """
        return self._content

    def _set_window(self, window):
        if self._content:
            for content in self._content:
                content.window = window

    def add(self, label, widget):
        """ Add a new option to the option container.

        Args:
            label (str): The label for the option.
            widget (:class:`toga.Widget`): The widget to add to the option.
        """
        widget.app = self.app
        widget.window = self.window

        self._content.append(widget)
        self._impl.add_content(label, widget._impl)
        widget.refresh()

    def refresh_sublayouts(self):
        """Refresh the layout and appearance of this widget."""
        for widget in self._content:
            widget.refresh()

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
