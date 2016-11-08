from .base import Widget


class Selection(Widget):
    """
    Selection widget

    :param id:          Identifier for this widget
    :param style:       Style of the button
    :type style:        colosseum.CSS
    :param items:       Items for the selection:
    :type items:        List[str]
    """
    def __init__(self, id=None, style=None, items=list()):
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
        return self._items

    @items.setter
    def items(self, items):
        self._remove_all_items()

        for i in items:
            self._add_item(i)

        self._items = items

    @property
    def value(self):
        return self._get_selected_item()

    @value.setter
    def value(self, value):
        if value not in self._items:
            raise ValueError("Not an item in the list.")

        self._select_item(value)
