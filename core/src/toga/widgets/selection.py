import warnings

from toga.handlers import wrapped_handler

from .base import Widget


class Selection(Widget):
    """The Selection widget lets you pick from a defined selection of options.

    Args:
        id (str): An identifier for this widget.
        style ( :obj:`Style`): An optional style object.
            If no style is provided then a new one will be created for the widget.
        items (``list`` of ``str``): The items for the selection.
    """

    def __init__(
        self,
        id=None,
        style=None,
        items=None,
        on_select=None,
        enabled=True,
        factory=None,  # DEPRECATED!
    ):
        super().__init__(id=id, style=style)
        ######################################################################
        # 2022-09: Backwards compatibility
        ######################################################################
        # factory no longer used
        if factory:
            warnings.warn("The factory argument is no longer used.", DeprecationWarning)
        ######################################################################
        # End backwards compatibility.
        ######################################################################

        self._on_select = None  # needed for _impl initialization
        self._impl = self.factory.Selection(interface=self)

        if items is None:
            self._items = []
        else:
            self._items = items
            for item in self._items:
                self._impl.add_item(item)

        self.on_select = on_select
        self.enabled = enabled

    @property
    def items(self):
        """The list of items.

        Returns:
             The ``list`` of ``str`` of all selectable items.
        """
        return self._items

    @items.setter
    def items(self, items):
        self._impl.remove_all_items()
        self._items = items

        for i in items:
            self._impl.add_item(i)

    @property
    def value(self):
        """The value of the currently selected item.

        Returns:
            The selected item as a ``str``.
        """
        return self._impl.get_selected_item()

    @value.setter
    def value(self, value):
        if value not in self._items:
            raise ValueError("Not an item in the list.")

        self._impl.select_item(value)

    @property
    def on_select(self):
        """The callable function for when a node on the Tree is selected.

        :rtype: ``callable``
        """
        return self._on_select

    @on_select.setter
    def on_select(self, handler):
        """Set the function to be executed on node selection.

        :param handler:     callback function
        :type handler:      ``callable``
        """
        self._on_select = wrapped_handler(self, handler)
        self._impl.set_on_select(self._on_select)
