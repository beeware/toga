from __future__ import annotations

from typing import Protocol


class Listener(Protocol):
    """The protocol that must be implemented by objects that will act as a listener on a
    data source.
    """

    def change(self, item: object) -> object:
        """A change has occurred in an item.

        :param item: The data object that has changed.
        """

    def insert(self, index: int, item: object) -> object:
        """An item has been added to the data source.

        :param index: The 0-index position in the data.
        :param item: The data object that was added.
        """

    def remove(self, index: int, item: object) -> object:
        """An item has been removed from the data source.

        :param index: The 0-index position in the data.
        :param item: The data object that was added.
        """

    def clear(self) -> object:
        """All items have been removed from the data source."""


class Source:
    """A base class for data sources, providing an implementation of data notifications."""

    def __init__(self) -> None:
        self._listeners: list[Listener] = []

    @property
    def listeners(self) -> list[Listener]:
        """The listeners of this data source.

        :returns: A list of objects that are listening to this data source.
        """
        return self._listeners

    def add_listener(self, listener: Listener) -> None:
        """Add a new listener to this data source.

        If the listener is already registered on this data source, the
        request to add is ignored.

        :param listener: The listener to add
        """
        if listener not in self._listeners:
            self._listeners.append(listener)

    def remove_listener(self, listener: Listener) -> None:
        """Remove a listener from this data source.

        :param listener: The listener to remove.
        """
        self._listeners.remove(listener)

    def notify(self, notification: str, **kwargs: object) -> None:
        """Notify all listeners an event has occurred.

        :param notification: The notification to emit.
        :param kwargs: The data associated with the notification.
        """
        for listener in self._listeners:
            try:
                method = getattr(listener, notification)
            except AttributeError:
                method = None

            if method:
                method(**kwargs)
