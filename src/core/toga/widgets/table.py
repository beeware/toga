from .base import Widget
from .icon import Icon


class TableRow:
    '''
    Row of the Table widget
    '''
    def __init__(self, source, data, icon=None):
        '''
        Instantiate a new instance of a row

        :param data: Information about the row
        :type  data: ``dict``
        '''
        self._impl = None
        self.source = source

        self._data = [data] if isinstance(data, str) else data
        self.icon = icon

    def __repr__(self):
        return "<TableRow: %s>" % repr(self._data)

    @property
    def data(self):
        '''
        :returns: TableRow data
        :rtype: ``data``
        '''
        return self._data

    @data.setter
    def data(self, data):
        '''
        TableRow data

        :param data: Contains the row data
        :type  data: ``dict``
        '''
        self._data = data
        if self.source.interface:
            self.source.interface._impl.refresh()

    @property
    def icon(self):
        '''
        :returns: The image url of the row
        :rtype: ``str``
        '''
        return self._icon

    @icon.setter
    def icon(self, path):
        '''
        Set an icon on the row

        :param image_url: Url of the icon
        :type  image_url: ``str``
        '''
        if path is None:
            self._icon = None
        else:
            self._icon = Icon.load(path)
            if self.source.interface:
                self.source.interface._impl.refresh_row(self)


class ListDataSource:
    def __init__(self, data):
        self._data = self.create_rows(data)
        self.interface = None

    def create_rows(self, data):
        return [
            TableRow(source=self, data=item)
            for item in data
        ]

    def data(self):
        return self._data

    def insert(self, index, data, icon=None):
        node = TreeNode(source=self, data=data, icon=icon)
        self._data.insert(index, node)
        if self.interface:
            self.interface._impl.insert_node(node)
        return node

    def remove(self, node):
        self._data.remove(node)
        if self.interface:
            self.interface._impl.remove_node(node)



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
    def __init__(self, headings, id=None, style=None, data=None, on_select=None, factory=None):
        super().__init__(id=id, style=style, factory=factory)
        self.headings = headings
        self._data = data
        self._impl = self.factory.Table(interface=self)

        self.on_select = on_select

    @property
    def data(self):
        '''
        :returns: The data source of the tree
        :rtype: ``dict``
        '''
        return self._data

    @data.setter
    def data(self, data):
        '''
        Set the data source of the data

        :param data: Data source
        :type  data: ``list``, ``tuple``, or ``class``
        '''
        if isinstance(data, (list, tuple)):
            self._data = ListDataSource(data)
        else:
            self._data = data

        if data is not None:
            self._data.interface = self

        self._impl.refresh()

    @property
    def on_select(self):
        """
        The callable function for when a node on the Table is selected

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
