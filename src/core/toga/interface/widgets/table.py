from .base import Widget


class Table(Widget):
    '''
    Table widget
    '''
    def __init__(self, headings, id=None, style=None, on_select=None):
        '''
        Instantiate a new instance of the split container widget

        :param headings: The list of headings for the table
        :type  headings: ``list`` of ``str``

        :param id:          An identifier for this widget.
        :type  id:          ``str``

        :param style:       an optional style object. If no style is provided then a
                            new one will be created for the widget.
        :type style:        :class:`colosseum.CSSNode`

        :param on_select:    Function to execute when row/column selected 
        :type on_select:     ``callable``
        '''
        super().__init__(id=id, style=style, on_select=on_select)
        self.headings = headings

    def _configure(self, on_select):
        self.on_select = on_select

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
    
    @property
    def on_select(self):
        """
        The callable function for when the button is pressed

        :rtype: ``callable``
        """
        return self._on_select

    @on_select.setter
    def on_select(self, handler):
        """
        Set the function to be executed on button press.

        :param handler:     callback function
        :type handler:      ``callable``
        """
        self._on_select = handler
        self._set_on_select(handler)

    def _set_on_select(self, value):
        pass
