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
        self.data = data
        self.children = None
        self._icon = {'url' : None, 'obj' : None}
        self._update = []

    def collapse(self):
        '''
        Collapse a node on the tree
        '''
        pass

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
    def __init__(self, headings, id=None, style=None):
        '''
        Instantiate a new instance of the tree widget

        :param headings: The list of headings for the tree
        :type  headings: ``list`` of ``str``

        :param id:          An identifier for this widget.
        :type  id:          ``int``

        :param style:       an optional style object. If no style is provide
                            then a new one will be created for the widget.
        :type style:        :class:`colosseum.CSSNode`
        '''
        super().__init__(id=id, style=style)
        self.headings = headings
        self.tree = { None: Node(None) }

    def _configure(self):
        pass

    def insert(self, item, parent=None, index=None, collapse=True):
        '''
        Insert a node on the tree

        :param item: Item to be add on the tree
        :type  item: ``str``

        :param parent: Path of the node's parent
        :type  parent: ``int``

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
            node_parent = self.tree[parent]

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

    def apply_layout(self):
        '''
        Applies modifications on the layout of the tree
        '''
        for ids, node in self.tree.items():
            if node._update:
                type_layout = node._update.pop()
                if type_layout == 'icon':
                    self._set_icon(node)

        self.rehint()

    def remove(self, path):
        '''
        Remove a node on the tree

        :param path: Path of the node's parent
        :type  path: ``str``
        '''
        pass

    def edit(self, item, path):
        '''
        Edit a node on the tree

        :param item: New Item to be edited on the tree
        :type  item: ``str``

        :param path: Path of the node
        :type  path: ``str``
        '''
        pass

    def _insert(self, node):
        raise NotImplementedError('Tree widget must define _insert()')

    def _set_icon(self, node):
        raise NotImplementedError('Tree widget must define _set_icon()')

    def rehint(self):
        raise NotImplementedError('Tree widget must define rehint()')
