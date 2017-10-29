from .base import Widget
from .icon import Icon


class TableRow:
    """ Row of the Table widget

    Args:
        data: A ``tuple`` where each element is a column of the row.
        icon: A icon displayed in the row.
    """

    def __init__(self, data, icon=None):
        self._data = [data] if isinstance(data, str) else data
        self.icon = icon

    def __repr__(self):
        return "<TableRow: %s>" % repr(self._data)

    @property
    def data(self):
        """ TableRow data

        Returns:
            (``data``)
        """
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def icon(self):
        """ Icon on the row.
        To set a image provide the path to the image as a ``str``.

        Returns:
            (str) The image url of the row as a ``str`.
        """
        return self._icon

    @icon.setter
    def icon(self, path):
        if path is None:
            self._icon = None
        else:
            self._icon = Icon.load(path)


class ListDataSource:
    """ A data source that helps you to store and manage data in a row like fashion.

    Args:
        data (`list` of `tuple`): A list of tuples containing the data for every row.
        refresh_function (`callable`): A function invoked on data change.
    """

    def __init__(self, data, refresh_function=None):
        self._data = self.create_rows(data)
        self.refresh = refresh_function if refresh_function else None
        self._data_user = []

    def create_rows(self, data):
        return [TableRow(data=row_data) for row_data in data]

    @property
    def data(self):
        return self._data

    @property
    def data_user(self):
        return self._data_user

    @data_user.setter
    def data_user(self, widget):
        self._data_user.append(widget)

    @data_user.deleter
    def data_user(self, widget):
        self._data_user.remove(widget)

    def _refresh(self):
        """ Invoke the refresh function on all widgets that use this ListDataSource."""
        for widget in self._data_user:
            widget.refresh()

        if self.refresh:
            self.refresh()

    def clear(self):
        self._data = []
        self._refresh()

    def insert(self, index: int, data, icon=None):
        node = TableRow(data=data, icon=icon)
        self._data.insert(index, node)
        self._refresh()
        return node

    def remove(self, node):
        self._data.remove(node)
        self._refresh()

    def item(self, row: int, column: int):
        if isinstance(row and column, int):
            return self.data[row].data[column]

    def row(self, row: int) -> TableRow:
        if row >= 0:
            return self.data[row]

    def rows(self) -> list:
        return self.data


class Table(Widget):
    """ A Table Widget allows the display of data in the from of columns and rows.

    Args:
        headings (``list`` of ``str``): The list of headings for the table.
        id (str): An identifier for this widget.
        data (``list`` of ``tuple``): The data to be displayed on the table.
        style (:class:`colosseum.CSSNode`): An optional style object.
            If no style is provided` then a new one will be created for the widget.
        on_select(``callable``): A function to be invoked on selecting a row of the table.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)

    Examples:
        >>> headings = ['Head 1', 'Head 2', 'Head 3']
        >>> data = [('item 1', 'item 2', 'item3'),
        >>>         ('item 1', 'item 2', 'item3')]
        >>>
        >>> table = Table(headings, data=data)
    """

    def __init__(self, headings, id=None, style=None, data=None, on_select=None, factory=None):
        super().__init__(id=id, style=style, factory=factory)
        self.headings = headings
        self._data = None
        self._impl = self.factory.Table(interface=self)
        self.data = data

        self.on_select = on_select

    @property
    def data(self):
        """ The data source of the widget. It accepts table data
        in the form of ``list``, ``tuple``, or :obj:`ListDataSource`

        Returns:
            (list) Returns a ``list`` of lists. Where the outer lists represents the
            rows and each inner list represents a column.
        """
        return self._data if self._data is not None else None

    @data.setter
    def data(self, data):
        if isinstance(data, (list, tuple)):
            self._data = ListDataSource(data, refresh_function=self._impl.refresh)
        else:
            self._data = data

        if data is not None:
            self._data.data_user = self

    @property
    def on_select(self):
        """ The callback function that is invoked when a row of the table is selected.
        The provided callback function has to accept two arguments table (``:obj:Table`)
        and row (``int`` or ``None``).

        Returns:
            (``callable``) The callback function.
        """
        return self._on_select

    @on_select.setter
    def on_select(self, handler):
        self._on_select = handler

    def refresh(self):
        self._impl.refresh()
