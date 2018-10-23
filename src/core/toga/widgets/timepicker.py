from .base import Widget
from toga.handlers import wrapped_handler
import datetime


class TimePicker(Widget):
    """
    A widget to get user selected datetime object

    Args:
        id (str): An identifier for this widget.
        style (:obj:`Style`): An optional style object. If no style is provided then
            a new one will be created for the widget.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)
    """
    MIN_WIDTH = 100

    def __init__(self, id=None, style=None, factory=None, initial=None, min_time=None, max_time=None, on_change=None):
        super().__init__(id=id, style=style, factory=factory)
        # Create a platform specific implementation of a TimePicker
        self._impl = self.factory.TimePicker(interface=self)
        self.value = initial
        self.min_time = min_time
        self.max_time = max_time
        self.on_change = on_change

    @property
    def value(self):
        """
        The value of the currently selected date.

        :return: Selected date as Date object
        """
        return self._impl.get_value()

    @value.setter
    def value(self, value):
        if value is None:
            v = str(datetime.datetime.today())
        else:
            v = str(value)
        self._impl.set_value(v)

    @property
    def min_time(self):
        """
        The minimum allowable date for the widget. All dates prior to the minimum date will be blanked out.

        :return: The minimum date specified. Returns None if min_date not specified
        """
        return self._min_time

    @min_time.setter
    def min_time(self, value):
        self._min_time = None
        if value is not None:
            self._min_time = str(value)
            self._impl.set_min_time(self._min_time)

    @property
    def max_time(self):
        """
        The maximum allowable date for the widget. All dates prior to the minimum date will be blanked out.

        :return: The maximum date specified. Returns None if max_date not specified
        """
        return self._max_time

    @max_time.setter
    def max_time(self, value):
        self._max_time = None
        if value is not None:
            self._max_time = str(value)
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
