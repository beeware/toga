from .base import Widget


class Box(Widget):
    def __init__(
        self,
        id=None,
        style=None,
        children=None,
    ):
        """Create a new Box container widget.

        Inherits from :class:`~toga.widgets.base.Widget`.

        :param text: The text to display on the button.
        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        :param children: An optional list of children for to add to the Box.
        """
        super().__init__(id=id, style=style)

        # Create a platform specific implementation of a Box
        self._impl = self.factory.Box(interface=self)

        self._children = []
        if children:
            self.add(*children)

    @Widget.enabled.setter
    def enabled(self, value):
        # Box doesn't have a "disabled" state
        pass
