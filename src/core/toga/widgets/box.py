from .base import Widget


class Box(Widget):
    '''
    This is a Widget that contains other widgets, but has no rendering or
    interaction of its own.

    :param id:          An identifier for this widget.
    :type  id:          ``str``

    :param style:       an optional style object. If no style is provided then a
                        new one will be created for the widget.
    :type style:        :class:`colosseum.CSSNode`

    :param children:    An optional list of child Widgets that will be in this
                        box.
    :type children:     ``list``
    '''

    def __init__(self, id=None, style=None, factory=None, children=None):
        super().__init__(id=id, style=style, factory=factory)
        self._children = []
        if children:
            for child in children:
                self.add(child)

        self._impl = self.factory.Box(interface=self)

