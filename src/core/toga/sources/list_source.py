from typing import Any, Union, Iterable, Dict

from .base import Source


Data = Union[Iterable[Dict[str, Any]], Iterable[Iterable]]
RowData = Union[Dict[str, Any], Iterable]


class Row:
    """A row in a :class:`ListSource`.

    The containing data can be accessed through instance attributes.

    :Example:

        >>> row = Row(region='London', population=9*10**6)
        >>> print(row.region)
        'London'
        >>> print(row.population)
        9000000

    :param data: Keyword arguments with data to create the row. Argument names will
        become instance attributes.
    """

    def __init__(self, **data: Any) -> None:
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
                self._source._notify("change", item=self)

    def __repr__(self):
        attr_str_list = [
            "{0}={1}".format(attr, repr(getattr(self, attr))) for attr in self._attrs
        ]
        attr_str = ", ".join(attr_str_list)
        return "<{0}({1})>".format(self.__class__.__name__, attr_str)


class ListSource(Source):
    """A data source to store a list of multiple data values

    Data is stored in a row-like fashion. The :class:`ListSource` acts like Python list
    where entries are :class:`Row` instances. Data values are accessible as attributes
    of each :class:`Row` and the attribute names are defined by the ``accessor``
    argument.

    Listeners can be registered with :meth:`add_listener` and should implement methods
    ``insert``, ``change``, ``remove`` and ``clear`` to react to changes to the data
    source. If the :class:`ListSource` is set as a data store for a :class:`toga.Table`,
    the table will be automatically registered as a listener.

    :Example:

        Data can be provided in several forms.
        A list of dictionaries, where the keys match the accessors names:

        >>> data = [
        ...     {'head_1': 'value 1', 'head_2': 'value 2', 'head_3': 'value3'},
        ...     {'head_1': 'value 1', 'head_2': 'value 2', 'head_3': 'value3'},
        ... ]
        >>> accessors = ('head_1', 'head_2', 'head_3')]
        >>> source = ListSource(data, accessors)

        A list of lists. These will be mapped to the accessors in order:

        >>> data = [
        ...     ('value 1', 'value 2', 'value3'),
        ...     ('value 1', 'value 2', 'value3'),
        ... ]
        >>> accessors = ('head_1', 'head_2', 'head_3')]
        >>> source = ListSource(data, accessors)

        Rows in the source can be accessed by index:

        >>> print(source[0])
        <Row(head_1='value 1', head_2='value 2', head_3='value 3')>

        Data values can be accessed as row attributes:

        >>> print(source[0].head_1)
        'value 1'

    :param data: The data in the list. Each entry in the list should have the same
        number of entries as there are accessors. Data can be provided either as a
        dictionary where keys are accessor names, or as a list of values in the same
        order as the ``accessors`` argument.
    :param accessors: A list of attribute names for accessing the value in each column
        of the row. This must be given if accessors are not provided by the data.
    """

    def __init__(self, data: Data, accessors: Iterable[str]) -> None:
        super().__init__()
        self.accessors = list(accessors)
        self._data = []
        for value in data:
            self._data.append(self._create_row(value))

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

    def _create_row(self, data: RowData) -> Row:
        """Create a Row object from the given data.

        :param data: The type of ``data`` determines how it is handled.
            ``dict``: each key corresponds to a column accessor
            iterables, except ``str`` and ``dict``: each item corresponds to a column
            all else: ``data`` will fill the first column
        """

        if isinstance(data, dict):
            row = Row(**data)
        elif hasattr(data, "__iter__") and not isinstance(data, str):
            row = Row(**dict(zip(self.accessors, data)))
        else:
            row = Row(**{self.accessors[0]: data})
        row._source = self
        return row

    ######################################################################
    # Utility methods to make ListSources more list-like
    ######################################################################

    def __setitem__(self, index: int, value: RowData) -> None:
        row = self._create_row(value)
        self._data[index] = row
        self._notify("insert", index=index, item=row)

    def __iter__(self) -> Iterable[Row]:
        return iter(self._data)

    def clear(self) -> None:
        """Removes all rows from this source."""
        self._data = []
        self._notify("clear")

    def insert(self, index: int, *values: Any, **named: Any) -> Row:
        """
        Create and insert a new Row at the given index.

        :param index: Index at which to insert row.
        :param values: An iterable of values to insert. The length must match the length
            of accessors.
        :param named: Keyword arguments assigning values to accessor names.
        :return: The created row.
        """
        # Coalesce values and data into a single data dictionary,
        # and use that to create the data row. Explicitly named data override.
        row = self._create_row(dict(zip(self.accessors, values), **named))
        self._data.insert(index, row)
        self._notify("insert", index=index, item=row)
        return row

    def prepend(self, *values, **named) -> Row:
        """
        Create and prepend a new Row..

        :param values: An iterable of values to insert. The length must match the length
            of accessors.
        :param named: Keyword arguments assigning values to accessor names.
        :return: The created row.
        """
        return self.insert(0, *values, **named)

    def append(self, *values, **named):
        """
        Create and append a new Row.

        :param values: An iterable of values to insert. The length must match the length
            of accessors.
        :param named: Keyword arguments assigning values to accessor names.
        :return: The created row.
        """
        return self.insert(len(self), *values, **named)

    def remove(self, row) -> Row:
        """
        Remove the given Row from this :class:`ListSource`.

        :param row: The row to remove.
        :return: The removed row.
        """
        i = self._data.index(row)
        del self._data[i]
        self._notify("remove", index=i, item=row)
        return row

    def index(self, row: Row) -> int:
        """
        Retrieves the index of a row in the :class:`ListSource`.

        :param row: A node in the list source.
        :return: The index of the row.
        """
        return self._data.index(row)
