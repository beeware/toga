from .base import Widget
from .icon import Icon
from ..utils import wrapped_handler
from ..sources import ListSource
from ..sources.base import build_accessors


class Table(Widget):
    """ A Table Widget allows the display of data in the from of columns and rows.

    Args:
        headings (``list`` of ``str``): The list of headings for the table.
        id (str): An identifier for this widget.
        data (``list`` of ``tuple``): The data to be displayed on the table.
        accessors: A list of methods, same length as ``headings``, that describes
            how to extract the data value for each column from the row. (Optional)
        style (:class:`colosseum.CSSNode`): An optional style object.
            If no style is provided` then a new one will be created for the widget.
        on_select (``callable``): A function to be invoked on selecting a row of the table.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)

    Examples:
        >>> headings = ['Head 1', 'Head 2', 'Head 3']
        >>> data = []
        >>> table = Table(headings, data=data)

        # Data can be in several forms.
        # A list of dictionaries, where the keys match the heading names:
        >>> data = [{'head_1': 'value 1', 'head_2': 'value 2', 'head_3': 'value3'}),
        >>>         {'head_1': 'value 1', 'head_2': 'value 2', 'head_3': 'value3'}]

        # A list of lists. These will be mapped to the headings in order:
        >>> data = [('value 1', 'value 2', 'value3'),
        >>>         ('value 1', 'value 2', 'value3')]

        # A list of values. This is only accepted if there is a single heading.
        >>> data = ['item 1', 'item 2', 'item 3']
    """

    def __init__(self, headings, id=None, style=None, data=None, accessors=None, on_select=None, factory=None):
        super().__init__(id=id, style=style, factory=factory)
        self.headings = headings
        self._accessors = build_accessors(headings, accessors)

        self._data = None
        self._impl = self.factory.Table(interface=self)
        self.data = data

        self.on_select = on_select

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
            self._data = ListSource(accessors=self._accessors, data=[])
        elif isinstance(data, (list, tuple)):
            self._data = ListSource(accessors=self._accessors, data=data)
        else:
            self._data = data

        self._data.add_listener(self._impl)
        self._impl.change_source(source=self._data)

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
