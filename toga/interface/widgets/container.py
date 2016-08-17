class Container(object):
    '''This is a Widget that contains other widgets, but has no rendering or
    interaction of its own.

    :param children: An optional list of child Widgets that will be in this
                     container.
    :param style: an optional CSSNode object; if none is provided then a
                  new one will be created for the widget.
    '''
    def __init__(self, children=None, style=None):
        raise NotImplemented
