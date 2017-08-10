from .base import Widget


class DetailedList(Widget):
    """

    Args:
        id (str):
        data:
        on_delete:
        on_refresh:
        style:
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)

    Todo:
        * Add missing docstrings.
    """

    def __init__(self, id=None, data=None, on_delete=None, on_refresh=None, style=None, factory=None):
        super().__init__(id=id, style=style, factory=factory)

        self._impl = self.factory.DetailedList(interface=self)

        self.data = data
        self.on_delete = on_delete
        self.on_refresh = on_refresh

    def add(self, item):
        self._data.append(item)
        self._impl.add(item)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data_list):
        self._data = data_list
        self._impl.set_data(self._data)

    @property
    def on_delete(self):
        return self._on_delete

    @on_delete.setter
    def on_delete(self, handler):
        self._on_delete = handler

    @property
    def on_refresh(self):
        return self._on_refresh

    @on_refresh.setter
    def on_refresh(self, handler):
        self._on_refresh = handler
