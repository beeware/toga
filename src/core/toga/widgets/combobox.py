from toga.handlers import wrapped_handler

from .base import Widget


class ComboBox(Widget):
    ''' A widget similar to textinput that provides a predefined set of choices

    Args:
        id (str): An identifier for this widget.
        style (:obj:`Style`): An optional style object. If no style is provided then
            a new one will be created for the widget.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)
        initial (str): The initial text for the combobox.
        items (list[str]): The dropdown list of items
        placeholder (str): If no input is present this text is shown.
        on_change (callable[[], None]): Handle input/selection change
    '''
    MIN_WIDTH = 100

    def __init__(
            self, id=None, style=None, factory=None, items=None,
            initial=None, placeholder=None, on_change=None):
        super().__init__(id=id, style=style, factory=factory)

        # Create a platform specific implementation of a ComboBox
        self._impl = self.factory.ComboBox(interface=self)

        # # Initialize private values
        self._on_change = None

        # Use public setters
        self.placeholder = placeholder
        self.items = items if items else []
        self.value = initial
        self.on_change = on_change

    @property
    def items(self):
        ''' The list of items.

        Returns:
             The ``list`` of ``str`` of all selectable items.
        '''
        return self._items

    @items.setter
    def items(self, items):
        self._impl.remove_all_items()

        for i in items:
            self._impl.add_item(i)

        self._items = items

    @property
    def placeholder(self):
        ''' The placeholder text.

        Returns:
            The placeholder text as a ``str``.
        '''
        return self._placeholder

    @placeholder.setter
    def placeholder(self, value):
        if value is None:
            self._placeholder = ''
        else:
            self._placeholder = str(value)
        self._impl.set_placeholder(value)

    @property
    def value(self):
        ''' The value of the text input field

        Returns:
            The current text of the widget as a ``str``.
        '''
        return self._impl.get_value()

    @value.setter
    def value(self, value):
        if value is None:
            v = ''
        else:
            v = str(value)
        self._impl.set_value(v)

    def clear(self):
        ''' Clears the text of the widget '''
        self.value = ''

    @property
    def on_change(self):
        '''The handler to invoke when the value changes

        Returns:
            The function ``callable`` that is called on a content change.
        '''
        return self._on_change

    @on_change.setter
    def on_change(self, handler):
        '''Set the handler to invoke when the value is changeed.

        Args:
            handler (:obj:`callable`): The handler to invoke when the value is changeed.
        '''
        self._on_change = wrapped_handler(self, handler)
        self._impl.set_on_change(self._on_change)
