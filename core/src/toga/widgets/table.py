import warnings

from toga.handlers import wrapped_handler
from toga.sources import ListSource
from toga.sources.accessors import build_accessors, to_accessor

from .base import Widget


class Table(Widget):
    """A Table Widget allows the display of data in the form of columns and
    rows.

    Args:
        headings (``list`` of ``str``): The list of headings for the table.
        id (str): An identifier for this widget.
        data (``list`` of ``tuple``): The data to be displayed on the table.
        accessors: A list of methods, same length as ``headings``, that describes
            how to extract the data value for each column from the row. (Optional)
        style (:obj:`Style`): An optional style object.
            If no style is provided` then a new one will be created for the widget.
        on_select (``callable``): A function to be invoked on selecting a row of the table.
        on_double_click (``callable``): A function to be invoked on double clicking a row of
            the table.
        missing_value (``str`` or ``None``): value for replacing a missing value
            in the data source. (Default: None). When 'None', a warning message
            will be shown.

    Examples:
        >>> headings = ['Head 1', 'Head 2', 'Head 3']
        >>> data = []
        >>> table = Table(headings, data=data)

        Data can be in several forms.
        A list of dictionaries, where the keys match the heading names:

        >>> data = [{'head_1': 'value 1', 'head_2': 'value 2', 'head_3': 'value3'}),
        >>>         {'head_1': 'value 1', 'head_2': 'value 2', 'head_3': 'value3'}]

        A list of lists. These will be mapped to the headings in order:

        >>> data = [('value 1', 'value 2', 'value3'),
        >>>         ('value 1', 'value 2', 'value3')]

        A list of values. This is only accepted if there is a single heading.

        >>> data = ['item 1', 'item 2', 'item 3']
    """

    def __init__(
        self,
        headings,
        id=None,
        style=None,
        data=None,
        accessors=None,
        multiple_select=False,
        on_select=None,
        on_double_click=None,
        missing_value=None,
        factory=None,  # DEPRECATED!
    ):
        super().__init__(id=id, style=style)
        ######################################################################
        # 2022-09: Backwards compatibility
        ######################################################################
        # factory no longer used
        if factory:
            warnings.warn("The factory argument is no longer used.", DeprecationWarning)
        ######################################################################
        # End backwards compatibility.
        ######################################################################

        self.headings = headings[:]
        self._accessors = build_accessors(self.headings, accessors)
        self._multiple_select = multiple_select
        self._on_select = None
        self._on_double_click = None
        self._data = None
        if missing_value is None:
            print(
                "WARNING: Using empty string for missing value in data. "
                "Define a 'missing_value' on the table to silence this message"
            )
        self._missing_value = missing_value or ""

        self._impl = self.factory.Table(interface=self)
        self.data = data

        self.on_select = on_select
        self.on_double_click = on_double_click

    @property
    def data(self):
        """The data source of the widget. It accepts table data in the form of
        ``list``, ``tuple``, or :obj:`ListSource`

        Returns:
            Returns a (:obj:`ListSource`).
        """
        return self._data

    @data.setter
    def data(self, data):
        if data is None:
            self._data = ListSource(accessors=self._accessors, data=[])
        elif isinstance(data, (list, tuple)):
            self._data = ListSource(accessors=self._accessors, data=data)
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
        """Scroll the view so that the top of the list (first row) is
        visible."""
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
        """Scroll the view so that the bottom of the list (last row) is
        visible."""
        self.scroll_to_row(-1)

    @property
    def on_select(self):
        """The callback function that is invoked when a row of the table is
        selected. The provided callback function has to accept two arguments
        table (:obj:`Table`) and row (``Row`` or ``None``).

        The value of a column of row can be accessed with row.accessor_name

        Returns:
            (``callable``) The callback function.
        """
        return self._on_select

    @on_select.setter
    def on_select(self, handler):
        """Set the function to be executed on node selection.

        :param handler: callback function
        :type handler: ``callable``
        """
        self._on_select = wrapped_handler(self, handler)
        self._impl.set_on_select(self._on_select)

    @property
    def on_double_click(self):
        """The callback function that is invoked when a row of the table is
        double clicked. The provided callback function has to accept two
        arguments table (:obj:`Table`) and row (``Row`` or ``None``).

        The value of a column of row can be accessed with row.accessor_name

        Returns:
            (``callable``) The callback function.
        """
        return self._on_double_click

    @on_double_click.setter
    def on_double_click(self, handler):
        """Set the function to be executed on node double click.

        :param handler: callback function
        :type handler: ``callable``
        """
        self._on_double_click = wrapped_handler(self, handler)
        self._impl.set_on_double_click(self._on_double_click)

    def add_column(self, heading, accessor=None):
        """Add a new column to the table.

        :param heading: title of the column
        :type heading: ``string``
        :param accessor: accessor of this new column
        :type heading: ``string``
        """

        if not accessor:
            accessor = to_accessor(heading)

        if accessor in self._accessors:
            raise ValueError(f'Accessor "{accessor}" is already in use')

        self.headings.append(heading)
        self._accessors.append(accessor)

        self._impl.add_column(heading, accessor)

    def remove_column(self, column):
        """Remove a table column.

        :param column: accessor or position (>0)
        :type column: ``string``
        :type column: ``int``
        """

        if isinstance(column, str):
            # Column is a string; use as-is
            accessor = column
        else:
            try:
                accessor = self._accessors[column]
            except IndexError:
                # Column specified as an integer, but the integer is out of range.
                raise ValueError(f"Column {column} does not exist")
            except TypeError:
                # Column specified as something other than int or str
                raise ValueError("Column must be an integer or string")

        try:
            # Remove column
            self._impl.remove_column(accessor)
            del self.headings[self._accessors.index(accessor)]
            self._accessors.remove(accessor)
        except KeyError:
            raise ValueError(f'Invalid column: "{column}"')

    @property
    def missing_value(self):
        return self._missing_value
