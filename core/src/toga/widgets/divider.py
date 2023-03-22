from .base import Widget


class Divider(Widget):
    HORIZONTAL = 0
    VERTICAL = 1

    def __init__(
        self,
        id=None,
        style=None,
        direction=HORIZONTAL,
    ):
        """Create a new text label.

        Inherits from :class:`~toga.widgets.base.Widget`.

        :param text: Text of the label.
        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        :param direction: The direction in which the divider will be drawn.
            Defaults to ``Divider.HORIZONTAL``
        """
        super().__init__(id=id, style=style)

        # Create a platform specific implementation of a Divider
        self._impl = self.factory.Divider(interface=self)
        self.direction = direction

    @property
    def direction(self):
        """The direction in which the visual separator will be drawn.

        :returns: ``Divider.HORIZONTAL`` or ``Divider.VERTICAL``
        """
        return self._impl.get_direction()

    @direction.setter
    def direction(self, value):
        self._direction = value
        self._impl.set_direction(value)
        self.refresh()
