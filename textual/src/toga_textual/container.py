from toga_textual.widgets.base import Scalable


class Container(Scalable):
    def __init__(self, native_parent, on_refresh=None):
        self.native_parent = native_parent
        self._content = None
        self.on_refresh = on_refresh

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
        return self.scale_out_horizontal(self.native_parent.size[0])

    @property
    def height(self):
        # Subtract 1 to remove the height of the header
        return self.scale_out_vertical(self.native_parent.size[1] - 1)

    def refreshed(self):
        if self.on_refresh:
            self.on_refresh()
