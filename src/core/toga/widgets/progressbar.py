from .base import Widget
from types import GeneratorType


class ProgressBar(Widget):
    """"""

    def __init__(self, id=None, style=None, max=1, value=None, factory=None):
        """

        Args:
            id (str):  An identifier for this widget.
            style (:class:`colosseum.CSSNode`): An optional style object. If no style is provided then a
                new one will be created for the widget.
            max (float): The maximum value of the progressbar.
            value (float): To define the current progress of the progressbar.
            factory (:obj:`module`): A python module that is capable to return a
                implementation of this class with the same name. (optional & normally not needed)
        """
        super().__init__(id=id, style=style, factory=factory)

        self._value = None
        self._impl = self.factory.ProgressBar(interface=self)

        self.max = max
        self.value = value

        self.rehint()

    @property
    def running(self):
        """
        Returns:
            True if the progress bar is running,
            False if a specific value is displayed
        """
        return self.value is None

    @property
    def value(self):
        """ The progress value. Set to None to enter "running" mode.

        Returns:
            The current value as a ``int`` or ``float``.
        """
        return self._value

    @value.setter
    def value(self, value):
        if not isinstance(value, (int, float)) and value is not None:
            raise TypeError("expected int or float, got {}".format(type(value)))

        if value:
            if self.running:
                self._impl.stop()
                
            # bound value between 0 and self.max
            value = max(0, min(self.max, value))
            self._impl.set_value(value)
        elif not self.running:
            self._impl.start()

        self._value = value

    @property
    def max(self):
        """ The maximum value of the progressbar.

        Returns:
            The maximum value as a ``int`` or ``float``.
        """
        return self._max

    @max.setter
    def max(self, value):
        if not isinstance(value, (int, float)) and value is not None:
            raise TypeError("expected int or float, got {}".format(type(value)))

        self._max = value
        self._impl.set_max(value)
