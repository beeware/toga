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
        self.data = data
        self.children = []

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
        super().__init__(id=id, style=style, headings=headings)

    def _configure(self, headings):
        self.headings = headings

    def insert(self, item, path=None, index=None):
        '''
        Insert a node on the tree

        :param item: Item to be add on the tree
        :type  item: ``str``

        :param path: Path of the node's parent
        :type  path: ``str``

        :param index: Location to add the node on its parent node
        :type  index: ``int``
        '''
        pass

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

    def collapse(self):
        '''
        Collpase a node on the tree
        '''
        pass

    @property
    def set_icon(self):
        '''
        :returns: The image url of the node
        :rtype: ``str``
        '''
        pass

    @set_icon.setter
    def set_icon(self, image_url):
        '''
        Set an icon on the node

        :param image_url: Url of the icon
        :type  image_url: ``str``
        '''
        pass

    @property
    def item_color(self):
        '''
        :returns: The current color of the node
        :rtype: ``str``
        '''
        pass

    @item_color.setter
    def item_color(self, color):
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
