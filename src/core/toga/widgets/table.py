from .base import Widget
from .icon import Icon
from ..utils import wrapped_handler


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

    def __init__(self, data, on_refresh=None):
        self._data = self.create_rows(data)
        self._on_refresh = on_refresh if on_refresh else None
        self._listeners = []

    def create_rows(self, data):
        return [TableRow(data=row_data) for row_data in data]

    @property
    def data(self):
        return self._data

    @property
    def listeners(self):
        return self._listeners

    def add_listener(self, widget):
        self._listeners.append(widget)

    def remove_listener(self, widget):
        self._listeners.remove(widget)

    @property
    def on_refresh(self) -> callable:
        return self._on_refresh

    @on_refresh.setter
    def on_refresh(self, handler: callable):
        if callable(handler) or handler is None:
            self._on_refresh = handler

    def _refresh(self):
        """ Invoke the refresh function on all widgets that are subscribed to this data source."""
        for widget in self._listeners:
            widget._impl.refresh()
        if self._on_refresh:
            self._on_refresh()

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
            return self._data[row].data[column]

    def row(self, row: int) -> TableRow:
        if row >= 0:
            return self._data[row]

    @property
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
        on_select (``callable``): A function to be invoked on selecting a row of the table.
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
            Returns a (:obj:`ListDataSource`).
        """
        return self._data if self._data is not None else None

    @data.setter
    def data(self, data):
        if isinstance(data, (list, tuple)):
            self._data = ListDataSource(data)
        elif isinstance(data, ListDataSource):
            self._data = data
        else:
            raise UserWarning('The table widgets should get data in form of a list or ListDataSource.')

        if data is not None:
            self._data.add_listener(self)

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
        """
        Set the function to be executed on node selection

        :param handler:     callback function
        :type handler:      ``callable``
        """
        self._on_select = wrapped_handler(self, handler)
        self._impl.set_on_select(self._on_select)
