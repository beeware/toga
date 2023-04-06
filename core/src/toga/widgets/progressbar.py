from .base import Widget


class ProgressBar(Widget):
    _MIN_WIDTH = 100

    def __init__(
        self,
        id=None,
        style=None,
        max=1.0,
        value=0.0,
        running=False,
    ):
        """Create a new Progress Bar widget.

        Inherits from :class:`~toga.widgets.base.Widget`.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        :param max: The value that represents completion of the task. Must
            be > 0.0; defaults to 1.0. A value of ``None`` indicates that the task
            length is indeterminate.
        :param value: The current progress against the maximum value. Must be
            between 0.0 and ``max``; any value outside this range will be
            clipped. Defaults to 0.0.
        :param running: Describes whether the indicator is running at the time
            it is created. Default is False.
        """
        super().__init__(id=id, style=style)

        self._impl = self.factory.ProgressBar(interface=self)

        self.max = max
        self.value = value

        if running:
            self.start()

    @property
    def enabled(self):
        """Is the widget currently enabled? i.e., can the user interact with the
        widget?

        ProgressBar widgets cannot be disabled; this property will always
        return True; any attempt to modify it will be ignored."""
        return True

    @enabled.setter
    def enabled(self, value):
        pass

    @property
    def is_running(self):
        """Describe if the activity indicator is currently running.

        Use ``start()`` and ``stop()`` to change the running state.

        True if this activity indicator is running; False otherwise.
        """
        return self._impl.is_running()

    @property
    def is_determinate(self):
        """Describe whether the progress bar has a known or indeterminate maximum.

        True if the progress bar has determinate length; False otherwise.
        """
        return self.max is not None

    def start(self):
        """Start the progress bar.

        If the progress bar is already started, this is a no-op.
        """
        if not self.is_running:
            self._impl.start()

    def stop(self):
        """Stop the progress bar.

        If the progress bar is already stopped, this is a no-op.
        """
        if self.is_running:
            self._impl.stop()

    @property
    def value(self):
        """The current value of the progress indicator.

        If the progress bar is determinate, the value must be between 0 and
        ``max``. Any value outside this range will be clipped.

        If the progress bar is indeterminate, changes in value will be ignored,
        and the current value will be returned as ``None``.
        """
        return self._impl.get_value()

    @value.setter
    def value(self, value):
        if self.max is not None:
            value = max(0.0, min(self.max, float(value)))
            self._impl.set_value(value)

    @property
    def max(self):
        """The value indicating completion of the task being monitored.

        Must be a number > 0, or ``None`` for a task of indeterminate length.
        """
        return self._impl.get_max()

    @max.setter
    def max(self, value):
        if value is None:
            self._impl.set_max(None)
        elif float(value) > 0.0:
            self._impl.set_max(float(value))
        else:
            raise ValueError("max value must be None, or a numerical value > 0")
