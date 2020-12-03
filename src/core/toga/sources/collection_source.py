from toga.sources import Source
from toga.sources.row import Row


class CollectionSource(Source):
    """An abstract data source to store a collection of multiple data values, in a row-like fashion.
    Example implementations can be list, stack, set, queue, etc.

    Args:
        data (`list`): The data in the list. Each entry in the list should have the
            same number of entries as there are accessors.
        accessors (`list`): A list of attribute names for accessing the value
            in each column of the row.
    """
    def __init__(self, data, accessors):
        super().__init__()
        self._accessors = accessors.copy()
        self._data = []
        for value in data:
            self._data.append(
                Row.create_row(data=value, accessors=self._accessors, source=self)
            )

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]

    def __delitem__(self, index):
        del self._data[index]

    def __iter__(self):
        return iter(self._data)

    def clear(self):
        self._data = []
        self._notify('clear')

    def index(self, row):
        return self._data.index(row)
