import datetime

from toga.handlers import wrapped_handler

from .base import Widget


class TimePicker(Widget):
    """
    A widget to get user selected datetime object

    Args:
        id (str): An identifier for this widget.
        style (:obj:`Style`): An optional style object. If no style is provided then
            a new one will be created for the widget.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)
        initial (str): The initial value to set the widget to. (Defaults to time of program execution)
        min_time (str): The minimum allowable time for the widget.
        max_time (str): The maximum allowable time for the widget.
        on_change (``callable``): Function that is invoked on time value change.
    """
    MIN_WIDTH = 100

    def __init__(self, id=None, style=None, factory=None, initial=None, min_time=None, max_time=None, on_change=None):
        super().__init__(id=id, style=style, factory=factory)
        self._on_change = None

        # Create a platform specific implementation of a TimePicker
        self._impl = self.factory.TimePicker(interface=self)
        self.min_time = min_time
        self.max_time = max_time
        # Set the value after the min/max has been set
        self.value = initial
        # Set the change handler after the initial value has been set
        self.on_change = on_change

    @property
    def value(self):
        """
        The value of the currently selected time.

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
        """
        The minimum allowable time for the widget. The widget will not allow the user to enter at time less than the
        min time. If initial time set is less than the minimum time, the minimum time will be used as
        the initial value.

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
        """
        The maximum allowable time for the widget. The widget will not allow the user to enter at time greater than the
        max time. If initial time set is greater than the maximum time, the maximum time will be used as
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
        """The handler to invoke when the value changes

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
