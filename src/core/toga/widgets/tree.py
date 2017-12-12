from toga.handlers import wrapped_handler
from toga.sources import TreeSource
from toga.sources.accessors import build_accessors

from .base import Widget
from .icon import Icon


class Tree(Widget):
    """ Tree Widget

    Args:
        headings (``list`` of ``str``): The list of headings for the interface.
        id (str):  An identifier for this widget.
        style (:class:`colosseum.CSSNode`): An optional style object. If no style is provided then
            a new one will be created for the widget.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)
    """

    def __init__(self, headings, id=None, style=None, data=None, accessors=None, on_select=None, factory=None):
        super().__init__(id=id, style=style, factory=factory)

        self.headings = headings
        self._accessors = build_accessors(headings, accessors)

        self._data = None
        self._impl = self.factory.Tree(interface=self)
        self.data = data

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
        :type  data: ``dict`` or ``class``
        '''
        if data is None:
            self._data = TreeSource(accessors=self._accessors, data=[])
        elif isinstance(data, (list, tuple, dict)):
            self._data = TreeSource(accessors=self._accessors, data=data)
        else:
            self._data = data

        self._data.add_listener(self._impl)
        self._impl.change_source(source=self._data)

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
        Set the function to be executed on node select

        :param handler:     callback function
        :type handler:      ``callable``
        """
        self._on_select = wrapped_handler(self, handler)
        self._impl.set_on_select(self._on_select)
