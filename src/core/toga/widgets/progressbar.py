from .base import Widget
from types import GeneratorType


class ProgressBar(Widget):
    """"""

    def __init__(self,
                 id=None,
                 style=None,
                 max=1,
                 value=0,
                 running=False,
                 factory=None):
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

        self._running = False
        self._impl = self.factory.ProgressBar(interface=self)

        self.max = max
        self.running = running
        self.value = value

        self.rehint()

    @property
    def running(self):
        """
        Returns:
            True if the progress bar is running,
            False if not
        """
        return self._running

    @running.setter
    def running(self, value):
        #changed = value != self._running

        self._running = value

        # if changed:
        self.enabled = bool(value or self.max)
        self._impl.set_running(value)

    @property
    def value(self):
        """
        Returns:
            The current value as a ``int`` or ``float``.
        """
        return self._value

    @value.setter
    def value(self, value):
        if self.max:
            # default to 0 if value is None
            # bound value between 0 and self.max
            self._value = max(0, min(self.max, value or 0))
            self._impl.set_value(value)

    @property
    def max(self):
        """ The maximum value of the progressbar.

        Returns:
            The maximum value as a ``int`` or ``float``.
        """
        return self._max

    @max.setter
    def max(self, value):
        self.enabled = bool(value or self.running)

        self._max = value
        self._impl.set_max(value)
