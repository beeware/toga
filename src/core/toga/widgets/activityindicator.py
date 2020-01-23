from .base import Widget


class ActivityIndicator(Widget):

    def __init__(self, id=None, style=None, running=False, hide_when_stopped=True, factory=None):
        """

        Args:
            id (str):  An identifier for this widget.
            style (:obj:`Style`): An optional style object. If no style is provided then a
                new one will be created for the widget.
            running (bool):  Set the inital running mode. Defaults to False
            hide_when_stopped (bool):  Hide the indicator when not running. Defaults to
                True.
            factory (:obj:`module`): A python module that is capable to return a
                implementation of this class with the same name. (optional & normally not needed)
        """
        super().__init__(id=id, style=style, factory=factory)

        self._is_running = False
        self._hide_when_stopped = hide_when_stopped

        self._impl = self.factory.ActivityIndicator(interface=self)

        if running:
            self.start()
        else:
            self.stop()

    @property
    def is_running(self):
        """
        Use ``start()`` and ``stop()`` to change the running state.

        Returns:
            True if this activity indicator is running
            False otherwise
        """
        return self._is_running

    @property
    def hide_when_stopped(self):
        """Hide this activity indicator when stopped."""
        return self._hide_when_stopped

    @hide_when_stopped.setter
    def hide_when_stopped(self, value):
        self._hide_when_stopped = value
        self._impl.set_hide_when_stopped(value)

    def start(self):
        """
        Start this acivity indicator.
        """
        if not self.is_running:
            self._impl.start()
        self._is_running = True

    def stop(self):
        """
        Stop this acivity indicator (if not already stopped).
        """
        if self.is_running:
            self._impl.stop()
        self._is_running = False
