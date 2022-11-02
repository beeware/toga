import warnings

from .base import Widget


class Divider(Widget):
    """A visual divider line.

    Args:
        id (str): An identifier for this widget.
        style (:obj:`Style`): An optional style object. If no style is provided then
            a new one will be created for the widget.
        direction: The direction for divider, either ``Divider.HORIZONTAL``
            or ``Divider.VERTICAL``. Defaults to `Divider.HORIZONTAL``
    """

    HORIZONTAL = 0
    VERTICAL = 1

    def __init__(
        self,
        id=None,
        style=None,
        direction=HORIZONTAL,
        factory=None,  # DEPRECATED!
    ):
        super().__init__(id=id, style=style)

        ######################################################################
        # 2022-09: Backwards compatibility
        ######################################################################
        # factory no longer used
        if factory:
            warnings.warn("The factory argument is no longer used.", DeprecationWarning)
        ######################################################################
        # End backwards compatibility.
        ######################################################################

        self._direction = direction

        # Create a platform specific implementation of a Divider
        self._impl = self.factory.Divider(interface=self)
        self.direction = direction

    @property
    def direction(self):
        """The direction of the split.

        Returns:
            0 for vertical, 1 for horizontal.
        """
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = value
        self._impl.set_direction(value)
        self._impl.rehint()
