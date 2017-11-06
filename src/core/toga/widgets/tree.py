from .base import Widget
from .icon import Icon
from ..utils import wrapped_handler


class TreeNode:
    '''
    Node of the Tree widget
    '''
    def __init__(self, source, data, icon=None, expanded=False, children=None):
        '''
        Instantiate a new instance of a node

        :param data: Information about the node
        :type  data: ``dict``
        '''
        self._impl = None
        self.source = source

        self._expanded = expanded
        self._data = [data] if isinstance(data, str) else data
        self.icon = icon

        self.parent = None
        self._children = children
        if children:
            for child in self._children:
                child.parent = self

    def __repr__(self):
        return "<TreeNode: %s>" % repr(self._data)

    @property
    def data(self):
        '''
        :returns: TreeNode data
        :rtype: ``data``
        '''
        return self._data

    @data.setter
    def data(self, data):
        '''
        TreeNode data

        :param data: Contains the node data
        :type  data: ``dict``
        '''
        self._data = data
        self.source._refresh()

    @property
    def expanded(self):
        return self._expanded

    @expanded.setter
    def expanded(self, value):
        self._expanded = value
        self.source._refresh_node(self)

    @property
    def icon(self):
        '''
        :returns: The image url of the node
        :rtype: ``str``
        '''
        return self._icon

    @icon.setter
    def icon(self, path):
        '''
        Set an icon on the node

        :param image_url: Url of the icon
        :type  image_url: ``str``
        '''
        if path is None:
            self._icon = None
        else:
            self._icon = Icon.load(path)
        self.source._refresh_node(self)

    @property
    def children(self):
        return self._children

    def insert(self, index, data, icon=None):
        node = TreeNode(source=self.source, data=data, icon=icon)
        if self._children is None:
            self._children = []
        self._children.insert(index, node)
        self.source._insert_node(node)
        return node

    def remove(self, node):
        self.parent._children.remove(node)
        self.source._remove_node(node)


class DictionaryDataSource:
    def __init__(self, data):
        self._roots = self.create_nodes(data)
        self.interface = None
        self._listeners = []

    @property
    def listeners(self) -> list:
        """ The listeners of this data source.
        Listeners can be ``callable`` or :obj:``toga.Widget``.

        Returns:
            A list of objects that are listening for data change.
        """
        return self._listeners

    def add_listener(self, listener):
        """
        Args:
            listener: ``callable`` or :obj:``toga.Widget`
        """
        self._listeners.append(listener)

    def remove_listener(self, listener):
        self._listeners.remove(listener)

    def _refresh(self):
        """Invoke the refresh function on all listeners that are subscribed to this data source."""
        for listener in self._listeners:
            listener.refresh()

    def _insert_node(self, node):
        """Invoke the insert_node function on all listeners that are subscribed to this data source."""
        for listener in self._listeners:
            listener.insert_node(node)

    def _refresh_node(self, node):
        """Invoke the refresh_node function on all listeners that are subscribed to this data source."""
        for listener in self._listeners:
            listener.refresh_node(node)

    def _remove_node(self, node):
        """ Invoke the remove_node function on all listeners that are subscribed to this data source."""
        for listener in self._listeners:
            listener.remove_node(node)

    def create_nodes(self, data):
        if isinstance(data, dict):
            return [
                TreeNode(source=self, data=item, children=self.create_nodes(children))
                for item, children in sorted(data.items())
            ]
        else:
            return [
                TreeNode(source=self, data=item)
                for item in data
            ]

    def roots(self):
        return self._roots

    def root(self, index):
        return self._roots[index]

    def insert(self, parent, index, data, icon=None):
        return parent.insert(index, data=data, icon=icon)

    def remove(self, node):
        return node.parent.remove(node)


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

    def __init__(self, headings, id=None, style=None, data=None, on_select=None, factory=None):
        super().__init__(id=id, style=style, factory=factory)

        self.headings = headings
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
        if isinstance(data, dict):
            self._data = DictionaryDataSource(data)
        else:
            self._data = data

        if data is not None:
            self._data.add_listener(self._impl)

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
