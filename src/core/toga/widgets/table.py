from toga.handlers import wrapped_handler
from toga.sources import ListSource
from toga.sources.accessors import to_accessor

from .base import Widget
from .internal.column import Column


class Table(Widget):
    """ A Table Widget allows the display of data in the form of columns and rows.

    Args:
        columns (``list`` of ``Column`` or ``list`` of ``str``): The list of columns for
            the table or a list of column titles. If only column titles are given, the
            content of the columns will be fetches by matching the column titles against
            attributes of the data source.
        id (str): An identifier for this widget.
        data (``list`` of ``tuple``, ``list`` of ``dict``, or ``toga.sources.ListSource``):
            The data to be displayed on the table. If a list of dictionaries is provided,
            the keys will be used to access the values of the data.
        accessors: A list of strings, same length as ``data``, that describes how to extract
            the data value for each row. Required when providing a list of tuples as data,
            otherwise ignored.
        style (:obj:`Style`): An optional style object.
            If no style is provided` then a new one will be created for the widget.
        on_select (``callable``): A function to be invoked on selecting a row of the table.
        on_double_click (``callable``): A function to be invoked on double clicking a row of
            the table.
        missing_value (``str`` or ``None``): value for replacing a missing value
            in the data source. (Default: None). When 'None', a warning message
            will be shown.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)

    Examples:
        >>> columns = ['Head 1', 'Head 2', 'Head 3']
        >>> data = []
        >>> table = Table(columns, data=data)

        The data should be structured as a list rows and can be passed in several forms.
        A list of dictionaries, where the keys match :

        >>> data = [{'head_1': 'value 1', 'head_2': 'value 2', 'head_3': 'value3'}),
        >>>         {'head_1': 'value 1', 'head_2': 'value 2', 'head_3': 'value3'}]

        A list of lists. These will be mapped to the accessors in order:

        >>> data = [('value 1', 'value 2', 'value3'),
        >>>         ('value 1', 'value 2', 'value3')]

        A list of values. This is only accepted if there is a single heading.

        >>> data = ['item 1', 'item 2', 'item 3']
    """
    MIN_WIDTH = 100
    MIN_HEIGHT = 100

    Column = Column

    def __init__(self, columns, id=None, style=None, data=None, accessors=None,
                 multiple_select=False, on_select=None, on_double_click=None,
                 missing_value=None, factory=None):
        super().__init__(id=id, style=style, factory=factory)

        if missing_value is None:
            print("WARNING: Using empty string for missing value in data. "
                  "Define a 'missing_value' on the table to silence this message")

        self._columns = []
        self._accessors = accessors

        for column in columns:
            if isinstance(column, Column):
                self._columns.append(column)
            elif isinstance(column, str):
                self._columns.append(
                    Table.Column(
                        title=column,
                        text_accessor=to_accessor(column),
                        factory=factory,
                        text_fallback=missing_value or "",
                    )
                )

        self._multiple_select = multiple_select
        self._on_select = None
        self._on_double_click = None
        self._data = None

        self._impl = self.factory.Table(interface=self)

        self.data = data
        self.on_select = on_select
        self.on_double_click = on_double_click

    @property
    def columns(self):
        return self._columns

    @property
    def headings(self):
        return [col.title for col in self.columns]

    @property
    def data(self):
        """ The data source of the widget. It accepts table data
        in the form of ``list``, ``tuple``, or :obj:`ListSource`

        Returns:
            Returns a (:obj:`ListSource`).
        """
        return self._data

    @data.setter
    def data(self, data):
        if data is None:
            self._data = ListSource([])
        elif isinstance(data, (list, tuple)):
            if not all(isinstance(row, dict) for row in data):
                data = [{key: value for key, value in zip(self._accessors, row)} for row in data]
            self._data = ListSource(data)
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
        If the table allows multiple selection, returns a list of
        selected data nodes. Otherwise, returns a single data node.

        The value of a column of the selection can be accessed with selection.accessor_name
        (for single selection) and with selection[x].accessor_name (for multiple selection)
        """
        return self._impl.get_selection()

    def scroll_to_top(self):
        """Scroll the view so that the top of the list (first row) is visible
        """
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
        """Scroll the view so that the bottom of the list (last row) is visible
        """
        self.scroll_to_row(-1)

    @property
    def on_select(self):
        """ The callback function that is invoked when a row of the table is selected.
        The provided callback function has to accept two arguments table (:obj:`Table`)
        and row (``Row`` or ``None``).

        The value of a column of row can be accessed with row.accessor_name

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
        """ The callback function that is invoked when a row of the table is double clicked.
        The provided callback function has to accept two arguments table (:obj:`Table`)
        and row (``Row`` or ``None``).

        The value of a column of row can be accessed with row.accessor_name

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

    def add_column(self, heading, accessor=None):
        """
        Add a new column to the table

        :param heading: title of the column
        :type heading: ``string``
        :param accessor: accessor of this new column
        :type heading: ``string``
        """

        if not accessor:
            accessor = to_accessor(heading)

        column = Column(heading, accessor, factory=self.factory)

        self._columns.append(column)
        self._impl.add_column(column)

    def remove_column(self, column):
        """
        Remove a table column.

        :param column: accessor, position (>0) or Column instance
        :type column: ``string``
        :type column: ``int``
        :type column: ``Table.Column``
        """

        if isinstance(column, str):
            try:
                column = next(col for col in self._columns if col.text == column)
            except StopIteration:
                raise ValueError(f"No column with accessor '{column}'")
        elif isinstance(column, int):
            try:
                column = self._columns[column]
            except IndexError:
                # Column specified as an integer, but the integer is out of range.
                raise ValueError("Column {} does not exist".format(column))
        elif not isinstance(column, Column):
            raise ValueError("Column must be an integer or string")

        try:
            # Remove column
            self._columns.remove(column)
            self._impl.remove_column(column)
        except KeyError:
            raise ValueError('Invalid column: "{}"'.format(column))
