from PySide6.QtWidgets import QWidget


class Container:
    def __init__(self, content=None, layout_native=None, on_refresh=None):
        self.native = QWidget()
        self.native.hide()
        self.layout_native = self.native if layout_native is None else layout_native
        self._content = None
        self.on_refresh = on_refresh

        self.content = content  # Set initial content

    def __del__(self):
        self.native = None

    @property
    def width(self):
        return self.layout_native.width()

    @property
    def height(self):
        return self.layout_native.height() - self.top_offset

    @property
    def top_offset(self):
        return 0  ## Stub (?)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        if self._content:
            self._content.container = None
            self._content.native.setParent(None)

        self._content = widget

        if widget:
            widget.container = self
            widget.native.setParent(self.native)

    def refreshed(self):
        if self.on_refresh is not None:
            self.on_refresh(self)
