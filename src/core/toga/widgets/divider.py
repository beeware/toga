from .base import Widget


class Divider(Widget):
    """A visual divider line.

    Args:
        id (str): An identifier for this widget.
        style (:obj:`Style`): An optional style object. If no style is provided then
            a new one will be created for the widget.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)
    """

    def __init__(self, id=None, style=None, factory=None):
        super().__init__(id=id, style=style, factory=factory)

        # Create a platform specific implementation of a Divider
        self._impl = self.factory.Divider(interface=self)
