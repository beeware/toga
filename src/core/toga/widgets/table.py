from .base import Widget


class Table(Widget):
    """ A Table Widget allows the disply of data in the from of columns and rows.

    Args:
        headings (``list`` of ``str``): The list of headings for the table.
        id (str): An identifier for this widget.
        style (:class:`colosseum.CSSNode`): An optional style object.
            If no style is provided then a new one will be created for the widget.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)
    """

    def __init__(self, headings, id=None, style=None, on_select=None, factory=None):
        super().__init__(id=id, style=style, factory=factory)
        self.headings = headings
        self._impl = self.factory.Table(interface=self)

        self.on_select = on_select

    def insert(self, index, *data):
        """ Insert a new row into the table.

        Args:
            index (``int`` or ``NoneType``): The index to insert at, the end if `None`.
            *data (``list`` of ``object``): A list of values for each of the columns.

        Raises:
            Exception: If data size does not match number of headings.
        """
        if len(data) != len(self.headings):
            raise Exception('Data size does not match number of headings')

        if index is None:
            self._impl.data.append(data)
        else:
            self._impl.data.insert(index, data)

    @property
    def on_select(self):
        """
        The callable function for when a node on the Tree is selected

        :rtype: ``callable``
        """
        return self._on_select

    @on_select.setter
    def on_select(self, handler):
        """
        Set the function to be executed on node selection

        :param handler:     callback function
        :type handler:      ``callable``
        """
        self._on_select = handler
