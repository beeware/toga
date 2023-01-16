class Source:
    def __init__(self):
        self._listeners = []

    @property
    def listeners(self) -> list:
        """The listeners of this data source. Listeners can be ``callable`` or
        :obj:``toga.Widget``.

        Returns:
            A list of objects that are listening for data change.
        """
        return self._listeners

    def add_listener(self, listener):
        """
        Args:
            listener: ``callable`` or :obj:``toga.Widget`
        """
        self._listeners.append(listener)

    def remove_listener(self, listener):
        self._listeners.remove(listener)

    def _notify(self, notification, **kwargs):
        """Invoke a notification function on all listeners that are subscribed
        to this data source."""
        for listener in self._listeners:
            try:
                method = getattr(listener, notification)
            except AttributeError:
                method = None

            if method:
                method(**kwargs)
