
class Variable:
    """A data source that helps you to store and manage data in a row like fashion.

    Args:
        data: The value for the variable.
        refresh_function (`callable`): A function invoked on data change.
    """

    def __init__(self, value):
        self._data = value
        self._listeners = []

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
        self._refresh()

    @property
    def listeners(self) -> list:
        """ The listeners of this data source.
        Listeners can be ``callable`` or :obj:``toga.Widget``.

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

    def _refresh(self):
        """ Invoke the refresh function on all widgets that are subscribed to this data source."""
        for listener in self._listeners:
            listener.refresh()
