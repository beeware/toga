from .base import Widget


class ActivityIndicator(Widget):
    def __init__(self, id=None, style=None, running=False):
        """
        Create a new ActivityIndicator widget.

        Inherits from :class:`~toga.widgets.base.Widget`.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        :param running: Describes whether the indicator is running at the
            time it is created.
        """
        super().__init__(id=id, style=style)

        self._impl = self.factory.ActivityIndicator(interface=self)

        if running:
            self.start()

    @property
    def enabled(self):
        """Is the widget currently enabled? i.e., can the user interact with the
        widget?

        ActivityIndicator widgets cannot be disabled; this property will always
        return True; any attempt to modify it will be ignored."""
        return True

    @enabled.setter
    def enabled(self, value):
        pass

    def focus(self):
        "No-op; ActivityIndicator cannot accept input focus"
        pass

    @property
    def is_running(self):
        """Determine if the activity indicator is currently running.

        Use ``start()`` and ``stop()`` to change the running state.

        True if this activity indicator is running; False otherwise.
        """
        return self._impl.is_running()

    def start(self):
        """Start the activity indicator.

        If the activity indicator is already started, this is a no-op.
        """
        if not self.is_running:
            self._impl.start()

    def stop(self):
        """Stop the activity indicator.

        If the activity indicator is already stopped, this is a no-op.
        """
        if self.is_running:
            self._impl.stop()
