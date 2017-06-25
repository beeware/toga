from .base import Widget


class Selection(Widget):
    '''
    Selection widget
    '''
    def __init__(self, id=None, style=None, items=list()):
        '''
        Instantiate a new instance of the selection widget

        :param id:          An identifier for this widget.
        :type  id:          ``str``

        :param style:       an optional style object. If no style is provided then a
                            new one will be created for the widget.
        :type style:        :class:`colosseum.CSSNode`

        :param items:       Items for the selection:
        :type  items:       ``list`` of ``str``
        '''
        self._items = items
        super().__init__(id=id, style=style, items=items)

    def _configure(self, items):
        pass

    def _create(self):
        super()._create()
        for item in self._items:
            self._add_item(item)

    @property
    def items(self):
        '''
        The list of items
        
        :rtype: ``list`` of ``str``
        '''
        return self._items

    @items.setter
    def items(self, items):
        self._remove_all_items()

        for i in items:
            self._add_item(i)

        self._items = items

    @property
    def value(self):
        '''
        The value of the selected item
        
        :rtype: ``str``
        '''
        return self._get_selected_item()

    @value.setter
    def value(self, value):
        if value not in self._items:
            raise ValueError("Not an item in the list.")

        self._select_item(value)
