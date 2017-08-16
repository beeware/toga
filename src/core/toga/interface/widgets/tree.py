from .base import Widget

class Node:
    '''
    Node of the Tree widget
    '''
    def __init__(self, data):
        '''
        Instantiate a new instance of a node
        
        :param data: Information about the node
        :type  data: ``dict``
        '''
        self._impl = None
        self.id = None
        self._update = []
        self.children = None
        self.data = data

    @property
    def data(self):
        '''
        :returns: Node data
        :rtype: ``dict``
        '''
        return self._data

    @data.setter
    def data(self, node_data):
        '''
        Node data

        :param node_data: Contains the node data
                            Text, icon and a bool that indicates if a node is
                            collapsed or expanded
        :type  node_data: ``dict``
        '''
        self._data = node_data
        if node_data:
            update_call = 'collapse' if self._data['collapse'] else 'expand'
            self._update.append(update_call)
            if node_data['icon']['url'] is not None:
                self._update.append('icon')

    def collapse(self):
        self.data['collapse'] = True
        self._update.append('collapse')

    def expand(self):
        self.data['collapse'] = False
        self._update.append('expand')

    @property
    def icon(self):
        '''
        :returns: The image url of the node
        :rtype: ``str``
        '''
        return self._data['icon']['url']

    @icon.setter
    def icon(self, image_url):
        '''
        Set an icon on the node

        :param image_url: Url of the icon
        :type  image_url: ``str``
        '''
        self._data['icon']['url'] = image_url
        self._update.append('icon')

class Tree(Widget):
    '''
    Tree widget
    '''
    def __init__(self, headings, data=None, id=None, style=None,
                                on_selection=None):
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
        super().__init__(id=id, style=style, data=data,
                                on_selection=on_selection)
        self.headings = headings
        self.tree = { None: Node(None) }

    def _configure(self, data, on_selection):
        self.on_selection = on_selection
        if data is not None:
            self.data = data

    def insert(self, item, parent=None, index=None,
                                    collapse=True):
        '''
        Insert a node on the tree

        :param item: Item to be add on the tree
        :type  item: ``str``

        :param parent: Node's parent
        :type  parent: :class:`tree.Node`

        :param index: Location to add the node on its parent node
        :type  index: ``int``

        :param collapse: Sets a node to be shown expanded or collapsed
        :type  collapse: ``bool``

        :returns: The node inserted on the tree
        :type:      :class:`tree.Node`
        '''
        if isinstance(item, dict):
            new_item_icon = {'url': item['icon'], 'obj': None}
            item['icon'] = new_item_icon
            node_data = item
        else:
            node_data = {'text': item,
                        'icon': {'url': None, 'obj': None},
                        'collapse': collapse}

        node = Node(node_data)

        node_id = self._insert(node)
        node.id = node_id

        # Insert node on the tree
        self.tree[node.id] = node
        # Insert node on its parent children
        if parent is not None:
            # Search node's parent
            node_parent = self.tree[parent.id]

            if node_parent.children is None:
                node_parent.children = []

            node_parent.children.append(node.id)
        else:
            # Insert node on top level of the tree
            if self.tree[parent].children is None:
                self.tree[parent].children = []

            self.tree[parent].children.append(node.id)

        self.rehint()

        return node

    def update(self):
        '''
        Update Tree data
        '''
        # reset tree data
        self.tree = { None: Node(None) }

        if isinstance(self._data, dict):
            for parent, children in self._data.items():
                parent_node = self.insert(parent)
                self._add_from_dict(parent_node, children)
        else:
            parents = self._data.roots()
            for node in parents:
                parent_node = self.insert(node)
                self._add_from_data_source(parent_node)

        self.apply_layout()

    @property
    def data(self):
        '''
        :returns: The data source of the tree
        :rtype: ``dict``
        '''
        return self._data

    @data.setter
    def data(self, tree):
        '''
        Set the data source of the tree

        :param tree: Data source
        :type  tree: ``dict`` or ``class``
        '''
        self._data = tree

        self.update()

    def _add_from_data_source(self, parent_node):
        '''
        Add nodes from a data source on the Tree

        :param parent_node: Parent's node
        :type  parent_node: :class:`tree.Node`
        '''
        # list of dict
        children = self._data.children(parent_node)
        if children:
            for child_data in children:
                new_child = self.insert(child_data, parent_node)
                self._add_from_data_source(new_child)

    def _add_from_dict(self, parent_node, children):
        '''
        Add nodes from a dictionary on the Tree

        :param parent_node: Parent's node
        :type  parent_node: :class:`tree.Node`

        :param children: Items of each parent node
        :type  children: ``dict`` or ``str`` or ``None``
        '''
        if isinstance(children, str):
            self.insert(children, parent_node)
        elif isinstance(children, dict):
            for new_parent, child in children.items():
                new_parent_node = self.insert(new_parent, parent_node)
                self._add_from_dict(new_parent_node, child)

    def _update_node_layout(self, node):
        type_layout = node._update.pop()
        if type_layout == 'icon':
            self._set_icon(node)
        elif type_layout == 'collapse':
            self._set_collapse(node, True)
        elif type_layout == 'expand':
            self._set_collapse(node, False)

    def apply_layout(self):
        '''
        Applies modifications on the layout of the tree
        '''
        for ids, node in self.tree.items():
            if node._update:
                self._update_node_layout(node)

        self.rehint()

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

    def _insert(self, node):
        raise NotImplementedError('Tree widget must define _insert()')

    def _set_icon(self, node):
        raise NotImplementedError('Tree widget must define _set_icon()')

    def _set_collapse(self, node):
        raise NotImplementedError('Tree widget must define _set_collapse()')

    def rehint(self):
        raise NotImplementedError('Tree widget must define rehint()')
