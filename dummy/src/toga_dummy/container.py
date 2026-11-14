class Container:
    def __init__(self, content=None):
        self.baseline_dpi = 96
        self.dpi = 96

        # Prime the underlying storage before using setter
        self._content = None
        self.content = content

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if self._content:
            self._content.container = None

        self._content = value
        if value:
            value.container = self

    @property
    def width(self):
        return self.content.get_size().width

    @property
    def height(self):
        return self.content.get_size().height

    def refreshed(self):
        if self.content:
            self.content.refresh()
