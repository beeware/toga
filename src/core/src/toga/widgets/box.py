import warnings

from .base import Widget


class Box(Widget):
    """This is a Widget that contains other widgets, but has no rendering or
    interaction of its own.

    Args:
        id (str): An identifier for this widget.
        style (:class:~colosseum.CSSNode`): An optional style object. If no
            style is provided then a new one will be created for the widget.
        children (``list`` of :class:`~toga.Widget`):  An optional list of child
            Widgets that will be in this box.
    """

    def __init__(
        self,
        id=None,
        style=None,
        children=None,
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

        self._children = []
        if children:
            self.add(*children)

        # Create a platform specific implementation of a Box
        self._impl = self.factory.Box(interface=self)
