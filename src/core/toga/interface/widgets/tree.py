from .base import Widget

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
        self.__impl = None
        self.source = source

        self._data = [data] if isinstance(data, str) else data
        self._icon = icon
        self._expanded = expanded

        self.parent = None
        self._children = children
        if children:
            for child in self._children:
                child.parent = self

    def __repr__(self):
        return "<TreeNode: %s>" % repr(self._data)

    @property
    def _impl(self):
        return self.__impl

    @_impl.setter
    def _impl(self, value):
        self.__impl = value
        self.source._impls[value] = self

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
        if self.source.tree:
            self.source.tree.refresh()

    def label(self, index):
        print("NODE", self, "label", index)
        return str(self._data[index])

    @property
    def expanded(self):
        return self._expanded

    @expanded.setter
    def expanded(self, value):
        self._expanded = value
        if self.source.tree:
            self.source.tree.refresh_node(self)

    @property
    def icon(self):
        '''
        :returns: The image url of the node
        :rtype: ``str``
        '''
        return self._icon

    @icon.setter
    def icon(self, icon):
        '''
        Set an icon on the node

        :param image_url: Url of the icon
        :type  image_url: ``str``
        '''
        self._icon = icon
        if self.source.tree:
            self.source.tree.refresh_node(self)

    @property
    def children(self):
        return self._children

    def insert(self, index, data, icon=None):
        node = TreeNode(source=self.source, data=data, icon=icon)
        self._children.insert(index, node)
        if self.source.tree:
            self.source.tree.refresh()
        return node

    def remove(self, node):
        self.parent._children.remove(node)
        if self.source.tree:
            self.source.tree.refresh()


class DictionaryDataSource:
    def __init__(self, data):
        self._roots = self.create_nodes(data)
        self._impls = {}
        self.tree = None

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

    def node(self, impl):
        return self._impls[impl]

    def insert(self, parent, index, data, icon=None):
        return parent.insert(index, data=data, icon=icon)

    def remove(self, node):
        return node.parent.remove(node)


class Tree(Widget):
    '''
    Tree widget
    '''
    def __init__(self, headings, id=None, style=None, data=None, on_selection=None):
        '''
        Instantiate a new instance of the tree widget

        :param headings: The list of headings for the tree
        :type  headings: ``list`` of ``str``

        :param data: Data source for the tree
        :type  data: ``dict``

        :param id: An identifier for this widget.
        :type  id: ``int``

        :param style: an optional style object. If no style is provide
                        then a new one will be created for the widget.
        :type style: :class:`colosseum.CSSNode`

        :param on_selection: Function to execute when select a node on the Tree
        :type on_selection:  ``callable``
        '''
        super().__init__(id=id, style=style, data=data, on_selection=on_selection)
        self.headings = [headings] if isinstance(headings, str) else headings
        self._data = None

    def _configure(self, data, on_selection):
        self.on_selection = on_selection
        self.data = data

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
        self._data.tree = self

        self.refresh()

    @property
    def on_selection(self):
        """
        The callable function for when a node on the Tree is selected

        :rtype: ``callable``
        """
        return self._on_selection

    @on_selection.setter
    def on_selection(self, handler):
        """
        Set the function to be executed on node selection

        :param handler:     callback function
        :type handler:      ``callable``
        """
        self._on_selection = handler
