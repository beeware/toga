from .base import Widget


class ScrollContainer(Widget):
    def __init__(self, id=None, style=None, horizontal=True, vertical=True):
        super().__init__(id=None, style=None)
        self.horizontal = horizontal
        self.vertical = vertical
        self._content = None

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget
        self._content.window = self.window
        self._content.app = self.app
        self._set_content(widget)

    def _set_app(self, app):
        if self._content:
            self._content.app = self.app

    def _set_window(self, window):
        if self._content:
            self._content.window = self.window
