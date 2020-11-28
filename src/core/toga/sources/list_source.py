from .base import Source
from .row import Row


class ListSource(Source):
    """A data source to store a list of multiple data values, in a row-like fashion.

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

    ######################################################################
    # Methods required by the ListSource interface
    ######################################################################

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]

    ######################################################################
    # Utility methods to make ListSources more list-like
    ######################################################################

    def __setitem__(self, index, value):
        row = Row.create_row(data=value, accessors=self._accessors, source=self)
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
        row = Row.create_row(
            data=dict(zip(self._accessors, values), **named),
            accessors=self._accessors,
            source=self,
        )
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
