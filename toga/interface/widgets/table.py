from .base import Widget


class Table(Widget):
    """
    Table widget

    :param headings:    Headings of the columns
    :type headings:     List[str]
    :param id:          Identifier for this widget
    :param style:       Style of the button
    :type style:        colosseum.CSS
    """
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
