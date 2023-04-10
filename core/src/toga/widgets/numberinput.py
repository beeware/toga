import warnings
from decimal import Decimal, InvalidOperation

from toga.handlers import wrapped_handler

from .base import Widget


class NumberInput(Widget):
    """A `NumberInput` widget specifies a fixed range of possible numbers. The
    user has two buttons to increment/decrement the value by a step size. Step,
    min and max can be integers, floats, or Decimals; They can also be
    specified as strings, which will be converted to Decimals internally. The
    value of the widget will be evaluated as a Decimal.

    Args:
        id (str): An identifier for this widget.
        style (:obj:`Style`):  an optional style object.
            If no style is provided then a new one will be created for the widget.

        step (number): Step size of the adjustment buttons.
        min_value (number): The minimum bound for the widget's value.
        max_value (number): The maximum bound for the widget's value.
        value (number): Initial value for the widget
        readonly (bool):  Whether a user can write/change the number input, defaults to `False`.
        on_change (``callable``): The handler to invoke when the value changes.
        **ex:
    """

    def __init__(
        self,
        id=None,
        style=None,
        factory=None,  # DEPRECATED!
        step=1,
        min_value=None,
        max_value=None,
        value=None,
        readonly=False,
        on_change=None,
        default=None,  # DEPRECATED!
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

        self._value = None
        self._on_change = None
        self._impl = self.factory.NumberInput(interface=self)

        ##################################################################
        # 2022-07: Backwards compatibility
        ##################################################################

        # default replaced with value
        if default is not None:
            if value is not None:
                raise ValueError(
                    "Cannot specify both `default` and `value`; "
                    "`default` has been deprecated, use `value`"
                )
            else:
                warnings.warn("`default` has been renamed `value`", DeprecationWarning)
            value = default

        ##################################################################
        # End backwards compatibility.
        ##################################################################

        self.readonly = readonly
        self.step = step
        self.min_value = min_value
        self.max_value = max_value
        self.on_change = on_change

        if value is not None:
            self.value = value

    @property
    def readonly(self):
        """Whether a user can write/change the number input.

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
        """The step value for the widget.

        Returns:
            The current step value for the widget.
        """
        return self._step

    @step.setter
    def step(self, step):
        try:
            self._step = Decimal(step)
        except (ValueError, TypeError, InvalidOperation):
            raise ValueError("step must be an number")
        self._impl.set_step(self._step)

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
            self._min_value = Decimal(value)
        except (ValueError, InvalidOperation):
            raise ValueError("min_value must be a number")
        except TypeError:
            self._min_value = None
        self._impl.set_min_value(self._min_value)

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
            self._max_value = Decimal(value)
        except (ValueError, InvalidOperation):
            raise ValueError("max_value must be a number")
        except TypeError:
            self._max_value = None
        self._impl.set_max_value(self._max_value)

    @property
    def value(self):
        """Current value contained by the widget.

        Returns:
            The current value(int) of the widget. Returns None
            if the field has no value set.
        """
        return self._value

    @value.setter
    def value(self, value):
        try:
            self._value = Decimal(value)

            if self.min_value is not None and self._value < self.min_value:
                self._value = self.min_value
            elif self.max_value is not None and self._value > self.max_value:
                self._value = self.max_value
        except (ValueError, InvalidOperation):
            raise ValueError("value must be a number")
        except TypeError:
            self._value = None

        self._impl.set_value(value)

    @property
    def on_change(self):
        """The handler to invoke when the value changes.

        Returns:
            The function ``callable`` that is called on a content change.
        """
        return self._on_change

    @on_change.setter
    def on_change(self, handler):
        """Set the handler to invoke when the value is changed.

        Args:
            handler (:obj:`callable`): The handler to invoke when the value is changed.
        """
        self._on_change = wrapped_handler(self, handler)
        self._impl.set_on_change(self._on_change)
