from toga.style.pack import ROW

from .base import Widget


class Divider(Widget):
    """A visual divider line.

    Args:
        id (str): An identifier for this widget.
        style (:obj:`Style`): An optional style object. If no style is provided then
            a new one will be created for the widget.
        direction: The direction for divider, either `Divider.AUTO`, `Divider.HORIZONTAL`
            or `Divider.VERTICAL`. In case of `Divider.AUTO`, the direction will be
            determined from the layout when the divider is added to a `toga.Box`.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)
    """
    AUTO = 0
    HORIZONTAL = 1
    VERTICAL = 2

    def __init__(self, id=None, style=None, direction=AUTO, factory=None):
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

    def _get_direction_from_layout(self):
        # automatically determines best direction from parent layout
        # implementations can use this in `rehint`
        if self.parent and self.parent.style.direction == ROW:
            return self.VERTICAL
        else:
            return self.HORIZONTAL
