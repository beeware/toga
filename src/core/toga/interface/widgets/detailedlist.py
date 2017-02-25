from .base import Widget


class DetailedList(Widget):
    def __init__(self, id=None, data=None, on_delete=None, on_refresh=None, style=None):
        super().__init__(id=id, data=data, on_delete=on_delete, on_refresh=on_refresh, style=style)

    def _configure(self, data, on_delete, on_refresh):
        self.data = data
        self.on_delete = on_delete
        self.on_refresh = on_refresh

    def add(self, item):
        self.data.append(item)
        self._add(item)
