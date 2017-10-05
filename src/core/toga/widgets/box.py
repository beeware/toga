from .base import Widget


class Box(Widget):
    """ This is a Widget that contains other widgets, but has no rendering or
    interaction of its own.

    Args:
        id (str): An identifier for this widget.
        style (:class:colosseum.CSSNode`): An optional style object. If no style is provided then a new one will be created for the widget.
        children (``list`` of :class:`toga.Widget`):  An optional list of child Widgets that will be in this box.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)
    """

    def __init__(self, id=None, style=None, children=None, factory=None):
        super().__init__(id=id, style=style, factory=factory)
        self._children = []
        if children:
            for child in children:
                self.add(child)

        self._impl = self.factory.Box(interface=self)

