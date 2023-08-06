class Container:
    def __init__(self, on_refresh=None):
        self._content = None
        self.on_refresh = on_refresh

        # FIXME...
        self.dpi = 96
        self.baseline_dpi = self.dpi

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        if self._content:
            self._content.container = None

        self._content = widget
        if widget:
            widget.container = self

    @property
    def width(self):
        if self._content:
            return self.content.native.size.width
        else:
            return 0

    @property
    def height(self):
        if self._content:
            return self.content.native.size.height
        else:
            return 0

    def refreshed(self):
        if self.on_refresh:
            self.on_refresh()
