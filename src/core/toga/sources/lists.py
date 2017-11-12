from .base import Source, Row, Value, to_accessor


class BaseListSource(Source):
    def __init__(self, accessors=None):
        super().__init__()
        self._accessors = accessors

    def prepend(self, *values, **data):
        return self.insert(0, *values, **data)

    def append(self, *values, **data):
        return self.insert(len(self), *values, **data)


class ListSource(BaseListSource):
    """A data source that helps you to store and manage data in a row like fashion.

    Args:
        accessors (`list`): A list of attribute names for accessing the value
            in each column of the row.
        data (`list`): The data in the list. Each entry in the list should have the
            same number of entries as there are accessors.
    """

    def __init__(self, data, accessors=None):
        super().__init__(accessors)
        self._data = []
        for datum in data:
            if isinstance(datum, dict):
                if self._accessors:
                    self._data.append(Row(self, **datum))
                else:
                    self._data.append(Value(self, **datum))
            elif isinstance(datum, (list, tuple)):
                if self._accessors:
                    self._data.append(
                        Row(self, **{
                            accessor: Value(self, value)
                            for accessor, value in zip(self._accessors, datum)
                        })
                    )
                else:
                    raise Exception("Can't add a list to a single-valued ListSource")
            else:
                self._data.append(datum)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]

    def clear(self):
        self._data = []
        self._notify('data_changed')

    def insert(self, index, *values, **data):
        # Coalesce values and data into a single data dictionary,
        # and use that to create the data row
        node = Row(self, **dict(
            data,
            **{
                accessor: value
                for accessor, value in zip(self._accessors, values)
            }
        ))
        self._data.insert(index, node)
        self._notify('data_changed')
        return node

    def remove(self, node):
        self._data.remove(node)
        self._notify('data_changed')
