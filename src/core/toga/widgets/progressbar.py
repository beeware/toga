from .base import Widget


class ProgressBar(Widget):
    """
    """
    MIN_WIDTH = 100

    def __init__(self, id=None, style=None, max=None, value=None, factory=None):
        """

        Args:
            id (str):  An identifier for this widget.
            style (:obj:`Style`): An optional style object. If no style is provided then a
                new one will be created for the widget.
            max (float): The maximum value of the progressbar.
            value (float): To define the current progress of the progressbar.
            factory (:obj:`module`): A python module that is capable to return a
                implementation of this class with the same name. (optional & normally not needed)
        """
        super().__init__(id=id, style=style, factory=factory)
        self._impl = self.factory.ProgressBar(interface=self)

        self.max = max
        self.value = value
        self._running = False

    @property
    def value(self):
        """ The progress value

        Returns:
            The current value as a ``int`` or ``float``.
        """
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self._impl.set_value(value)
        self._running = self._value is not None

    @property
    def max(self):
        """ The maximum value of the progressbar.

        Returns:
            The maximum value as a ``int`` or ``float``.
        """
        return self._max

    @max.setter
    def max(self, max):
        self._max = max
        self._impl.set_max(max)
