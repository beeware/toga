from .base import Widget

class Node:
    '''
    Node of the Tree widget
    '''
    def __init__(self, data, id=None, children=None,
                                        icon={'url' : None, 'obj' : None},
                                        collapse=True):
        '''
        Instantiate a new instance of a node

        :param data: Information about the node
        :type  data: ``dict``
        '''
        self._impl = None
        self.id = id
        self.data = data
        self.children = children
        self._icon = icon
        self._collapse = collapse
        self._update = []

    @property
    def collapse(self):
        '''
        :returns: The status of the node displayed
        :rtype: ``bool``
        '''
        return self._collapse

    @collapse.setter
    def collapse(self, status):
        '''
        Collapse a node on the tree

        :param status: True for collapse the node, otherwise False expand it
        :type  status: ``bool``
        '''
        self._collapse = status
        update_call = 'collapse' if status else 'expand'
        self._update.append(update_call)

    @property
    def icon(self):
        '''
        :returns: The image url of the node
        :rtype: ``str``
        '''
        return self._icon['url']

    @icon.setter
    def icon(self, image_url):
        '''
        Set an icon on the node

        :param image_url: Url of the icon
        :type  image_url: ``str``
        '''
        self._icon['url'] = image_url
        self._update.append('icon')

    @property
    def color(self):
        '''
        :returns: The current color of the node
        :rtype: ``str``
        '''
        pass

    @color.setter
    def color(self, color):
        '''
        Set a color for the text of the node

        :param color: Color to be set on the text
        :type  color: ``str``
        '''
        pass

    @property
    def tags(self):
        '''
        :returns: Current tags of the node
        :rtype: ``list`` of ``str``
        '''
        pass

    @tags.setter
    def tags(self, data):
        '''
        Set tags for the node

        :param data: Tags to be add on the node
        :type  data: ``list`` of ``str``
        '''
        pass


class Tree(Widget):
    '''
    Tree widget
    '''
    def __init__(self, headings, data=None, id=None, style=None):
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
        '''
        super().__init__(id=id, style=style, data=data)
        self.headings = headings
        self.tree = { None: Node(None) }

    def _configure(self, data):
        if data:
            self.data = data

    def insert(self, item, parent=None, index=None, collapse=True):
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
        node_data = {'text': item, 'collapse': collapse}
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
            parents = self._data.source.roots()
            for node in parents:
                parent_node = self.insert(node)
                self._add_from_data_source(parent_node)
                self._update_cosmetic(parent_node)

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

    def _update_cosmetic(self, node):
        self._set_collapse(node, self._data.source.is_collapsed(node))

    def _add_from_data_source(self, parent_node):
        '''
        Add nodes from a data source on the Tree

        :param parent_node: Parent's node
        :type  parent_node: :class:`tree.Node`
        '''
        children = self._data.source.children(parent_node)
        if children:
            # list of str
            for child in children:
                new_child = self.insert(child, parent_node)
                self._add_from_data_source(new_child)
                self._update_cosmetic(new_child)

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

    def apply_layout(self):
        '''
        Applies modifications on the layout of the tree
        '''
        for ids, node in self.tree.items():
            if node._update:
                type_layout = node._update.pop()
                if type_layout == 'icon':
                    self._set_icon(node)
                elif type_layout == 'collapse':
                    self._set_collapse(node, True)
                elif type_layout == 'expand':
                    self._set_collapse(node, False)

        self.rehint()

    def _insert(self, node):
        raise NotImplementedError('Tree widget must define _insert()')

    def _set_icon(self, node):
        raise NotImplementedError('Tree widget must define _set_icon()')

    def _set_collapse(self, node):
        raise NotImplementedError('Tree widget must define _set_collapse()')

    def rehint(self):
        raise NotImplementedError('Tree widget must define rehint()')
