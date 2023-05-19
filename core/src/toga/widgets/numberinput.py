from decimal import Decimal, InvalidOperation
from typing import Optional

from toga.handlers import wrapped_handler

from .base import Widget


class NumberInput(Widget):
    def __init__(
        self,
        id=None,
        style=None,
        step: Decimal = 1,
        min_value: Optional[Decimal] = None,
        max_value: Optional[Decimal] = None,
        value: Optional[Decimal] = None,
        readonly: bool = False,
        on_change=None,
    ):
        """Create a new single-line text input widget.

        Inherits from :class:`~toga.widgets.base.Widget`.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        :param step: The amount that any increment/decrement operations will
            apply to the widget's current value.
        :param min_value: Optional; if provided, ``value`` will be guaranteed to
            be greater than or equal to this minimum.
        :param min_value: Optional; if provided, ``value`` will be guaranteed to
            be greater than or equal to this minimum.
        :param value: Optional; the initial value for the widget.
        :param readonly: Can the value of the widget be modified by the user?
        :param on_change: A handler that will be invoked when the the value of
            the widget changes.
        """

        super().__init__(id=id, style=style)

        self.on_change = None
        self._impl = self.factory.NumberInput(interface=self)

        self.readonly = readonly
        self.step = step
        self.min_value = min_value
        self.max_value = max_value
        self.on_change = on_change

        if value is not None:
            self.value = value

    @property
    def readonly(self) -> bool:
        """Can the value of the widget be modified by the user?

        This only controls manual changes by the user (i.e., typing at the
        keyboard). Programmatic changes are permitted while the widget has
        ``readonly`` enabled.
        """
        return self._readonly

    @readonly.setter
    def readonly(self, value):
        self._readonly = value
        self._impl.set_readonly(value)

    @property
    def step(self) -> Decimal:
        """The amount that any increment/decrement operations will apply to the
        widget's current value.
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
    def min_value(self) -> Optional[Decimal]:
        """The minimum bound for the widget's value.

        Returns ``None`` if there is no minimum bound.
        """
        return self._impl.get_min_value()

    @min_value.setter
    def min_value(self, value):
        try:
            value = Decimal(value)
        except (ValueError, InvalidOperation):
            raise ValueError("min_value must be a number")
        except TypeError:
            value = None
        self._impl.set_min_value(value)

    @property
    def max_value(self) -> Optional[Decimal]:
        """The maximum bound for the widget's value.

        Returns ``None`` if there is no maximum bound.
        """
        return self.get_max_value()

    @max_value.setter
    def max_value(self, value):
        try:
            value = Decimal(value)
        except (ValueError, InvalidOperation):
            raise ValueError("max_value must be a number")
        except TypeError:
            value = None
        self._impl.set_max_value(value)

    @property
    def value(self) -> Optional[Decimal]:
        """Current value of the widget.

        Returns ``None`` if no value has been set on the widget
        """
        return self.get_value()

    @value.setter
    def value(self, value):
        try:
            value = Decimal(value)

            if self.min_value is not None and value < self.min_value:
                value = self.min_value
            elif self.max_value is not None and value > self.max_value:
                value = self.max_value
        except (ValueError, InvalidOperation):
            raise ValueError("value must be a number")
        except TypeError:
            value = None

        self._impl.set_value(value)

    @property
    def on_change(self):
        """The handler to invoke when the value of the widget changes."""
        return self._on_change

    @on_change.setter
    def on_change(self, handler):
        self._on_change = wrapped_handler(self, handler)
