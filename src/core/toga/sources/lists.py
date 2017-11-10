from .base import Source, Row, Datum, to_accessor


class BaseListSource(Source):
    def __init__(self, accessors):
        super().__init__()
        self._accessors = accessors

    def append(self, *values, **data):
        return self.insert(len(self._data), *values, **data)


class ListSource(BaseListSource):
    """A data source that helps you to store and manage data in a row like fashion.

    Args:
        accessors (`list`): A list of attribute names for accessing the value
            in each column of the row.
        data (`list`): The data in the list. Each entry in the list should have the
            same number of entries as there are accessors.
    """

    def __init__(self, accessors, data):
        super().__init__(accessors)
        self._data = []
        self.create_rows(data)

    def create_rows(self, data):
        for datum in data:
            if isinstance(datum, dict):
                self._data.append(Row(**datum))
            elif isinstance(datum, (list, tuple)):
                self._data.append(
                    Row(**{
                        accessor: Datum(value)
                        for accessor, value in zip(self._accessors, datum)
                    })
                )
            else:
                self._data.append(datum)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]

    def clear(self):
        self._data = []
        self._notify('refresh')

    def insert(self, index, *values, **data):
        # Coalesce values and data into a single data dictionary,
        # and use that to create the data row
        node = Row(**dict(
            data,
            **{
                accessor: value
                for accessor, value in zip(self._accessors, values)
            }
        ))
        self._data.insert(index, node)
        self._notify('refresh')
        return node

    def remove(self, node):
        self._data.remove(node)
        self._notify('refresh')
