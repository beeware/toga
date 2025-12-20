from PySide6.QtWidgets import QWidget


class Container:
    def __init__(self, content=None, layout_native=None, on_refresh=None):
        self.native = QWidget()
        self.native.hide()
        self.layout_native = self.native if layout_native is None else layout_native
        self._content = None
        self.on_refresh = on_refresh

        self.content = content  # Set initial content

    @property
    def width(self):
        return self.layout_native.width()

    @property
    def height(self):
        return self.layout_native.height()

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        if self.content:
            self._content.container = None
            self._content.native.setParent(None)

        self._content = widget

        if widget:
            widget.container = self
            widget.native.setParent(self.native)

    def refreshed(self):
        self.on_refresh(self)
