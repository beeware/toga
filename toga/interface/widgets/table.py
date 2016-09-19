from .base import Widget


class Table(Widget):
    def __init__(self, headings, id=None, style=None):
        super().__init__(id=id, style=style)
        self.headings = headings

    def _configure(self):
        pass

    def insert(self, index, *data):
        if len(data) != len(self.headings):
            raise Exception('Data size does not match number of headings')

        if index is None:
            self._data.append(data)
        else:
            self._data.insert(index, data)
