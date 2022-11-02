import datetime
import warnings

from toga.handlers import wrapped_handler

from .base import Widget


class TimePicker(Widget):
    """A widget to get user selected datetime object.

    Args:
        id (str): An identifier for this widget.
        style (:obj:`Style`): An optional style object. If no style is provided then
            a new one will be created for the widget.
        value (str): The initial value to set the widget to. (Defaults to time of program execution)
        min_time (str): The minimum allowable time for the widget.
        max_time (str): The maximum allowable time for the widget.
        on_change (``callable``): Function that is invoked on time value change.
    """

    MIN_WIDTH = 100

    def __init__(
        self,
        id=None,
        style=None,
        factory=None,  # DEPRECATED!
        value=None,
        min_time=None,
        max_time=None,
        on_change=None,
        initial=None,  # DEPRECATED!
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

        self._on_change = None

        # Create a platform specific implementation of a TimePicker
        self._impl = self.factory.TimePicker(interface=self)

        ##################################################################
        # 2022-07: Backwards compatibility
        ##################################################################

        # initial replaced with value
        if initial is not None:
            if value is not None:
                raise ValueError(
                    "Cannot specify both `initial` and `value`; "
                    "`initial` has been deprecated, use `value`"
                )
            else:
                warnings.warn("`initial` has been renamed `value`", DeprecationWarning)
            value = initial

        ##################################################################
        # End backwards compatibility.
        ##################################################################

        self.min_time = min_time
        self.max_time = max_time
        # Set the value after the min/max has been set
        self.value = value
        # Set the change handler after the initial value has been set
        self.on_change = on_change

    @property
    def value(self):
        """The value of the currently selected time.

        :return: Selected time as time object
        """
        return self._impl.get_value()

    def _convert_time(self, value):
        if value is None:
            return datetime.datetime.today().time().replace(microsecond=0)
        elif isinstance(value, datetime.time):
            return value
        elif isinstance(value, datetime.datetime):
            return value.time()
        elif isinstance(value, str):
            return datetime.time.fromisoformat(value)
        else:
            raise TypeError("not a valid time value")

    @value.setter
    def value(self, value):
        self._impl.set_value(self._convert_time(value))

    @property
    def min_time(self):
        """The minimum allowable time for the widget. The widget will not allow
        the user to enter at time less than the min time. If initial time set
        is less than the minimum time, the minimum time will be used as the
        initial value.

        :return: The minimum time specified. Returns None if min_time not specified
        """
        return self._min_time

    @min_time.setter
    def min_time(self, value):
        if value is None:
            self._min_time = None
        else:
            self._min_time = self._convert_time(value)
        self._impl.set_min_time(self._min_time)

    @property
    def max_time(self):
        """The maximum allowable time for the widget. The widget will not allow
        the user to enter at time greater than the max time. If initial time
        set is greater than the maximum time, the maximum time will be used as
        the initial value.

        :return: The maximum time specified. Returns None if max_time not specified
        """
        return self._max_time

    @max_time.setter
    def max_time(self, value):
        if value is None:
            self._max_time = None
        else:
            self._max_time = self._convert_time(value)

        self._impl.set_max_time(self._max_time)

    @property
    def on_change(self):
        """The handler to invoke when the value changes.

        Returns:
            The function ``callable`` that is called on a content change.
        """
        return self._on_change

    @on_change.setter
    def on_change(self, handler):
        """Set the handler to invoke when the date is changed.

        Args:
            handler (:obj:`callable`): The handler to invoke when the date is changed.
        """
        self._on_change = wrapped_handler(self, handler)
        self._impl.set_on_change(self._on_change)
