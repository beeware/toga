from __future__ import annotations

from typing import Generic, Protocol, TypeVar, runtime_checkable

ListenerT = TypeVar("ListenerT")
ItemT = TypeVar("ItemT", contravariant=True)


@runtime_checkable
class ValueListener(Protocol, Generic[ItemT]):
    """The protocol that must be implemented by objects that will act as a listener on a
    value data source.
    """

    def change(self, *, item: ItemT) -> None:
        """A change has occurred in an item.

        :param item: The data object that has changed.
        """


@runtime_checkable
class ListListener(ValueListener[ItemT], Protocol, Generic[ItemT]):
    """The protocol that must be implemented by objects that will act as a listener on a
    list data source.
    """

    def insert(self, *, index: int, item: ItemT) -> None:
        """An item has been added to the data source.

        :param index: The 0-index position in the data.
        :param item: The data object that was added.
        """

    def remove(self, *, index: int, item: ItemT) -> None:
        """An item has been removed from the data source.

        :param index: The 0-index position in the data.
        :param item: The data object that was added.
        """

    def clear(self) -> None:
        """All items have been removed from the data source."""


@runtime_checkable
class TreeListener(ListListener[ItemT], Protocol, Generic[ItemT]):
    """The protocol that must be implemented by objects that will act as a listener on a
    tree data source.
    """

    def insert(self, *, index: int, item: object, parent: ItemT | None = None) -> None:
        """An item has been added to the data source.

        :param index: The 0-index position in the data.
        :param item: The data object that was added.
        :param parent: The parent of the data object that was added, or `None`
            if it is a root item.
        """

    def remove(self, *, index: int, item: object, parent: ItemT | None = None) -> None:
        """An item has been removed from the data source.

        :param index: The 0-index position in the data.
        :param item: The data object that was added.
        :param parent: The parent of the data object that was removed, or `None`
            if it is a root item.
        """


class Source(Generic[ListenerT]):
    """A base class for data sources, providing an implementation of data
    notifications."""

    def __init__(self) -> None:
        self._listeners: list[ListenerT] = []

    @property
    def listeners(self) -> list[ListenerT]:
        """The listeners of this data source.

        :returns: A list of objects that are listening to this data source.
        """
        return self._listeners

    def add_listener(self, listener: ListenerT) -> None:
        """Add a new listener to this data source.

        If the listener is already registered on this data source, the request to add is
        ignored.

        :param listener: The listener to add
        """
        if listener not in self._listeners:
            self._listeners.append(listener)

    def remove_listener(self, listener: ListenerT) -> None:
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


def __getattr__(name):
    if name == "Listener":
        import warnings

        # Alias for backwards compatibility:
        # Jan 2025: In 0.5.3 and earlier, ListListener was named Listener
        global Listener
        Listener = ListListener
        warnings.warn(
            "The Listener protocol has been deprecated; "
            "use ListListener or TreeListener instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return Listener
    else:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
