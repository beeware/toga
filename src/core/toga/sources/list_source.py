from .base import Source


class Row:
    def __init__(self, **data):
        self._attrs = list(data.keys())
        self._source = None
        for name, value in data.items():
            setattr(self, name, value)

    ######################################################################
    # Utility wrappers
    ######################################################################

    def __setattr__(self, attr, value):
        super().__setattr__(attr, value)
        if attr in self._attrs:
            if self._source is not None:
                self._source._notify('change', item=self)


class ListSource(Source):
    """A data source to store a list of multiple data values, in a row-like fashion.

    Args:
        data (`list` of `dict`): The data for the list. Each entry in the list should
            be dict of accessors as keys and the data as values.
    """
    def __init__(self, data):
        super().__init__()
        self._data = []
        for value in data:
            self._data.append(self._create_row(value))

    ######################################################################
    # Methods required by the ListSource interface
    ######################################################################

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]

    ######################################################################
    # Factory methods for new rows
    ######################################################################

    def _create_row(self, data):
        """Create a Row object from the given data.
        Args:
            data (``dict`): Each key corresponds to a column accessor.
        """
        row = Row(**data)
        row._source = self
        return row

    ######################################################################
    # Utility methods to make ListSources more list-like
    ######################################################################

    def __setitem__(self, index, value):
        row = self._create_row(value)
        self._data[index] = row
        self._notify('insert', index=index, item=row)

    def __iter__(self):
        return iter(self._data)

    def clear(self):
        self._data = []
        self._notify('clear')

    def insert(self, index, *values, **named):
        # Coalesce values and data into a single data dictionary,
        # and use that to create the data row. Explicitly named data override.
        row = self._create_row(dict(zip(self._accessors, values), **named))
        self._data.insert(index, row)
        self._notify('insert', index=index, item=row)
        return row

    def prepend(self, *values, **named):
        return self.insert(0, *values, **named)

    def append(self, *values, **named):
        return self.insert(len(self), *values, **named)

    def remove(self, row):
        i = self._data.index(row)
        del self._data[i]
        self._notify('remove', index=i, item=row)
        return row

    def index(self, row):
        return self._data.index(row)
