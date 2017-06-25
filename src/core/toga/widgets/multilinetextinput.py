from .base import Widget


class MultilineTextInput(Widget):
    '''
    A multi-line text input widget
    '''
    def __init__(self, id=None, style=None, initial=None):
        '''
        Instantiate a new instance of the multi-line text input widget

        :param id:          An identifier for this widget.
        :type  id:          ``str``

        :param style:       an optional style object. If no style is provided then a
                            new one will be created for the widget.
        :type style:        :class:`colosseum.CSSNode`

        :param initial:     The initial value
        :type  initial:     ``str``
        '''
        super().__init__(id=id, style=style, initial=initial)
