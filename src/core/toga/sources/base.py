from typing import Any


class Source:
    def __init__(self) -> None:
        """Base class for data sources in toga."""
        self._listeners = []

    @property
    def listeners(self) -> list:
        """The listeners of this data source.

        Listeners should be objects which can react to changes in the data source.
        Different data source implementations may emit different notifications, e.g.,
        "changed" or "insert", and listeners should implement corresponding methods to
        be invoked,

        :returns: List of listeners.
        """
        return self._listeners

    def add_listener(self, listener: Any) -> None:
        """Adds a new lister to the source."""
        self._listeners.append(listener)

    def remove_listener(self, listener: Any) -> None:
        """Removes the given listener from the source."""
        self._listeners.remove(listener)

    def _notify(self, notification: str, **kwargs: Any) -> None:
        """
        Invoke a notification function on all listeners that are subscribed to this data
        source.

        :param notification: Name of method to call on the listeners.
        :param kwargs: Keyword arguments to provide to method call.
        """
        for listener in self._listeners:
            try:
                method = getattr(listener, notification)
            except AttributeError:
                method = None

            if method:
                method(**kwargs)
