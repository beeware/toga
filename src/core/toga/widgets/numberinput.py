from toga.handlers import wrapped_handler

from .base import Widget


class NumberInput(Widget):
    """ A `NumberInput` widget specifies a fixed range of possible numbers.
    The user has two buttons to increment/decrement the value by a step size.

    Args:
        id (str): An identifier for this widget.
        style (:obj:`Style`):  an optional style object.
            If no style is provided then a new one will be created for the widget.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)

        step (int): Step size of the adjustment buttons.
        **ex:
    """
    MIN_WIDTH = 100

    def __init__(self, id=None, style=None, factory=None, step=1,
                 min_value=None, max_value=None, readonly=False, on_change=None):
        super().__init__(id=id, style=style, factory=factory)
        self._value = None
        self._impl = self.factory.NumberInput(interface=self)

        self.readonly = readonly
        self.step = step
        self.min_value = min_value
        self.max_value = max_value
        self.on_change = on_change

    @property
    def readonly(self):
        """ Whether a user can write into the text input

        Returns:
            ``True`` if only read is possible.
            ``False`` if read and write is possible.
        """
        return self._readonly

    @readonly.setter
    def readonly(self, value):
        self._readonly = value
        self._impl.set_readonly(value)

    @property
    def step(self):
        """The step value for the widget

        Returns:
            The current step value for the widget.
        """
        return self._step

    @step.setter
    def step(self, step):
        try:
            self._step = int(step)
        except (ValueError, TypeError):
            raise ValueError("step must be an integer")
        self._impl.set_step(step)

    @property
    def min_value(self):
        """The minimum bound for the widget's value.

        Returns:
            The minimum bound for the widget's value. If the minimum bound
            is None, there is no minimum bound.
        """
        return self._min_value

    @min_value.setter
    def min_value(self, value):
        try:
            self._min_value = int(value)
        except ValueError:
            raise ValueError("min_value must be an integer")
        except TypeError:
            self._min_value = None
        self._impl.set_min_value(value)

    @property
    def max_value(self):
        """The maximum bound for the widget's value.

        Returns:
            The maximum bound for the widget's value. If the maximum bound
            is None, there is no maximum bound.
        """
        return self._max_value

    @max_value.setter
    def max_value(self, value):
        try:
            self._max_value = int(value)
        except ValueError:
            raise ValueError("max_value must be an integer")
        except TypeError:
            self._max_value = None
        self._impl.set_max_value(value)

    @property
    def value(self):
        """Current value contained by the widget

        Returns:
            The current value(int) of the widget. Returns None
            if the field has no value set.
        """
        return self._value

    @value.setter
    def value(self, value):
        try:
            self._value = int(value)
        except ValueError:
            raise ValueError("value must be an integer")
        except TypeError:
            self._value = None

        if self.min_value is not None and value < self.min_value:
            self._value = self.min_value
        elif self.max_value is not None and value > self.max_value:
            self._value = self.max_value
        self._impl.set_value(value)

    @property
    def on_change(self):
        """The handler to invoke when the value changes

        Returns:
            The function ``callable`` that is called on a content change.
        """
        return self._on_change

    @on_change.setter
    def on_change(self, handler):
        """Set the handler to invoke when the value is changeed.

        Args:
            handler (:obj:`callable`): The handler to invoke when the value is changeed.
        """
        self._on_change = wrapped_handler(self, handler)
        self._impl.set_on_change(self._on_change)
