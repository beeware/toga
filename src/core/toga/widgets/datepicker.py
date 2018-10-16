from .base import Widget


class DatePicker(Widget):
    """
    A widget to get user selected datetime object

    Args:
        id (str): An identifier for this widget.
        style (:obj:`Style`): An optional style object. If no style is provided then
            a new one will be created for the widget.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)
    """
    MIN_WIDTH = 200

    def __init__(self, id=None, style=None, factory=None):
        super().__init__(id=id, style=style, factory=factory)
        # Create a platform specific implementation of a DatePicker
        self._impl = self.factory.DatePicker(interface=self)

    @property
    def value(self):
        """
        The value of the currently selected date.

        :return: Selected date as DateTime object
        """
        return self._impl.get_value()


