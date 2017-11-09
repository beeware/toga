

class ListDataSource:
    """ A data source that helps you to store and manage data in a row like fashion.

    Args:
        data (`list` of `tuple`): A list of tuples containing the data for every row.
        refresh_function (`callable`): A function invoked on data change.
    """

    def __init__(self, data):
        self._data = self.create_rows(data)
        self._listeners = []

    def create_rows(self, data):
        return [TableRow(data=row_data) for row_data in data]

    @property
    def data(self):
        return self._data

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

    def clear(self):
        self._data = []
        self._refresh()

    def insert(self, index: int, data, icon=None):
        node = TableRow(data=data, icon=icon)
        self._data.insert(index, node)
        self._refresh()
        return node

    def remove(self, node):
        self._data.remove(node)
        self._refresh()

    def item(self, row: int, column: int):
        if isinstance(row and column, int):
            return self._data[row].data[column]

    def row(self, row: int) -> TableRow:
        if row >= 0:
            return self._data[row]

    @property
    def rows(self) -> list:
        return self.data
