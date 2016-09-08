from .base import Widget


class ScrollContainer(Widget):
    def __init__(self, id=None, style=None, horizontal=True, vertical=True, content=None):
        super().__init__(id=None, style=None, horizontal=True, vertical=True, content=None)

    def _configure(self, horizontal, vertical, content):
        self.horizontal = horizontal
        self.vertical = vertical
        self.content = content

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget
        if widget:
            self._content.window = self.window
            self._content.app = self.app
            self._set_content(widget)

    def _set_app(self, app):
        if self._content:
            self._content.app = self.app

    def _set_window(self, window):
        if self._content:
            self._content.window = self.window

    @property
    def vertical(self):
        return self._vertical

    @vertical.setter
    def vertical(self, value):
        self._vertical = value
        self._set_vertical(value)

    @property
    def horizontal(self):
        return self._horizontal

    @horizontal.setter
    def horizontal(self, value):
        self._horizontal = value
        self._set_horizontal(value)

    def _set_vertical(self, value):
        raise NotImplementedError('ScrollContainer must define _set_vertical()')

    def _set_horizontal(self, value):
        raise NotImplementedError('ScrollContainer must define _set_horizontal()')
