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
                self.create_row(data=value, accessors=self._accessors, source=self)
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

    @classmethod
    def create_row(cls, data, accessors, source=None):
        """Create a Row object from the given data.
        Args:
            data (any): The type of `data` determines how it is handled
                ``dict``: each key corresponds to a column accessor
                iterables, except ``str`` and ``dict``: each item corresponds to a column
                all else: `data` will fill the first column
            accessors (`list`): A list of attribute names for accessing the value
                in each column of the row.
            source (any): A source to attach to the row
        """

        if isinstance(data, dict):
            row = Row(**data)
        elif hasattr(data, '__iter__') and not isinstance(data, str):
            row = Row(**dict(zip(accessors, data)))
        else:
            row = Row(**{accessors[0]: data})
        if source is not None:
            row._source = source
        return row

