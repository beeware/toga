from .base import Widget


class DetailedList(Widget):
    """ A widget to hold data in a list form. Rows are selectable and can be deleted.
    A updated function can be invoked by pulling the list down.

    Args:
        id (str): An identifier for this widget.
        data (list of `str`): List of strings which to display on the widget.
        on_delete (``callable``): Function that is invoked on row deletion.
        on_refresh (``callable``): Function that is invoked on user initialised refresh.
        on_select (``callable``): Function that is invoked on row selection.
        style (:class:`colosseum.CSSNode`): An optional style object. If no style is provided then
            a new one will be created for the widget.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)

    Examples:
        >>> import toga
        >>> def selection_handler(widget, selection):
        >>>     print('Row {} of widget {} was selected.'.format(selection, widget))
        >>>
        >>> dlist = toga.DetailedList(data=['Item 0', 'Item 1', 'Item 2'], on_select=selection_handler)
    """

    def __init__(self, id=None, data=None, on_delete=None, on_refresh=None, on_select=None, style=None, factory=None):
        super().__init__(id=id, style=style, factory=factory)

        self._impl = self.factory.DetailedList(interface=self)

        self.data = data
        self.on_delete = on_delete
        self.on_refresh = on_refresh
        self.on_select = on_select

    def add(self, item):
        """ Add a item to the list.

        Args:
            item (str): String add to the list.
        """
        self._data.append(item)
        self._impl.add(item)

    @property
    def data(self) -> list:
        """ The data displayed in the rows of the list.

        Returns:
            The row data in form of a list.
        """
        return self._data

    @data.setter
    def data(self, data_list: list):
        self._data = data_list
        self._impl.set_data(self._data)

    @property
    def on_delete(self):
        """ The function invoked on row deletion. The delete handler must accept two arguments.
        The first is a ref. to the widget and the second the row that is about to be deleted.

        Examples:
            >>> def delete_handler(widget, row):
            >>>     print('row ', row, 'is going to be deleted from widget', widget)

        Returns:
            The function that is invoked when deleting a row.
        """
        return self._on_delete

    @on_delete.setter
    def on_delete(self, handler: callable):
        self._on_delete = handler

    @property
    def on_refresh(self):
        """
        Returns:
            The function to be invoked on user initialised refresh.
        """
        return self._on_refresh

    @on_refresh.setter
    def on_refresh(self, handler: callable):
        if callable(handler) or handler is None:
            self._on_refresh = handler
            # If a function to handle refreshing was provided enable refreshing.
            self._impl.enable_refresh(True if handler is not None else False)
        else:
            raise ValueError('on_refresh must be a function or `None.')

    @property
    def on_select(self):
        """ The handler function must accept two arguments, widget and row.

        Returns:
            The function to be invoked on selecting a row.
        """
        return self._on_select

    @on_select.setter
    def on_select(self, handler: callable):
        if callable(handler) or handler is None:
            self._on_select = handler
        else:
            raise ValueError('on_select must be of type callable or None.')
