import datetime
import warnings

from toga.handlers import wrapped_handler

from .base import Widget


class DatePicker(Widget):
    """A widget to get user selected datetime object.

    Args:
        id (str): An identifier for this widget.
        style (:obj:`Style`): An optional style object. If no style is provided then
            a new one will be created for the widget.
    """

    _MIN_WIDTH = 200

    def __init__(
        self,
        id=None,
        style=None,
        factory=None,  # DEPRECATED!
        value=None,
        min_date=None,
        max_date=None,
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

        # Create a platform specific implementation of a DatePicker
        self._impl = self.factory.DatePicker(interface=self)

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

        self.value = value
        self.min_date = min_date
        self.max_date = max_date
        self.on_change = on_change

    @property
    def value(self):
        """The value of the currently selected date.

        :return: Selected date as Date object
        """
        return self._impl.get_value()

    def _convert_date(self, value):
        if value is None:
            return datetime.date.today()
        elif isinstance(value, datetime.datetime):
            return value.date()
        elif isinstance(value, datetime.date):
            return value
        elif isinstance(value, str):
            return datetime.date.fromisoformat(value)
        else:
            raise TypeError("not a valid date value")

    @value.setter
    def value(self, value):
        self._impl.set_value(self._convert_date(value))

    @property
    def min_date(self):
        """The minimum allowable date for the widget. All dates prior to the
        minimum date will be blanked out.

        :return: The minimum date specified. Returns None if min_date not specified
        """
        return self._min_date

    @min_date.setter
    def min_date(self, value):
        if value is None:
            self._min_date = None
        else:
            self._min_date = self._convert_date(value)

        self._impl.set_min_date(self._min_date)

    @property
    def max_date(self):
        """The maximum allowable date for the widget. All dates prior to the
        minimum date will be blanked out.

        :return: The maximum date specified. Returns None if max_date not specified
        """
        return self._max_date

    @max_date.setter
    def max_date(self, value):
        if value is None:
            self._max_date = None
        else:
            self._max_date = self._convert_date(value)

        self._impl.set_max_date(self._max_date)

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
