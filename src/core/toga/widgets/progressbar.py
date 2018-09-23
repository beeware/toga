from .base import Widget


class ProgressBar(Widget):
    """
    """
    MIN_WIDTH = 100

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
            style (:obj:`Style`): An optional style object. If no style is provided then a
                new one will be created for the widget.
            max (float): The maximum value of the progressbar.
            value (float): To define the current progress of the progressbar.
            running (bool): Set the inital running mode.
            factory (:obj:`module`): A python module that is capable to return a
                implementation of this class with the same name. (optional & normally not needed)
        """
        super().__init__(id=id, style=style, factory=factory)

        self._is_running = False
        self._impl = self.factory.ProgressBar(interface=self)
        self._value = value

        self.max = max

        if running:
            self.start()
        else:
            self.stop()

        self.value = value

    @property
    def is_running(self):
        """
        Use ``start()`` and ``stop()`` to change the running state.

        Returns:
            True if this progress bar is running
            False otherwise
        """
        return self._is_running

    @property
    def is_determinate(self):
        """
        Determinate progress bars have a numeric ``max`` value (not None).

        Returns:
            True if this progress bar is determinate (``max`` is not None)
            False if ``max`` is None
        """
        return self.max is not None

    def start(self):
        """
        Starting this progress bar puts it into running mode.
        """
        self.enabled = True
        if not self.is_running:
            self._impl.start()
        self._is_running = True

    def stop(self):
        """
        Stop this progress bar (if not already stopped).
        """
        self._enabled = bool(self.max)
        if self.is_running:
            self._impl.stop()
        self._is_running = False

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
        self.enabled = bool(value or self.is_running)

        self._max = value
        self._impl.set_max(value)
