from .base import Widget


class Table(Widget):
    '''
    Table widget
    '''
    def __init__(self, headings, id=None, style=None):
        '''
        Instantiate a new instance of the split container widget

        :param headings: The list of headings for the table
        :type  headings: ``list`` of ``str``

        :param id:          An identifier for this widget.
        :type  id:          ``str``

        :param style:       an optional style object. If no style is provided then a
                            new one will be created for the widget.
        :type style:        :class:`colosseum.CSSNode`
        '''
        super().__init__(id=id, style=style)
        self.headings = headings

    def _configure(self):
        pass

    def insert(self, index, *data):
        '''
        Insert a new row into the table
        
        :param index: The index to insert at, the end if `None`
        :type  index: ``int`` or ``NoneType``
        
        :param *data: A list of values for each of the columns
        :type  *data: ``list`` of ``object``
        '''
        if len(data) != len(self.headings):
            raise Exception('Data size does not match number of headings')

        if index is None:
            self._data.append(data)
        else:
            self._data.insert(index, data)
