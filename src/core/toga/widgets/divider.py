from .base import Widget


class Divider(Widget):
    """A visual divider line.

    Args:
        id (str): An identifier for this widget.
        style (:obj:`Style`): An optional style object. If no style is provided then
            a new one will be created for the widget.
        direction: The direction for divider, either ``Divider.HORIZONTAL``
            or ``Divider.VERTICAL``. Defaults to `Divider.HORIZONTAL``
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)
    """
    HORIZONTAL = 0
    VERTICAL = 1

    def __init__(self, id=None, style=None, direction=HORIZONTAL, factory=None):
        super().__init__(id=id, style=style, factory=factory)

        # Create a platform specific implementation of a Divider
        self._impl = self.factory.Divider(interface=self)
        self.direction = direction

    @property
    def direction(self):
        """ The direction of the split

        Returns:
            True if `True` for vertical, `False` for horizontal.
        """
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = value
        self._impl.set_direction(value)
        self._impl.rehint()
