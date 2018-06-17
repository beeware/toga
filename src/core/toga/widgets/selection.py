from toga.handlers import wrapped_handler
from toga.sources import ListSource

from .base import Widget


class Selection(Widget):
    """ The Selection widget lets you pick from a defined selection of options.

    Args:
        id (str): An identifier for this widget.
        style ( :obj:`Style`): An optional style object.
            If no style is provided then a new one will be created for the widget.
        items (``list`` of ``str``): The items for the selection.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)
    """
    MIN_WIDTH = 100

    def __init__(self, id=None, style=None, items=None, on_select=None, enabled=True, factory=None):
        super().__init__(id=id, style=style, factory=factory)
        self._on_select = None # needed for _impl initialization
        self._impl = self.factory.Selection(interface=self)

        # use public setters
        self.items = items
        self.on_select = on_select
        self.enabled = enabled

    @property
    def items(self):
        """ The list of items.

        Returns:
             The ``list`` of ``str`` of all selectable items.
        """
        return self._items

    @items.setter
    def items(self, items):
        if items is None:
            self._items = ListSource(data=[], accessors=['label'])
        elif isinstance(items, (list, tuple)):
            self._items = ListSource(data=items, accessors=['label'])
        else:
            self._items = items

        self._items.add_listener(self._impl)
        self._impl.change_source(self._items)

    @property
    def value(self):
        """ The value of the currently selected item.

        Returns:
            The selected item as a ``str``.
        """
        return self._impl.get_selected_item()

    @value.setter
    def value(self, value):
        if value in self.items:
            self._impl.select_item(value)
        else:
            try:
                item = next(i for i in self.items if i.label == value)
            except StopIteration:
                raise ValueError("Not an item in the list.")
            self._impl.select_item(item)

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
        Set the function to be executed on node selection

        :param handler:     callback function
        :type handler:      ``callable``
        """
        self._on_select = wrapped_handler(self, handler)
        self._impl.set_on_select(self._on_select)
