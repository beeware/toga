from .base import Widget


class NumberInput(Widget):
    """ A `NumberInput` widget specifies a fixed range of possible numbers.
    The user has two buttons to increment/decrement the value by a step size.

    Args:
        id (str): An identifier for this widget.
        style (:class:`colosseum.CSSNode`):  an optional style object.
            If no style is provided then a new one will be created for the widget.
        factory (:obj:`module`): A python module that is capable to return a
        implementation of this class with the same name. (optional & normally not needed)

        min_value (int): Minimum value (default 0)
        max_value (int): Maximum value (default 100)
        step (int): Step size of the adjustment buttons.
        **ex:
    """

    def __init__(self, id=None, style=None, factory=None,
                 min_value=0, max_value=100, step=1, **ex):
        super().__init__(id=id, style=style, factory=factory)
        self._min_value = min_value
        self._max_value = max_value
        self._step = step
        self._impl = self.factory.NumberInput(interface=self)

    @property
    def value(self):
        """ Current value

        Returns:
            The current value(int) of the widget.
        """
        return self._impl.get_value()

    @value.setter
    def value(self, value):
        self._impl.set_value(value)
