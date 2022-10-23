from .base import Widget


class SplitContainer(Widget):
    """ A SplitContainer displays two widgets vertically or horizontally
    next to each other with a movable divider.

    Args:
        id (str):  An identifier for this widget.
        style (:obj:`Style`): An optional style object.
            If no style is provided then a new one will be created for the widget.
        direction: The direction for the container split,
            either `SplitContainer.HORIZONTAL` or `SplitContainer.VERTICAL`
        content(``list`` of :class:`toga.Widget`): The list of components to be
            split or tuples of components to be split and adjusting parameters
            in the following order:
            widget (:class:`toga.Widget`): The widget that will be added.
            weight (float): Specifying the weighted splits.
            flex (boolean): Should the content expand when the widget is resized. (optional)
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)
    """
    HORIZONTAL = False
    VERTICAL = True

    def __init__(self, id=None, style=None, direction=VERTICAL, content=None, factory=None):
        super().__init__(id=id, style=style, factory=factory)
        self._direction = direction
        self._content = []
        self._weight = []

        # Create a platform specific implementation of a SplitContainer
        self._impl = self.factory.SplitContainer(interface=self)

        self.content = content
        self.direction = direction

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

    @content.setter
    def content(self, content):
        if content is None:
            self._content = None
            return

        if len(content) < 2:
            raise ValueError('SplitContainer content must have at least 2 elements')

        self._content = []
        for position, item in enumerate(content):
            if isinstance(item, tuple):
                if len(item) == 2:
                    widget, weight = item
                    flex = True
                elif len(item) == 3:
                    widget, weight, flex = item
                else:
                    raise ValueError("The tuple of the content must be the length of "
                                     "2 or 3 parameters, with the following order: "
                                     "widget, weight and flex (optional)")
            else:
                widget = item
                weight = 1.0
                flex = True

            self._content.append(widget)
            self._weight.append(weight)

            widget.app = self.app
            widget.window = self.window
            self._impl.add_content(position, widget._impl, flex)
            widget.refresh()

    def _set_app(self, app):
        # Also assign the app to the content in the container
        if self.content:
            for content in self.content:
                content.app = app

    def _set_window(self, window):
        # Also assign the window to the content in the container
        if self._content:
            for content in self._content:
                content.window = window

    def refresh_sublayouts(self):
        """Refresh the layout and appearance of this widget."""
        if self.content is None:
            return
        for widget in self.content:
            widget.refresh()

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
