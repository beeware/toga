from __future__ import annotations

from typing import Any

from .base import Source


class Row:
    def __init__(self, **data):
        """Create a new Row object.

        The keyword arguments specified in the constructor will be converted
        into attributes on the new Row object.

        When any of the named attributes are modified, the source to which the
        row belongs will be notified.
        """
        self._attrs = list(data.keys())
        self._source = None
        for name, value in data.items():
            setattr(self, name, value)

    def __repr__(self):
        descriptor = " ".join(f"{attr}={getattr(self, attr)!r}" for attr in self._attrs)
        return f"<Row {id(self):x} {descriptor if descriptor else '(no attributes)'}>"

    ######################################################################
    # Utility wrappers
    ######################################################################

    def __setattr__(self, attr: str, value):
        """Set an attribute on the Row object, notifying the source of the change.

        :param attr: The attribute to change.
        :param value: The new attribute value.
        """
        super().__setattr__(attr, value)
        if attr in self._attrs:
            if self._source is not None:
                self._source.notify("change", item=self)


class ListSource(Source):
    def __init__(self, accessors: list[str], data: list[Any] | None = None):
        """A data source to store an ordered list of multiple data values.

        :param accessors: A list of attribute names for accessing the value
            in each column of the row.
        :param data: The initial list of items in the source.
        """

        super().__init__()
        if isinstance(accessors, str) or not hasattr(accessors, "__iter__"):
            raise ValueError("accessors should be a list of attribute names")

        # Copy the list of accessors
        self._accessors = [a for a in accessors]
        if len(self._accessors) == 0:
            raise ValueError("ListSource must be provided a list of accessors")

        # Convert the data into row objects
        if data:
            self._data = [self._create_row(value) for value in data]
        else:
            self._data = []

    ######################################################################
    # Methods required by the ListSource interface
    ######################################################################

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, index: int) -> Row:
        return self._data[index]

    ######################################################################
    # Factory methods for new rows
    ######################################################################

    def _create_row(self, data: Any) -> Row:
        """Create a Row object from the given data.

        The type of ``data`` determines how it is converted.

        If ``data`` is a dictionary, each key in the dictionary will be
        converted into an attribute on the Row.

        If ``data`` is a non-string iterable, the items in the data will be
        mapped in order to the list of accessors, and the Row will have an
        attribute for each accessor.

        Otherwise, the Row will have a single attribute corresponding to the
        name of the first accessor.

        :param data: The data to convert into a row.
        """
        if isinstance(data, dict):
            row = Row(**data)
        elif hasattr(data, "__iter__") and not isinstance(data, str):
            row = Row(**dict(zip(self._accessors, data)))
        else:
            row = Row(**{self._accessors[0]: data})
        row._source = self
        return row

    ######################################################################
    # Utility methods to make ListSources more list-like
    ######################################################################

    def __setitem__(self, index: int, value: Any):
        """Set the value of a specific item in the data source.

        :param index: The item to change
        :param value: The data for the updated item. This data will be converted
            into a Row object.
        """
        row = self._create_row(value)
        self._data[index] = row
        self.notify("insert", index=index, item=row)

    def __iter__(self):
        """Obtain an iterator over the Rows in the data source."""
        return iter(self._data)

    def clear(self):
        """Clear all data from the data source."""
        self._data = []
        self.notify("clear")

    def insert(self, index: int, data: Any):
        """Insert a row into the data source at a specific index.

        :param index: The index at which to insert the item.
        :param data: The data to insert into the ListSource. This data will be converted
            into a Row for storage.
        """
        row = self._create_row(data)
        self._data.insert(index, row)
        self.notify("insert", index=index, item=row)
        return row

    def append(self, data):
        """Insert a row at the end of the data source.

        :param data: The data to append to the ListSource. This data will be converted
            into a Row for storage.
        """
        return self.insert(len(self), data)

    def remove(self, row: Row):
        """Remove an item from the data source.

        :param row: The row to remove from the data source.
        """
        i = self._data.index(row)
        del self._data[i]
        self.notify("remove", index=i, item=row)
        return row

    def index(self, row):
        """The index of a specific row in the data source.

        This search uses Row instances, and searches for an *instance* match.
        If two Row instances have the same values, only the Row that is the
        same Python instance will match. To search for values based on equality,
        use :meth:`~toga.sources.ListSource.find`.

        Raises ValueError if the row cannot be found in the data source.

        :param row: The row to find in the data source.
        :returns: The index of the row in the data source.
        """
        return self._data.index(row)

    def find(self, data, start=None):
        """Find the first item in the data that matches all the provided
        attributes.

        This is a value based search, rather than an instance search. If two Row
        instances have the same values, the first instance that matches will be
        returned. To search for a second instance, provide the first found instance
        as the ``start`` argument. To search for a specific Row instance, use the
        :meth:`~toga.sources.ListSource.index`.

        Raises ValueError if no match is found.

        :param data: The data to search for. Only the values specified in data will be
            used as matching criteria; if the row contains additional data attributes,
            they won't be considered as part of the match.
        :param start: The instance from which to start the search. Defaults to ``None``,
            indicating that the first match should be returned.
        :return: The matching Row object
        """
        if start:
            start_index = self._data.index(start) + 1
        else:
            start_index = 0

        for item in self._data[start_index:]:
            try:
                if isinstance(data, dict):
                    found = all(
                        getattr(item, attr) == value for attr, value in data.items()
                    )
                elif hasattr(data, "__iter__") and not isinstance(data, str):
                    found = all(
                        getattr(item, attr) == value
                        for value, attr in zip(data, self._accessors)
                    )
                else:
                    found = getattr(item, self._accessors[0]) == data

                if found:
                    return item
            except AttributeError:
                # Attribute didn't exist, so it's not a match
                pass

        raise ValueError(f"No row matching {data!r} in data")
