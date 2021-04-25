import warnings

from toga.handlers import wrapped_handler
from toga.sources import ListSource
from toga.sources.accessors import to_accessor, build_accessors

from .base import Widget
from .internal.tablecolumn import Column


class Table(Widget):
    """A Table Widget allows the display of data in the form of columns and rows.

    :param columns: Can be a list of titles to generate columns, a list of tuples
        ``(title, accessor)`` where the accessor defines which column of the data source
        to access, or a list of :class:`Column` instances.
    :param id: An identifier for this widget.
    :param data: The data to display in the widget. Must be an instance of
        :class:`toga.sources.ListSource` or a class instance which implements the
        interface of :class:`toga.sources.ListSource`.
    :param style: An optional style object. If no style is provided` then a new one will
        be created for the widget.
    :param on_select: A function to be invoked on selecting a row of the table.
    :param on_double_click: A function to be invoked on double clicking a row of the table.
    :param factory: A python module that is capable to return a implementation of this
        class with the same name. (optional & normally not needed)

    Examples:

        Lets prepare a data source first.

        >>> rows = [
        ...     {'head_1': 'value 1', 'head_2': 'value 2', 'head_3': 'value3'}),
        ...     {'head_1': 'value 1', 'head_2': 'value 2', 'head_3': 'value3'},
        ... ]
        >>> table_source = ListSource(rows, accessors=['head_1', 'head_2', 'head_3'])

        Columns can be provided in several forms.
        As a list of column titles which will be matched against accessors in the data:

        >>> columns = ['Head 1', 'Head 2', 'Head 3']

        As ``Column`` instances with column properties assigned to data accessors:

        >>> columns = [
        ...     Table.Column(title='Head 1', text='head_1', icon='head_2'),
        ...     Table.Column(title='Head 2', text='head_1'),
        ... ]

        Now we can create our Table:

        >>> table = Table(columns=columns, data=table_source)
    """

    MIN_WIDTH = 100
    MIN_HEIGHT = 100

    Column = Column

    def __init__(
        self,
        columns=None,
        headings=None,
        accessors=None,
        id=None,
        style=None,
        data=None,
        multiple_select=False,
        on_select=None,
        on_double_click=None,
        factory=None,
    ):
        super().__init__(id=id, style=style, factory=factory)

        # backward compatibility
        if not columns:
            warnings.warn(
                "Future versions will require a columns argument", DeprecationWarning
            )

        if headings is not None:
            warnings.warn(
                "'headings' and 'accessors' are deprecated and will be removed in a "
                "future version. Use 'columns' instead.", DeprecationWarning
            )
            accessors = build_accessors(headings, accessors)
            columns = [Table.Column(title=h, text=a) for h, a in zip(headings, accessors)]

        if not (columns or headings):
            raise ValueError("Must provide columns or headers for table")

        self._columns = []
        for col_index, col in enumerate(columns):
            if isinstance(col, Table.Column):
                self._columns.append(col)
            elif isinstance(col, str):
                title = col
                accessor = to_accessor(title)
                self._columns.append(Table.Column(title, text=accessor, factory=self.factory))
            else:
                raise ValueError("Column must be tuple str or Column instance")

        self._accessors = [col.text for col in self._columns]  # backward compatibility

        self._multiple_select = multiple_select
        self._on_select = None
        self._on_double_click = None
        self._data = ListSource([], [])

        self._impl = self.factory.Table(interface=self)
        if data is not None:
            self.data = data
        self.on_select = on_select
        self.on_double_click = on_double_click

    @property
    def columns(self):
        return self._columns

    @property
    def data(self):
        """The data source of the widget. It accepts table data in the form of
        :obj:`ListSource`

        Returns:
            Returns a (:obj:`ListSource`).
        """
        return self._data

    @data.setter
    def data(self, data):
        if data is None:
            self._data = ListSource([], [])
        elif isinstance(data, (list, tuple)):
            warnings.warn(
                "Future versions will only accept a TreeSource instance or None",
                DeprecationWarning
            )
            self._data = ListSource(data=data, accessors=self._accessors)
        else:
            self._data = data

        self._data.add_listener(self._impl)
        self._impl.change_source(source=self._data)

    @property
    def multiple_select(self):
        """Does the table allow multiple rows to be selected?"""
        return self._multiple_select

    @property
    def selection(self):
        """The current selection of the table.

        A value of None indicates no selection.
        If the tree allows multiple selection, returns a list of
        selected data nodes. Otherwise, returns a single data node.
        """
        return self._impl.get_selection()

    def scroll_to_top(self):
        """Scroll the view so that the top of the list (first row) is visible"""
        self.scroll_to_row(0)

    def scroll_to_row(self, row):
        """Scroll the view so that the specified row index is visible.

        Args:
            row: The index of the row to make visible. Negative values refer
                 to the nth last row (-1 is the last row, -2 second last,
                 and so on)
        """
        if row >= 0:
            self._impl.scroll_to_row(row)
        else:
            self._impl.scroll_to_row(len(self.data) + row)

    def scroll_to_bottom(self):
        """Scroll the view so that the bottom of the list (last row) is visible"""
        self.scroll_to_row(-1)

    @property
    def on_select(self):
        """The callback function that is invoked when a row of the table is selected.
        The provided callback function has to accept two arguments table (:obj:`Table`)
        and row (``Row`` or ``None``).

        Returns:
            (``callable``) The callback function.
        """
        return self._on_select

    @on_select.setter
    def on_select(self, handler):
        """
        Set the function to be executed on node selection

        :param handler: callback function
        :type handler: ``callable``
        """
        self._on_select = wrapped_handler(self, handler)
        self._impl.set_on_select(self._on_select)

    @property
    def on_double_click(self):
        """The callback function that is invoked when a row of the table is double clicked.
        The provided callback function has to accept two arguments table (:obj:`Table`)
        and row (``Row`` or ``None``).

        Returns:
            (``callable``) The callback function.
        """
        return self._on_double_click

    @on_double_click.setter
    def on_double_click(self, handler):
        """
        Set the function to be executed on node double click

        :param handler: callback function
        :type handler: ``callable``
        """
        self._on_double_click = wrapped_handler(self, handler)
        self._impl.set_on_double_click(self._on_double_click)

    def add_column(self, column, accessor=None):
        """
        Add a new column to the table

        :param column: title of the column or Column instance
        :param accessor: attribute name in data source
        """

        if isinstance(column, str):
            accessor = accessor or to_accessor(column)
            column = Column(title=column, text=accessor)
        elif isinstance(column, Column):
            pass
        else:
            raise ValueError("Column must of type str or column")

        self._columns.append(column)
        self._impl.add_column(column)

        return column

    def remove_column(self, column):
        """
        Remove a table column.

        :param column: Column instance
        """

        try:
            # Remove column
            self._columns.remove(column)
            self._impl.remove_column(column)
        except KeyError:
            raise ValueError('Invalid column: "{}"'.format(column))
