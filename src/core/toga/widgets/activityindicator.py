from .base import Widget


class ActivityIndicator(Widget):

    def __init__(self, id=None, style=None, hide_when_stopped=True, factory=None):
        super().__init__(id=id, style=style, factory=factory)

        self._is_running = False
        self._hide_when_stopped = hide_when_stopped

        # Create a platform specific implementation
        self._impl = self.factory.ActivityIndicator(interface=self)


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
        self._impl.stop()
        if self.is_running:
            self._impl.stop()
        self._is_running = False
