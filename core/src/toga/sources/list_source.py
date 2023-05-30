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
                self._source._notify("change", item=self)


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
        self._notify("insert", index=index, item=row)

    def __iter__(self):
        """Obtain an iterator over the Rows in the data source."""
        return iter(self._data)

    def clear(self):
        """Clear all data from the data source."""
        self._data = []
        self._notify("clear")

    def insert(self, index: int, *values, **named):
        """Insert data into the data source at a specific index.

        :param index: The index at which to insert the item.
        :param values: A list of attribute values for the new item. These values
            will be mapped in order onto the accessors.
        :param named: Specific named attributes to include on the data row.
            Any name provided explicitly will override an automatically
            mapped value from ``values``.
        """
        # Coalesce values and data into a single data dictionary,
        # and use that to create the data row. Explicitly named data override.
        row = self._create_row(dict(zip(self._accessors, values), **named))
        self._data.insert(index, row)
        self._notify("insert", index=index, item=row)
        return row

    def prepend(self, *values, **named):
        """Insert data at the start of the data source.

        :param values: A list of attribute values for the new item. These values
            will be mapped in order onto the accessors.
        :param named: Specific named attributes to include on the data row. Any
            name provided explicitly will override an automatically mapped value
            from ``values``.
        """
        return self.insert(0, *values, **named)

    def append(self, *values, **named):
        """Insert data at the end of the data source.

        :param values: A list of attribute values for the new item. These values
            will be mapped in order onto the accessors.
        :param named: Specific named attributes to include on the data row. Any
            name provided explicitly will override an automatically mapped value
            from ``values``.
        """
        return self.insert(len(self), *values, **named)

    def remove(self, row: Row):
        """Remove an item from the data source.

        :param row: The row to remove from the data source, or an object
            whose value is equivalent to that row.
        """
        i = self._data.index(row)
        del self._data[i]
        self._notify("remove", index=i, item=row)
        return row

    def index(self, row):
        """The index of a specific row in the data source.

        Raises ValueError if the row cannot be found in the data source.

        :param row: The row to find in the data source, or an object whose value
            is equivalent to that row.
        :returns: The index of the row in the data source.
        """
        return self._data.index(row)

    def find(self, **attrs):
        """Find the first item in the data that matches all the provided
        attributes.

        :param attrs: The attributes and their values to search for
        :return: The matching Row object
        """
        for item in self._data:
            try:
                if all(getattr(item, attr) == value for attr, value in attrs.items()):
                    return item
            except AttributeError:
                # Attribute didn't exist, so it's not a match
                pass

        descriptor = ", ".join(f"{attr}={value!r}" for attr, value in attrs.items())
        raise ValueError(f"No row with {descriptor} in data")
