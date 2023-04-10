import warnings

from toga.handlers import wrapped_handler
from toga.sources import ListSource

from .base import Widget


class DetailedList(Widget):
    """A widget to hold data in a list form. Rows are selectable and can be
    deleted. An updated function can be invoked by pulling the list down.

    Args:
        id (str): An identifier for this widget.
        data (list of `dict`): List of dictionaries with required 'icon', 'title', and
            'subtitle' keys as well as optional custom keys to store additional
            info like 'pk' for a database primary key (think Django ORM)
        on_delete (``Callable``): Function that is invoked on row deletion.
        on_refresh (``Callable``): Function that is invoked on user initialized refresh.
        on_select (``Callable``): Function that is invoked on row selection.
        style (:obj:`Style`): An optional style object. If no style is provided then
            a new one will be created for the widget.

    Examples:
        >>> import toga
        >>> def selection_handler(widget, row):
        >>>     print('Row {} of widget {} was selected.'.format(row, widget))
        >>>
        >>> dlist = toga.DetailedList(
        ...     data=[
        ...         {
        ...             'icon': '',
        ...             'title': 'John Doe',
        ...             'subtitle': 'Employee of the Month',
        ...             'pk': 100
        ...          }
        ...      ],
        ...      on_select=selection_handler
        ... )
    """

    MIN_HEIGHT = 100
    MIN_WIDTH = 100

    def __init__(
        self,
        id=None,
        data=None,
        on_delete=None,
        on_refresh=None,
        on_select=None,
        style=None,
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

        self._data = None
        self._on_delete = None
        self._on_refresh = None
        # at least _on_select must be defined before setting data for the Gtk impl
        self._on_select = None
        self._impl = self.factory.DetailedList(interface=self)

        self.data = data
        self.on_delete = on_delete
        self.on_refresh = on_refresh
        self.on_select = on_select

    @property
    def data(self):
        """The data source of the widget. It accepts data in the form of
        ``list`` of ``dict`` or :class:`ListSource`

        Returns:
            Returns a (:obj:`ListSource`).
        """
        return self._data

    @data.setter
    def data(self, data):
        if data is None:
            self._data = ListSource(data=[], accessors=["icon", "title", "subtitle"])
        elif isinstance(data, (list, tuple)):
            self._data = ListSource(data=data, accessors=["icon", "title", "subtitle"])
        else:
            self._data = data

        self._data.add_listener(self._impl)
        self._impl.change_source(source=self._data)

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
    def on_delete(self):
        """The function invoked on row deletion. The delete handler must accept
        two arguments. The first is a ref. to the widget and the second the row
        that is about to be deleted.

        Examples:
            >>> def delete_handler(widget, row):
            >>>     print('row ', row, 'is going to be deleted from widget', widget)

        Returns:
            The function that is invoked when deleting a row.
        """
        return self._on_delete

    @on_delete.setter
    def on_delete(self, handler: callable):
        self._on_delete = wrapped_handler(self, handler)
        self._impl.set_on_delete(self._on_delete)

    @property
    def on_refresh(self):
        """
        Returns:
            The function to be invoked on user initialized refresh.
        """
        return self._on_refresh

    @on_refresh.setter
    def on_refresh(self, handler: callable):
        self._on_refresh = wrapped_handler(self, handler, self._impl.after_on_refresh)
        self._impl.set_on_refresh(self._on_refresh)

    @property
    def selection(self):
        """The current selection.

        A value of None indicates no selection.
        """
        return self._impl.get_selection()

    @property
    def on_select(self):
        """The handler function must accept two arguments, widget and row.

        Returns:
            The function to be invoked on selecting a row.
        """
        return self._on_select

    @on_select.setter
    def on_select(self, handler: callable):
        self._on_select = wrapped_handler(self, handler)
        self._impl.set_on_select(self._on_select)
